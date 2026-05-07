---
orphan: true
---

> Draft operational policy; not legal advice; not a contract.
> Subject to qualified legal review before any binding use. Korea
> first-to-file rule applies; consult a Korean patent attorney
> before any further public disclosure of candidate inventions.

# Patent candidate intake

Procedure that runs *before* a candidate invention enters any public
PCCX artefact (commit, doc page, paper, talk, demo, or release).

## Trigger

A candidate invention enters intake when any of the following is
true:

- An engineer believes a piece of work may be novel.
- A reviewer flags a piece of work as potentially novel.
- A draft public artefact (paper, talk, doc) is being prepared that
  describes a piece of work that has not been disclosed yet.

## Intake steps

1. **Identify** the smallest novel claim. Distinguish from the
   prior art the project is already aware of.
2. **Classify** into exactly one of:
   - already-publicly-disclosed,
   - not-public-yet,
   - patent-candidate,
   - trade-secret-candidate,
   - defensive-publication-candidate.
   When classification is unclear, default to *not-public-yet* and
   route to qualified legal review before any further public
   action.
3. **Record** the candidate in the private docket. Public PCCX
   repositories receive only the *category* of the candidate; see
   [`patent-strategy.md`](patent-strategy.md) for the categories.
4. **Decide** before disclosure:
   - patent-candidate → file before any further public disclosure,
   - trade-secret-candidate → keep out of public repos and apply
     [`trade-secret-policy.md`](trade-secret-policy.md),
   - defensive-publication-candidate → publish in a form that
     establishes timestamp and authorship under the project's name.
5. **Verify** that the chosen disposition is consistent with the
   underlying repository licence (Apache 2.0 already includes a
   contributor patent grant; see [`../../PATENTS.md`](../../PATENTS.md)).

## Disclosure review checklist

Before a public artefact lands that may describe a candidate
invention, the reviewer checks:

- [ ] Is the smallest novel claim explicitly described?
- [ ] Has the candidate been classified per step 2?
- [ ] If patent-candidate, is the corresponding filing ready or has
      qualified legal review explicitly approved deferring it?
- [ ] If trade-secret-candidate, is the public artefact stripped of
      the secret content?
- [ ] If defensive publication, is the timestamp and authorship
      established?
- [ ] Has the public-safe / private boundary in
      [`private-disclosure-boundary.md`](private-disclosure-boundary.md)
      been respected?

## Failure modes

- A candidate is published before classification → patent-candidate
  status may be lost in jurisdictions with no novelty grace period.
  This is the dominant failure mode for first-to-file regimes.
- A candidate is classified as trade-secret but appears in a public
  artefact → trade-secret status is forfeited.
- A defensive publication is missing timestamp/authorship → the
  prior-art value is weakened.

## Linked

- [`patent-strategy.md`](patent-strategy.md) — categories of
  candidates.
- [`../../PATENTS.md`](../../PATENTS.md) — operational posture +
  Apache 2.0 patent grant note.
- [`private-disclosure-boundary.md`](private-disclosure-boundary.md)
  — what is never committed to public repos.
