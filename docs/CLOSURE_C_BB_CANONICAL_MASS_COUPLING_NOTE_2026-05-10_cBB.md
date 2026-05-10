# Closure C-B(b) — Canonical Mass Coupling `rho_mass = M * rho_grav` (cBB)

**Date:** 2026-05-10
**Type:** bounded_theorem (bounded-positive structural forcing of M-linearity from retained Grassmann staggered-Dirac action + Born-rule operationalism)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — FULL-BLAST closure attempt on admission B(b) of
[`G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md`](G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md),
covering the canonical mass coupling
`rho_mass(x) = M * rho_grav(x)` — the same B(b) load shared between
gnewtonG3 (`V_grav = m * phi(x)`) and W-GNewton-Valley (`rho_mass = M * rho_grav`).
The M-linearity of the gravitational source IS forced by the retained
Grassmann staggered-Dirac action
`S_F = chi-bar (m + M_KS) chi` (per `AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29`)
plus the Born-rule operationalism (per `CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08`)
and the unified Born map of gnewtonG2. No new admission, no new repo-wide axiom.
**Status:** source-note proposal. Closes the M-linearity load at the bounded-positive
tier under retained content. The companion Born-as-source identification (gnewtonG2)
remains at bounded support; the parent admission (b) of `GRAVITY_CLEAN_DERIVATION_NOTE`
narrows to "given Born identification, M-linearity is forced".
Cascade: closes the canonical-mass-coupling load shared between gnewtonG3 and W-GNewton-Valley.
**Authority disclaimer:** source-note proposal — audit verdict and downstream
status set only by the independent audit lane.
**Loop:** closure-c-bb-canonical-mass-coupling-20260510-cBB
**Primary runner:** [`scripts/cl3_closure_c_bb_2026_05_10_cBB.py`](../scripts/cl3_closure_c_bb_2026_05_10_cBB.py)
**Cache:** [`logs/runner-cache/cl3_closure_c_bb_2026_05_10_cBB.txt`](../logs/runner-cache/cl3_closure_c_bb_2026_05_10_cBB.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived `claim_type`,
`audit_status`, and `effective_status` are generated only after the
independent audit lane reviews the claim, dependency chain, and runner.
The audit lane has full authority to retag, narrow, or reject the
proposal.

## Question

The planckP4 sharpening note
[`G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md`](G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md)
identified three admissions of `GRAVITY_CLEAN_DERIVATION_NOTE`:

> (a) `L^{-1} = G_0` — self-consistency identification of the field
>     operator inverse with the propagator Green's function.
> (b) `ρ = |ψ|²` — Born / mass-density source map.
> (c) `S = L (1 - φ)` — weak-field test-mass response.

The B(b) admission has **two structural sub-parts**:

1. **Born-as-source identification**: `rho_grav(x) = <x|rho_hat|x>` (the
   quantum-mechanical probability density operator). This was given bounded
   support by gnewtonG2.
2. **Canonical mass coupling**: `rho_mass(x) = M * rho_grav(x)`. This is the
   B(b) load shared between gnewtonG3 (`V_grav = m*phi`) and W-GNewton-Valley
   (`V(r;M)` linear in M). It loads on the question:

> **Why does mass enter LINEARLY** in the gravitational source, rather
> than as `M^2`, `sqrt(M)`, `exp(M)`, `1/M`, or some other function of M?

The probe question for this full-blast closure attempt:

> Can the M-linearity of the gravitational source be DERIVED from
> retained `Cl(3)` / `Z^3` content (axioms A1+A2 plus already-cited
> Grassmann staggered-Dirac action, Born-rule operationalism, and
> spectrum condition), without introducing a new admission?

## Answer

**Bounded positive forcing — derived, not admitted.** The M-linearity of
the gravitational source is **structurally forced** by the canonical
Grassmann staggered-Dirac action plus Born-rule operationalism. The chain:

```
Retained: S_F = chi-bar (m + M_KS) chi    [AXIOM_FIRST_LATTICE_NOETHER line 151]
                                           M = m + M_KS is the canonical
                                           staggered Dirac matrix
                                           (m enters with coefficient 1)

Mass term: m * (chi-bar chi)
         = m * Sigma_x chi-bar_x chi_x    [bilinear in fermion fields]

Born operationalism: <chi-bar_x chi_x>
                   = Tr(rho_hat |x><x|)
                   = rho_grav(x)         [gnewtonG2 unified Born map]

Mass-energy density: H_mass(x) = m * rho_grav(x)    (LINEAR in m, exact)
```

Identifying `M = m * <Q>` (total mass content of the wavefunction) with
the gravitational mass coupling constant gives:

```
rho_mass(x) = M * rho_grav(x)             [canonical mass coupling, FORCED]
```

The runner verifies this in six sections (31 PASS / 0 FAIL):

- **Section 1** (retained surface): the canonical Grassmann staggered-Dirac
  matrix `M = m * I + M_KS` is Hermitian, has additive mass + hop structure,
  and `dM/dm = I` exactly (literal linearity in m).
- **Section 2** (linear-in-m action): `S_F(m) = chi-bar (m+M_KS) chi` is
  EXACTLY AFFINE in m (linear fit residuals at machine precision, slope =
  `chi-bar chi`, all higher derivatives vanish). Hermiticity + U(1) phase
  symmetry constrain m to a real scalar.
- **Section 3** (Born + Dirac give canonical coupling): combining S1+S2 with
  gnewtonG2's unified Born map gives the local mass-energy density
  `m * rho_grav(x)` (linear in m). Multi-particle, equal-mass, and
  integrated-mass cases all preserve linearity.
- **Section 4** (hostile-review forecloses alternatives): each of
  `f(m) = m^2`, `sqrt(m)`, `exp(m)`, `1/m`, arbitrary nonlinear is
  forbidden by a *distinct* retained constraint (canonical bilinear action,
  analyticity, bounded H spectrum, massless limit, additivity). Only
  `f(m) = c*m` survives all five — **UNIQUENESS RESULT**.
- **Section 5** (downstream consistency): the canonical mass coupling
  reproduces gnewtonG3's `V_grav = m*phi`, W-GNewton-Valley's `V(r;M)`
  linear in M, the Schiff (1968) standard Newton-limit coupling form,
  Newton mass conservation, and STAGGERED_FERMION_CARD's
  `H_diag = (m + Phi)*epsilon` mass linearity.
- **Section 6** (synthesis): the closure verdict and cascade.

**Boundary:** the forcing is bounded (not unconditional positive theorem)
because:
1. it uses the staggered-Dirac realization as an admitted carrier (per
   `MINIMAL_AXIOMS_2026-05-03` — currently an open derivation target,
   not yet a positive theorem from A1+A2 alone). When that gate closes
   on A1+A2, this becomes a clean positive theorem.
2. it uses gnewtonG2's bounded Born-as-source identification as input.

But the M-linearity ITSELF is the new closure: given the staggered-Dirac
carrier and Born identification, NO non-linear mass coupling is admissible
in retained content. The B(b) admission narrows from "mass enters as
some function of M (which function?)" to "mass enters LINEARLY (this
is forced)".

## Setup

### Premises for the bounded positive forcing lemma

| ID | Statement | Class |
|---|---|---|
| A1 | Physical `Cl(3)` local algebra | framework axiom: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| A2 | `Z^3` spatial substrate | framework axiom: same source |
| StaggDirac | Grassmann staggered Dirac action `S_F = chi-bar (m+M_KS) chi` | admitted carrier per `MINIMAL_AXIOMS` (open derivation target, canonical form cited from `AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29` line 151) |
| Noether | Global U(1) phase symmetry → conserved fermion number `Q = Sigma_x chi-bar_x chi_x` | bounded_theorem: [`AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md) (N2) |
| BornOp | Born-rule operationalism | cited meta: [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md) |
| BornMap | Unified position-density Born map `rho_grav(x) := <x|rho_hat|x>` | bounded support: [`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md) |
| SpecCond | Spectrum condition: `H = -log(T)/a_tau` bounded operator | unaudited (positive_theorem): [`AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md) |
| Hermiticity | Self-adjoint Hamiltonian / Hermitian action matrix | unaudited (positive_theorem): same source (and `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`) |

### Forbidden imports

- NO PDG observed values used as derivation input.
- NO new repo-wide axioms.
- NO promotion of unaudited content to retained-grade.
- NO empirical fits (the runner uses RANDOM-FREE structural checks; no
  fitting against observation).
- NO same-surface family arguments.

## Theorem (bounded positive forcing of M-linearity)

**Theorem (cBB, canonical mass coupling).** Under the premises above, the
gravitational source density `rho_mass(x; M)` is exactly LINEAR in the
mass parameter M:

```
rho_mass(x; M) = M * rho_grav(x)        (M-linearity, forced)        (1)
```

where `rho_grav(x) := <x|rho_hat|x>` is the unified position-density
Born map of gnewtonG2 and `M = m * <Q>` is the total mass content of the
wavefunction (single-particle: `M = m`; N-particle: `M = sum_i m_i`).

**Foreclosure.** No alternative coupling
`rho_mass(x; M) = f(M) * rho_grav(x)` with `f(M) != alpha * M` is
admissible under retained content. Specifically:

| Form | Foreclosed by |
|---|---|
| `f(M) = M^2` | canonical bilinear Grassmann action (non-renormalizable 4-fermion term) |
| `f(M) = sqrt(M)` | analyticity at M=0 (chiral limit must exist) |
| `f(M) = exp(M)` | bounded H spectrum (spectrum condition violated for large M) |
| `f(M) = 1/M` | massless limit (chiral M=0 surface required by staggered carrier) |
| `f(M) = arbitrary nonlinear` | additivity for multi-species (`f(m1)+f(m2)` != `f(m1+m2)`) |

**Cascade.** Closes the B(b) load shared between:
- gnewtonG3: `V_grav = m * phi(x)` is the Newton-limit coupling. Combined
  with this note's `rho_mass = M*rho_grav`, the chain is internally
  consistent and the leading-order valley-linear response `S = L(1 - phi)`
  follows from gnewtonG3.
- W-GNewton-Valley: `V(r; M)` linear in M follows from
  `rho_mass = M*rho_grav` + Poisson linearity of `-Delta_lat`. Mass-linearity
  is now FORCED, not admitted.

## Proof

### Step 1 — Retained staggered-Dirac action surface

By `AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md` line 151,
the canonical Grassmann staggered-Dirac action is:

```text
    S_F[chi-bar, chi] = Sigma_{x,y} chi-bar_x M_xy chi_y                (2)
    M = m * I + M_KS                                                    (3)
```

where `M_KS` is the staggered Kogut-Susskind hop (`M_KS_{x, x±μ̂} = ±(1/2)η_μ(x)`)
and m is the mass parameter (a real scalar). The matrix `M` is Hermitian
(verified in runner S1.1), additive in m + M_KS (S1.2), and depends
LINEARLY on m with `dM/dm = I` (S1.3).

By Noether N2 of the same axiom-first note, the global U(1) phase
symmetry `chi -> e^(iα) chi` yields the conserved fermion-number
current `J^μ_x` whose integrated charge is:

```text
    Q = Sigma_x chi-bar_x chi_x                                         (4)
```

The operator `chi-bar_x chi_x` is the local fermion-number density
(in the single-particle Fock reduction: the projector `|x><x|`).
Verified in runner S1.4 (Hermitian, idempotent) and S1.5 (commutes
with the mass term, U(1) symmetry).

**Boundary check:** the staggered-Dirac realization itself is admitted as
a carrier per `MINIMAL_AXIOMS_2026-05-03` (open derivation target from
A1+A2). When that gate closes, S1 is retained-from-axioms. Until then,
S1 is a *retained-carrier* surface.

### Step 2 — Linear-in-mass action contribution

The action (2)-(3) is bilinear in chi, with m appearing only as a
coefficient of the diagonal mass term. Therefore:

```text
    S_F = chi-bar (m*I + M_KS) chi
        = m * (chi-bar chi)  +  chi-bar M_KS chi                        (5)
```

Differentiating with respect to m:

```text
    d S_F / d m = chi-bar chi = Sigma_x chi-bar_x chi_x                 (6)
    d^n S_F / d m^n = 0  for all n >= 2                                 (7)
```

The action is EXACTLY AFFINE in m. Runner S2.1-S2.3 verify this:
- S2.1: `d S_F / d m = 1.0` (numerical) = `chi-bar chi` (exact)
- S2.2: `d^2 S_F / d m^2 = 0` (numerical noise level)
- S2.3: linear-fit residuals to `S_F(m)` over 10 m-values are
  `< 4.44e-16` (machine precision); slope matches `chi-bar chi` exactly.

**Hermiticity constraint (S2.4).** If m were complex, the mass term
`m * I + ... = (Re m) I + i (Im m) I + ...` would have an anti-Hermitian
part, so the action matrix M would not be Hermitian. By the Hermiticity
of M (cited surface, Step 1), m is constrained to be real.

**Scalar constraint (S2.5).** Under global U(1) phase symmetry
`chi -> e^(iα) chi` (N2 of Noether), the bilinear `chi-bar chi` is
invariant for any scalar α. If m had a spinor index `m_i`, the action
would only be U(1)-invariant if all `m_i` are equal (in which case m
collapses to a scalar). So m is a real scalar.

### Step 3 — Born-rule expectation gives linear local mass-density

By gnewtonG2 ([`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md)),
the unified position-density Born map is:

```text
    rho_grav(x) := <x|rho_hat|x> = Tr(rho_hat * M_hat(x))               (8)
    where M_hat(x) := |x><x|
```

The Born-rule operationalism (`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08`)
identifies the expectation value of `chi-bar_x chi_x` in any state with
the local fermion-number density:

```text
    <chi-bar_x chi_x>_rho = Tr(rho_hat * M_hat(x)) = rho_grav(x)        (9)
```

Combining (6) and (9), the expectation value of the mass-term
contribution to the action is:

```text
    <m * chi-bar chi>_rho = m * Sigma_x <chi-bar_x chi_x>_rho
                          = m * Sigma_x rho_grav(x)
                          = m * <Q>                                     (10)
```

The local mass-energy density (the source of gravitational coupling) is:

```text
    H_mass(x) = m * rho_grav(x)                                         (11)
```

This is the canonical mass coupling. Runner S3.1 verifies
`<chi-bar_x chi_x> = |psi_x|^2` exactly (max |diff| = 0); S3.2 verifies
linearity in m; S3.3 verifies additivity for multi-species; S3.4
verifies the equal-mass N-particle case (`M_eff = N*m`); S3.5 verifies
total integrated mass conservation.

### Step 4 — Foreclosure of non-linear alternatives

**Claim:** No non-linear coupling `rho_mass = f(m) * rho_grav` with
`f(m) != alpha * m` is admissible under retained content.

**Proof (by exhaustion of natural alternatives).**

**(S4.1) `f(m) = m^2` is forbidden.** A term proportional to `m^2` in
the action would have to appear as `m^2 * (chi-bar chi)` — but this is
*linear* in `(chi-bar chi)` with coefficient `m^2`, which (via (6))
gives `d^2 S/dm^2 = 2 * <chi-bar chi> != 0`, contradicting (7).
Alternatively, if the `m^2` dependence came from a `(chi-bar chi)^2`
term, that's a *four-fermion vertex*, dimension 6 in 4D
(with `chi` dimension 3/2), which is non-renormalizable and NOT in the
canonical Grassmann staggered-Dirac action (per S1). Excluded.

**(S4.2) `f(m) = sqrt(m)` is forbidden.** A `sqrt(m)` coefficient would
be non-analytic at `m = 0`. The staggered-Dirac realization gate admits
the chiral limit `m = 0` as a valid surface (`m = 0` is the massless
fermion case, standard in lattice QCD). Non-analyticity at m=0 introduces
a branch point that obstructs the massless limit. Excluded.

**(S4.3) `f(m) = exp(m)` is forbidden.** An `exp(m)` coefficient would
grow unboundedly with m, injecting an exponentially large term into the
action for any `m > log(J)/a_tau`. The reconstructed Hamiltonian
`H = -log(T)/a_tau` is bounded
(`AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29`), which requires
bounded action contributions. Excluded.

**(S4.4) `f(m) = 1/m` is forbidden.** A `1/m` coefficient diverges as
`m -> 0`, forbidding the chiral limit. Same obstruction as S4.2 (different
mechanism: divergence rather than non-analyticity). Excluded.

**(S4.5) Arbitrary nonlinear `f(m)` is forbidden by additivity.** For
two distinguishable particle species 1, 2 with masses m1, m2, the Dirac
action has separate mass terms
`m1 chi-bar_1 chi_1 + m2 chi-bar_2 chi_2`, additive in mass parameters.
A nonlinear `f` would give `f(m1) chi-bar_1 chi_1 + f(m2) chi-bar_2 chi_2`,
which is NOT obtained by `f(m1 + m2)` applied to a joint density (e.g.,
`f(m) = m^2` gives `m1^2 + m2^2 != (m1+m2)^2`). Only the linear form
`f(m) = c*m` satisfies `f(m1) + f(m2) = f(m1 + m2)`. Excluded.

**(S4.6) UNIQUENESS.** The five constraints (canonical bilinear action,
analyticity at m=0, bounded H spectrum, chiral limit existence,
multi-species additivity) jointly admit ONLY `f(m) = c*m`. The
coefficient c is fixed by the canonical staggered-Dirac normalization
convention (per `AXIOM_FIRST_LATTICE_NOETHER_THEOREM` line 151) to
c = 1, giving the canonical mass coupling. ∎

### Step 5 — Consistency with downstream chain

The canonical mass coupling `rho_mass = M * rho_grav` correctly
reproduces:

**S5.1 gnewtonG3 Newton-limit coupling.** Setting `V_grav(x) = m * phi(x)`
(per `G_NEWTON_WEAK_FIELD_RESPONSE_BOUNDED_CLOSURE_NOTE_2026-05-10_gnewtonG3`):
for uniform phi, the total potential energy is `m * phi * <Q> = m * phi`
(linear in m). This is the standard textbook Newton-limit coupling
(Schiff 1968 eq. 24.12; modern QM treatments).

**S5.2 W-GNewton-Valley M-linearity.** With `rho_mass = M * rho_grav`,
the lattice Poisson equation `(-Delta_lat) phi = rho_mass` gives
`phi = M * (-Delta_lat)^{-1} rho_grav`. By linearity of `-Delta_lat`,
`phi(alpha M) = alpha * phi(M)`. Runner S5.2 verifies
`max |phi(alpha M) - alpha phi(M)| < 1e-14`.

**S5.3 Schiff (1968) standard form.** Standard nonrelativistic limit of
the Dirac equation in a weak gravitational field yields
`V_grav = m * phi` (linear in m). References:
- Schiff, *Quantum Mechanics*, 3rd ed. (1968), eq. 24.12.
- Wikipedia, "Schrödinger-Newton equation".
- arXiv:2210.02405 ("Non-relativistic limit of scalar and Dirac fields
  in curved spacetime", 2023).
This is the universal textbook form; our derivation via the canonical
staggered-Dirac action recovers it from retained content.

**S5.4 Newton mass conservation.** Total integrated source density
`Integral rho_mass dx = M * <Q> = M` (for normalized state). The
integrated mass equals the input mass. Mass is conserved.

**S5.5 STAGGERED_FERMION_CARD coupling form.** The retained card
`STAGGERED_FERMION_CARD_2026-04-11.md` has
`H_diag = (m + Phi) * epsilon(x)`. The mass enters linearly:
`d H_diag / d m = epsilon(x)` (independent of m). Runner S5.5
verifies this to machine precision. ∎

## What this supports

- **Closes admission B(b) M-linearity load.** The canonical mass
  coupling `rho_mass = M * rho_grav` is structurally forced. The B(b)
  admission narrows from "what M-power?" to "linear (forced); Born
  identification (bounded via gnewtonG2)".
- **Cascade: closes gnewtonG3 B(b) load.** The canonical Newton-limit
  coupling `V_grav = m * phi(x)` (which gnewtonG3 required as input)
  is no longer an admission — its mass-linearity is forced.
- **Cascade: closes W-GNewton-Valley B(b) load.** The canonical mass
  coupling `rho_mass = M * rho_grav` (which W-GNewton-Valley required)
  is no longer an admission — its mass-linearity is forced.
- **Cleans the GRAVITY_CLEAN_DERIVATION_NOTE Step 4-8 chain.** The
  "Poisson linearity, exact" claim of Step 8 (composition of two linear
  maps) becomes a forced consequence rather than a tacit admission of
  M-linearity.
- **Identifies the residual frontier.** The remaining open admissions
  of `GRAVITY_CLEAN_DERIVATION_NOTE`:
  - (a) `L^{-1} = G_0` skeleton selection — still OPEN per
    `G_NEWTON_SKELETON_SELECTION_BOUNDED_NOTE_2026-05-10_gnewtonG1`.
  - (b) Born-as-source identification — still BOUNDED via gnewtonG2;
    M-linearity now FORCED via this note.
  - (c) `S = L(1 - phi)` weak-field response — still BOUNDED via gnewtonG3;
    canonical coupling load now FORCED via this note.

## What this does NOT close

- **Born-as-source identification.** This note does NOT derive that gravity
  must source from the Born density (i.e., it does not close gnewtonG2's
  bounded-support gate). It closes only the M-linearity sub-part of B(b),
  given the Born identification.
- **The staggered-Dirac realization derivation target.** Per
  `MINIMAL_AXIOMS_2026-05-03`, this is an open derivation target (open
  gate from A1+A2). This note uses it as an admitted carrier.
- **Admission (a) of GRAVITY_CLEAN_DERIVATION_NOTE.** The skeleton selection
  `L^{-1} = G_0` remains open per gnewtonG1.
- **Strong-field gravity beyond linearized weak-field.** This note works
  at the level of the source coupling, not the geodesic / strong-field
  regime. Strong-field gravity, horizons, frame-dragging are out of scope.
- **Multi-particle interactions beyond linear superposition.** Quantum
  exchange / antisymmetry effects in multi-fermion states are not analyzed
  here; the additivity result (S4.5) assumes distinguishable species.
- **The Koide flavor-sector closure.** The mass-linearity is the
  *coefficient* of the source density, not the *mass spectrum* itself.
  Koide-style mass-spectrum derivations are independent.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| M-linearity (P1) | Demonstrate a gravitational source `rho_mass(M)` with non-linear M-scaling. The runner verifies linearity exact to machine precision (S2.3, S3.2, S5.2). |
| Hermiticity of canonical action (P1.1) | Demonstrate a Hermitian canonical fermion action with non-real mass coupling. The runner verifies S2.4 (complex m breaks Hermiticity). |
| U(1) phase scalar mass (P1.5) | Demonstrate a per-component mass coupling consistent with global U(1) phase symmetry. Mathematically impossible (S2.5). |
| Bounded H + exp(m) coupling | Demonstrate a bounded H with an `exp(m)` mass term. Spectrum condition prohibits (S4.3). |
| Chiral limit + 1/m coupling | Demonstrate a 1/m coupling consistent with `m = 0` limit. Divergent (S4.4). |
| Additivity for multi-species + nonlinear coupling | Demonstrate that nonlinear `f(m)` satisfies `f(m1) + f(m2) = f(m1+m2)`. Only `f(m) = c*m` does (S4.5). |
| Downstream consistency | Demonstrate gnewtonG3 `V_grav = m*phi` with non-linear m-coupling. Standard textbook treatment is linear (S5.3). |

## Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane. The bounded theorem is a structural forcing of the
M-linearity sub-part of admission B(b):

- The staggered-Dirac realization gate is admitted (open per `MINIMAL_AXIOMS`).
- The Born-rule operationalism is cited meta (not retained-grade).
- The Born-as-source identification is bounded (gnewtonG2).
- Under these, the M-linearity of the gravitational source is **FORCED** —
  no non-linear power admissible.

No new repo-wide axioms are proposed. No automatic cross-tier promotion.
The audit lane has full authority to retag, narrow, or reject this
proposal.

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | Partial yes — the M-linearity sub-part of admission B(b) is closed. The Born-as-source identification remains bounded (gnewtonG2 status unchanged). |
| V2 | New bounded derivation? | Yes — the M-linearity is *derived* from the canonical Grassmann staggered-Dirac action (`AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29` line 151) plus Born-rule operationalism. The hostile-review uniqueness result (S4) is structurally new: it foreclosures *all* natural non-linear alternatives via distinct retained constraints (canonical bilinear action, analyticity, bounded H, massless limit, additivity). |
| V3 | Audit lane could complete? | Yes — audit lane can review: (i) the canonical Grassmann action form (cited), (ii) the linear-in-m structure (verified to machine precision in runner S2.3), (iii) the Born-operationalism + Born map identification, (iv) each of the five foreclosure mechanisms in S4, (v) downstream consistency with gnewtonG3, W-GNewton-Valley, STAGGERED_FERMION_CARD. |
| V4 | Marginal content non-trivial? | Yes — the B(b) admission has been a structural blocker on multiple gravity-chain probes (gnewtonG3 bounded, W-GNewton-Valley bounded, GRAVITY_CLEAN_DERIVATION_NOTE bounded conditional). Closing the M-linearity sub-part is a non-trivial bounded-positive forcing, qualitatively different from a relabel or one-step variant. |
| V5 | One-step variant? | No — this note is NOT a relabel of gnewtonG2 (which addresses Born-as-source identification, not M-coupling) nor gnewtonG3 (which uses M-coupling as input). The new content is the *uniqueness proof* of M-linearity via five-fold foreclosure (S4). |

**Source-note V1-V5 screen: pass for bounded-theorem audit seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule is
to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of any prior gravity, Born, or mass-coupling note.
  gnewtonG2 addresses Born-as-source (different sub-part of B(b));
  gnewtonG3 admits the canonical coupling as input;
  W-GNewton-Valley admits the canonical coupling as input;
  this note DERIVES the M-linearity.
- Identifies a NEW STRUCTURAL FORCING (M-linearity via canonical bilinear
  Grassmann action + Born map) — not a tweak of prior bounded notes.
- Provides a UNIQUENESS RESULT (S4: five-fold foreclosure of alternatives)
  — qualitatively new structural content.
- Sharpens the open frontier: B(b) was "what M-power?" → now
  "M-linear, forced". The residual question is the Born-as-source
  identification itself (gnewtonG2's open sub-part).
- Closes a cascade: gnewtonG3 + W-GNewton-Valley were both bounded by
  the canonical coupling load; both now have that load FORCED.

## First-principles exercise (Elon-style minimum)

A literal minimum: what is the simplest functional `rho_mass = F(M, rho_grav)`?

**Constraints from retained content (NOT new admissions):**
1. **Linearity in `rho_grav`**: gnewtonG2 verified linearity in `rho_hat`
   (the density operator). The map `rho_hat -> rho_grav` is linear, so
   `F` must be linear in `rho_grav` to preserve linearity in `rho_hat`.
2. **Additive multi-particle**: distinguishable species contribute additively
   (Dirac action mass terms are additive). `F(M_1+M_2, rho) = F(M_1, rho) + F(M_2, rho_2)`
   for separate species → forces F to be of the form `M * G(rho)` where
   G is some function of `rho_grav` alone.
3. **Pure-state `rho_mass = m * |psi|^2` matches gnewtonG3 and STAGGERED_FERMION_CARD
   on pure states** → `G(rho) = rho` (just linear in `rho_grav`).
4. **Hermiticity of action / real M** → M is a real scalar.
5. **Bounded H spectrum, analyticity, multi-species additivity** → forces
   M-linearity (S4 of runner).

**Conclusion of the literal minimum:** `F(M, rho_grav) = M * rho_grav`
is the UNIQUE linear, additive, real, multi-species-consistent functional
that reduces to `m * |psi|^2` on single-particle pure states. This is
exactly the canonical mass coupling.

## Cross-references

- Parent gravity-clean note: [`GRAVITY_CLEAN_DERIVATION_NOTE.md`](GRAVITY_CLEAN_DERIVATION_NOTE.md)
- Parent G_Newton self-consistency probe:
  [`G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md`](G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md)
- Sister gnewtonG2 (Born-as-source identification, the other sub-part of B(b)):
  [`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md)
- Sister gnewtonG3 (weak-field response under canonical coupling — the
  load this note closes for gnewtonG3):
  [`G_NEWTON_WEAK_FIELD_RESPONSE_BOUNDED_CLOSURE_NOTE_2026-05-10_gnewtonG3.md`](G_NEWTON_WEAK_FIELD_RESPONSE_BOUNDED_CLOSURE_NOTE_2026-05-10_gnewtonG3.md)
- Sister W-GNewton-Valley (V(r;M) linear in M — the other downstream
  load this note closes; in-flight PR #1024 branch
  `probe/w-gnewton-valley-2026-05-10`).
- Canonical staggered-Dirac action form: [`AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md) line 151
- Born-rule operationalism: [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)
- Spectrum condition (bounded H): [`AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md)
- Reflection positivity (Hermitian action): [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- Staggered-Dirac realization gate (admitted carrier): [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Retained `(m+Phi)*epsilon` coupling form: [`STAGGERED_FERMION_CARD_2026-04-11.md`](STAGGERED_FERMION_CARD_2026-04-11.md)
- Newton-from-Z^3 chain: [`NEWTON_LAW_DERIVED_NOTE.md`](NEWTON_LAW_DERIVED_NOTE.md)
- MINIMAL_AXIOMS: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)

## Literature support (external)

- Schiff, L.I., *Quantum Mechanics*, 3rd ed. (McGraw-Hill, 1968), §24
  ("Quantum theory in a gravitational field"), eq. 24.12.
- Tong, D., *Quantum Field Theory* lecture notes (DAMTP/Cambridge),
  Chapter 5 ("Quantizing the Dirac Field"): standard fermion mass
  term `m * psi-bar psi` is bilinear, real, scalar.
- arXiv:2210.02405, "Non-relativistic limit of scalar and Dirac fields
  in curved spacetime" (2023): explicit derivation of Newton-limit
  coupling `V_grav = m * phi` from the Dirac equation in weak-field
  gravity.
- Wikipedia, "Schrödinger-Newton equation" — standard treatment of
  gravitational source as `m * |psi|^2` (linear in m).
- These confirm that mass-linearity is the universal textbook form;
  our derivation supplies the structural reason from retained
  Cl(3)/Z^3 content.

## Validation

```bash
python3 scripts/cl3_closure_c_bb_2026_05_10_cBB.py
```

Expected output: structural verification of (1) the canonical retained
staggered-Dirac action surface `M = m*I + M_KS` (Hermitian, additive,
m-linear); (2) the action is exactly affine in m (residuals from linear
fit < 1e-15); (3) Born-rule operationalism + gnewtonG2 give the local
mass-energy density `m * rho_grav(x)` (linear); (4) hostile-review
foreclosure of `m^2`, `sqrt(m)`, `exp(m)`, `1/m`, arbitrary nonlinear
mass-couplings (each by a distinct retained constraint); (5) consistency
with gnewtonG3, W-GNewton-Valley, STAGGERED_FERMION_CARD, Schiff (1968);
(6) cascade closure synthesis. Total: 31 PASS / 0 FAIL.

Cached: [`logs/runner-cache/cl3_closure_c_bb_2026_05_10_cBB.txt`](../logs/runner-cache/cl3_closure_c_bb_2026_05_10_cBB.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note does NOT
  rely on consistency-equality. The M-linearity is *derived* from the
  canonical Grassmann staggered-Dirac action (a retained carrier),
  not consistent with empirical observation. The hostile-review
  uniqueness result (S4) is a structural exhaustion of natural
  alternatives, each foreclosed by a distinct retained constraint.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim that "M-linearity is admitted" by deriving it
  structurally from retained content. The S4 hostile-review section
  explicitly enumerates the natural non-linear alternatives and
  forecloses each by a distinct retained constraint, not a single
  global argument.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note proposes bounded-theorem support for
  M-linearity (not retained-grade promotion); gnewtonG2 remains at
  bounded support; the parent `GRAVITY_CLEAN_DERIVATION_NOTE` remains
  at its prior status until all three admissions close.
- `feedback_physics_loop_corollary_churn.md`: the M-linearity uniqueness
  result with five-fold foreclosure is substantive new structural
  content, not a relabel of gnewtonG2 (Born-as-source) nor gnewtonG3
  (which admits the coupling) nor W-GNewton-Valley (which admits the
  coupling). The structural derivation from the canonical Grassmann
  action is qualitatively new.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  are characterized as WHAT additional content would be needed to
  resurrect them (e.g., a 4-fermion vertex theorem would resurrect the
  `m^2` alternative; a chiral-symmetry-violating mass term theorem
  could resurrect `sqrt(m)`), not how-long-they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note packages
  the full-blast B(b) closure attack with sharp PASS/FAIL deliverables
  in the runner: S1 (retained action surface), S2 (linear-in-m),
  S3 (Born-Dirac gives canonical coupling), S4 (hostile-review),
  S5 (downstream consistency), S6 (synthesis).
- `feedback_review_loop_source_only_policy.md`: source-only — this PR
  ships exactly (a) source theorem note, (b) paired runner, (c) cached
  output. No output-packets, lane promotions, synthesis notes, or
  "Block" notes.
- `feedback_bridge_gap_fragmentation_2026_05_07.md`: the parent
  G_Newton lane is being fragmented. planckP4 isolated three named
  admissions; gnewtonG2 narrowed Born-as-source identification of B(b);
  gnewtonG3 narrowed B(c) under canonical coupling input; W-GNewton-Valley
  narrowed V(r;M) under canonical coupling input; THIS note narrows
  the canonical coupling itself — M-linearity FORCED. No new admissions
  are introduced.
- `feedback_primitives_means_derivations.md`: "new primitives" /
  derivations from A1+A2+retained, not new axioms. This note uses ONLY
  the retained Cl(3)/Z^3 surface (canonical Grassmann staggered-Dirac
  action + Noether U(1) + spectrum cond + Born-rule operationalism +
  gnewtonG2 Born map) — no new axiom, no import beyond what is already
  retained or cited.
