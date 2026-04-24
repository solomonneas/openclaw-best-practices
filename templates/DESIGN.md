---
colors:
  primary: "#2563eb"
  secondary: "#0f172a"
  accent: "#14b8a6"
  surface: "#ffffff"
  background: "#f8fafc"
  text: "#0f172a"
typography:
  font-sans: "Inter, ui-sans-serif, system-ui, sans-serif"
  font-mono: "JetBrains Mono, ui-monospace, monospace"
  scale:
    body: "16px"
    h1: "48px"
    h2: "36px"
    h3: "24px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "40px"
rounded:
  sm: "8px"
  md: "14px"
  lg: "24px"
components:
  button:
    radius: "{rounded.md}"
    paddingY: "{spacing.sm}"
    paddingX: "{spacing.md}"
  card:
    radius: "{rounded.lg}"
    padding: "{spacing.lg}"
---

# Overview

Describe the product feel in one short paragraph. Focus on tone, density, and interaction style.

# Colors

- State where the brand color should dominate.
- State where neutral surfaces should dominate.
- Call out any forbidden color behavior.

# Typography

- Define hierarchy and reading rhythm.
- Call out where mono should appear.
- Note any casing or weight preferences.

# Layout

- Define max width, grid behavior, and section spacing.
- Note whether the layout should feel dense, airy, editorial, or dashboard-heavy.

# Elevation and depth

- State whether the system uses flat surfaces, soft shadows, hard borders, or both.

# Shapes

- Describe corner radius philosophy.
- Note whether shapes should feel sharp, soft, or mixed.

# Components

## Buttons
- Primary button behavior
- Secondary button behavior

## Cards
- Padding, border, and hover expectations

## Forms
- Input density and error-state tone

# Do

- Keep spacing consistent with the token scale.
- Reuse the same surface treatment across repeated components.
- Preserve hierarchy through type and spacing before adding decoration.

# Do not

- Invent new token values without updating this file.
- Mix unrelated radius styles on the same screen.
- Use decorative gradients or shadows unless the system explicitly calls for them.
