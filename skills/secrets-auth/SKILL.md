# Secrets and Auth Skill

Use when working with OAuth, API keys, tokens, or credentials in this repo.

## Hard rules

- **Do NOT read secret-bearing files to find API keys.** If a tool can't find its config, say so and ask where it is.
- Never inline tokens, secrets, or credentials in files or chat.
- Never commit `.env`, secrets, credential stores, or OAuth client files.

## Where secrets live

- OAuth client secrets: `C:\Users\HomePC\Downloads\secrets\client_secret_*.json`
- Specifically for Google Workspace: `C:\Users\HomePC\Downloads\secrets\client_secret_898008036081-8163176d1io8bst4lan4stb6t6fnn55p.apps.googleusercontent.com.json`
- `.env` files: never read them to extract keys. If config is missing, ask.

## Auth setup preferences

When setting up authentication:
- Prefer **device-code flows** (gh device code, OAuth device flow) over interactive browser login — they work in headless/agent sessions.
- Use the tool's native credential store or the OS keyring for tokens — not files or environment variables unless that's the only option.
- For GitHub: `gh auth login` with device code, then `gh auth setup-git` to wire git credential helper.
- For Google OAuth: follow the tool's OAuth flow; store tokens in the tool's store.

## When auth isn't set up

- Say so plainly. Don't guess at paths or tokens.
- Ask where the config/secret is if the tool can't find it.
- Offer the device-code flow as the path when interactive login isn't practical.

## Secret-bearing files to leave alone

- `.env`, `.envrc`
- `client_secret_*.json`
- `.git-credentials` (if it exists with tokens)
- `~/.config/gh/hosts.yml` (contains tokens)
- Any credential store or keyring

## Verification

After auth setup, verify with the tool's status command (e.g. `gh auth status`) — don't assume.
