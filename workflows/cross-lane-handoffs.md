# Cross-Lane Handoffs

How to move work cleanly between OpenClaw, Codex, Claude Code, and other agent lanes without losing state, duplicating effort, or making the next agent reverse-engineer your intent.

**Tested on:** OpenClaw orchestration, Codex build lanes, Claude Code review lanes, structured task-file handoffs
**Last updated:** 2026-04-24

---

## The problem

Most multi-agent failures are not model failures. They are handoff failures.

One lane knows the goal. Another lane knows the files. A third lane knows the blocker. None of them wrote it down in a way the next lane can actually use.

## The rule

**If work changes lanes, leave a structured artifact.**

Do not rely on:
- chat memory
- vague "continue from here" prompts
- a wall of transcript pasted into the next tool

## When a handoff is required

Create a handoff when any of these are true:
- a different model or tool lane will continue the work
- the task pauses and will resume later
- implementation and review happen in different places
- a frontend task moves from design to build to polish
- the next agent needs exact verification steps

## Minimum handoff shape

Every useful handoff should answer six things:

1. **Goal**: what outcome is being pursued
2. **Current state**: what is already done
3. **Files**: exact paths that matter
4. **Constraints**: what must not change
5. **Verification**: how to prove success
6. **Next action**: the specific next move for the receiving lane

## Recommended template

Use `templates/cross-lane-handoff.md`.

The handoff should be short enough to scan in under a minute and specific enough that the next lane can act immediately.

## Lane roles

### OpenClaw orchestrator

Best for:
- writing the plan
- setting constraints
- deciding who should do what next
- synthesizing results back to the user

### Codex or coding lane

Best for:
- implementation
- mechanical refactors
- file edits and test passes
- producing diffs and concrete outputs

### Claude Code or review lane

Best for:
- design critique
- architecture review
- polish passes
- human-quality review when taste matters

## Good handoff example

```md
# Cross-Lane Handoff

## Goal
Publish-safe cleanup of the docs repo and add reusable templates.

## Current state
- README and agent bootstrap docs already updated once
- private network examples still exist in security docs
- no templates/ folder exists yet

## Files
- README.md
- AGENTS.md
- INSTALL_FOR_AGENTS.md
- security/linux-hardening.md
- security/wsl-hardening.md

## Constraints
- remove personal hostnames and exact LAN IPs
- keep commands runnable with placeholders
- do not expose private paths or host labels

## Verification
- rg for private IPs and personal hostnames returns no hits
- llms docs rebuild cleanly

## Next action
Sanitize the listed docs, add the templates folder, rebuild llms artifacts, then report the final file list.
```

## Bad handoff example

"I cleaned some stuff up. You can probably finish it from here."

That is not a handoff. That is sabotage with friendly branding.

## File vs prompt

### Use a real handoff file when:
- multiple lanes may touch the task
- the work may pause or span sessions
- exact paths and constraints matter

### Use an inline prompt only when:
- the task is tiny
- the receiving lane can finish it immediately
- no one will need to resume later

## Relationship to memory handoffs

A cross-lane handoff moves **task state**.
A memory handoff moves **durable knowledge**.

Sometimes a task produces both. Treat them as separate artifacts.

## Recommended repo layout

```text
templates/cross-lane-handoff.md
templates/memory-handoff.md
templates/frontend-variant-request.md
```

If a repo has heavy agent traffic, document the handoff rule in `AGENTS.md` too.

## Verification

```bash
# Check that the repo points people at the handoff guide and template
rg -n "cross-lane handoff|templates/cross-lane-handoff\.md|DESIGN\.md" README.md AGENTS.md workflows
```

Expected result:
- guide exists
- template exists
- bootstrap docs reference the workflow where appropriate

## Gotchas

1. **Do not paste whole transcripts.** Summarize the task state instead.
2. **If files are missing from the handoff, the next lane will guess.** Guessing is where avoidable damage happens.
3. **A handoff without verification is just a hope note.**
4. **If constraints matter, write them down explicitly.** "Keep behavior the same" is not the same as naming the invariant.
