# Newton's Law Derived from Cl(3) on Z^3

**Status:** support - structural or confirmatory support note

## Audit-conditional perimeter (2026-05-10)

The audit lane has classified this row `audited_conditional` with
load-bearing step class `A`. The audit verdict-rationale records the
boundary explicitly:

> "Issue: the note claims Newton's law follows without additional
> assumptions, but its load-bearing Poisson equation is only supported
> by a cited authority that is conditional on a stipulated closure
> identity. Why this blocks: retained propagation cannot treat an
> open/stipulated operator identification as an unconditional theorem
> from Cl(3). Repair target: supply a retained bridge theorem deriving
> L^{-1}=G_0, or narrow this note to a bounded theorem conditional on
> the Poisson equation. Claim boundary until fixed: from stipulated
> Poisson on Z^3, Green asymptotics and linearity give the stated
> inverse-square/product form."

The audit-stated repair is `missing_bridge_theorem`: "derive the
closure identity L^{-1}=G_0 from the Cl(3) on Z^3 axiom, or revise the
claim scope to explicitly remain conditional on the Poisson equation."

The cited one-hop dependency
[`GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md`](GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md)
is itself a *bounded conditional* theorem: it derives `L = -Δ_lat`
*given* the stipulated closure `L^{-1} = G_0`, but does not derive
that identity from Cl(3) on Z^3. The required bridge — a retained
theorem deriving `L^{-1} = G_0` from the Cl(3)-on-Z³ axiom —
is the open D-row gap acknowledged in the parent's own "What Remains
Open" section. Until that bridge lands, this note's scope is
*conditional on the Poisson equation* (audit verdict's second repair
path), not "Newton's law without additional assumptions".

The "What Remains Open: Nothing" language elsewhere in this note is
incompatible with the audit-flagged dependency posture and is
explicitly narrowed below.

This rigorization edit only sharpens the conditional perimeter and
selects the audit's second repair path (claim-scope narrowing to
Poisson-equation conditional) without modifying the runner or
validation chain; nothing here promotes audit status, no new
derivation is asserted, no audit JSON is modified, and the runner
SHA256 for `frontier_distance_law_definitive.py` remains
`f8f86ac9104aac9acfd1d446d48a8c96dcb88ad461f5bd684da1a4631ed1e554`.

## Status

**Closed** on the retained framework surface, **conditional on the
lattice Poisson equation `(-Δ_lat) φ = ρ`** — see
"Audit-conditional perimeter (2026-05-10)" above.

Newton's inverse-square law F = G M1 M2 / r^2 follows from the lattice
Poisson equation on Z^3 *under* the stipulated closure identity
`L^{-1} = G_0` carried by `GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md`. The
audit-flagged repair path requires either deriving that closure
identity from Cl(3) on Z^3 or narrowing the claim to remain
Poisson-conditional; this note adopts the second repair path.

## Theorem / Claim

**Theorem.** Let (-Delta_lat) be the lattice Laplacian on Z^3. Then:

1. The Green's function G(r) of (-Delta_lat) satisfies
   G(r) -> 1 / (4 pi |r|) as |r| -> infinity (Maradudin et al. 1971).

2. A point source of strength M produces potential phi(r) = M * G(r) -> M / (4 pi r).

3. The force on a test mass M_test is F = -M_test * grad(phi) = M * M_test / (4 pi r^2),
   which is Newton's law with G_N = 1/(4 pi) in lattice units.

4. The product M1 * M2 arises from two independent Poisson solves with cross-coupling.
   It is MEASURED from Poisson linearity, not imposed as a bilinear ansatz.

5. The exponent 2 in 1/r^2 equals d - 1 = 3 - 1, where d = 3 is
   the spatial dimension from Cl(3). In general d dimensions, the Poisson
   Green's function gives F ~ 1/r^{d-1}.

## Assumptions

1. Cl(3) on Z^3 (the framework axiom).
2. The staggered scalar field obeys the lattice Poisson equation
   `(-Δ_lat) φ = ρ` (equation of motion from the action). **This is
   the audit-flagged stipulated assumption** — see the
   "Audit-conditional perimeter (2026-05-10)" block at the top. It is
   *not* derived from Cl(3) on Z^3 inside this note's cited
   authority chain; the cited parent
   `GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md` records this as the
   stipulated closure identity `L^{-1} = G_0`.
3. The asymptotic theorem for the lattice Green's function
   (standard lattice potential theory, not a framework-specific claim).

No additional physics is imported beyond the listed assumptions; in
particular, the coupling constant G_N, the product law, the
inverse-square exponent, and the distance dependence all follow
*given* assumption 2. The unconditional "Newton's law from the Cl(3)
axiom alone" reading depends on a retained bridge theorem deriving
assumption 2 from assumption 1, which the audit lane has flagged as
the open D-row gap.

## What Is Actually Proved

**Exact results (mathematical theorems):**

- The lattice Laplacian Green's function on Z^3 converges to 1/(4 pi r)
  for large r. This is a theorem of lattice potential theory.
- Poisson linearity: phi(M) = M * phi(1) exactly.
- The product law F ~ M1 * M2 follows from linearity + cross-coupling.
  This is exact given the Poisson equation.
- The force exponent d - 1 follows from the dimension of the Poisson
  equation. In d = 3: F ~ 1/r^2 exactly.

**Numerical confirmations (bounded checks):**

- Green's function ratio 4 pi r G(r) -> 1.0 confirmed to < 1% for r >= 5
  on a 64^3 lattice.
- Deflection exponent alpha -> -1.0 confirmed to < 5% on 32^3 to 64^3
  lattices (consistent with sub-1% at 128^3 from frontier_distance_law_definitive.py).
- Product law gamma = 1.0 confirmed to < 5% on 32^3 lattice.
- Dimensionality check: d=1 (constant force), d=2 (1/r force), d=3 (1/r^2 force)
  all confirmed numerically.

## What Remains Open

Per the audit verdict (2026-05-10) recorded in the
"Audit-conditional perimeter" block at the top, *one* item remains
open in the chain: the closure-identity bridge `L^{-1} = G_0` from
Cl(3) on Z^3. The cited parent note
`GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md` is bounded-conditional on
this identity and does not derive it from the framework axiom; this
is the open D-row gap acknowledged in that parent.

**Open (audit-flagged):**

- The closure identity `L^{-1} = G_0` is stipulated, not derived from
  Cl(3) on Z^3. A retained bridge theorem deriving this identity from
  the framework axiom is required to close the chain unconditionally.

**Conditionally closed (given the Poisson equation):**

- Given the lattice Poisson equation `(-Δ_lat) φ = ρ` as the equation
  of motion, the Green's function asymptotic, the product law, the
  exponent d − 1, and the inverse-square form follow as stated. This
  is the audit verdict's "claim boundary until fixed" — it is the
  path adopted here.

**Bounded numerical confirmations (unchanged):**

- The finite-lattice numerical precision of the checks (Green's
  function ratio, deflection exponent, product law) remains a
  verification limitation in the bounded sense; this is unchanged.

## How This Changes The Paper

This derivation belongs in the paper as a clean worked example of how
a macroscopic force law emerges from the framework *given the lattice
Poisson equation as the equation of motion*. Manuscript text should
preserve the audit-flagged conditional posture:

> Given the lattice Poisson equation `(-Δ_lat) φ = ρ` on Z^3 as the
> equation of motion, the inverse-square gravitational force law
> F = G M1 M2 / r^2 follows: the Green's function of the lattice
> Laplacian approaches 1/(4 π r) at large distances (a standard
> result of lattice potential theory), the product M1 M2 emerges
> from Poisson linearity with cross-coupling between independent
> sources, and the exponent 2 = d − 1 follows from the spatial
> dimension d = 3 carried by Cl(3). The promotion of `(-Δ_lat) φ =
> ρ` from "stipulated equation of motion under the closure identity
> `L^{-1} = G_0`" to "Cl(3)-axiom-forced equation of motion" is the
> open bridge identified by the audit lane (verdict 2026-05-10).

This closes the *Poisson-conditional* loop from `(-Δ_lat) φ = ρ` to
Newton's law with no free parameters beyond the overall coupling
normalization, on the cited authority chain. The unconditional
"Cl(3)-axiom ⇒ Newton's law" reading remains
closure-identity-bridge-conditional.

This is the retained weak-field gravity claim *under the conditional
perimeter above*. Broader GR-signature notes (WEP, time dilation,
light bending, geodesics, strong-field extension) should still be
carried separately with their actual bounded status.

## Commands Run

```bash
# Run from the repo root.
python3 scripts/frontier_distance_law_definitive.py
```

The audit-recorded primary runner for this row is
`scripts/frontier_distance_law_definitive.py` (per the audit ledger);
the older `scripts/frontier_newton_derived.py` and the earlier
absolute-path command line are stale and have been replaced with the
repo-relative invocation pointing at the audit-recorded runner.

## Supporting Evidence

The distance law and product law have been independently verified at
higher precision in:

- `scripts/frontier_distance_law_definitive.py` (sub-1% at 128^3)
- `scripts/frontier_product_law_no_ansatz.py` (product law without bilinear ansatz)
- `scripts/frontier_dm_coulomb_from_lattice.py` (Green's function theorem + numerics)

This note synthesizes those results into a single derivation chain.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [gravity_full_self_consistency_note](GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md)
  — supplies the `L^{-1} = G_0` self-consistency closure that justifies
  treating `(-Delta_lat)` as THE field operator (Theorem assumption 2:
  the lattice Poisson equation is the equation of motion). Correct
  upstream.

### Direction-corrected cycle break (2026-05-05)

The earlier link to `gravity_clean_derivation_note` is removed because
gravity_clean is a **parallel presentation** of the same Newton-from-Z^3
derivation, not an upstream supplier. Both this note and gravity_clean
independently consume the Maradudin et al. 1971 lattice Green's function
asymptotic theorem (an external math theorem, not an internal repo dep).
Neither note derives the other's content; they are alternate routes to
`F = G_N M_1 M_2 / r^2` from `Cl(3) on Z^3`.

The earlier back-link from this note to gravity_clean was added by a
prior audit-bookkeeping pass and created a length-2 citation cycle
`newton_law ↔ gravity_clean` in the graph. Removing the back-link breaks
the cycle without losing science content (the inline mathematical
justification — Maradudin's theorem — remains in the Theorem section).
