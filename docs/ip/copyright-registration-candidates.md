---
orphan: true
---

> Draft operational policy; not legal advice; not a contract.
> Subject to qualified legal review before any binding use.

# Copyright registration candidates

Public-safe view of which PCCX artefacts are candidates for an
explicit copyright registration in addition to the
licence-and-source-header coverage already in place.

## Default position

The Apache-2.0 licence on each repository, combined with per-file
SPDX headers (see [`copyright-header-policy.md`](copyright-header-policy.md)),
is enough to assert and license copyright in most jurisdictions.

A separate copyright registration (e.g. with the Korea Copyright
Commission) is **not required** for the open core. It is
optionally useful in two cases:

1. Establishing a cleaner evidentiary record for jurisdictions
   where registration affects remedies or burden of proof.
2. Capturing a specific *snapshot* of a particular work for use in
   commercial / legal contexts (e.g. an enterprise customer asks
   for evidence that the project owns a particular release).

## Candidate snapshots

| Artefact | Why register | Decision |
| --- | --- | --- |
| `pccx` documentation set as of a public-notice release | Establishes a snapshot of the canonical specification at a point in time | TBD; coordinate with the trademark docket and any forthcoming public release |
| `pccx-v002` IP-core package as of a tagged release | Establishes a snapshot of the reusable RTL package | TBD; gated on a tagged `v002` release |
| Reference SDK / simulator releases | Establishes a snapshot of the open-track tooling | TBD |
| ASIC layout (when produced) | Layout-design rights also apply; copyright is secondary | TBD; not applicable today (RTL stage) |

## What this page does not do

- It does not file anything.
- It does not promise registration timelines.
- It does not modify the underlying open licence.

## Update procedure

When a registration decision is made for any candidate, this page
records:

- artefact identifier (repo, tag, or commit SHA);
- jurisdiction;
- registration outcome (filed / granted / withdrawn);
- public reference (registration number, if applicable).

It does **not** record private materials (applicant identifiers,
receipts, internal correspondence). Those live under
[`private-disclosure-boundary.md`](private-disclosure-boundary.md).
