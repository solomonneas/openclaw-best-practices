# DESIGN.md as a Frontend Contract

How to use `DESIGN.md` as the visual source of truth for agent-driven frontend work so Codex, Claude Code, and OpenClaw stop inventing a new design system every pass.

**Tested on:** Astro + Tailwind workflows, agent-driven UI rebuilds, screenshot-to-code and variant passes
**Last updated:** 2026-04-24

---

## Why this exists

Prompt adjectives are not a design system.

If you tell three coding agents to build something "clean, modern, and minimal," you usually get three different spacing scales, three different radii, and at least one cursed button. `DESIGN.md` fixes that by giving every lane the same visual contract.

## What `DESIGN.md` is

`DESIGN.md` is a plain-text design artifact with two jobs:

1. **machine-readable tokens** in YAML frontmatter
2. **human-readable intent** in markdown sections

That makes it good for both coding agents and humans reviewing the work.

## Repo pattern

For any frontend that matters, keep these files near the project root:

```text
DESIGN.md
AGENTS.md
reference/design/            # optional screenshots or inspiration
```

Recommended support files:

```text
templates/DESIGN.md
templates/AGENTS.md
templates/frontend-variant-request.md
```

## Workflow

### 1. Write or update `DESIGN.md` first

Define the rules before generating UI:
- color tokens
- typography scale
- spacing rhythm
- radius and elevation
- component behavior
- explicit do / do not rules

### 2. Make agents read it before frontend work

Your repo-level `AGENTS.md` should say:
- read `DESIGN.md` before changing UI
- treat design tokens as authoritative
- do not invent new colors, radii, or spacing unless the task is a design-system update

### 3. Use structured variant requests

When you want alternatives, request them against the contract, not against vibes.

Bad:
- "make it pop more"

Good:
- "keep the existing token system, preserve density, and explore two hero-layout variants that improve scanability"

### 4. Diff design-system changes deliberately

If a task changes the design system itself, call that out as a contract change, not a random UI tweak.

### 5. Export or mirror tokens carefully

If your stack uses Tailwind or CSS custom properties, derive them from the same `DESIGN.md` contract instead of manually maintaining three competing token sets.

## Recommended section shape

A useful `DESIGN.md` usually includes:

1. Overview
2. Colors
3. Typography
4. Layout
5. Elevation and depth
6. Shapes
7. Components
8. Do and do not rules

## Good use cases

- public marketing sites
- dashboards with repeated UI patterns
- redesign projects with multiple agent passes
- screenshot recreation or clone workflows
- frontend variant generation where consistency matters

## Bad use cases

- quick internal throwaway pages
- prototypes you genuinely do not care about maintaining
- projects with no visual system beyond default framework styles

## Verification

```bash
# Validate the design contract if you use the official tooling
npx @google/design.md lint DESIGN.md

# Spot-check that agents were pointed at the contract
rg -n "DESIGN\.md" AGENTS.md README.md
```

Expected result:
- `DESIGN.md` exists
- `AGENTS.md` points agents at it before UI work
- variant requests reference the contract instead of restyling from scratch

## Gotchas

1. **`DESIGN.md` is a contract, not decoration.** If agents ignore it, the file is dead weight.
2. **Do not stuff implementation details into tokens.** Keep the contract at the design-system layer.
3. **One contract per product surface is usually enough.** Do not create a new `DESIGN.md` for every page unless the product truly has separate design systems.
4. **If the UI changed but the contract did not, expect drift.** Update both when the system changes.
