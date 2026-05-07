---
orphan: true
---

> Draft operational policy; not legal advice; not a contract.
> Subject to qualified legal review before any binding use.
> Korea first-to-file rule applies; consult a Korean patent
> attorney before any further public disclosure of candidate
> inventions.

# Trade secret policy

Trade secret protection covers material whose value depends on it
remaining confidential. Once such material is publicly disclosed,
trade secret protection is lost; that is the structural difference
versus patents and copyrights.

## What is treated as trade secret

| Category | Reason for trade-secret treatment |
| --- | --- |
| **PCCX ProCore RTL bundles** | Hardened, integration-tuned RTL whose competitive value depends on it not being public. The published open core covers the architectural baseline; ProCore extends it under commercial terms. |
| **Enterprise compiler backend** | The closed compiler backend that targets the IP-core's instruction stream for commercial customers. The reference frontend or open-source compiler interface is not trade secret; the closed backend is. |
| **Timing / PPA scripts** | Scripts and configuration that achieve specific power, performance, and area outcomes on real silicon. These contain accumulated tuning and are not part of the open release. |
| **Customer-specific optimizations** | Engineering work delivered under commercial-track contracts to a specific customer. The customer's contract may further govern use; the project does not republish customer-specific work. |

## What is *not* trade secret

- Anything in the open repositories under the project's open
  licence. Once published in `pccx`, `pccx-v00N`, or the
  application integration repos, material is no longer trade
  secret.
- The architectural spec, ISA reference, register/memory maps, and
  other public documentation under `pccx/docs/`.
- The reference flows that exist to demonstrate the open core (sim
  wrapper, evidence pack index, fresh-clone reachability).

## Access control

- Trade-secret material lives outside the open repositories. It is
  stored, accessed, and shared under separate confidentiality
  controls.
- Access is granted role-by-role under written confidentiality
  obligations: NDAs for evaluators, employment agreements for
  staff, commercial-track contracts for customers.
- Access logs and authorisation records live with the project's
  primary entity, not in this repository.

## Boundary against the open track

Open-track contributors never see trade-secret material as part of
their open-track work. The two streams are deliberately separated;
crossing the boundary requires a written confidentiality agreement
in advance.

## Boundary against patent strategy

A candidate invention can only be classified as **patent candidate**
or **trade secret candidate**, not both. Patent filing requires
disclosure that destroys trade secret status; trade-secret protection
requires non-disclosure that prevents patent filing. The
classification decision lives in the
[patent strategy](patent-strategy.md) page.

## Status

Trade-secret material is not enumerated in this public page. This
page only describes the policy. Specific items, access lists, and
custody records are kept under the confidentiality controls
described above.
