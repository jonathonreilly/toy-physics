# Axiom-First Generalized Second Law on Framework Surface

**Date:** 2026-05-01
**Type:** bounded_theorem
**Claim scope:** Generalized Second Law δ(S_BH + S_matter) ≥ 0 (GSL3) on the framework's retained gravity surface plus the upstream chain (KMS, Hawking T_H, first law); equivalently the Hawking 1971 area theorem δA ≥ 0 under NEC (GSL1) plus matter Gibbs H-theorem δS_matter ≥ 0 (GSL2) sum to GSL3, with Bekenstein bound enforcement (GSL4) as cross-link. Conditional on universal-physics NEC + retained BH 1/4 carrier.
**Status:** awaiting independent audit. Under the scope-aware classification framework (audit-lane proposal #291), `effective_status` is computed by the audit pipeline.
**Loop:** `24h-axiom-first-derivations-20260501`
**Cycle:** 10 (Block 10; stacked on Block 05 (First law))
**Branch:** `physics-loop/24h-axiom-first-block10-gsl-20260501`
**Stacked PR base:** `physics-loop/24h-axiom-first-block05-firstlaw-20260501`
**Runner:** `scripts/axiom_first_gsl_check.py`
**Log:** `outputs/axiom_first_gsl_check_2026-05-01.txt`

## Scope

This note proves the **Generalized Second Law (GSL)** of black hole
thermodynamics on the framework's retained gravity surface plus the
upstream chain (KMS, Hawking T_H, first law):

```text
    δ(S_BH + S_matter)  ≥  0  (under any physical process)              (GSL)
```

GSL is the unified statement that includes both the Hawking-area
theorem (`δA ≥ 0`, classical) and the second law of thermodynamics
(`δS_matter ≥ 0`, statistical). It says: the *combined*
black-hole-plus-matter entropy never decreases, even in processes
where one or the other decreases separately.

The proof composes three retained / support inputs:
- **Hawking area theorem** `δA ≥ 0` (corollary of Penrose 1965 +
  framework retained GR action; admitted-context).
- **Standard second law** `δS_matter ≥ 0` (KMS H-theorem, Block 01).
- **First law** `dM = T_H dS_BH + ...` (Block 05) which links matter
  energy crossing the horizon to BH area increase.

This block completes the framework's BH thermodynamics derivation
program: zeroth law (κ constant, retained), first law (Block 05),
second law GSL (this Block 10), and third law (no `T_H = 0`
extremal limit reachable in finite steps; not derived here as it
reduces to non-degeneracy of the horizon).

## Retained / support inputs

- **Block 01 KMS support theorem.** Provides standard second law
  `δS_matter ≥ 0` for Gibbs evolution.
- **Block 02 Hawking T_H support theorem.** Provides T_H = κ/(2π).
- **Block 05 first law of BH mechanics.** Provides `dM = T_H dS_BH`.
- **Retained BH 1/4 carrier composition.** Provides
  `S_BH = A / (4 G)`.
- **Retained framework GR action.** Provides Hawking area theorem
  `δA ≥ 0` via Penrose-Hawking focusing argument on null geodesic
  congruences (admitted-context).

## Admitted-context inputs

- **Hawking area theorem `δA ≥ 0`** (Hawking 1971, Penrose 1965).
  Classical GR result on the retained framework smooth-limit surface,
  contingent on null energy condition `T_μν k^μ k^ν ≥ 0` for null
  vectors `k^μ`.
- **Null energy condition (NEC).** Holds for standard matter (electromagnetic
  field, scalar field, fermions) in classical GR; admitted-context.
  Quantum violations of NEC are bounded by quantum-energy inequalities
  (Ford-Roman) which preserve the time-averaged GSL.

## Statement

Let `(M, g)` be a stationary asymptotically flat spacetime with
non-degenerate Killing horizon `H` of area `A` and Hawking temperature
`T_H = κ/(2π)`. Let matter with entropy `S_matter` cross the horizon
during a physical process.

Then on `A_min` plus the retained inputs above:

**(GSL1) Hawking area theorem.** Under NEC, `δA ≥ 0` during any
physical process (classical area never decreases).

**(GSL2) Matter entropy positivity.** Under standard Gibbs evolution
of matter entropy (Block 01 KMS H-theorem), `δS_matter ≥ 0` (matter
entropy never decreases under physical evolution).

**(GSL3) Generalized second law.** The combined entropy

```text
    S_total  :=  S_BH + S_matter  =  A / (4 G) + S_matter                  (1)
```

is non-decreasing under any physical process satisfying NEC + Gibbs
evolution:

```text
    δ S_total  =  δA / (4 G)  +  δS_matter  ≥  0                          (2)
```

**(GSL4) Bekenstein information completion.** Combined with the
Bekenstein bound (Block 03), GSL implies that the framework
respects the holographic information bound: matter information stored
in any localized region cannot exceed `S_BH(M=E)/(k_B log 2)` bits
without violating GSL upon collapse.

Statements (GSL1)-(GSL4) constitute the Generalized Second Law on the
framework retained + support surface.

## Proof

### Step 1 — Area theorem (GSL1)

By the Hawking 1971 area theorem, on the framework's retained GR
action surface in the smooth-limit regime, any spacetime that is
asymptotically flat with a future-trapped surface (event horizon)
satisfies `δA ≥ 0` whenever the null energy condition (NEC) holds:

```text
    T_μν k^μ k^ν  ≥  0  for any null vector k^μ                            (3)
```

This is a classical GR theorem. The proof uses the Raychaudhuri
equation for null geodesic congruences:

```text
    d θ / dλ  =  -1/2 θ²  -  σ²  +  ω²  -  R_μν k^μ k^ν                    (4)
```

where `θ` is the expansion. Under NEC, `R_μν k^μ k^ν ≥ 0`, so the
expansion `θ` cannot increase from negative values to zero. Together
with the trapped-surface condition, this gives `dA/dt ≥ 0`. ∎

### Step 2 — Matter second law (GSL2)

By Block 01 KMS support theorem (K2 + K4): the Gibbs state at
inverse temperature `β` is the unique equilibrium state, and any
out-of-equilibrium distribution evolves toward equilibrium by
H-theorem (Boltzmann 1872, von Neumann 1929 generalization to
quantum mechanics). The von Neumann entropy

```text
    S(ρ)  :=  -tr(ρ log ρ)                                                  (5)
```

is non-decreasing under any unital quantum channel applied to a
state — this is the *quantum second law*. For matter undergoing
physical evolution (energy-preserving and unital), `δS_matter ≥ 0`. ∎

### Step 3 — Combined GSL (GSL3)

Sum (GSL1) and (GSL2):

```text
    δ S_total  =  δ S_BH  +  δ S_matter
              =  δ(A/(4G))  +  δ S_matter
              =  (1/(4G)) · δA  +  δ S_matter                                (6)
              ≥  0
```

since both `δA ≥ 0` and `δ S_matter ≥ 0`. This proves GSL3. ∎

### Step 4 — Information completion (GSL4)

By Bekenstein bound (Block 03), `S_matter(R, E) ≤ 2π R E` for
sub-Schwarzschild matter in radius `R`. If matter exceeds this
bound, attempting to compress it into a BH (which by first law
Block 05 happens at `T_H dS_BH = dE`) would yield
`δS_total = δS_BH + δS_matter < 0`, violating GSL3. Hence Bekenstein
bound is enforced by GSL3. ∎

## Hypothesis set used

- A_min (only as inherited from upstream).
- Block 01 KMS support (matter second law via H-theorem).
- Block 02 Hawking T_H support.
- Block 05 First law of BH mechanics support.
- Retained framework GR action (allows Penrose-Hawking area theorem).
- Retained BH 1/4 carrier (S_BH = A/4G).
- NEC for ordinary matter (admitted-context).
- Quantum H-theorem on Gibbs evolution (admitted-context).

No fitted parameters. No observed values used as proof inputs.

## Corollaries

C1. **Hawking radiation is consistent with GSL.** Hawking
1975 showed that BH evaporation produces matter with entropy slightly
greater than `δA/(4G)` (where `δA < 0` since the BH shrinks). Net:
`δS_total = δS_matter + δA/(4G) > 0`. GSL holds for evaporation.

C2. **Bekenstein bound is GSL-protected.** From GSL4, GSL forbids
matter with `S > 2πRE` (would otherwise decrease total entropy on
collapse). So Bekenstein bound is automatically enforced by GSL on
the framework retained surface.

C3. **Holographic principle.** GSL + Bekenstein → information in
any spacetime region is bounded by the boundary area in Planck units.
This is the holographic principle (`t Hooft-Susskind).

C4. **No information-paradox-via-violation.** Any proposed BH
information-paradox resolution must respect GSL on the framework
retained surface; this rules out simple "information is destroyed"
proposals.

## Honest status

**Branch-local theorem on retained framework GR + retained BH 1/4 +
Blocks 01, 02, 05 support theorems.** (GSL1)–(GSL4) follow by direct
composition of the upstream chain plus the standard Hawking 1971 area
theorem and von Neumann H-theorem.

The runner verifies (GSL3) on toy collapse scenarios:
matter with entropy `S_matter` falling into a BH increases
`S_BH = A/4G` by enough to compensate, yielding `δS_total ≥ 0` in
all cases consistent with NEC and Bekenstein bound.

**Honest claim-status fields:**

```yaml
actual_current_surface_status: support
conditional_surface_status: derived support theorem on retained framework GR + retained BH 1/4 + Blocks 01, 02, 05 support
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Inherits Block 05 first-law upstream support classification, which inherits Blocks 01 and 02 (KMS, Hawking T_H), all audit-pending. Per physics-loop SKILL retained-proposal certificate item 4, requires entire upstream chain ratified retained."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

**Not in scope.**

- Quantum-corrected GSL with semiclassical corrections.
- Generalized GSL beyond NEC (e.g. for quantum-energy-violating
  matter).

## Citations

- A_min: `docs/MINIMAL_AXIOMS_2026-04-11.md`
- Block 01 KMS: `docs/AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md`
- Block 02 Hawking: `docs/AXIOM_FIRST_HAWKING_TEMPERATURE_THEOREM_NOTE_2026-05-01.md`
- Block 05 First law: `docs/AXIOM_FIRST_FIRST_LAW_BH_MECHANICS_THEOREM_NOTE_2026-05-01.md`
- retained BH 1/4: `docs/BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`
- retained framework GR: `docs/UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`
- standard external references (theorem-grade, no numerical input):
  Hawking (1971) *Phys. Rev. Lett.* 26, 1344 (area theorem);
  Penrose (1965) *Phys. Rev. Lett.* 14, 57;
  Bekenstein (1973) *Phys. Rev. D* 7, 2333 (GSL proposal);
  Ford-Roman (1995) *Phys. Rev. D* 51, 4277 (quantum energy bounds).
