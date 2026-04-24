# Upgrade and Drift Checklist

How to survive OpenClaw upgrades without losing the boring glue that makes your actual deployment work.

**Tested on:** OpenClaw 2026.4.x, Ubuntu 24.04, systemd user service, ACPX plugin, custom hooks and channel setup
**Last updated:** 2026-04-21

---

## The Real Problem

OpenClaw upgrades usually do not break the obvious thing. They break the little deployment-specific assumptions around it:

- plugin entries drift
- systemd customizations disappear
- env injection stops loading
- gateway hardening gets reset
- ACP still exists, but not the way you configured it

If you upgrade often and do not run a post-upgrade checklist, you are gambling.

## Post-Upgrade Checklist

Run these in order.

### 1. Confirm the gateway is alive

```bash
openclaw status
```

### 2. Re-check plugin load and entries

```bash
jq '.plugins.allow' ~/.openclaw/openclaw.json
jq '.plugins.load.paths' ~/.openclaw/openclaw.json
jq '.plugins.entries.acpx' ~/.openclaw/openclaw.json
```

Look for:

- `acpx` still present in `plugins.allow`
- custom plugin load paths still present
- ACPX entry still enabled with the expected config

### 3. Re-check service overrides and env injection

```bash
systemctl --user cat openclaw-gateway.service
```

If you rely on `EnvironmentFile=`, verify it still exists. This is a repeat offender.

### 4. Re-check security-sensitive config drift

```bash
jq '.gateway.controlUi, .gateway.auth.rateLimit, .tools.exec, .agents.defaults.sandbox' \
  ~/.openclaw/openclaw.json

openclaw status | sed -n '/Security audit/,+18p'
```

### 5. Re-check channels

```bash
openclaw status --deep
```

You want configured accounts present and healthy, not just “the service started.”

### 6. Re-check cron jobs

```bash
openclaw cron list --json | jq '.[] | {name, enabled, next: .state.nextRunAtMs, last: .state.lastRunStatus, delivery: .delivery}'
```

Focus on:

- jobs disabled unexpectedly
- `lastRunStatus: "error"`
- missing explicit `delivery.to`

### 7. Re-check agent model routing

```bash
jq '.agents.defaults.model, .agents.list[] | {id, model}' ~/.openclaw/openclaw.json
```

### 8. Re-check file permissions

```bash
find ~/.openclaw -type f \( -name 'auth-profiles.json' -o -name 'openclaw.json' \) -printf '%m %p\n'
```

## Fast Triage Table

| Symptom | Most likely cause |
|--------|-------------------|
| Gateway starts but tools or plugins are missing | `plugins.allow` or `plugins.entries` drift |
| Service crash-loops after upgrade | lost env injection or invalid config |
| Claude ACP stopped working | ACPX entry drift or Claude CLI path issue |
| Web UI behaves weird on LAN | Control UI origin policy drift |
| Cron jobs exist but output vanishes | delivery target drift |

## Suggested Wrapper Pattern

If you update often, wrap the upgrade with your own post-checks.

```bash
#!/usr/bin/env bash
set -euo pipefail

openclaw update
openclaw status
jq '.plugins.entries.acpx' ~/.openclaw/openclaw.json
systemctl --user cat openclaw-gateway.service | grep EnvironmentFile || true
openclaw cron list --json >/dev/null
```

It does not need to be fancy. It just needs to stop you from trusting a green install message.

## Gotchas

1. **A successful restart is not a successful upgrade.** It only means the binary launched.

2. **Minor version bumps are enough to reintroduce config drift.** Treat every upgrade like it might reset one custom thing you forgot mattered.

3. **Write down the weird stuff.** If your deployment depends on one ugly local override, document it now instead of rediscovering it at 1:40 AM.
