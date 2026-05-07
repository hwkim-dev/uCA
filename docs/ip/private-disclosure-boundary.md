---
orphan: true
---

> Draft operational policy; not legal advice; not a contract.
> Subject to qualified legal review before any binding use.

# Private disclosure boundary

Defines what is *never* committed to public PCCX repositories,
regardless of how convenient it would be to keep next to the related
docs.

## Always private

The following items must not appear in public repositories. They are
kept under separate confidentiality controls (e.g. a private docket
repository, encrypted storage, or off-line records).

| Item | Where it lives | Why |
| --- | --- | --- |
| Trademark filing artefacts (특허고객번호, raw XML, payment receipts, applicant private contact details, screenshots containing personal data) | Private docket / personal records | KIPRIS-published metadata is OK; raw filing materials are not. |
| Detailed patent claims for not-yet-public candidate inventions | Private docket | Public disclosure can defeat patentability. |
| ProCore / Enterprise SDK / ASICKit implementation details | Private engineering repos under separate confidentiality controls | Trade-secret protection. |
| Customer-specific optimisations and integration details | Per-customer engineering deliverables under contract | Trade-secret + customer contractual obligations. |
| Investor / sponsor / customer contract drafts that are not yet final | Private legal repository | Drafts are not the same as published policy. |
| Internal financial projections, burn-rate, cap table, term sheets | Private finance repository | Not project-level engineering material. |
| Personal contact details (phone numbers, residential addresses, ID numbers) | Off-repo records | Privacy. |
| Anything marked "confidential" by a counterparty under NDA | Per-NDA storage | Contractual obligation. |

## Public-safe equivalents

For each private item there is usually a public-safe equivalent:

| Private item | Public-safe equivalent |
| --- | --- |
| Raw trademark filing | Application number, class, filing date, status (see [`trademark-filing-log.md`](trademark-filing-log.md)) |
| Specific patent claim | Category of candidate (see [`patent-strategy.md`](patent-strategy.md)) |
| ProCore RTL bundle | OpenCore RTL package (`pccx-v00N`) |
| Customer optimisation report | Architectural pattern published as a docs page once generalised |
| Investor term sheet | Description of the capital track structure (see [`../commercial/capital-track.md`](../commercial/capital-track.md)) |

## Verification

Public PRs are scanned before merge for the patterns listed in
[`copyright-header-policy.md`](copyright-header-policy.md) and for
private-disclosure leaks (e.g. customer numbers, raw filing IDs,
personal phone / address lines). The scan is best-effort and does
not replace human review.

## Not legal advice

Subject to qualified legal review before any binding use. If in
doubt about whether an item belongs on the private side, default to
private.
