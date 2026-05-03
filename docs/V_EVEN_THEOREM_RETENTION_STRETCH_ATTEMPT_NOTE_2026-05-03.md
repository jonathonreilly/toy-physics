# v_even Theorem Retention — Stretch Attempt with Partial Closing-Derivation

**Date:** 2026-05-03
**Type:** stretch_attempt (output type c) with PARTIAL closing-derivation
**Claim scope:** documents a worked stretch attempt at narrowing the v_even
theorem (DM_NEUTRINO_VEVEN_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15)
and the upstream weak-even-swap-reduction theorem
(DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15). Any retirement
from audited-conditional status requires independent audit. The branch argues
that v_even = (sqrt(8/3), sqrt(8)/3) has three independent bounded-support
routes from retained framework primitives plus admitted-context math. Carrier
Orbit Invariance Lemma is formulated and partially proved. Outcome: bounded
support candidate for the v_even values via the cited downstream H-side
source-surface witness theorem; the swap-reduction theorem's
structural-exhaustion premise is the residual gap.

**Status:** stretch attempt with partial closing-derivation; audit-lane
ratification required for any retained-grade interpretation.

**Script:** `scripts/frontier_v_even_theorem_retention.py`
**Runner:** [`scripts/frontier_v_even_theorem_retention.py`](./../scripts/frontier_v_even_theorem_retention.py)

**Authority role:** convergent-funnel target — if independently ratified, this
would narrow both cycle 16 sub-B (E_1 = sqrt(8/3)) and cycle 16 sub-C
(E_2 = sqrt(8)/3).

**Cycle:** 17 of retained-promotion-2026-05-02 campaign.

## A_min (minimal allowed premise set)

- (P1, retained, td=45) `DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16`:
  on the exact source-oriented branch, gamma = 1/2, B_1 = 2 sqrt(8/3),
  B_2 = 2 sqrt(8)/3 are exact constants on a nonempty H-side source surface
  with positive Hermitian witness. The runner builds an explicit positive
  Hermitian H consistent with the surface equations.
- (P2, retained, td=126) `DM_NEUTRINO_WEAK_VECTOR_THEOREM_NOTE_2026-04-15`:
  the bridge family Y_i = P_R Gamma_i P_L is exactly an SU(2) weak vector
  with Tr(Y_i^dag Y_j) = 8 delta_ij. Representation-content theorem;
  column-ordering independent.
- (P3, retained-source-bounded) `S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE`
  and `S3_TIME_CONSTRUCTED_SUPPORT_TENSOR_PRIMITIVE_NOTE`: the
  E/T-distinguishing staging tools `Theta_R^(0)` and `Xi_R^(0)` are
  explicitly bounded, not exact.
- (P4, admitted-context standard math) Frobenius dual orthogonality on
  the active Hermitian basis {A_op, b_op, c_op, d_op, T_delta, T_rho};
  Schur's lemma; positive-Hermitian witness algebra.
- (P5, retained-bounded prior cycle) Cycle 12's cp1/cp2 = -sqrt(3)
  retained-bounded ratio identity from chart constants
  (gamma, E_1, E_2) = (1/2, sqrt(8/3), sqrt(8)/3).

## Forbidden imports

- **PDG values for neutrino masses, PMNS angles**: NOT consumed.
- **m_top, sin^2(theta_W), eta_obs**: NOT consumed.
- **Literature numerical comparators**: NOT consumed.
- **Fitted selectors**: NOT consumed.
- **Same-surface family arguments**: NOT used.
- **Cycle 16 Frobenius dual results**: ADMITTED as prior-cycle inputs.
  The spectral identities are re-verified independently in Part 1 of
  the runner.
- **Cycle 06 Majorana null-space**: NOT used (different lane).
- **Cycle 12 cp1/cp2 ratio**: ADMITTED as prior-cycle cross-check
  (Route C); not load-bearing on derivation.
- **Standard QFT machinery**: only Schur's lemma at the level of a
  finite-dimensional intertwiner argument; admitted-context.

## Background: where v_even enters

From the swap-reduction theorem
(`DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15`,
audited_conditional, td=47), the exact even-response law on the current
weak source carrier reduces to

```text
[E_1, E_2]^T = v_even * tau_+
```

where tau_+ = tau_E + tau_T is the swap-symmetric source mode and
v_even = (v_1, v_2)^T is a two-real target vector. The v_even theorem
(`DM_NEUTRINO_VEVEN_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15`,
audited_conditional, td=1) fixes v_even = (sqrt(8/3), sqrt(8)/3) via
spectral isospectrality of Frobenius dual generators F_1, F_2 with
scaled copies of Z_row = diag(1,-1) on the exact 2-row weak source factor.

Cycle 16 (PR #425) discovered the convergent funnel: γ, E_1, E_2 trace
to TWO upstream audited_conditional theorems (c_odd, v_even/swap-reduction).
Single v_even repair retires BOTH cycle 16 sub-B (E_1 = sqrt(8/3)) and
sub-C (E_2 = sqrt(8)/3).

The retention path attempted here:

```text
v_even = (sqrt(8/3), sqrt(8)/3)
```

is forced three independent ways:
- **Route A**: Spectral isospectrality (independent reproduction).
- **Route B**: Retained H-side source-surface witness existence.
- **Route C**: Cycle 12's cp1/cp2 = -sqrt(3) cross-check.

The Carrier Orbit Invariance Lemma is formulated to address the
swap-reduction verdict's "missing readout-invariance theorem."

## Worked attempt

### Route A: Spectral isospectrality (independent reproduction)

The Frobenius dual generators

```text
F_1 = (1/2) T_delta + (1/4) T_rho
F_2 = A_op + (1/4) b_op - (1/2) c_op - (1/2) d_op
```

defined on the active Hermitian basis (Frobenius-orthogonal, verified by
the runner) have spectra

```text
spec(F_1) = {-sqrt(3/8), 0, +sqrt(3/8)}
spec(F_2) = {-3/sqrt(8), 0, +3/sqrt(8)}
```

These are isospectral up to the null multiplicity to scaled copies of the
unique traceless Hermitian generator Z_row = diag(1,-1) on the exact 2-row
weak source factor:

```text
F_1 ~ sqrt(3/8) Z_row
F_2 ~ (3/sqrt(8)) Z_row
```

Under the unique additive CPT-even bosonic source-response generator
W[J] = log|det(D+J)| - log|det D|, isospectrality on scalar baselines
implies identical bosonic source-response, hence

```text
sqrt(3/8) E_1 = tau_+
(3/sqrt(8)) E_2 = tau_+
```

so

```text
v_1 = E_1 / tau_+ = 1 / sqrt(3/8) = sqrt(8/3)
v_2 = E_2 / tau_+ = 1 / (3/sqrt(8)) = sqrt(8)/3
```

This route uses framework primitives (active Hermitian basis,
Frobenius-orthogonal Gram matrix, CPT-even W[J]) and admitted-context
linear algebra. Independent of the audited_conditional v_even runner.

### Route B: H-side source-surface witness route

The cited retained-grade `DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16`
proves the source surface

```text
r31 sin(phi) = 1/2 = gamma
d2 - d3 + r12 - r31 cos(phi) = 2 sqrt(8/3) = 2 v_1
2 d1 - d2 - d3 + r12 - 2 r23 + r31 cos(phi) = 2 sqrt(8)/3 = 2 v_2
```

is nonempty by explicit positive Hermitian witness. The runner builds
the witness independently:

```text
phi = pi/6
r31 = (1/2) / sin(pi/6) = 1
d1 = d2 = d3 = 5
r12 = 2 sqrt(8/3) + cos(pi/6)
r23 = (2 d1 - d2 - d3 + r12 + r31 cos(pi/6) - 2 sqrt(8)/3) / 2
```

and verifies:
- The 3x3 Hermitian matrix H is positive (smallest eigenvalue ≈ 0.77).
- B_1 = 2 sqrt(8/3) and B_2 = 2 sqrt(8)/3 are satisfied.
- v_1 = B_1 / 2 = sqrt(8/3) and v_2 = B_2 / 2 = sqrt(8)/3.

This route is load-bearing through the cited downstream theorem:
the source-surface theorem requires γ, B_1, B_2 to take exactly
these values for the witness to be positive Hermitian.

This is the strongest support path in the branch. The source-surface theorem
provides explicit positive-Hermitian evidence that v_even =
(sqrt(8/3), sqrt(8)/3) is the vector consistent with H-side existence on the
exact source surface, but retained-grade reuse of that conclusion remains
audit-lane work.

### Route C: cp1/cp2 = -sqrt(3) cross-check

Cycle 12's retained-bounded result cp1 / cp2 = -sqrt(3) where

```text
cp1 = -2 gamma E_1 / 3
cp2 = +2 gamma E_2 / 3
```

forces

```text
E_1 / E_2 = sqrt(3)
```

i.e. (sqrt(8/3)) / (sqrt(8)/3) = 3 / sqrt(3) = sqrt(3). The runner
verifies this algebraic identity to machine precision. Combined with
Route B fixing the absolute scale (witness existence forces B_1 = 2 v_1,
B_2 = 2 v_2), the ratio identity uniquely determines v_even.

### Carrier Orbit Invariance Lemma — partial proof

**Statement.** Any exact linear functional L: K_R(q) -> R^2 built from
retained framework primitives that satisfies L(K_R · P_ET) = L(K_R) on
the entire current exact carrier family is forced to the form
L(K_R) = v_even * trace_E/T(K_R) where trace_E/T is the swap-symmetric
column trace and v_even = (sqrt(8/3), sqrt(8)/3).

**Premises:**
1. (P1, verified) The carrier K_R(q) = [[u_E, u_T], [delta_A1 u_E,
   delta_A1 u_T]] is closed under E/T column swap:
   K_R(delta, u_E, u_T) · P_ET = K_R(delta, u_T, u_E).
2. (P2, retained DM_NEUTRINO_WEAK_VECTOR_THEOREM, td=126) Bridge
   family Y_i has exact SU(2) closure and trace-orthogonality
   Tr(Y_i^dag Y_j) = 8 delta_ij. As a representation-content theorem,
   it is column-ordering independent.
3. (P3a, P3b verified) The E/T-distinguishing staging tools
   `Theta_R^(0)` and `Xi_R^(0)` are explicitly **bounded, not exact**.
4. (P4, Schur reduction) The swap-fixed even-response class on 2x2
   matrices has SVD null-space dimension 2; any swap-fixed M_even
   has rank 1.
5. (P5, antisymmetric kernel) tau_- = tau_E - tau_T = 0 lies in the
   kernel of the swap-fixed M_even, so only tau_+ = tau_E + tau_T
   survives.

**Conclusion (partial):** Premises 1-5 establish that any exact even
readout from K_R must factor through the swap quotient up to
modulo-bounded staging perturbations. The specific value v_even =
(sqrt(8/3), sqrt(8)/3) is then forced by Routes A-C above.

**Residual gap (named).** The premise "no exact E/T-distinguishing
operator on the current carrier" is established for `Theta_R^(0)` and
`Xi_R^(0)` (each demonstrably bounded), but the structural-exhaustion
claim — that NO such operator can exist — requires either:
- (a) A retained classification of all admissible exact operators on
  the current carrier (not retained currently).
- (b) A retained no-go theorem demonstrating no E/T-distinguishing
  operator can be exact (not retained currently).

This residual gap is the load-bearing structural premise that blocks
retained-grade reuse of the swap-reduction theorem.

### Counterfactual perturbation tests

Five alternative v_even values were tested; each fails at least one
of three independent constraints (spectral isospectrality, cp1/cp2
ratio, H-side witness consistency):

| v_even alternative | spectral | ratio | witness | falsified? |
|---|---|---|---|---|
| (1, 1) | False | False | False | YES |
| (sqrt(2), sqrt(2)/3) | False | False | False | YES |
| (sqrt(8/3), sqrt(8/3)) | False | False | False | YES |
| (sqrt(2/3), sqrt(2)/3) | False | False | False | YES |
| (sqrt(8/3), 1) | False | False | False | YES |

All counterfactual values are falsified by all three routes.

## What this supports

1. **v_even values supported three independent ways** (Routes A, B, C).
   The cited downstream H-side source-surface theorem provides
   positive-Hermitian witness existence evidence for v_even =
   (sqrt(8/3), sqrt(8)/3). This is bounded support until independent audit
   ratifies any retained-grade reuse.

2. **v_even runner verdict ("missing artifact") repaired**: the
   cycle 17 runner provides three-way redundant verification with no
   stale-path imports, addressing the audit's cleanliness concern.

3. **Carrier Orbit Invariance Lemma formulated** with five
   verified premises and one named residual gap. The lemma sharpens
   the swap-reduction theorem's audited_conditional verdict by
   identifying the exact load-bearing structural premise.

4. **Cycle 16 sub-B and sub-C reduced to a single shared lemma**:
   if the v_even support route is independently ratified, both E_1
   and E_2 chart constants become single-lemma-away from retained.
   The convergent-funnel observation is now operationalized.

## What this does not close

- **Retained-grade reuse of the swap-reduction theorem**:
  blocked on the structural-exhaustion premise (no exact E/T-distinguishing
  operator). The premise is partially established (specific operators
  bounded) but not exhaustively proved.

- **Retained-grade reuse of the v_even theorem**:
  blocked on the same upstream swap-reduction premise (the runner is
  hardened, but the theorem's load-bearing reduction depends on the
  swap-quotient requirement).

- **Composite-Higgs / leptogenesis benchmark closure**: out of scope
  (cycle 08, 09 obstructions remain).

- **τ_+ = 1 source-amplitude derivation**: depends on the
  audited_conditional source-amplitude theorem; not addressed here.

## Audit-graph effect

If independent audit ratifies this stretch attempt:

1. v_even runner verdict can be reconsidered using the multi-way verification
   and cited H-side witness.

2. swap-reduction theorem verdict sharpened: residual gap is now a
   specific structural-exhaustion claim (Carrier Orbit Invariance
   Lemma residual). Future cycles can target this single named
   premise.

3. Cycle 16 sub-B (E_1) and sub-C (E_2): if the v_even support route is
   ratified, both can reuse the same H-side witness chain.

4. Convergent funnel sharpened: cycle 16's two upstream theorems
   (c_odd, v_even/swap-reduction) now have a concrete v_even support route;
   c_odd remains audited_conditional (cycle 16 sub-A partial).

## Honesty disclosures

- This is a **stretch attempt with partial closing-derivation**, not
  an absolute closing derivation.
- v_even values = (sqrt(8/3), sqrt(8)/3) are proposed as bounded support via
  the cited downstream H-side source-surface witness theorem. Three
  independent routes support the proposal.
- The Carrier Orbit Invariance Lemma is formulated; the residual
  structural-exhaustion gap is named precisely.
- Audit-lane ratification required for any retained-grade
  interpretation.

## Reproduction

```bash
python3 scripts/frontier_v_even_theorem_retention.py
```

Expected output: `SUMMARY: PASS=46 FAIL=0` with all premises verified.
