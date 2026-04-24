# Gateway Exposure Hardening

How to harden an OpenClaw gateway that binds to your LAN without leaving browser-origin checks and auth throttling in their factory-default weak state.

**Tested on:** OpenClaw 2026.4.x, Ubuntu 24.04, local gateway on `bind: "lan"`
**Last updated:** 2026-04-21

---

## The Problem

The easiest way to get OpenClaw working on a real network is also the easiest way to leave it too open:

- `gateway.bind: "lan"`
- no explicit `gateway.controlUi.allowedOrigins`
- `dangerouslyAllowHostHeaderOriginFallback: true`
- no `gateway.auth.rateLimit`

That combination works. It also weakens your boundary for the Control UI and makes brute-force auth attempts cheaper than they should be.

If your gateway is reachable from anything beyond strict loopback, fix this first.

## Hardened Baseline

Use an explicit origin allowlist and auth throttling.

```json
{
  "gateway": {
    "bind": "lan",
    "controlUi": {
      "allowedOrigins": [
        "http://127.0.0.1:18789",
        "http://localhost:18789",
        "http://<HOST_LAN_IP>:18789"
      ],
      "dangerouslyAllowHostHeaderOriginFallback": false
    },
    "auth": {
      "mode": "token",
      "rateLimit": {
        "maxAttempts": 10,
        "windowMs": 60000,
        "lockoutMs": 300000,
        "exemptLoopback": true
      }
    }
  }
}
```

### Why this baseline

- **Explicit origins** beat Host-header fallback every time.
- **Loopback stays convenient** with `exemptLoopback: true`.
- **LAN access still works** for the exact dashboard origins you use.
- **Auth abuse gets slowed down** instead of running unthrottled.

## Before / After

### Before

```json
{
  "gateway": {
    "bind": "lan",
    "controlUi": {
      "dangerouslyAllowHostHeaderOriginFallback": true
    },
    "auth": {
      "mode": "token"
    }
  }
}
```

### After

```json
{
  "gateway": {
    "bind": "lan",
    "controlUi": {
      "allowedOrigins": [
        "http://127.0.0.1:18789",
        "http://localhost:18789",
        "http://<HOST_LAN_IP>:18789"
      ],
      "dangerouslyAllowHostHeaderOriginFallback": false
    },
    "auth": {
      "mode": "token",
      "rateLimit": {
        "maxAttempts": 10,
        "windowMs": 60000,
        "lockoutMs": 300000,
        "exemptLoopback": true
      }
    }
  }
}
```

## Implementation

### 1. Check the schema first

```bash
openclaw config schema lookup gateway.controlUi
openclaw config schema lookup gateway.auth.rateLimit
```

### 2. Patch the Control UI origin policy

Preferred path:

```bash
openclaw config patch '{
  "gateway": {
    "controlUi": {
      "allowedOrigins": [
        "http://127.0.0.1:18789",
        "http://localhost:18789",
        "http://<HOST_LAN_IP>:18789"
      ],
      "dangerouslyAllowHostHeaderOriginFallback": false
    }
  }
}'
```

### 3. Add auth rate limiting

If your config helper blocks `gateway.auth` edits as a protected path, edit `~/.openclaw/openclaw.json` directly and restart the gateway.

```json
"auth": {
  "mode": "token",
  "token": "...",
  "rateLimit": {
    "maxAttempts": 10,
    "windowMs": 60000,
    "lockoutMs": 300000,
    "exemptLoopback": true
  }
}
```

Then:

```bash
openclaw gateway restart
```

## Verification

```bash
# Show the hardened gateway block
jq '.gateway | {bind, controlUi, auth: {mode: .auth.mode, rateLimit: .auth.rateLimit}}' \
  ~/.openclaw/openclaw.json

# Run the security audit section only
openclaw status | sed -n '/Security audit/,+18p'
```

Expected result:

- no critical warning about Host-header origin fallback
- no warning about missing auth rate limiting on a LAN-bound gateway

## Gotchas

1. **List every origin you actually use.** If you open the dashboard from a different hostname or IP than the allowlist, websocket auth will fail and the UI will look broken.

2. **`allowedOrigins` wants full origins, not hosts.** Include `http://` or `https://` and the port.

3. **Loopback exemption is fine.** It preserves local ergonomics without relaxing the LAN boundary.

4. **This is not internet exposure guidance.** If you are publishing OpenClaw beyond a trusted LAN, put it behind a real reverse proxy and tighten auth even further.
