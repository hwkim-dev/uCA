# PCCX IP policy (operational, draft)

Status: draft operational policy; not legal advice; not a contract;
subject to qualified legal review before any binding use.

## Public / private boundary

PCCX maintains a deliberate boundary between what is published in
open repositories and what is held under separate confidentiality
controls.

| Layer | Public (open licence) | Private (separate controls) |
| --- | --- | --- |
| Architecture | PCCX Standard, ISA reference, register/memory map docs | n/a |
| RTL | Reusable v00N OpenCore RTL | ProCore hardened RTL bundles |
| Software | Reference SDK, simulator, conformance harness | Enterprise compiler backend, runtime extensions |
| ASIC tooling | Documentation only | ASICKit deliverables, PPA / timing-closure scripts |
| Customer work | Documentation of *categories* only | Customer-specific optimisations, NRE deliverables |
| Patents | Categories of candidates | Specific candidate inventions and disclosures |
| Trade secrets | Treated as out of scope of public repos | Trade-secret register, access-control records |
| Trademarks | Pending PCCX™ in KR Class 09 / 42 | Filing customer numbers, payment receipts, contact details |

Anything published under the open licence is, from that moment,
public domain for the purposes of any further patent application by
the project. Trade-secret protection is forfeited by publication.

## What this file is

A single index that points at the layered policy:

- [`TRADEMARKS.md`](TRADEMARKS.md) — canonical trademark policy.
- [`docs/ip/`](docs/ip/README.md) — IP layers (patent, trademark,
  trade secret, CLA, filing log, intake, boundary).
- [`docs/commercial/`](docs/commercial/README.md) — commercial
  tracks (open, commercial, capital) and the
  contributor-vs-sponsor-vs-investor separation matrix.
- [`PATENTS.md`](PATENTS.md) — patent posture.
- [`DCO.md`](DCO.md) — sign-off intent (draft).
- [`NOTICE`](NOTICE) — public-safe trademark + copyright notice.

## What contributors do not receive

Contributing code, documentation, or evidence to this repository
does **not** entitle the contributor to equity, royalties, revenue
share, profit share, employment, sponsorship payments, investor
returns, IP ownership, or future commercial licence rights beyond
the licence in effect at the time of merge.

## Layout-design rights

Layout-design rights (e.g. Korea's Act on the Layout-Designs of
Semiconductor Integrated Circuits) become relevant only when an
ASIC layout / GDS / mask work is produced by the project. The
current PCCX repositories are pre-layout (RTL + spec only); no
layout-design right claim is asserted today. When and if an ASIC
layout is produced, the project will publish a separate layout-design
notice and registration record.

## Not legal advice

Reading this document is not a substitute for legal counsel. Any
binding use (CLA, sponsorship terms, investor terms, trademark
registration claim, patent filing, trade-secret enforcement, layout
registration) requires qualified legal review.
