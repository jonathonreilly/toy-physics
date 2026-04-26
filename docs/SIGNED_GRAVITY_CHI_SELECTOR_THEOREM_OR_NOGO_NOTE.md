# Signed Gravity `chi_g` Selector Theorem / No-Go Note

**Date:** 2026-04-25
**Status:** first strict local/taste-cell selector no-go; discovery lane remains
open only for broader selector constructions
**Script:** [`../scripts/frontier_signed_gravity_chi_selector_algebra.py`](../scripts/frontier_signed_gravity_chi_selector_algebra.py)

This note records the next P0 step after
[`ANTIGRAVITY_SIGN_SELECTOR_BOUNDARY_NOTE.md`](ANTIGRAVITY_SIGN_SELECTOR_BOUNDARY_NOTE.md)
and
[`SIGNED_GRAVITY_RESPONSE_BACKLOG_2026-04-25.md`](SIGNED_GRAVITY_RESPONSE_BACKLOG_2026-04-25.md).

The first signed-response harness showed that a locked branch label would have
coherent consequences: same-sector attraction, opposite-sector repulsion,
positive inertial mass, and two-body action-reaction. This note asks the harder
question:

> Is there a native local/taste-cell operator `Q_chi` that can be the branch
> label `chi_g = +/-1`?

## Strict Gate

The first scan imposes the following requirements on the retained 8D
Kogut-Susskind taste cell:

```text
Q_chi = Q_chi^dagger
Q_chi^2 = I
dim(P_+) > 0 and dim(P_-) > 0
[Q_chi, Gamma_i] = 0 for the retained kinetic generators
[Q_chi, epsilon] = 0 for the parity-correct scalar/mass channel
epsilon acts as a fixed +/- sign inside the Q_chi branches
```

The last condition is the crucial one. A conserved taste label is not enough.
For `chi_g` to be a signed gravitational source branch, the branch itself must
pin the scalar source sign. Otherwise the branch is only a neutral degeneracy
label.

The scalar operator is the retained parity-correct scalar channel:

```text
H_diag = (m + Phi) epsilon(x)
epsilon = Z tensor Z tensor Z
```

## Scan Surface

The script scans all non-identity 3-qubit Pauli-string involutions on the
8-dimensional taste space:

```text
Q in {I, X, Y, Z}^{tensor 3} \ {I tensor I tensor I}
```

It also reports named candidates:

- `epsilon = ZZZ`
- `i Omega`, where `Omega = Gamma_1 Gamma_2 Gamma_3`
- `C_taste = XXX`
- the three `Gamma_i`

The retained generators match the existing `Cl(3)` support theorem:

- [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
- [`../scripts/verify_cl3_sm_embedding.py`](../scripts/verify_cl3_sm_embedding.py)
- [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md)
- [`../scripts/frontier_cpt_exact.py`](../scripts/frontier_cpt_exact.py)
- [`STAGGERED_FERMION_CARD_2026-04-11.md`](STAGGERED_FERMION_CARD_2026-04-11.md)

## Result

Command:

```bash
python3 scripts/frontier_signed_gravity_chi_selector_algebra.py
```

Summary output:

```text
Pauli-string involutions scanned: 63
kinetic-conserved candidates: 7
massive parity-scalar conserved candidates: 3
scalar-source pinned candidates: 1
strict selector candidates: 0
FINAL_TAG: NO_GO_STRICT_SELECTOR
```

The three candidates that commute with the full massive parity-scalar generator
set are:

| candidate | status | scalar trace in `+/-` sectors |
|---|---|---:|
| `IXY` | conserved neutral taste label | `0, 0` |
| `XYI` | conserved neutral taste label | `0, 0` |
| `XZY` | conserved neutral taste label | `0, 0` |

They are conserved labels, but they do not pin the scalar source sign. In each
branch, the trace of `epsilon` is zero. That is a taste-degeneracy label, not a
signed gravitational source branch.

The candidate that does pin scalar sign is:

| candidate | status |
|---|---|
| `epsilon = ZZZ` | scalar sign pinned but kinetic-broken |

`epsilon` gives branch scalar signs, but it anticommutes with kinetic hopping
and is therefore not a conserved branch of the retained free staggered
Hamiltonian.

The pseudoscalar route also fails this strict gate:

| candidate | status |
|---|---|
| `i Omega = XYX` | kinetic-conserved but broken by parity-scalar mass/coupling |

So `i Omega` is not a branch selector for the retained massive scalar-response
surface.

## Interpretation

The first strict local/taste-cell selector scan gives a no-go:

> No local Pauli-string involution on the retained 8D Kogut-Susskind taste cell
> is both conserved by the massive parity-correct scalar surface and able to
> pin the scalar source sign.

What survives:

- conserved neutral taste labels
- a coherent consequence harness if a branch is externally supplied
- the source/response locking criterion as a necessary condition

What fails:

- `epsilon` as a conserved branch selector
- `i Omega` as a massive scalar-response selector
- any scanned local Pauli-string `Q_chi` as a strict physical `chi_g`

## Claim Boundary

This is not a full mathematical impossibility theorem over every possible
construction. It does not exclude:

- nonlocal/global boundary selectors
- constrained sector-preparation rules
- a source-normalization or variational route that changes the source
  primitive
- a broader interacting-theory superselection mechanism

It does close the simplest local/taste-cell route. Therefore the lane should not
spend major effort on graph portability or phenomenology until one of the
remaining P0 routes changes this result.

## Next Work To Push

The next highest-value work is not family portability. It is the source
primitive:

1. `scripts/frontier_signed_gravity_source_variational_audit.py`
2. `docs/GRAVITY_SIGNED_SOURCE_DENSITY_BOUNDARY_NOTE.md`

The question should be:

> Does the parity-correct scalar coupling variationally source positive
> `|psi|^2`, a signed scalar bilinear, or no branch-fixed signed density at all?

If the source audit also lands negative, the signed-response lane should be
classified as a useful toy/no-go control unless a nonlocal or boundary selector
is proposed explicitly.
