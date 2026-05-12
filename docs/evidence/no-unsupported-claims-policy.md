---
orphan: true
---

> Draft operational policy. Not legal advice. Subject to legal, tax,
> accounting, securities, and IP counsel review before use. Not an
> offer to sell securities. Not an investment solicitation.
> Sponsorship is not investment and provides no financial return.
> Contributions do not create equity, royalties, revenue share,
> profit share, employment, sponsorship payments, or investor returns.

# No-unsupported-claims policy

PCCX™ public docs and PRs must not claim any of the following
without measured, reproducible evidence (each phrase is the
*exact* claim form that requires evidence):

- board inference operability
- end-to-end Gemma 3N E4B runtime on KV260
- numeric throughput claims or targets without measurement
- timing-closure completion
- bitstream-success outcomes
- production-readiness
- stable application interface or stable application binary interface
- conformance certification (e.g. an "official" badge or a
  "PCCX-Compatible" badge)
- frames-per-second numeric figures
- mean-average-precision numeric figures

In short: any phrase that asserts the existence of a measured
hardware / runtime / timing / bitstream / latency / accuracy /
certification outcome must be backed by a reproducible measurement
or marked TBD.

The CI banned-claim grep is run before merge of any release / docs /
metadata PR. See `docs/evidence/release-evidence-gate.md`.
