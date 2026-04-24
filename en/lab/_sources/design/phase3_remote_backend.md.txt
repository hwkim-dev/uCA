# Phase 3 — Secure Remote Backend

**Status:** scaffold landed (2026-04-24, `pccx-remote` crate + OpenAPI draft); implementation kicks off in Phase 3 proper.
**Scope:** roadmap Weeks 10-13; milestones M3.1 - M3.6.
**Target experience:** "GitHub Codespaces, but 100% secure" — install pccx-remote on a workstation, connect from a laptop, session indistinguishable from local.

## 1. Threat model

Attack surface = auth layer + tunnel + session isolation.  Three
adversaries to model:

| Adversary | Capability | Mitigation |
|---|---|---|
| Network attacker (MITM) | passive + active on any path between client & server | mTLS-over-QUIC, hardware-bound device keys, no cleartext anywhere |
| Compromised endpoint | runs arbitrary code on one side | OIDC + hardware 2FA, per-session sandbox, kill-switch |
| Insider (same org) | valid credentials, elevated intent | per-project RBAC, append-only audit log replicated off-box |

STRIDE applied to each protocol message: spoofing countered by device
+ user dual auth; tampering by QUIC AEAD; repudiation by audit log;
information disclosure by per-project encryption at rest; denial of
service is rate-limited at the tunnel entrypoint; EoP gated by RBAC.

## 2. Tunnel

**Default: WireGuard.**  Well-understood threat model, built-in key
rotation, zero configuration surprise.  Fallback: mTLS over QUIC (for
networks that block UDP or require TCP egress).

- Device keys are Curve25519, generated inside a hardware token
  (YubiKey / TPM 2.0) and **never exported**.  Loss of the token =
  revocation via audit log.
- Peer list authenticated by OIDC identity — WireGuard AllowedIPs
  tied to user + session, not to IP.
- Keepalive 25s; idle sessions auto-terminate after 30 min (configurable).

## 3. Auth layer

### 3.1 OIDC + hardware 2FA

- Client redirects to the configured OIDC provider (Google Workspace
  / Azure AD / Authentik).
- JWT returned, then augmented with a WebAuthn challenge satisfied by
  the hardware token.
- Session issued as a Ed25519-signed bearer token with a 12-hour hard
  expiry + 30-min sliding expiry.

### 3.2 RBAC

- Three roles today: `owner`, `maintainer`, `viewer`.
- Per-project scoping via the `projects` claim in the session token.
- All reads/writes check `can(user, project, action)` via a tiny
  Casbin-style policy table in pccx-remote.

## 4. Session isolation

Each session gets:

- A process namespace (pid, net, mount) — systemd user scope.
- An **overlayfs sandbox** rooted at `/var/lib/pccx-remote/sessions/<uuid>/`.
  Reads fall through to the project tree; writes stay in the overlay
  and are squashed or discarded at session end.
- CPU + memory cgroup (configurable per project).
- Network access defaults to **deny-all** — session opts in per tool
  (e.g. `cargo fetch` requires an explicit allow entry in project
  config).

**Kill-switch**: `DELETE /v1/sessions/{id}` or the audit log's "revoke"
event yanks the namespace in ~100 ms.

## 5. REST + WebSocket surface

Already drafted in `crates/remote/openapi.yaml`.  Five endpoint families:

| Family | Prefix | Purpose |
|---|---|---|
| Auth | `/v1/auth` | OIDC login kickoff + session refresh |
| Sessions | `/v1/sessions` | Open / list / kill sessions |
| Traces | `/v1/traces` | Upload .pccx, stream verification verdict |
| Reports | `/v1/reports/{id}` | Fetch rendered report |
| Events | `/v1/events` | WebSocket audit-log subscription |

All paths require the `bearerAuth + deviceKey` security combination.

## 6. Milestones

### M3.1 — Daemon + tunnel (Week 10)

- `pccx-remote` binary skeleton (Tokio + Axum).
- WireGuard control plane via `boringtun-rs` (userspace impl).
- Device-key registration flow; first end-to-end handshake.

### M3.2 — Auth (Week 11)

- OIDC redirect flow (via `oxide-auth` or `openidconnect`).
- WebAuthn challenge + verification (via `webauthn-rs`).
- RBAC policy table + `can(...)` predicate.

### M3.3 — Zero-trust posture (Week 11)

- Every request signed; signature verified by the receiving side.
- Append-only audit log (SQLite with FTS, replicated to S3-compatible store).

### M3.4 — Session manager (Week 12)

- overlayfs sandbox + cgroup v2 resource limits.
- Multi-concurrent sessions per user.
- Kill-switch latency SLA < 200 ms.

### M3.5 — Web client (Week 12)

- **GATED on M3.1-M3.3 complete.**  No remote UI before the auth
  layer lands.
- WASM build of pccx-ide's data-plane surfaces (trace viewer, report
  panel) — full IDE feature parity deferred to Phase 4.

### M3.6 — External pentest + STRIDE review (Week 13)

- Hire an external auditor for a 1-week engagement.
- STRIDE threat model delivered as a tracked doc.
- Any CRITICAL / HIGH finding blocks Phase 3 close.

## 7. Crypto choices

- **No innovation.**  Only proven primitives.
- WireGuard → ChaCha20-Poly1305 + Curve25519 + BLAKE2s (standard).
- JWT → Ed25519 signatures.
- At-rest per-project encryption → age (XChaCha20-Poly1305 + X25519).
- TOTP deprecated in favour of WebAuthn (TOTP code interception has
  been exploited at scale).

## 8. Non-goals

- Multi-tenant SaaS.  pccx-remote is single-operator, self-hosted.
- Streaming video of the remote session (RDP-style).  The native
  Tauri client renders locally from typed IPC messages only.
- Windows host.  Linux primary, macOS best-effort; Windows sessions
  are client-only.

## 9. Open questions

- YubiKey vs TPM for device keys: YubiKey is portable (one token
  works on multiple workstations); TPM is built-in but non-portable.
  Recommend: YubiKey default, TPM fallback behind config flag.
- Audit log storage: SQLite WAL on the box + nightly S3 replication,
  vs. real-time shipping to S3.  Real-time is more secure (insider
  can't tamper in-flight) but adds an SPoF.  Resolve at M3.3.
