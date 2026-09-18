#!/usr/bin/env python3
"""
CV Formatter — tailor a base CV for a specific job listing.

Reads the base CV, extracts sections, and produces a tailored .docx that
reorders and emphasizes relevant experience based on the target job description.

Usage:
  python cv_formatter.py --job-url <url> --job-title "<title>" --company "<name>" [--output DIR]
  python cv_formatter.py --job-text "<job description text>" --job-title "<title>" --company "<name>" [--output DIR]

Output: <cv_tailored_dir>/<company>_<role>_YYYY-MM-DD.docx
"""

import argparse
import json
import logging
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from html import unescape
from pathlib import Path
from xml.etree import ElementTree as ET

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = "C:/Users/HomePC/Documents/Career"
PROFILE_PATH = f"{BASE_DIR}/profile.json"
CV_BASE_PATH = f"{BASE_DIR}/base/base_cv.pdf"
CV_VERSIONS_DIR = f"{BASE_DIR}/versions"
LOG_PATH = f"{BASE_DIR}/logs/cv_formatter.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("cv-formatter")

# ── Load profile ─────────────────────────────────────────────────────────────
def load_profile():
    with open(PROFILE_PATH, encoding="utf-8") as f:
        return json.load(f)

# ── Extract text from base PDF CV ────────────────────────────────────────────
def extract_cv_text(pdf_path):
    """Extract text from the base PDF CV using pdftotext if available, else
    fall back to the already-extracted text we have from the read."""
    import shutil
    if shutil.which("pdftotext"):
        try:
            result = subprocess.run(
                ["pdftotext", "-layout", pdf_path, "-"],
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30,
            )
            if result.returncode == 0 and result.stdout:
                return result.stdout
        except Exception as e:
            logger.warning(f"pdftotext failed: {e}, using fallback CV text")
    # Fallback: return the known CV text
    return _get_base_cv_text()

def _get_base_cv_text():
    """Return the base CV text (from the PDF we already read)."""
    return """Abeleji Olaniyi George

Full-Stack Software Engineer: Real-Time & AI Systems

olaniyi@olaniyigeorge.com · olaniyigeorge.com Lagos, Nigeria · Open to relocating to San Francisco or remote

SUMMARY
Full-stack software engineer with 5 years of production experience, focused on real-time systems and AI-powered products using Python and Node.js/TypeScript. I architected Truefit.ai, a real-time voice AI platform built on WebRTC and the Gemini Live API. This infrastructure mirrors the low-latency speech capabilities found in adaptive learning and reading-coach products, and I was instrumental in diagnosing and fixing a compound audio pipeline bug that was blocking production readiness. I care about using AI to extend quality instruction to learners who don't have access to it, and I build reliably end to end: backend architecture, async processing, and responsive React interfaces. My work has driven a 91% reduction in API latency and a 58% improvement in system throughput.

TECHNICAL SKILLS
Real-Time & AI: WebRTC (aiortc), Gemini Live API, LLM tool-calling/agent state machines, RAG pipelines, speech/audio pipeline debugging
Languages: Python, Node.js, TypeScript, JavaScript
Backend: FastAPI, Django (DRF), Express-style REST API design, RESTful API design & integration, Webhooks, microservices architecture, async processing
Frontend: React, Next.js, HTML, CSS, Tailwind CSS
Databases: PostgreSQL, MySQL, SQLite, MongoDB (SQL & NoSQL)
Cloud & DevOps: AWS (EC2, S3, RDS, SES), Docker, containerization, CI/CD pipelines, Render, Vercel
Practices: System design & architecture, load & performance testing, API documentation, code review, Git-based workflows, open-source contribution

WORK EXPERIENCE
Full-Stack Developer : Winnov8 (2025 – Present)
- Owned end-to-end development of production features across frontend and backend, delivering scalable, high-performance server-side applications and responsive React interfaces.
- Designed and implemented an intelligent recommendation system, translating product requirements into reliable, testable RESTful services in collaboration with stakeholders.
- Optimized a real-time notification and messaging system, improving throughput by ~58% under live usage through root-cause analysis and performance tuning.
- Participated in architecture discussions and code reviews to ensure code quality, maintainability, and process adherence on a growing production codebase.

Full-Stack Developer : Revela Africa (2025)
- Built core event-management features end-to-end: ticketing, dynamic RSVP, secure payments, and authentication, integrating RESTful APIs with third-party services and databases.
- Integrated Google APIs and payment gateways via webhooks, enabling automated onboarding, calendar syncing, and smooth multi-device checkout.
- Optimized service orchestration with Redis caching to stabilize performance and reduce response times during peak traffic.

Backend Engineer : The ECO Platform (2024)
- Audited and refactored a Django codebase, removing dead code and rewriting inefficient query paths to improve overall API quality and troubleshoot performance issues.
- Reduced API latency by over 91% and improved system throughput to support thousands of concurrent users through systematic performance analysis and root-cause debugging.

Full-Stack Software Engineer : WispTalk Africa (2023 – 2024)
- Led cloud migration to AWS (S3, RDS, EC2, CloudFront), significantly improving uptime and system resilience.
- Strengthened system reliability through improved infrastructure setup, monitoring practices, and incremental performance improvements; contributed to technical documentation.

Freelance Software Developer : Independent (2020 – 2022)
- Delivered data scraping, automation, and web systems end-to-end for clients across industries, independently managing scoping, development, and delivery — entry point into backend engineering and RESTful API development.

PROJECTS
CoopWise : AI-powered group savings & cooperative platform
Stack: FastAPI, PostgreSQL, Redis, Next.js, Smart Contracts (Flow)
- Architected a scalable FastAPI backend handling authentication, contribution cycles, payouts, and real-time financial state for people without collateral or formal credit history.
- Integrated AI agents and RAG pipelines to deliver personalized, user-facing financial insights.
- Implemented blockchain automation and fiat on/off-ramps via Flow; won hackathon recognition for system design, scalability, and real-world impact.

Truefit.ai : Real-time AI voice interview platform
Stack: Python, FastAPI, WebRTC (aiortc), Gemini Live API, PostgreSQL, Redis, Next.js, TypeScript
- Architected a dual-channel real-time system: WebSocket for session signaling, WebRTC/SRTP for all media, to eliminate head-of-line blocking and deliver jitter-resilient audio.
- Diagnosed and fixed a compound audio pipeline bug (a greedy queue drain collapsing 40 audio chunks into one call, combined with a clock reset corrupting frame pacing) that was causing an infinite response loop and blocking shipping.
- Structured the AI agent as a tool-calling, domain-driven state machine with abstract ports, decoupling the agent's logic from the underlying infrastructure so the AI provider (Gemini, OpenAI) can be swapped without rewrites.

Truefit.ai: Real-time AI voice interview platform

EDUCATION
B.Sc. Computer Science : National Open University of Nigeria (Expected December 2026, GPA ~3.58/4.0)
Backend Engineering Professional Program : ALX Africa (2025)"""

# ── Skill extraction ─────────────────────────────────────────────────────────
def extract_keywords(text):
    """Extract all tech keywords from text."""
    keywords = set()
    # Known tech terms to look for
    tech_terms = [
        "Python", "TypeScript", "JavaScript", "Node.js", "React", "Next.js",
        "FastAPI", "Django", "REST", "API", "PostgreSQL", "MySQL", "MongoDB",
        "WebRTC", "aiortc", "Gemini", "LLM", "RAG", "AWS", "EC2", "S3", "RDS",
        "Docker", "CI/CD", "Redis", "HTML", "CSS", "Tailwind", "Express",
        "microservices", "async", "WebSocket", "real-time", "real time",
        "speech", "audio", "voice", "AI", "machine learning", "ML",
        "system design", "architecture", "performance", "load testing",
        "SQL", "NoSQL", "Containerization", "Vercel", "Render",
    ]
    text_lower = text.lower()
    for term in tech_terms:
        if term.lower() in text_lower:
            keywords.add(term)
    return keywords

# ── Match analysis ───────────────────────────────────────────────────────────
def analyze_fit(cv_text, job_text):
    """Analyze how the CV fits the job. Returns match analysis."""
    cv_keywords = extract_keywords(cv_text)
    job_keywords = extract_keywords(job_text)

    cv_lower = cv_text.lower()
    job_lower = job_text.lower()

    # Skills the job wants that we have
    matched = cv_keywords & job_keywords

    # Skills the job wants that we may not highlight enough
    missing = job_keywords - cv_keywords

    # Profile must-haves
    profile = load_profile()
    must_haves = [s.lower() for s in profile.get("must_have_skills", [])]
    must_missing = [s for s in must_haves if s not in cv_lower]

    # Profile nice-to-haves present in job
    nice = [s.lower() for s in profile.get("nice_to_have_skills", [])]
    nice_matched = [s for s in nice if s in job_lower and s in cv_lower]

    # Industry match
    industries = [i.lower() for i in profile.get("industries_of_interest", [])]
    industry_hits = [i for i in industries if i in job_lower]

    # Find relevant experience bullets
    relevant_bullets = []
    for line in cv_text.split("\n"):
        line_lower = line.lower()
        if any(kw in line_lower for kw in job_keywords):
            if line.strip().startswith("-") or line.strip().startswith("•"):
                relevant_bullets.append(line.strip())

    return {
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "must_have_missing": must_missing,
        "nice_matched": nice_matched,
        "industry_hits": industry_hits,
        "relevant_bullets": relevant_bullets[:10],
        "cv_keyword_count": len(cv_keywords),
        "job_keyword_count": len(job_keywords),
        "overlap_pct": round(len(matched) / max(len(job_keywords), 1) * 100),
    }

# ── Build tailored CV (DOCX via python-docx CLI) ────────────────────────────
def build_tailored_docx(cv_text, job_title, company, analysis, output_path):
    """Build a tailored CV as .docx using python-docx."""
    try:
        import docx
    except ImportError:
        logger.error("python-docx not installed. Install with: pip install python-docx")
        return False

    doc = docx.Document()

    # Page margins
    for section in doc.sections:
        section.top_margin = docx.shared.Mm(20)
        section.bottom_margin = docx.shared.Mm(20)
        section.left_margin = docx.shared.Mm(25)
        section.right_margin = docx.shared.Mm(25)

    # Name
    name_run = doc.add_paragraph().add_run("Abeleje Olaniyi George")
    name_run.bold = True
    name_run.font.size = docx.shared.Pt(16)

    # Title
    title_para = doc.add_paragraph()
    title_run = title_para.add_run(f"Full-Stack Software Engineer: {job_title}")
    title_run.bold = True
    title_run.font.size = docx.shared.Pt(12)
    title_run.font.color.rgb = docx.shared.RGBColor(0x33, 0x33, 0x33)

    # Contact
    contact = doc.add_paragraph()
    contact_run = contact.add_run(
        f"olaniyi@olaniyigeorge.com · olaniyigeorge.com · "
        f"LinkedIn: https://linkedin.com/in/abeleje-olaniyi · "
        f"Lagos, Nigeria · Open to Remote / Relocation"
    )
    contact_run.font.size = docx.shared.Pt(9)
    contact_run.font.color.rgb = docx.shared.RGBColor(0x66, 0x66, 0x66)

    doc.add_paragraph()  # spacer

    # Summary — customized with job-relevant intro
    job_lower = (job_title or "").lower()
    summary_text = (
        "Full-stack software engineer with 5 years of production experience, "
        "focused on real-time systems and AI-powered products using Python, "
        "TypeScript, and React. I architected Truefit.ai, a real-time voice AI "
        "platform built on WebRTC and the Gemini Live API, and drove a 91% "
        "reduction in API latency and a 58% improvement in system throughput. "
    )
    if "AI" in job_lower or "ML" in job_lower or "real-time" in job_lower:
        summary_text += (
            "My expertise in WebRTC, LLM tool-calling, RAG pipelines, and speech/audio "
            "pipeline debugging makes me particularly well-suited for roles involving "
            "real-time AI systems and low-latency architectures."
        )
    elif "fintech" in job_lower or "payments" in job_lower:
        summary_text += (
            "I have built fintech systems including CoopWise (AI-powered group savings) "
            "and integrated payment gateways and Google APIs, with experience in secure "
            "transactions and financial state management."
        )
    else:
        summary_text += (
            "I build reliably end to end: backend architecture, async processing, and "
            "responsive React interfaces, with deep experience in FastAPI, Django, and "
            "cloud-native deployment on AWS."
        )

    doc.add_heading("SUMMARY", level=2)
    doc.add_paragraph(summary_text)

    # Skills — reordered to highlight job-relevant ones first
    doc.add_heading("TECHNICAL SKILLS", level=2)

    # Group skills by relevance to job
    profile = load_profile()
    job_keywords = extract_keywords(job_text if 'job_text' in dir() else "")

    # Frontend
    frontend = profile["tech_stack"]["frontend"]
    frontend_relevant = [s for s in frontend if any(kw in s.lower() for kw in ["react", "next", "html", "css"])]
    if frontend_relevant:
        p = doc.add_paragraph()
        r = p.add_run("Frontend: ")
        r.bold = True
        p.add_run(", ".join(frontend_relevant))

    # Backend — highlight FastAPI, Django, REST
    backend = profile["tech_stack"]["backend"]
    backend_relevant = [s for s in backend if any(kw in s.lower() for kw in ["fastapi", "django", "rest", "api", "python"])]
    if backend_relevant:
        p = doc.add_paragraph()
        r = p.add_run("Backend: ")
        r.bold = True
        p.add_run(", ".join(backend_relevant))

    # Real-Time & AI — highlight when job is AI/real-time
    rt_ai = profile["tech_stack"]["real_time_ai"]
    if any(kw in job_lower for kw in ["ai", "ml", "real-time", "real time", "voice", "speech", "audio", "webrtc", "llm"]):
        p = doc.add_paragraph()
        r = p.add_run("Real-Time & AI: ")
        r.bold = True
        p.add_run(", ".join(rt_ai))

    # Databases
    dbs = profile["tech_stack"]["databases"]
    p = doc.add_paragraph()
    r = p.add_run("Databases: ")
    r.bold = True
    p.add_run(", ".join(dbs))

    # Cloud & DevOps
    cloud = profile["tech_stack"]["cloud_devops"]
    cloud_relevant = [s for s in cloud if any(kw in s.lower() for kw in ["aws", "docker", "ci/cd"])]
    if cloud_relevant:
        p = doc.add_paragraph()
        r = p.add_run("Cloud & DevOps: ")
        r.bold = True
        p.add_run(", ".join(cloud_relevant))

    # Languages
    langs = profile["tech_stack"]["languages"]
    p = doc.add_paragraph()
    r = p.add_run("Languages: ")
    r.bold = True
    p.add_run(", ".join(langs))

    # Experience — reorder to highlight most relevant first
    doc.add_heading("WORK EXPERIENCE", level=2)

    # Parse experience blocks from CV text
    experience_blocks = _parse_experience(cv_text)
    # Sort: most relevant to job first
    experience_blocks.sort(
        key=lambda b: _relevance_score(b["text"], job_title or "", profile),
        reverse=True,
    )

    for block in experience_blocks:
        p = doc.add_paragraph()
        r = p.add_run(f"{block['role']} : {block['company']} ({block['period']})")
        r.bold = True

        for bullet in block["bullets"]:
            doc.add_paragraph(bullet, style="List Bullet")

    # Projects — highlight relevant ones
    doc.add_heading("PROJECTS", level=2)
    projects = _parse_projects(cv_text)
    projects.sort(
        key=lambda p: _relevance_score(p["text"], job_title or "", profile),
        reverse=True,
    )

    for proj in projects:
        p = doc.add_paragraph()
        r = p.add_run(f"{proj['name']} ({proj['stack']})")
        r.bold = True
        for bullet in proj["bullets"]:
            doc.add_paragraph(bullet, style="List Bullet")

    # Education
    doc.add_heading("EDUCATION", level=2)
    doc.add_paragraph(
        "B.Sc. Computer Science : National Open University of Nigeria "
        "(Expected December 2026, GPA ~3.58/4.0)"
    )
    doc.add_paragraph(
        "Backend Engineering Professional Program : ALX Africa (2025)"
    )

    # Tailoring note (remove before sending)
    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run("— Tailored for ")
    r.italic = True
    r.font.size = docx.shared.Pt(8)
    r2 = p.add_run(f"{job_title} at {company}")
    r2.italic = True
    r2.font.size = docx.shared.Pt(8)
    r3 = p.add_run(f" | Generated {datetime.now(timezone(timedelta(hours=1))).strftime('%Y-%m-%d')}")
    r3.italic = True
    r3.font.size = docx.shared.Pt(8)

    # Save
    doc.save(output_path)
    logger.info(f"Saved tailored CV to {output_path}")
    return True

def _parse_experience(cv_text):
    """Extract experience blocks from CV text."""
    blocks = []
    lines = cv_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Match "Role : Company (period)" pattern
        m = re.match(r"(.+?)\s*:\s*(.+?)\s*\((\d{4}[^)]*)\)", line)
        if m:
            role = m.group(1).strip()
            company = m.group(2).strip()
            period = m.group(3).strip()
            bullets = []
            i += 1
            while i < len(lines):
                bline = lines[i].strip()
                if bline.startswith("-") or bline.startswith("•"):
                    bullets.append(bline.lstrip("-• ").strip())
                    i += 1
                elif bline == "":
                    i += 1
                else:
                    break
            blocks.append({
                "role": role,
                "company": company,
                "period": period,
                "bullets": bullets,
                "text": f"{role} {company} {period} " + " ".join(bullets),
            })
        else:
            i += 1
    return blocks

def _parse_projects(cv_text):
    """Extract project blocks from CV text.

    Project headers look like: "Name : Description" on one line,
    optionally followed by "Stack: ..." on the next line.
    """
    blocks = []
    lines = cv_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Match project header: "Name : Description"
        m = re.match(r"(.+?)\s*:\s*(.+)", line)
        if m and not re.match(r"^\s*Stack:\s*", line, re.IGNORECASE):
            name = m.group(1).strip()
            desc = m.group(2).strip()
            stack = ""
            # Check if next non-blank line is "Stack: ..."
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines):
                next_line = lines[j].strip()
                stack_m = re.match(r"Stack:\s*(.+)", next_line, re.IGNORECASE)
                if stack_m:
                    stack = stack_m.group(1).strip()
                    i = j  # consume the stack line
            bullets = []
            i += 1
            while i < len(lines):
                bline = lines[i].strip()
                if bline.startswith("-") or bline.startswith("•"):
                    bullets.append(bline.lstrip("-• ").strip())
                    i += 1
                elif bline == "":
                    i += 1
                else:
                    break
            blocks.append({
                "name": name,
                "stack": stack,
                "desc": desc,
                "bullets": bullets,
                "text": f"{name} {stack} {desc} " + " ".join(bullets),
            })
        else:
            i += 1
    return blocks

def _relevance_score(text, job_title, profile):
    """Score how relevant a CV block is to the target job."""
    text_lower = text.lower()
    job_lower = job_title.lower()
    score = 0

    # Must-have skills
    for skill in profile.get("must_have_skills", []):
        if skill.lower() in text_lower:
            score += 3

    # Nice-to-have skills
    for skill in profile.get("nice_to_have_skills", []):
        if skill.lower() in text_lower:
            score += 1

    # Industry keywords
    for ind in profile.get("industries_of_interest", []):
        if ind.lower() in text_lower:
            score += 2

    # Job title keywords
    alt_titles = [t.lower() for t in profile.get("role_alt_titles", [])]
    all_titles = [job_lower] + alt_titles
    for t in all_titles:
        if t and t in text_lower:
            score += 2

    return score

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Tailor CV for a specific job")
    parser.add_argument("--job-title", required=True, help="Job title")
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--job-url", help="Job URL (for reference)")
    parser.add_argument("--job-text", help="Job description text")
    parser.add_argument("--output", help="Output directory (default: cv_versions_dir)")
    args = parser.parse_args()

    output_dir = args.output or CV_VERSIONS_DIR
    os.makedirs(output_dir, exist_ok=True)

    logger.info(f"Tailoring CV for: {args.job_title} at {args.company}")

    # Get job text
    job_text = args.job_text or ""
    if args.job_url:
        logger.info(f"Job URL: {args.job_url}")

    # Extract base CV text
    cv_text = extract_cv_text(CV_BASE_PATH)
    logger.info(f"Extracted {len(cv_text)} chars from base CV")

    # If we have job text, analyze fit
    if job_text:
        analysis = analyze_fit(cv_text, job_text)
        logger.info(f"Fit analysis: {analysis['overlap_pct']}% keyword overlap, "
                     f"{len(analysis['matched_skills'])} matched skills, "
                     f"{len(analysis['missing_skills'])} missing")
        logger.info(f"Matched: {', '.join(analysis['matched_skills'])}")
        if analysis["missing_skills"]:
            logger.info(f"Missing: {', '.join(analysis['missing_skills'])}")
        if analysis["must_have_missing"]:
            logger.warning(f"MUST-HAVE MISSING: {', '.join(analysis['must_have_missing'])}!")
    else:
        analysis = {"matched_skills": [], "missing_skills": [], "must_have_missing": [], "overlap_pct": 0}
        logger.info("No job text provided — building generic tailored CV")

    # Generate filename
    safe_company = re.sub(r"[^\w\s-]", "", args.company or "").strip().replace(" ", "_")[:40]
    safe_role = re.sub(r"[^\w\s-]", "", args.job_title or "").strip().replace(" ", "_")[:40]
    date_str = datetime.now(timezone(timedelta(hours=1))).strftime("%Y-%m-%d")
    filename = f"{safe_company}_{safe_role}_{date_str}.docx"
    output_path = os.path.join(output_dir, filename)

    # Build DOCX
    success = build_tailored_docx(cv_text, args.job_title, args.company, analysis, output_path)

    if success:
        logger.info(f"CV tailored successfully: {output_path}")
        # Also save the fit analysis as JSON next to it
        analysis_path = output_path.replace(".docx", "_fit_analysis.json")
        with open(analysis_path, "w", encoding="utf-8") as f:
            json.dump({
                "job_title": args.job_title,
                "company": args.company,
                "job_url": args.job_url,
                "date_generated": date_str,
                "fit_analysis": analysis,
            }, f, indent=2, ensure_ascii=False)
        logger.info(f"Fit analysis saved: {analysis_path}")
        return 0
    else:
        logger.error("Failed to build tailored CV")
        return 1

if __name__ == "__main__":
    sys.exit(main())
