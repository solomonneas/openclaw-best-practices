# AGENTS.md template for frontend repos

Use this when a repo has meaningful UI work and you want coding agents to follow the design contract instead of improvising.

```md
# AGENTS.md

## Read this first

1. `AGENTS.md`
2. `README.md`
3. `DESIGN.md`
4. any active spec or task file for the current work

## Frontend rule

If the task touches UI, layout, styling, or component behavior:
- read `DESIGN.md` first
- treat its tokens and rules as authoritative
- do not invent new colors, radii, spacing, or typography values unless the task explicitly updates the design system

## Handoff rule

If work changes lanes or pauses:
- create a handoff using `templates/cross-lane-handoff.md`
- include files, constraints, verification, and the exact next action

## Variant rule

If the task asks for alternatives:
- keep the existing design contract intact
- generate variants against the contract, not against vague style adjectives
- use `templates/frontend-variant-request.md` when helpful
```
