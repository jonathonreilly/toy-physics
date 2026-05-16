# Planck-Scale Conditional Completion Note

**Date:** 2026-04-24 (narrowed 2026-05-16)
**Status:** proposed_retained support / conditional completion packet, not an
unqualified minimal-stack derivation. Audit verdict: `audited_conditional`
(status authority is the independent audit lane).
**Claim type (author-proposed):** `conditional_theorem` (narrowed from
`positive_theorem` per the auditor's 2026-05-05 repair target —
"missing_bridge_theorem: ... or a restricted packet citing such a theorem.")
The note packages the conditional algebraic implication
"(BP) ⇒ a/l_P = 1"; it does not claim to derive (BP). Status authority
remains the independent audit lane.
**Runner:** `scripts/frontier_planck_conditional_completion_audit.py`
**Companion support runner:**
`scripts/frontier_planck_boundary_density_extension.py`
**Companion no-go runners:**
`scripts/frontier_planck_finite_response_nogo.py`,
`scripts/frontier_planck_parent_source_hidden_character_nogo.py`

## Restricted Claim Statement (2026-05-16 narrowing)

The note's load-bearing claim, as packaged for audit consumption, is the
**conditional algebraic implication**:

```text
PREMISE (BP): the primitive one-step boundary/worldtube count is the
              microscopic carrier of the standard gravitational
              area/action density.

CONSEQUENCE:  on the primitive event cell, with c_cell = Tr(rho_cell P_A)
              = 1/4 (rank-four Hamming-weight-one projector on the
              source-free counting trace), and equating same-surface
              densities
                  c_cell / a^2  =  1 / (4 l_P^2),
              algebra gives
                  a / l_P  =  1.
```

This is a conditional algebraic theorem of the form `BP ⇒ (a/l_P = 1)`.
The note does **not** claim to derive `(BP)` from the retained minimal
stack. The audit verdict `audited_conditional` is acknowledged as the
correct verdict at retained grade for this restricted statement; the
named open bridge premise `(BP)` is listed in the Remaining Blockers
section.

The 2026-05-10 substrate-to-carrier round produced three independent
source-note proposals (P1/P2/P3 — see "Bounded support narrowing the
bridge premise" below) that **narrow** the `(BP)` problem into named
bounded sub-theorems with explicit cited-content load-bearing inputs.
None of those proposals is audited yet, so this note continues to treat
`(BP)` as an open named premise. The bounded supports are cited here as
narrowing structure, not as a closure of `(BP)`.

## Cited authorities (one-hop deps)

This note records explicit one-hop authority citations for the conditional
completion packet. The audit verdict `audited_conditional` correctly flags the
gravitational boundary/action density bridge as the named open premise; the
citations below sharpen the conditional structure on the live authority chain
without claiming to derive that bridge.

- [`PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md`](PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md)
  (`audited_conditional`) — the unique additive finite-boundary density
  extension `N_A(P) = c_cell A(P) / a^2`, conditional on the gravitational
  boundary/action density bridge premise (BP). PR #812 sharpened this note
  with an explicit conditional carrier-share derivation matching `c_cell =
  1/4` to `1/(4 G_Newton,lat)` via Wald-Noether on the cited authority
  chain.
- [`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`](PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md)
  (`audited_conditional`) — the upstream first-order coframe carrier
  theorem selecting `P_A` as the unique first-order boundary carrier on the
  primitive event cell. PR #829 sharpened this note's premise provenance:
  first-order locality is sourced to the link-local first-variation route,
  unit primitive response normalization is recorded as a canonical
  scheme/normalization choice.
- [`PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md`](PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md)
  — unaudited candidate authority for the substrate-to-`P_A` step from the
  algebraic first variation of the retained link-local microscopic action.
  This is the cited conditional route for the `P_A` selection that
  underpins the primitive coefficient `c_cell = 1/4`.
- [`PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md`](PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md)
  — separates the bare Green coefficient `G_kernel = 1/(4π)` from the
  conditional physical lattice Newton coefficient `G_Newton,lat = 1` on the
  carrier-normalized surface (forces `lambda = 1` from `c_cell = lambda/4`).
  This resolves the old bare-source failure mode `a/l_P = 2 sqrt(pi)`
  without removing the bridge premise itself.
- [`BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`](BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md)
  — composition surface recording the conditional chain
  `c_cell = 1/4 ⇒ S_BH = A · c_cell = A/(4 G_Newton,lat)` with
  `G_Newton,lat = 1` in framework lattice units, conditional on the
  Wald-Noether formula admitted as universal physics input and on the same
  bridge premise (BP). This is the composition surface cited by PR #812's
  conditional carrier-share derivation.
- [`PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md`](PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md)
  (`retained_no_go`) — closes the finite-automorphism-only response target
  negatively. Bare finite primitive-cell automorphisms have no
  infinitesimal tangent.
- [`PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md`](PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md)
  (`retained_no_go`) — closes the unconstrained Schur/event scalar
  shortcut negatively. Carrier commutation alone leaves an affine hidden
  character `delta`.

The above one-hop citations make the conditional completion packet's
authority chain explicit. The named open premise (BP) — gravitational
boundary/action density identified with the first-order coframe carrier — is
unchanged: this note does not claim to derive (BP) and the audit verdict
remains `audited_conditional`.

## Bounded support narrowing the bridge premise (post-2026-05-10)

The 2026-05-10 substrate-to-carrier round produced three independent
source-note proposals that decompose the previously-bundled `(BP)` premise
into named bounded / positive sub-theorems on cited-content surfaces.
These are cited here as **bounded narrowings** of the bridge premise,
not as closures of it. None is audited yet; each carries
`effective_status: unaudited` at the time of this narrowing edit, and
status authority remains the independent audit lane.

- [`PLANCK_SUBSTRATE_TO_CARRIER_FORCING_BOUNDED_NOTE_2026-05-10_planckP1.md`](PLANCK_SUBSTRATE_TO_CARRIER_FORCING_BOUNDED_NOTE_2026-05-10_planckP1.md)
  (P1, `bounded_theorem` candidate) — independent reflection-positivity
  (RP) route selecting `P_A` from the 17 rank-four equivariant
  projector classes. Under RP1+RP2 admissions, the OS Cauchy-Schwarz
  field-degree-one vacuum-reachable sector selects `P_A` uniquely. This
  narrows the **substrate-to-`P_A`** sub-question of (BP) but does not
  derive (BP).
- [`PLANCK_HIDDEN_CHARACTER_DELTA_ZERO_POSITIVE_THEOREM_NOTE_2026-05-10_planckP2.md`](PLANCK_HIDDEN_CHARACTER_DELTA_ZERO_POSITIVE_THEOREM_NOTE_2026-05-10_planckP2.md)
  (P2, `positive_theorem` candidate) — source-free state
  `rho_cell = I_16/16` collapses every Schur scalar reading to a function
  of the operator trace alone, forcing the affine hidden direction
  `delta` to be zero on the source-free counting trace. This closes the
  **parent-source hidden-character** sub-question of (BP) on the
  source-free state surface, but does not derive (BP).
- [`PLANCK_ORIENTATION_PRINCIPLE_BOUNDED_NOTE_2026-05-10_planckP3.md`](PLANCK_ORIENTATION_PRINCIPLE_BOUNDED_NOTE_2026-05-10_planckP3.md)
  (P3, `bounded_theorem` candidate) — the action-level temporal-axis
  Z_2 grading `Theta_RP := (-1)^{n_t}` breaks the Hodge `P_1 <-> P_3`
  degeneracy via asymmetric eigenspace dimensions. Combined with the
  cited single-clock theorem, this uniquely selects `P_1` as the
  first-order orientation carrier over `P_3`. This narrows the
  **orientation** sub-question of (BP) but does not derive (BP).
- [`PLANCK_FROM_STRUCTURE_PATH_OPENING_META_NOTE_2026-05-10.md`](PLANCK_FROM_STRUCTURE_PATH_OPENING_META_NOTE_2026-05-10.md)
  (path-opening meta) — records the audit-honest synthesis of P1+P2+P3
  plus the G_Newton self-consistency bounded sharpening, and the
  conditional path on which the conventional scale anchor row reaches
  zero pending audit ratification of P1+P2+P3 plus closure of the
  substep-4 staggered-Dirac realization gate. The phrase "path-opening,
  not closure" is load-bearing on the meta note.

Synthesis: (BP) is no longer a wholesale gap, but a structured trio of
named bounded narrowings. Under independent audit ratification of
P1+P2+P3 plus the substep-4 ratchet, (BP) becomes derivable on the
cited-content surface. Until then this note's `(BP) ⇒ a/l_P = 1`
implication stays explicitly conditional and the audit verdict
`audited_conditional` is correct at retained grade.

## Purpose

This note records the science worth retaining from the
`codex/planck-scale-program-2026-04-23` branch.

The branch substantially sharpens the Planck-scale program. It does **not**
make the older minimal stack alone derive the SI Planck length. Its durable
result is a conditional completion theorem:

> On the physical-lattice package, with explicit source-free primitive-cell
> state semantics and with the primitive one-step boundary count identified as
> the microscopic carrier of the standard gravitational area/action density,
> the dimensionless cell coefficient is `1/4`, the coefficient extends
> uniquely and additively to finite boundary patches, and the normalization
> gives `a/l_P = 1`.

The current public package may use that as a support theorem for the Planck
pin. It should not replace the public statement that the minimal-stack
derivation of the absolute scale remains open.

## Retained Results

### 1. Primitive coefficient

On the time-locked primitive event cell

```text
H_cell ~= C^2_t otimes C^2_x otimes C^2_y otimes C^2_z ~= C^16,
```

let `P_A` be the Hamming-weight-one event packet:

```text
P_A = P_t + P_x + P_y + P_z.
```

On the source-free primitive counting-trace surface,

```text
rho_cell = I_16 / 16
rank(P_A) = 4
c_cell = Tr(rho_cell P_A) = 4/16 = 1/4.
```

This is the strongest clean dimensionless output from the branch.

### 2. Area/action normalization

If the primitive boundary count is the microscopic carrier of the standard
gravitational area/action density, then

```text
S_cell / k_B = c_cell A / a^2
S_grav / k_B = A / (4 l_P^2).
```

Equating same-surface densities gives

```text
c_cell / a^2 = 1 / (4 l_P^2)
a^2 = 4 c_cell l_P^2.
```

With `c_cell = 1/4`,

```text
a^2 = l_P^2,
a/l_P = 1.
```

This is not a numerical fit for `a`; it is the algebraic consequence of the
primitive coefficient once the gravitational carrier identification is
accepted.

### 3. Finite-boundary density extension

The primitive result is not only single-cell arithmetic. Under locality,
additivity, cubic-frame orientation symmetry, and the primitive normalization
`c_cell = 1/4`, every finite boundary patch that is a finite disjoint union of
primitive faces has the unique additive density

```text
N_A(P) = c_cell A(P) / a^2.
```

This is closed positively in
[PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md](./PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md):
once the primitive boundary count is accepted as the microscopic
gravitational boundary/action carrier, the `1/4` coefficient extends
consistently from one primitive face to finite boundary patches.

### 4. Source-unit normalization support theorem

The 2026-04-25 source-unit normalization support theorem sharpens the same
conditional packet by resolving the residual `4 pi` source-unit ambiguity.

The retained lattice Poisson/Green theorem gives the bare unit-source
coefficient

```text
G_kernel = 1/(4 pi),
```

which is the response to a chosen regulator delta source. Exterior
observability and additivity leave a one-parameter family of physical source
units

```text
M_lambda = lambda C,
G_lambda = 1/lambda,
```

where `C` is the normalized Gauss charge / asymptotic monopole coefficient.
On the same conditional carrier surface,

```text
c_cell = 1/(4 G_lambda) = lambda / 4
```

forces `lambda = 1`, hence

```text
q_bare = 4 pi M_phys,
G_Newton,lat = 1.
```

So the conditional completion packet now has both:

- the primitive coefficient `c_cell = 1/4`, and
- the source-unit clarification that `1/(4 pi)` is a bare Green coefficient,
  not the physical Newton coefficient on the carrier-normalized surface.

This resolves the old bare-source failure mode

```text
a/l_P = 2 sqrt(pi)
```

without removing the carrier-identification premise itself.

### 4b. Conditional Clifford coframe bridge for the carrier premise

The 2026-04-25 Target 3 Clifford phase bridge gives a sufficient route for the
remaining carrier-identification premise: assume the active primitive boundary
response is the metric-compatible Clifford coframe response on `P_A H_cell`.
That response satisfies

```text
D(v)^2 = ||v||^2 I,
```

and therefore polarizes to the complex Clifford relation on the time-locked
primitive coframe:

```text
{D(u),D(v)} = 2 <u,v> I.
```

On `P_A H_cell` with `rank(P_A)=4`, this is the irreducible
`Cl_4(C) ~= M_4(C)` module, equivalently the two-mode complex CAR edge
carrier. The 2026-04-30 primitive Clifford-Majorana edge derivation theorem
(`PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30`,
audit verdict `audited_renaming`) constructs the four Hermitian generators
explicitly on `K = P_A H_cell` from the cited spatial `Cl(3)` bivectors plus
the anomaly-forced time axis. Its substrate-to-`P_A` provenance is sourced to
the cited link-local first-variation candidate authority; the algebraic
construction itself is unchanged. Combined with the primitive parity-gated
area-law theorem, this gives

```text
c_Widom = c_cell = 1/4.
```

Thus the conditional packet has a precise positive carrier route under the
primitive coframe-response premise, with the active-block algebra constructed
explicitly on `P_A H_cell`. It is not promoted here to a minimal-stack
retained theorem, because the coframe response on the active block remains the
explicit bridge premise and the substrate-to-`P_A` step remains conditional on
the unaudited link-local first-variation candidate authority.

### 5. Finite-only target is blocked

The branch correctly separates the conditional completion from a stronger
finite-automorphism-only claim.

The frozen finite cell cannot by itself provide the usual local gravitational
or canonical quantum response:

- finite signed-permutation frame symmetry has no infinitesimal local Ward
  generator;
- exact finite-dimensional canonical commutators are trace-forbidden because
  `Tr([X,P]) = 0`, while `Tr(i hbar I_n) != 0` for `hbar != 0`;
- coherent action phases require a history/representation surface, not just
  a finite static cell algebra.

So the branch does not prove:

```text
bare finite Cl(3)/Z^3 automorphisms alone force a = l_P and hbar.
```

This finite-response route is now closed negatively in
[PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md](./PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md):
the primitive finite frame automorphism group is finite
(`|B_4| = 384`), every nonidentity element has positive distance from the
identity, and the infinitesimal tangent available from finite automorphisms
alone is zero-dimensional. It cannot supply the local metric/coframe response
directions required for the gravitational carrier identification.

### 6. Realified response is a conditional response surface

The branch also sharpens the role of realification. If one asks for
first-order physical response maps from the retained translation module
`Z^3` into a real observable response space, the universal response envelope
is

```text
Z^3 tensor_Z R.
```

That makes the realified Clifford response surface natural for linear-response
gravity questions. It does not erase the distinction between:

- deriving Planck scale from the older minimal finite stack alone, and
- deriving `a/l_P = 1` on the realified physical-response surface plus the
  gravitational boundary/action carrier identification.

### 7. Cosmic pins and SI hbar remain nonclaims

Present age, present radius, or other cosmic address data can select a
macroscopic comparison surface. They do not determine the microscopic tick or
spacing without a derived dimensionless count.

Likewise, the branch can support structural action-phase statements such as
`S/hbar = Phi` on a coherent-history surface. It does not predict the decimal
SI value of `hbar`; that is a unit-convention statement once SI units are
chosen.

## Remaining Blockers

The exact open blockers are now sharper than before:

1. **Minimal-stack blocker.** The older minimal finite stack alone still does
   not derive the absolute lattice spacing.
2. **Carrier-identification blocker (BP).** To promote the conditional
   theorem to a stronger derivation, derive that the primitive one-step
   worldtube count is the microscopic carrier of the gravitational
   boundary/action density. This is the named open bridge premise (BP)
   inherited from `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM` §5
   and explicitly recorded in
   `PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM` after PR #812. If this is
   attempted through the parent-source scalar route, it must include a
   no-hidden-character law fixing `delta = 0`; the carrier-only scalar
   diagram is now closed negatively.
3. **Substrate-to-`P_A` blocker.** The `P_A` selection step underpinning the
   primitive coefficient `c_cell = 1/4` is sourced (conditionally) to the
   link-local first-variation candidate authority; the symmetry-only and
   first-order Hodge-degeneracy no-gos rule out pure-symmetry routes. If
   `PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM` audits clean,
   this blocker resolves; if it fails audit, this route reverts to an
   explicit cited assumption.

Closed positive support theorem:

- **Finite-boundary density extension.**
  [PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md](./PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md)
  closes the finite-patch extension positively. Given the gravitational
  carrier identification, locality, additivity, and cubic-frame orientation
  symmetry uniquely extend `c_cell = 1/4` to `N_A(P) = c_cell A(P)/a^2` on
  finite face-union boundary patches. Sharpened by PR #812 with an explicit
  conditional carrier-share derivation matching `c_cell/a^2` to
  `1/(4 G_Newton,lat)` via Wald-Noether.
- **Primitive coframe boundary carrier.**
  [PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md](./PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md)
  selects `P_A` as the unique first-order coframe boundary carrier. PR #829
  sharpened its premise provenance: first-order locality is sourced to the
  link-local first-variation route; unit primitive response normalization
  is recorded as a canonical scheme/normalization choice.

Closed negative routes:

- **Finite-response-only route.**
  [PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md](./PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md)
  closes the finite-automorphism-only response target negatively. Bare finite
  primitive-cell automorphisms have no infinitesimal tangent, so they cannot
  replace the realified local response surface.
- **Carrier-only parent-source scalar route.**
  [PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md](./PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md)
  closes the unconstrained Schur/event scalar shortcut negatively. Carrier
  commutation alone leaves an affine hidden character `delta`, and scalar
  equality is equivalent to the extra law `delta = 0`.

## Package Status

Use:

> The conditional Planck packet derives an exact primitive coefficient
> `c_cell = 1/4`, a unique additive finite-boundary density extension, and a
> conditional same-surface normalization `a/l_P = 1` once the primitive
> boundary count is accepted as the microscopic gravitational area/action
> carrier; the companion source-unit normalization support theorem shows that
> the retained `1/(4 pi)` is only the bare Green coefficient and that the
> physical lattice Newton coefficient is `1` on that same carrier surface.

Do not use:

> The minimal accepted theorem stack now derives the SI Planck length.

Do not use:

> Finite `Cl(3)` / `Z^3` automorphisms alone force Planck scale and `hbar`.

The current public package may continue to carry `a^(-1) = M_Pl` as the
Planck-scale package pin, now with a sharper conditional-completion theorem
and a precise list of remaining blockers. The finite-automorphism-only route
and the carrier-only parent-source scalar route are no longer live positive
targets; both are retained no-gos.
