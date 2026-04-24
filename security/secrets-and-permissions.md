# Secrets and File Permissions

How to keep OpenClaw credentials out of docs, out of git history, and out of world-readable files.

**Tested on:** OpenClaw 2026.4.x, Ubuntu 24.04, multi-channel personal assistant setup
**Last updated:** 2026-04-21

---

## The Rule

**If a token can send messages, run code, reach MCP servers, or access paid APIs, treat it like a production secret.**

The most common failure mode is not some elite attacker. It is you accidentally documenting a live key in `TOOLS.md`, committing it, and then forgetting it exists.

## What Must Not Live in Docs

Do **not** keep these in markdown files, screenshots, notes, or example configs:

- bot tokens
- bearer tokens
- API keys
- gateway auth tokens
- session cookies
- SSH private keys
- service passwords

If you need examples, use obvious placeholders:

```json
{
  "token": "__OPENCLAW_REDACTED__",
  "apiKey": "__REDACTED__"
}
```

## Permission Baseline

At minimum:

```bash
chmod 600 ~/.openclaw/openclaw.json
chmod 600 ~/.openclaw/agents/*/agent/auth-profiles.json 2>/dev/null || true
chmod 600 ~/.claude/settings.json 2>/dev/null || true
chmod 600 ~/.restic-passphrase 2>/dev/null || true
```

If `auth-profiles.json` is `664`, fix it immediately.

## Recommended Storage Pattern

### Good

- `~/.openclaw/openclaw.json` for structure
- environment variables for secrets where possible
- `EnvironmentFile=` in systemd if you need stable injected env
- redacted examples in repo docs

### Bad

- real keys in `TOOLS.md`
- real keys in screenshots
- real keys pasted into GitHub issues or Discord snippets
- committing live `.env` files to helper repos

## Audit Commands

### 1. Check dangerous permissions

```bash
find ~/.openclaw -type f \( -name 'auth-profiles.json' -o -name 'openclaw.json' \) \
  -printf '%m %p\n'
```

### 2. Grep for obvious leaks in docs

```bash
grep -RniE '(api[_-]?key|botToken|token|Bearer |JELLYFIN_API_KEY|CLOUDFLARE_API_TOKEN)' \
  ~/openclaw-best-practices ~/.openclaw/workspace 2>/dev/null
```

Then inspect hits manually. Some will be benign config keys. Some will be real leaks. Be honest about which is which.

### 3. Run OpenClaw's audit

```bash
openclaw security audit
```

## Rotation Checklist After a Leak

If a secret hit docs, git, or chat:

1. rotate the secret first
2. update the runtime config
3. confirm the new value works
4. remove the old value from docs and local notes
5. if it reached git, rewrite history or invalidate access permanently
6. document what leaked and where

## Safer Documentation Pattern

Instead of this:

```markdown
- Brave API key: abc123...
- Jellyfin API key: deadbeef...
```

Do this:

```markdown
- Brave API key: set in environment
- Jellyfin API key: stored in MCP env, not documented here
```

If future-you needs the exact location, write the location, not the value.

## Gotchas

1. **OpenClaw redacts some values in tool output.** Your markdown files do not. Don't confuse the two.

2. **Systemd upgrades can drop `EnvironmentFile=` customizations.** Re-verify after updates if you rely on env injection.

3. **A private repo is not a secret manager.** It is just a quieter way to leak things.
