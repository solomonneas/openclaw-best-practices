# AGENTS.md

This repo uses a lightweight agent-context pack so new agents can orient fast without guessing.

## Read This First

1. `AGENTS.md`
2. `README.md`
3. `configuration/multi-model-orchestration.md`
4. `security/agent-security-hardening.md`
5. `workflows/sub-agent-patterns.md`
6. `workflows/cross-lane-handoffs.md`
7. `workflows/design-contracts.md`
8. `workflows/session-management.md`
9. `llms.txt or llms-full.txt`

## Context Sources

- `README.md`
- `configuration/multi-model-orchestration.md`
- `security/agent-security-hardening.md`
- `workflows/sub-agent-patterns.md`
- `workflows/cross-lane-handoffs.md`
- `workflows/design-contracts.md`
- `workflows/session-management.md`

## Operating Guidance

- Treat this repo's existing docs as source of truth.
- Keep generated agent docs in sync with real docs.
- Prefer small curated context packs over dumping the whole repo into `llms-full.txt`.
- If a task touches frontend behavior, read the `DESIGN.md` workflow and use the templates folder instead of inventing structure.
- If behavior changes, update both the human-facing docs and the agent-facing entrypoints in the same pass.

## Verification

Run:

```bash
python3 scripts/build-llms.py
python3 scripts/check-llms.py
```
