# PMNS `C3` Nontrivial-Character Current Boundary

**Status:** support - structural or confirmatory support note
## Question
Once the retained PMNS lane has been reduced to the native `C3`-character
family, what is the exact smallest remaining sole-axiom source object?

## Answer
It is **one native complex nontrivial-character current**, not a larger value
family.

Let `h_0, h_1, h_2` be the exact native `C3`-character holonomies at phases

```text
0, 2 pi / 3, 4 pi / 3.
```

Define the native current

```text
J_chi(A) := (h_0 + omega h_1 + omega^2 h_2) / 3.
```

On the reduced graph-first PMNS family

```text
A_fwd(u, v, w) = (u + i v) E12 + w E23 + (u - i v) E31
```

one has exactly

```text
J_chi(A_fwd) = chi = u + i v.
```

So the PMNS value-selection problem is not a vague `3`-real problem anymore.
It is exactly the production of one complex native current.

## Boundary
The current exact bank still annihilates this current on every current
sole-axiom retained route:

- the free route
- the sole-axiom `hw=1` source/transfer route
- the retained scalar route

In symbols:

```text
J_chi = 0
```

on all of those routes.

## Consequence
The strongest honest next positive target is now fully explicit:

> derive a sole-axiom law producing nonzero `J_chi` on the retained `hw=1`
> response family.

That is the smallest remaining PMNS-side source object on the current bank.

## Runner

```bash
PYTHONPATH=scripts python3 scripts/frontier_pmns_c3_nontrivial_current_boundary.py
```

Last run (2026-05-10): `PASS=16 FAIL=0` on the present worktree. The
runner exercises five parts: (Part 1) construction of the native C3
character holonomies `h_0, h_1, h_2` at phases `0, 2pi/3, 4pi/3`;
(Part 2) the Fourier-projection identity
`J_chi(A) = (h_0 + omega h_1 + omega^2 h_2) / 3` evaluated on
`A_fwd(u, v, w)` to recover `chi = u + i v`; (Part 3) the
route-annihilation checks `J_chi = 0` on the free, sole-axiom
`hw=1` source/transfer, and cited scalar routes; (Part 4) the
downstream PMNS reduced-data link to `chi`; (Part 5) circularity
guards confirming the native character phases and current take no
PMNS-side target values as inputs.

## Class A bridge derivation

This section makes the two load-bearing algebraic bridges explicit
in-note from the basis already fixed by
`PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE` and the canonical holonomy
probe already fixed by `PMNS_TWISTED_FLUX_TRANSFER_HOLONOMY_BOUNDARY_NOTE`.
Both bridges are finite-dimensional matrix algebra on a fixed `3 x 3`
basis and do not introduce any new primitive.

### Bridge B1: `J_chi(A_fwd) = u + i v` from native holonomies

Fix the canonical graph-first reduced-cycle basis

```text
B1 = E12 + E31
B2 = i (E12 - E31)
B3 = E23
```

so that the reduced graph-first PMNS family is

```text
A_fwd(u, v, w) = u B1 + v B2 + w B3
               = (u + i v) E12 + w E23 + (u - i v) E31.
```

The canonical twisted-flux holonomy probe on this carrier is

```text
P_phi = cos(phi) B1 + sin(phi) B2 + B3,
```

and the flux holonomy at phase `phi` is

```text
h_phi(M) := Re tr(P_phi^* M).
```

The basis Gram matrix is exactly

```text
tr(B_i^* B_j) = diag(2, 2, 1)   for (i, j) in {1, 2, 3}^2,
```

so the three native C3-character holonomies evaluated on `A_fwd` are

```text
h_phi(A_fwd) = Re[ 2 u cos(phi) + 2 v sin(phi) + w ]
             = 2 u cos(phi) + 2 v sin(phi) + w.
```

At the canonical C3 phases `phi in {0, 2 pi / 3, 4 pi / 3}` this gives

```text
h_0 = 2 u + w
h_1 = -u + sqrt(3) v + w
h_2 = -u - sqrt(3) v + w,
```

which is the design-matrix law

```text
(h_0, h_1, h_2)^T = M . (u, v, w)^T,
M = [[ 2,  0,        1],
     [-1,  sqrt(3),  1],
     [-1, -sqrt(3),  1]]
```

already proven in `PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE` (Part 3) by
direct computation. Apply the C3-Fourier projection

```text
J_chi(A) := (h_0 + omega h_1 + omega^2 h_2) / 3,
```

with `omega = exp(2 pi i / 3) = -1/2 + i sqrt(3) / 2`. Collect
coefficients of `u`, `v`, `w` separately:

```text
coeff(u) = ( 2 + omega (-1) + omega^2 (-1) ) / 3
         = ( 2 - (omega + omega^2) ) / 3
         = ( 2 - (-1) ) / 3
         = 1,

coeff(v) = ( 0 + omega sqrt(3) + omega^2 (-sqrt(3)) ) / 3
         = sqrt(3) (omega - omega^2) / 3
         = sqrt(3) (i sqrt(3)) / 3
         = i,

coeff(w) = ( 1 + omega + omega^2 ) / 3
         = 0,
```

using the standard cyclotomic identities `1 + omega + omega^2 = 0` and
`omega - omega^2 = i sqrt(3)`. Therefore

```text
J_chi(A_fwd) = u + i v,
```

as claimed. The readout is a finite linear projection of the three
already-proven native holonomies and does not introduce a new primitive.

### Bridge B2: route-wise annihilation `J_chi = 0` on the three retained routes

The probe `P_phi` is supported entirely off the diagonal of the `3 x 3`
matrix carrier:

```text
diag(B1) = diag(B2) = diag(B3) = 0,
so diag(P_phi) = 0   for every phi.
```

Hence for any diagonal block `D = diag(d_1, d_2, d_3)`,

```text
tr(P_phi^* D) = sum_k (P_phi^*)_{kk} d_k = 0,
so h_phi(D) = 0   for every phi.
```

In particular `h_0(D) = h_1(D) = h_2(D) = 0`, and so

```text
J_chi(D) = (h_0 + omega h_1 + omega^2 h_2) / 3 = 0.
```

It therefore suffices to show that the active block produced by each of
the three named retained routes is diagonal in the canonical cycle
frame.

- **Free route.** The free retained block is `M_free = I3`, which is
  diagonal. Hence `J_chi(I3) = 0`.

- **Sole-axiom `hw=1` source/transfer route.** The `hw=1` triplet
  packet (cf. `PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE` and the
  realising script `scripts/frontier_pmns_sole_axiom_hw1_source_transfer_boundary.py`)
  constructs the active block as the joint-character free-sector
  identity built from the three commuting axis-translation
  projectors `Pi_a = (I + sign_a T_a) / 2`. The three translations
  `T_a` are simultaneously diagonalised in the cycle frame, so their
  joint character projectors `Pi_a` are diagonal, the sum
  `M_src = sum_a Pi_a Pi_id Pi_a = I3` is diagonal, and the derived
  active block from `derive_active_block_from_response_columns` (a
  resolvent kernel inversion of a product of diagonal pieces) is
  diagonal. Direct numerical evaluation at `lam = 0.31`, `lam_pass =
  0.27` confirms the active block is exactly `I3`. Hence
  `J_chi(M_src) = 0`.

- **Retained scalar route.** The scalar route block is `M_scalar = a I3`
  for the scalar amplitude `a` (cf.
  `PMNS_UNIFORM_SCALAR_DEFORMATION_BOUNDARY_NOTE` and the realising
  script `scripts/frontier_pmns_uniform_scalar_deformation_boundary.py`),
  which is diagonal for every scalar amplitude `a`. The derived active
  block from `derive_active_block_from_response_columns` is again a
  resolvent kernel inversion of `a I3` and remains diagonal. Direct
  numerical evaluation at `a = 1.13`, `lam = 0.31` confirms the active
  block is exactly `1.13 I3`. Hence `J_chi(M_scalar) = 0`.

In all three cases the route-wise annihilation `J_chi = 0` follows from
the same one-line fact: the canonical C3-character probe is supported
strictly off the diagonal, and every current sole-axiom retained route
produces a diagonal active block in that frame.

### Scope of this bridge

The two bridges above are class A (finite-dimensional matrix algebra
over the fixed canonical `3 x 3` cycle basis and the canonical
C3-Fourier projection). They do **not** prove that the listed three
retained routes exhaust the current sole-axiom retained-route bank;
that is a separate inventory claim and is treated as a registered
boundary condition in the next section. They also do **not** prove
minimality of "exactly one complex current"; that remains the open
class D target named in the verdict's `notes_for_re_audit_if_any`
field and is registered explicitly below.

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream authority
candidates the load-bearing C3 holonomy / route boundary premise
relies on, in response to the 2026-05-05 audit verdict's
`missing_bridge_theorem` repair target (audit row:
`pmns_c3_nontrivial_current_boundary_note`). It does not promote this
note or change the audited claim scope, which remains the conditional
algebraic identification of the smallest remaining sole-axiom source
object as one native complex C3-nontrivial-character current.

One-hop authority candidates cited:

- [`PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE.md`](PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE.md)
  — currently `unaudited` (audit row:
  `pmns_c3_character_holonomy_closure_note`). Sibling support note
  constructing the exact native C3 character holonomies at phases
  `0, 2pi/3, 4pi/3` on the cited `hw=1` triplet via the projected
  forward-cycle matrix `C`. Provides the holonomy readout
  `(h_0, h_1, h_2)` that the present note's Fourier projection
  `J_chi := (h_0 + omega h_1 + omega^2 h_2) / 3` post-composes with.
  Because this sibling is `unaudited`, it does not by itself lift
  the present note's effective status under the cite-chain rule.
- [`PMNS_C3_CHARACTER_MODE_REDUCTION_NOTE.md`](PMNS_C3_CHARACTER_MODE_REDUCTION_NOTE.md)
  — currently `unaudited` (audit row:
  `pmns_c3_character_mode_reduction_note`). Sibling support note
  showing that on the graph-first reduced forward-cycle channel the
  C3 Fourier modes are exactly `z_0 = w`, `z_1 = u - i v`,
  `z_2 = u + i v` with `z_1 = conjugate(z_2)` on the residual
  graph-first antiunitary slice. Supplies the precise readout
  `J_chi(A_fwd) = chi = u + i v` that the present note imports as a
  premise.
- [`PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md`](PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md)
  — currently `audited_conditional` (audit row:
  `pmns_hw1_source_transfer_boundary_note`). Adjacent boundary-grade
  authority for the sole-axiom `hw=1` source/transfer route on which
  the present note's annihilation claim `J_chi = 0` is one of three
  components.
- [`PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md`](PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md)
  — currently `unaudited` (audit row:
  `pmns_selector_current_stack_zero_law_note`). Sibling support note
  recording the current-stack zero law on the cited bank,
  consistent with the present note's `J_chi = 0` annihilation claim
  on all three listed cited routes.
- [`DM_PMNS_GRAPH_FIRST_ORDERED_CHAIN_NONZERO_CURRENT_ACTIVATION_THEOREM_NOTE_2026-04-21.md`](DM_PMNS_GRAPH_FIRST_ORDERED_CHAIN_NONZERO_CURRENT_ACTIVATION_THEOREM_NOTE_2026-04-21.md)
  — currently `unaudited` (audit row:
  `dm_pmns_graph_first_ordered_chain_nonzero_current_activation_theorem_note_2026-04-21`).
  Downstream activation theorem constructing one explicit sole-axiom
  nonzero-current law (`A_ord = diag(1,2,3) + (E12 + E23 + E31)`,
  `J_chi = 1`) that lands the very target named by the present
  note's "Consequence" section.

Open class D registration targets named by the 2026-05-05 audit
verdict as `missing_bridge_theorem`:

- (Now addressed in this note.) The exact native C3 holonomy readout
  on `A_fwd` is derived in the "Class A bridge derivation" section
  above as Bridge B1 from the canonical cycle basis Gram matrix and
  the standard cyclotomic identities `1 + omega + omega^2 = 0` and
  `omega - omega^2 = i sqrt(3)`. The native holonomies themselves are
  the already-proven design-matrix law of
  `PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE`, which provides the
  primitive readout; Bridge B1 only post-composes that with the
  C3-Fourier projection.
- (Now addressed in this note.) The route-wise annihilation
  `J_chi = 0` on the free, sole-axiom `hw=1` source/transfer, and
  retained scalar routes is derived in the "Class A bridge derivation"
  section above as Bridge B2 from the one-line fact that the canonical
  C3-character probe `P_phi` is supported off the diagonal of the cycle
  frame and every retained route produces a diagonal active block in
  that frame. The three route-by-route diagonality facts are imported
  from the three already-cited route source notes
  (`PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE`,
  `PMNS_UNIFORM_SCALAR_DEFORMATION_BOUNDARY_NOTE`, and the trivial free
  identity) and are directly verifiable numerically via the realising
  scripts.
- (Still open.) Minimality of "exactly one complex current" as the
  smallest remaining sole-axiom source object is asserted but not
  derived in the present note. Closing it requires a minimality
  theorem on the reduced graph-first PMNS family. This remains a
  separate open class D target.
- (Still open.) Inventory closure that the three named retained routes
  (free, sole-axiom `hw=1` source/transfer, retained scalar) exhaust
  the current sole-axiom retained-route bank. Bridge B2 above proves
  `J_chi = 0` on each route in the bank as named; it does not by
  itself prove no further retained route exists. This remains a
  separate open inventory target.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with
load-bearing-step class A and `chain_closes=False`, observing that
the algebraic Fourier-projection identity is plausible as algebra
over specified holonomies but the restricted packet did not provide
the holonomy/readout formulas or a proof that the listed sole-axiom
routes annihilate `J_chi`. The runner
`scripts/frontier_pmns_c3_nontrivial_current_boundary.py` exists in
the repository and verifies the conditional readout (`PASS=16 FAIL=0`
on 2026-05-10) on the projected forward-cycle algebra. The present
edit adds the "Class A bridge derivation" section above, which writes
out the two missing class A bridges in-note: Bridge B1 derives
`J_chi(A_fwd) = u + i v` as a finite linear combination of the
already-proven native holonomies of
`PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE`, using only the canonical
cycle-basis Gram matrix `diag(2, 2, 1)` and the standard cyclotomic
identities; Bridge B2 derives `J_chi = 0` on the three named retained
routes from the one-line fact that the canonical C3-character probe
`P_phi` has zero diagonal entries while every named retained route
produces a diagonal active block. The two open class D targets that
remain (minimality of one complex current, and inventory closure of
the three retained routes) are explicitly registered above and are
not claimed by this edit. Because this source note is being edited,
the audit lane must re-ratify it from the regenerated ledger; this
addendum does not apply an `audit_status` or promote effective status.

## Scope of this rigorization

This rigorization is class A (in-note bridge derivation of the two
load-bearing algebraic steps named by the audit verdict) plus class B
(graph-bookkeeping citation of the upstream authority candidates) plus
class D (registration of the two remaining open minimality and
inventory targets). It does not change the algebraic conclusion
(`J_chi(A_fwd) = u + i v`, `J_chi = 0` on the three named retained
routes), the runner output (`PASS=16 FAIL=0` on 2026-05-10), or the
audited claim scope (smallest remaining sole-axiom source object on
the named retained-route bank). It writes the two class A bridges
named by the verdict's `notes_for_re_audit_if_any` field in-note from
the canonical cycle basis and the already-proven native holonomies,
and it preserves the explicit registration of the two open class D
targets. The cite-chain pattern continues to mirror the
`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md` cluster
(commit `8e84f0c23`) and the PMNS active-source cluster (commit
`be5a06dbf`).
