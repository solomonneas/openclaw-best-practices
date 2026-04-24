# Claude Memory Handoffs

How to make Claude Code write durable findings back into OpenClaw's memory system without relying on a human to remember the handoff every time.

**Tested on:** OpenClaw 2026.4.x on a primary host with secondary-machine Claude Code sessions and conservative handoff ingestion
**Last updated:** 2026-04-21

---

## The Problem

Claude Code is great at implementation. It is terrible at durable memory unless you force the issue.

Without a handoff pattern, good findings die inside:

- repo-local Claude sessions
- ACP threads
- one-off coding sessions on secondary machines

If OpenClaw is your canonical orchestrator and memory owner, those findings need a repeatable path back home.

## Architecture

We use a simple rule:

**Claude Code may discover durable knowledge anywhere. One primary OpenClaw host should remain the canonical place that decides what becomes shared memory.**

Flow:

```text
Claude Code task finishes
  -> writes a handoff file to .claude/memory-handoffs/
  -> the primary host cron runs the ingest wrapper
  -> ingester validates target + format
  -> safe high-confidence updates are promoted or routed
  -> the original handoff is archived
```

## Components

### Handoff inbox

```text
.claude/memory-handoffs/
```

Claude writes structured handoff documents here at the end of substantial tasks.

### Conservative ingester

```text
scripts/ingest-memory-handoffs.py
scripts/run-memory-handoff-ingest.sh
```

The wrapper runs safe card promotion and explicit document routing in one pass.

### Scheduled intake

Run a cron job every 30 minutes on the primary OpenClaw host.

```json
{
  "name": "Claude Memory Handoff Ingest",
  "schedule": {
    "kind": "every",
    "everyMs": 1800000
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run bash ~/.openclaw/workspace/scripts/run-memory-handoff-ingest.sh and summarize any promoted cards or routed docs.",
    "model": "openai-codex/gpt-5.4",
    "thinking": "low"
  }
}
```

## Safety Rules

This system is intentionally conservative.

### Auto-promotion is explicit only

Cards are only auto-promoted when the handoff explicitly requests:

- `create-card` or `update-card`
- a safe target filename
- a full markdown card document
- valid frontmatter and expected structure

### Document routing is explicit only

Allowed non-card destinations should be limited to things like:

- `TOOLS.md`
- `USER.md`
- `rules/*.md`
- `.learnings/*`

No broad freeform mutation. No cleverness. No agent freestyle against your canonical docs.

### Dedupe matters

If the same handoff lands twice, do not append duplicate document blocks into destination docs.

## Handoff Template Rules

The parser matters more than your aesthetic preferences.

One gotcha that bit us hard:

- inside `Suggested document content`, **do not use level-2 headings (`##`)**
- the parser treats them as section boundaries
- use bullets, plain text, or `###` instead

Also ignore:

- `TEMPLATE.md`
- hidden files

Those should never be processed as real handoffs.

## What This Solves

- durable findings from secondary machines still reach the primary host
- repo-local Claude sessions stop being memory dead-ends
- OpenClaw remains the canonical intake and promotion point
- humans stop having to say “please write that down” after every useful Claude run

## Verification

```bash
# Run manual ingest
bash ~/.openclaw/workspace/scripts/run-memory-handoff-ingest.sh

# Check scheduled job
openclaw cron list --json | jq '.[] | select(.name == "Claude Memory Handoff Ingest")'

# Check promoted cards
find ~/.openclaw/workspace/memory/cards -type f | sort | tail -n 10
```

Expected behavior:

- `NO_UPDATES` when nothing useful was handed off
- promoted cards or routed docs when valid handoffs exist
- no template processing
- no duplicate appends

## Gotchas

1. **This workflow depends on one primary host staying canonical.** If secondary machines start writing shared memory directly, you lose traceability fast.

2. **Repo-level Claude instructions matter.** If the closeout rule is missing from active `CLAUDE.md` files, the system quietly degrades back to manual reminders.

3. **This is not autonomous memory magic.** It is a controlled intake pipeline. That's why it works.
