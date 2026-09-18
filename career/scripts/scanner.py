#!/usr/bin/env python3
"""
# Job Board Scanner — daily job hunt automation for Abeleje Olaniyi George.

Reads profile.json + job_boards.json, checks each enabled board for new jobs
matching the profile, deduplicates against the Google Sheet, and appends new
matches to the sheet.

Boards supported:
  - RSS feeds (RemoteOK, WWR, HN Who's Hiring, etc.)
  - API-based (Wellfound, YC Jobs, Ashby) — requires API tokens
  - Email monitor (LinkedIn job alerts via Gmail)

Usage:
  python scanner.py              # scan + append to sheet (requires gws auth)
  python scanner.py --dry-run    # scan only, print results, no sheet write
"""

import json
import logging
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from html import unescape
from xml.etree import ElementTree as ET

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = "C:/Users/HomePC/Documents/Career"
PROFILE_PATH = f"{BASE_DIR}/profile.json"
BOARDS_PATH = f"{BASE_DIR}/job_boards.json"
LOG_PATH = f"{BASE_DIR}/logs/scanner.log"
GAPI_PATH = "C:/Users/HomePC/AppData/Local/hermes/skills/productivity/google-workspace/scripts/google_api.py"
PY_EXE = sys.executable  # Use the same Python that has googleapiclient installed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("job-scanner")

# ── Load config ──────────────────────────────────────────────────────────────
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

profile = load_json(PROFILE_PATH)
boards_config = load_json(BOARDS_PATH)
sheet_cfg = boards_config["google_sheet"]

# ── GWS / google_api helpers ─────────────────────────────────────────────────
def find_gws():
    """Find gws binary or fallback to google_api.py.
    Returns (executable, script_path_or_None).
    """
    import os, shutil
    bin_path = shutil.which("gws")
    if bin_path:
        return (bin_path, None)
    if os.path.exists(GAPI_PATH):
        return (PY_EXE, GAPI_PATH)
    return (None, None)

def run_gws(args_list, gws_exec, gws_script):
    """Run a gws/google_api command. args_list is the args AFTER the executable."""
    if gws_script:
        cmd = [gws_exec, gws_script] + list(args_list)
    else:
        cmd = [gws_exec] + list(args_list)
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=30)
    return result

# ── Helpers ──────────────────────────────────────────────────────────────────
def now_wat_iso():
    """Return now in Africa/Lagos (WAT, UTC+1) as ISO date string."""
    wat = datetime.now(timezone(timedelta(hours=1)))
    return wat.strftime("%Y-%m-%d")

def slugify(text):
    """Create a dedup key from job text."""
    clean = re.sub(r"[^\w\s-]", "", unescape(text or "").lower())
    clean = re.sub(r"\s+", "-", clean.strip())
    return clean[:120]

def extract_salary(text):
    """Try to extract a USD salary figure from text."""
    patterns = [
        r"(?:usd\s*)?(\d{3,7})\s*(?:k|K)?\s*(?:per\s*)?(?:year|annum|yr|month)",
        r"(\d{3,7})\s*(?:k|K)\s*(?:USD|$)",
        r"\$\s*(\d{3,7})\s*(?:k|K)?",
        r"(?:salary|comp|pay)[:\s]+(\d{3,7})",
    ]
    for pat in patterns:
        m = re.search(pat, text or "", re.IGNORECASE)
        if m:
            val = int(m.group(1))
            if val < 1000:
                val *= 1000
            return val
    return ""

def extract_location(text):
    """Extract location string from job text."""
    m = re.search(r"(?:location|based|remote|work from|office)[:\s]+(.{3,80})", text or "", re.IGNORECASE)
    if m:
        loc = m.group(1).strip()
        if len(loc) > 3:
            return loc
    m = re.search(r"([A-Z][a-z]+(?:[\s-][A-Z][a-z]+){0,3}(?:,?\s*(?:USA|UK|CA|EU|Germany|France|Netherlands|Spain|Portugal|India|Nigeria|Canada))?)", text or "")
    if m:
        return m.group(1).strip()
    return "Remote (check listing)"

def classify_tier(company_name, description):
    name_lower = (company_name or "").lower()
    desc_lower = (description or "").lower()
    if any(w in desc_lower for w in ["series b", "series c", "series d", "series e", "leadership", "vp", "director"]):
        return "Series B+"
    if any(w in desc_lower for w in ["series a", "seed", "early stage"]):
        return "Series A"
    if any(w in name_lower for w in ["inc", "llc", "corp", "ltd", "gmbh", "ag", "pty", "limited"]):
        if len(name_lower) > 10:
            return "Established"
    if any(w in desc_lower for w in ["startup", "early", "founding", "seed"]):
        return "Startup / Seed"
    return "Unknown"

def score_fit(job_text, job_title_lower):
    score = 3
    text_lower = (job_text or "").lower()
    title_lower = job_title_lower.lower()
    must_haves = profile.get("must_have_skills", [])
    for skill in must_haves:
        if skill.lower() not in text_lower:
            score -= 1
    nice = profile.get("nice_to_have_skills", [])
    nice_hits = sum(1 for s in nice if s.lower() in text_lower)
    score += min(nice_hits, 2)
    target = profile.get("target_role", "").lower()
    alt_titles = [t.lower() for t in profile.get("role_alt_titles", [])]
    all_target = [target] + alt_titles
    if any(t in title_lower for t in all_target):
        score += 1
    elif any(t in text_lower for t in all_target):
        score += 0.5
    industries = [i.lower() for i in profile.get("industries_of_interest", [])]
    if any(ind in text_lower for ind in industries):
        score += 0.5
    return max(1, min(5, round(score)))

def is_excluded(job_title, job_text):
    combined = f"{job_title or ''} {job_text or ''}".lower()
    for kw in profile.get("exclusion_keywords", []):
        if kw in combined:
            return True
    return False

def index_to_col(n):
    """Convert 1-based index to Excel column letter."""
    result = ""
    while n > 0:
        n, rem = divmod(n - 1, 26)
        result = chr(65 + rem) + result
    return result

# ── RSS Scanner ──────────────────────────────────────────────────────────────
def scan_rss_board(board):
    """Scan an RSS feed board. Returns list of job dicts."""
    jobs = []
    rss_url = board.get("rss_feed")
    if not rss_url:
        logger.warning(f"Board {board['name']}: no RSS feed URL, skipping")
        return jobs

    try:
        req = urllib.request.Request(
            rss_url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; JobScanner/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            xml_bytes = resp.read()
        root = ET.fromstring(xml_bytes)
    except Exception as e:
        logger.error(f"Board {board['name']}: RSS fetch failed: {e}")
        return jobs

    items = root.findall(".//item")
    category_filter = board.get("query_params", {}).get("category", "")

    for item in items[:boards_config["scanner"]["max_jobs_per_board_per_run"]]:
        title_el = item.find("title")
        link_el = item.find("link")
        desc_el = item.find("description")
        cat_el = item.find("category")

        title = unescape((title_el.text or "").strip()) if title_el is not None else ""
        link = link_el.text.strip() if link_el is not None else ""
        desc_raw = (desc_el.text or "") if desc_el is not None else ""
        category = unescape((cat_el.text or "").strip()) if cat_el is not None else ""

        if category_filter and category_filter not in (category or ""):
            continue

        desc_clean = re.sub(r"<[^>]+>", " ", desc_raw)
        desc_clean = unescape(desc_clean).strip()
        job_text = f"{title} {desc_clean}"

        if is_excluded(title, job_text):
            continue

        salary = extract_salary(job_text)
        location = extract_location(job_text) or extract_location(desc_clean)

        company = ""
        if "·" in title:
            company = title.split("·")[0].strip()
        elif "at" in title.lower():
            parts = re.split(r"\bat\b", title, flags=re.IGNORECASE)
            company = parts[0].strip() if len(parts) > 1 else ""
        if not company:
            m = re.search(r"https?://(?:www\.)?([^/]+)", link)
            if m:
                company = m.group(1).replace("www.", "").split(".")[0].title()

        role_title = title
        if company and f"{company} " in title:
            role_title = title.replace(f"{company} ", "", 1).strip()
        elif company and f"— {company}" in title:
            role_title = title.split("—")[-1].strip()

        dedup_key = slugify(f"{company} {role_title} {link}")
        tier = classify_tier(company, desc_clean)
        fit_score = score_fit(job_text, role_title)

        job = {
            "job_id": dedup_key,
            "company": company or "Unknown",
            "role_title": role_title or title,
            "tier": tier,
            "location_tz": location,
            "salary_usd": salary,
            "job_url": link,
            "company_website": "",
            "date_found": now_wat_iso(),
            "date_applied": "",
            "status": "New — Review",
            "cv_version": "",
            "cover_note_sent": "",
            "gap_analysis_done": "",
            "projects_tailored": "",
            "follow_up_date": "",
            "interview_stage": "",
            "outcome": "",
            "excitement": "",
            "fit_score": fit_score,
            "notes": f"Source: {board['name']}",
        }
        jobs.append(job)

    logger.info(f"Board {board['name']}: found {len(jobs)} candidate jobs from RSS")
    return jobs

# ── LinkedIn Email Monitor ────────────────────────────────────────────────────
def scan_linkedin_email(gws_exec, gws_script):
    """Search Gmail for LinkedIn job alert emails. Returns list of job dicts."""
    jobs = []

    for board in boards_config["boards"]:
        if board.get("type") != "email_monitor":
            continue
        email_filter = board.get("email_filter", "")
        if not email_filter:
            continue

        result = run_gws(
            ["gmail", "search", email_filter, "--max", "20"],
            gws_exec, gws_script,
        )
        if result.returncode != 0:
            logger.error(f"LinkedIn email scan failed: {result.stderr}")
            continue
        try:
            messages = json.loads(result.stdout)
        except json.JSONDecodeError:
            logger.error(f"LinkedIn email scan: bad JSON: {result.stdout[:200]}")
            continue

        for msg in messages:
            subject = msg.get("subject", "")
            snippet = msg.get("snippet", "")
            job_text = f"{subject} {snippet}"

            title = subject
            company = ""
            m = re.search(r"(?:new|latest)\s+(.+?)\s+(?:job|position|role|opportunity)", subject, re.IGNORECASE)
            if m:
                role_part = m.group(1)
                at_m = re.search(r"(.+?)\s+at\s+(.+)", role_part)
                if at_m:
                    role_title = at_m.group(1).strip()
                    company = at_m.group(2).strip()
                    title = f"{role_title} at {company}"
                else:
                    role_title = role_part
            else:
                role_title = subject

            if is_excluded(title, job_text):
                continue

            salary = extract_salary(job_text)
            location = extract_location(job_text)
            dedup_key = slugify(f"{subject} {msg['id']}")
            fit_score = score_fit(job_text, role_title)

            job = {
                "job_id": dedup_key,
                "company": company or "LinkedIn Alert",
                "role_title": role_title,
                "tier": classify_tier(company, job_text),
                "location_tz": location,
                "salary_usd": salary,
                "job_url": msg.get("id", ""),
                "company_website": "",
                "date_found": now_wat_iso(),
                "date_applied": "",
                "status": "New — Review (LinkedIn Email)",
                "cv_version": "",
                "cover_note_sent": "",
                "gap_analysis_done": "",
                "projects_tailored": "",
                "follow_up_date": "",
                "interview_stage": "",
                "outcome": "",
                "excitement": "",
                "fit_score": fit_score,
                "notes": f"Source: LinkedIn email alert (Gmail ID: {msg['id']})",
            }
            jobs.append(job)

    logger.info(f"LinkedIn email monitor: found {len(jobs)} candidate jobs")
    return jobs

# ── Browser-based Scanner (RemoteOK, HN, etc.) ─────────────────────────────
def scan_browser_board(board):
    """Stub for browser-based job boards.

    These boards (RemoteOK, HN Who's Hiring, LinkedIn, Indeed, Glassdoor) 
    don't have clean APIs or RSS feeds. They need browser automation.

    Returns empty list for now — browser automation is wired separately.
    """
    logger.info(f"Board {board['name']}: browser scan requested (not yet implemented)")
    logger.info(f"  URL: {board.get('url', '')}")
    logger.info(f"  Query: {board.get('query_params', {})}")
    logger.warning(f"  → No jobs extracted (browser automation pending)")
    return []

# ── Dedup ────────────────────────────────────────────────────────────────────
def load_existing_jobs(gws_exec, gws_script):
    """Load existing job IDs from the Google Sheet for dedup."""
    existing = set()
    col_letter = index_to_col(sheet_cfg["columns"][0]["index"] + 1)  # job_id column
    range_str = f"'{sheet_cfg['sheet_name']}'!A{col_letter}1:A{col_letter}200"
    result = run_gws(["sheets", "get", sheet_cfg["spreadsheet_id"], range_str], gws_exec, gws_script)
    if result.returncode == 0:
        try:
            rows = json.loads(result.stdout)
            for row in rows[1:]:
                if row and len(row) > 0 and row[0]:
                    existing.add(str(row[0]))
        except json.JSONDecodeError:
            logger.warning(f"Could not parse sheet data for dedup: {result.stdout[:200]}")
    else:
        logger.warning(f"Could not load existing jobs for dedup: {result.stderr}")
    return existing

# ── Append to Sheet ──────────────────────────────────────────────────────────
def append_jobs(gws_exec, gws_script, new_jobs):
    """Append new job rows to the Google Sheet."""
    if not new_jobs:
        logger.info("No new jobs to append")
        return 0

    col_keys = [c["key"] for c in sheet_cfg["columns"]]
    rows = [[job.get(key, "") for key in col_keys] for job in new_jobs]
    values_json = json.dumps(rows)
    # Build a full-column range for append (e.g. 'Sheet1'!A:U)
    last_col_idx = sheet_cfg["columns"][-1]["index"] + 1  # 1-based
    last_col_letter = index_to_col(last_col_idx)
    range_str = f"'{sheet_cfg['sheet_name']}'!A:{last_col_letter}"

    result = run_gws(
        ["sheets", "append", sheet_cfg["spreadsheet_id"], range_str, "--values", values_json],
        gws_exec, gws_script,
    )
    if result.returncode == 0:
        logger.info(f"Appended {len(new_jobs)} jobs to sheet")
        return len(new_jobs)
    else:
        logger.error(f"Sheet append failed: {result.stderr}")
        return 0

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    dry_run = "--dry-run" in sys.argv

    logger.info("=" * 60)
    logger.info("Job Board Scanner starting")

    gws_exec, gws_script = find_gws()
    if not gws_exec:
        logger.error("Neither gws nor google_api.py found. Google auth may not be set up.")
        if dry_run:
            logger.info("Dry-run mode: scanning RSS only, no sheet writes")
        else:
            logger.error("Use --dry-run to scan without sheet access, or set up Google auth first.")
            return 1

    if not dry_run:
        existing = load_existing_jobs(gws_exec, gws_script)
        logger.info(f"Loaded {len(existing)} existing jobs for dedup")

    all_new_jobs = []
    seen_dedup = set()
    if not dry_run:
        seen_dedup.update(existing)

    for board in boards_config["boards"]:
        if not board.get("enabled", False):
            continue

        board_type = board.get("type", "")
        logger.info(f"Scanning board: {board['name']} (type={board_type})")

        if board_type == "rss":
            jobs = scan_rss_board(board)
        elif board_type == "email_monitor":
            if gws_exec:
                jobs = scan_linkedin_email(gws_exec, gws_script)
            else:
                logger.warning(f"Board {board['name']}: email_monitor requires gws auth, skipping")
                jobs = []
        elif board_type == "api":
            logger.warning(f"Board {board['name']}: API scan requested (not yet implemented, no API key configured)")
            jobs = []
        elif board_type == "browser":
            jobs = scan_browser_board(board)
        else:
            logger.warning(f"Board {board['name']}: unknown type {board_type}, skipping")
            jobs = []

        new_from_board = [j for j in jobs if j["job_id"] not in seen_dedup]
        for j in new_from_board:
            seen_dedup.add(j["job_id"])

        if new_from_board:
            logger.info(f"  → {len(new_from_board)} new jobs from {board['name']}")
            all_new_jobs.extend(new_from_board)
        else:
            logger.info(f"  → 0 new jobs from {board['name']} (all seen before)")

        if len(all_new_jobs) >= boards_config["scanner"]["max_total_new_jobs_per_run"]:
            logger.info(f"Reached max total new jobs, stopping")
            break

    # Print results
    if all_new_jobs:
        logger.info(f"\n--- {len(all_new_jobs)} NEW JOBS FOUND ---")
        for j in all_new_jobs:
            logger.info(f"  [{j['fit_score']}/5] {j['company']} — {j['role_title']} | {j['location_tz']} | {j.get('salary_usd', 'TBD')} | {j['job_url']}")
    else:
        logger.info("No new jobs found")

    # Append to sheet
    if not dry_run and all_new_jobs:
        appended = append_jobs(gws_exec, gws_script, all_new_jobs)
        logger.info(f"Scanner complete: {appended} jobs appended to sheet")
    elif dry_run and all_new_jobs:
        logger.info(f"Dry-run complete: {len(all_new_jobs)} jobs found (not written)")
    else:
        logger.info("Scanner complete: no new jobs")

    logger.info("Job Board Scanner finished")
    return 0

if __name__ == "__main__":
    sys.exit(main())
