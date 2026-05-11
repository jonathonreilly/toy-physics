# Hierarchy alpha_LM Exponent / Species-Count Bridge — Regulator-Dependence No-Go Note

**Date:** 2026-05-10
**Claim type:** no_go
**Scope:** at the level of standard lattice-field-theory primitives,
the identification "physical species count `N_species` of a fermion
regulator on the four-direction Euclidean lattice used by the fermion
regulator calculation equals the exponent in the framework's
hierarchy formula `v = M_Pl * alpha_LM^16 * (7/8)^(1/4)`" is
regulator-dependent. The exponent `16` in the hierarchy formula coincides
numerically with the naive lattice fermion species count `2^4 = 16`
(landed parent narrow theorem), but distinct standard regulators on the
same four-direction regulator surface produce distinct physical-species
counts (Wilson: 1, common twisted-mass doublet setup: 2, staggered after
Kawamoto-Smit spin-taste decomposition: 4, domain-wall: 1, overlap: 1),
and Symanzik improvement / continuum-limit
theorems require all of them to converge to the same continuum SM as
`a -> 0`. Therefore the identification cannot be derived from
regulator-independent QFT primitives alone; the framework's hierarchy
exponent `16` is consistent with the naive regulator only, and the choice
of regulator remains a substrate-imposed gate input, recorded in the open
[`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md).
**Status authority:** source-note proposal only; independent audit sets
any audit result and the pipeline-derived effective status.
**Runner:** [`scripts/frontier_hierarchy_alpha_lm_exponent_species_count_bridge_regulator_dependence_no_go.py`](../scripts/frontier_hierarchy_alpha_lm_exponent_species_count_bridge_regulator_dependence_no_go.py)
**Cache:** [`logs/runner-cache/frontier_hierarchy_alpha_lm_exponent_species_count_bridge_regulator_dependence_no_go.txt`](../logs/runner-cache/frontier_hierarchy_alpha_lm_exponent_species_count_bridge_regulator_dependence_no_go.txt)

## 0. Context

The framework's hierarchy formula

```text
v = M_Pl * alpha_LM^16 * (7/8)^(1/4) ≈ 246.28 GeV
```

uses the integer exponent `16`. The parent narrow theorem

- [`NAIVE_LATTICE_FERMION_TWO_POWER_D_SPECIES_COUNT_NARROW_THEOREM_NOTE_2026-05-10.md`](NAIVE_LATTICE_FERMION_TWO_POWER_D_SPECIES_COUNT_NARROW_THEOREM_NOTE_2026-05-10.md)

proves at exact-algebra level that the **naive** lattice Dirac operator
on `Z^d` has `2^d` Brillouin-zone-corner zero modes, giving `16` at
`d = 4`. The numerical coincidence is exact. The natural question is
whether the identification

```text
N_species(d=4) = 16   <-->   hierarchy exponent = 16
```

is a regulator-independent QFT theorem (i.e., reachable from minimal
lattice field-theory primitives alone, with no substrate-imposed choice).

This note answers **no**.

## 1. Claim

> **Theorem (no-go).** Within standard lattice-field-theory primitives
> applied uniformly to all renormalisable lattice fermion regulators on
> the four-direction regulator surface whose continuum limit is the SM,
> the identification of the
> hierarchy exponent `16` in `v = M_Pl * alpha_LM^16 * (7/8)^(1/4)` with
> the physical species count `N_species` of the regulator is
> **regulator-dependent**. Different standard regulators produce different
> `N_species` (Wilson: 1, twisted-mass: 2, staggered after Kawamoto-Smit:
> 4, domain-wall: 1, overlap: 1), while their common continuum limit is
> the same SM. Therefore the integer `16` cannot be derived from
> regulator-independent QFT properties of that four-direction lattice
> regulator alone, and the
> identification holds only on the naive operator regulator, which is the
> substrate-imposed reading already recorded in the open
> [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md).

## 2. Boundary

This is a narrow lattice-field-theory no-go theorem about a candidate
bridge identification. It is not a framework axiom and it consumes no
framework authority. It does not claim:

- that the parent narrow theorem (`2^d` for the naive operator) is
  incorrect (it is exact algebra and stands on its own);
- that the framework's hierarchy formula
  `v = M_Pl * alpha_LM^16 * (7/8)^(1/4)` itself is invalid (the formula
  is a separate derivation track with its own gate inputs);
- that the staggered-Dirac realization gate is closed (it remains open;
  see [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md));
- that any specific framework lane is retracted, demoted, or closed by
  this no-go;
- that the repo baseline physical `Cl(3)` local algebra plus `Z^3`
  spatial substrate, together with any staggered-realization gate input,
  is wrong; the no-go only constrains what the
  bridge identification can be derived **from**, not whether the
  framework's substrate is allowed to fix it as a primary modelling
  choice.

The no-go's only positive content is: **`N_species = hierarchy exponent`
is not a QFT identity at the lattice-action-uniform level.** The naive
match `16 = 2^4` is exact and standalone; the bridge identification is
substrate-imposed.

## 3. Standard species counts at d=4

The standard lattice fermion regulators on `Z^4` with continuum-limit
target equal to the SM produce the following physical-species counts:

| Regulator | `N_species` at `d=4` | Citation |
|---|---|---|
| naive (BZ corners) | 16 | parent narrow theorem |
| Wilson | 1 | K. Wilson, in "New Phenomena in Subnuclear Physics" (1977) |
| twisted-mass | 2 | R. Frezzotti and G. C. Rossi, JHEP 04 (2004) 070 |
| staggered (Kawamoto-Smit, pre-rooting) | 4 | N. Kawamoto and J. Smit, NPB 192 (1981) 100 |
| domain-wall | 1 | D. B. Kaplan, PLB 288 (1992) 342 |
| overlap | 1 | H. Neuberger, PLB 417 (1998) 141 |

(The staggered count `4` is the irreducible spin-taste decomposition of
the `16` BZ-corner modes via the Kawamoto-Smit gamma matrices; the
"rooting" reduction to `1` in lattice-QCD practice introduces a
non-locality controversy that does not affect this note's verdict — see
S. R. Sharpe, "Rooted staggered fermions", PoS LAT2006 (2007) 022,
[arXiv:hep-lat/0610094](https://arxiv.org/abs/hep-lat/0610094); and
C. Bernard et al., "Status of staggered simulations", PoS LAT2007 (2007)
090.) Including rooting, the count varies from 4 (taste-replicated) to 1
(rooted, controversial), all within standard regulators with the same
continuum limit.

The five non-naive regulator counts above differ from the naive `16`
count and differ from each other. The naive count `16` is the parent
narrow theorem; the other counts are textbook lattice-field-theory
results.

## 4. Continuum-limit uniqueness

Symanzik's improvement program (K. Symanzik, "Continuum limit and
improved action in lattice theories", NPB 226 (1983) 187) and Reisz's
power-counting theorem (T. Reisz, "A power-counting theorem for Feynman
integrals on the lattice", Comm. Math. Phys. 116 (1988) 81) establish
that any renormalisable lattice action whose tree-level action recovers
the continuum kinetic term, and whose loop-level power counting agrees
with the standard continuum classification, converges to the same
continuum theory as `a -> 0`. For each of the six regulators in §3:

- the naive action recovers Dirac kinetic term plus BZ-corner doublers
  (Karsten-Smit; see parent narrow theorem);
- Wilson adds `r/(2 a) sum_mu (1 - cos(k_mu a))` to lift the doublers
  while preserving the SM continuum limit (additive mass
  renormalisation);
- twisted-mass adds a chirally-twisted mass term retaining O(`a^2`)
  improvement at maximal twist;
- staggered uses the Kawamoto-Smit decomposition to reduce 16 modes to
  4 tastes carrying SM quantum numbers;
- domain-wall and overlap implement Ginsparg-Wilson chiral symmetry,
  reaching the SM in their respective `Ls -> ∞` or `epsilon_n` limits.

The continuum limits of all six regulators are SM observables (after
the regulator-specific reductions, e.g. rooting for staggered, additive
mass renormalisation for Wilson, maximal-twist tuning for twisted-mass).
This is the standard Symanzik regulator-independence statement for
continuum-limit observables in renormalisable lattice gauge theories.

## 5. The structural obstruction

Suppose for the sake of contradiction that there is a regulator-
independent QFT identification

```text
v / M_Pl = (regulator-independent constant) * alpha_LM(a)^{N_species(R)}
                                                  * (7/8)^(1/4)         (*)
```

valid for all standard regulators `R` with continuum limit SM. Take the
`a -> 0` limit on both sides. By §4, the left-hand side converges to the
same physical quantity `v / M_Pl` (continuum SM observable). On the
right-hand side, `alpha_LM(a)` converges to the standard continuum
coupling `alpha_s` at the matching scale, which by Symanzik
regulator-independence is also regulator-independent.

The remaining `N_species`-dependence on the right is therefore the only
regulator-dependent factor in the limit. By §3, `N_species(R)` takes
distinct integer values across regulators (16, 1, 2, 4, 1, 1).
Substituting into (*) yields distinct limits for distinct regulators
unless the framework's prefactor (regulator-independent constant) is
itself regulator-specific in a way that exactly cancels the
`N_species`-variation.

But the framework's hierarchy formula `v = M_Pl * alpha_LM^16 *
(7/8)^(1/4)` has a single, regulator-independent prefactor `M_Pl *
(7/8)^(1/4)`. There is no regulator-specific factor in the framework's
formula that could cancel `N_species` variation across regulators.

Therefore (*) cannot be a regulator-independent QFT identification.
Either:

- **(O1)** the framework's `alpha_LM` is regulator-specific (i.e.,
  `alpha_LM` is defined only on the naive/staggered-Dirac surface), so
  the formula's claim to give a regulator-independent `v/M_Pl` is itself
  substrate-imposed;
- **(O2)** the framework's hierarchy formula is regulator-specific
  (i.e., `v/M_Pl` as defined in the framework is not the continuum SM
  `v/M_Pl` but a lattice ratio on the naive/staggered surface), so the
  identification is substrate-imposed at the observable side;
- **(O3)** the identification "`N_species = hierarchy exponent`" is not
  a regulator-independent QFT theorem and the bridge is regulator-
  DEPENDENT.

All three routes require accepting that the bridge identification is
substrate-imposed (not derivable from lattice-action-uniform QFT
primitives alone). This is the no-go's content.

## 6. Relation to the staggered-Dirac realization gate

The open
[`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
already names "the framework forces the Grassmann staggered-Dirac
realization" as an open gate, not closed by the repo baseline physical
`Cl(3)` local algebra plus `Z^3` spatial substrate alone. This no-go
note is consistent with that gate boundary: under the open gate, the
framework's hierarchy exponent `16` is consistent with the naive /
staggered-Dirac substrate-imposed reading; under any closure of the gate
that produced a regulator-independent identification of `16`, the no-go
above would have to be evaded via one of routes (O1)-(O3) (regulator-
specific `alpha_LM`, regulator-specific `v/M_Pl`, or explicit regulator-
dependence). This note records the obstruction without adjudicating
which route the gate-closure attempt should take.

The no-go therefore **narrows** the open staggered-Dirac realization
gate. Closing that gate to a regulator-independent identification
requires explicit selection of one of (O1), (O2), or (O3), each of which
carries its own gate input.

## 7. Audit-named dependencies

| Authority | Role | Audit status |
|---|---|---|
| `NAIVE_LATTICE_FERMION_TWO_POWER_D_SPECIES_COUNT_NARROW_THEOREM_NOTE_2026-05-10` | parent narrow theorem (naive count `2^d`) | pipeline-owned |
| `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03` | substrate-imposed realisation gate | pipeline-owned |

The naive narrow theorem is cited because the numerical coincidence
`16 = 2^4` originates there; this no-go does **not** modify that
theorem or its claim scope.

The staggered-Dirac realization gate is cited as the canonical existing
gate surface for the framework's regulator choice;
this no-go does **not** close, modify, or promote that gate.

No framework lane is cited as a load-bearing input; the no-go
is a standard lattice-field-theory primitives-only statement.

## 8. Verification

The runner checks:

1. **T1** — the six standard regulators produce three distinct species
   counts at `d=4` (16, 1, 2, 4, 1, 1), with the naive count `16`
   matching the parent narrow theorem and Wilson/overlap/domain-wall
   each giving `1`.
2. **T2** — under the candidate regulator-independent reading of the
   bridge identification, distinct regulators would predict distinct
   `v/M_Pl` values; the predicted Wilson-vs-naive ratio spans ~15
   decades (15 factors of `alpha_LM`), forcing the no-go's bite.
3. **T3** — all six standard regulators target a single continuum limit
   (SM), per Symanzik improvement / Reisz power counting; the bridge's
   regulator-dependence is therefore a structural inconsistency with
   continuum-limit uniqueness.
4. **T4** — the numerical match `naive count = hierarchy exponent = 16`
   at `d=4` is exact (parent narrow theorem). This is the standalone
   coincidence; the no-go only constrains its derivation status.
5. **T5** — at `d != 4`, the naive count is `2^d`, and the bridge would
   substitute distinct hierarchy exponents (`alpha_LM^4`, `alpha_LM^8`,
   `alpha_LM^32`, `alpha_LM^64`) at `d = 2, 3, 5, 6`. The framework's
   `d=4` regulator calculation (three spatial directions plus one
   Euclidean/Matsubara direction) is the
   only sensible reading; the dependency on `d` confirms the bridge
   reads off the regulator-specific corner count, not a regulator-
   independent QFT property.
6. **T6** — regulator-independence formal check: three exhaustive routes
   (O1, O2, O3) around the no-go all require substrate-imposed gate
   inputs.
7. **T7** — source-note boundary: required keywords present, no
   promotion leakage.

Expected runner result: `PASS=12`, `FAIL=0`.

## 9. Independent audit handoff

```yaml
proposed_claim_type: no_go
proposed_claim_scope: |
  At the level of standard lattice-field-theory primitives applied
  uniformly to all renormalisable lattice fermion regulators on the
  four-direction regulator surface with continuum limit SM, the
  identification "physical species count
  N_species(d=4) = exponent in v = M_Pl * alpha_LM^16 * (7/8)^(1/4)"
  is regulator-dependent. Wilson, twisted-mass, staggered, domain-wall,
  and overlap regulators produce species counts {1, 2, 4, 1, 1}
  distinct from the naive 16, while all six share the same continuum
  limit by Symanzik improvement. The exponent 16 cannot be derived
  from regulator-independent QFT primitives alone; the bridge holds
  only on the substrate-imposed naive/staggered surface and remains
  consistent with the open staggered-Dirac realization gate.

proposed_load_bearing_step_class: B
status_authority: independent audit lane only

declared_one_hop_deps:
  - naive_lattice_fermion_two_power_d_species_count_narrow_theorem_note_2026-05-10
  - staggered_dirac_realization_gate_note_2026-05-03

admitted_context_inputs:
  - standard textbook species counts for Wilson, twisted-mass,
    staggered (Kawamoto-Smit), domain-wall, overlap (citations in §3)
  - Symanzik improvement / Reisz power counting for regulator-
    independence of continuum-limit observables (citations in §4)
  - the numerical coincidence 16 = 2^4 at d=4 between naive species
    count and hierarchy exponent

forbidden_imports_used: false
proposal_allowed: true
audit_required_before_effective_status_change: true
```

## 10. Counterfactual Pass record (audit transparency)

Per `feedback_run_counterfactual_before_compute`, the assumptions in
this no-go were exercised before authoring:

1. **"The framework's hierarchy formula `v = M_Pl * alpha_LM^16 *
   (7/8)^(1/4)` is regulator-independent on the lattice surface"** —
   negated: distinct regulators on `Z^4` produce distinct species counts
   (T1). The framework's choice of `16` is consistent only with the
   naive/staggered substrate.

2. **"Wilson, twisted-mass, staggered, domain-wall, overlap all reduce
   to a single species in the continuum"** — verified for `N_species`
   readouts: Wilson 1, overlap 1, domain-wall 1, twisted-mass 2,
   staggered 4 (pre-rooting). Symanzik / Reisz guarantee they all reach
   the same SM continuum. The no-go's bite is on the regulator-specific
   identification, not on the regulator-independent continuum limit.

3. **"The integer 16 can be derived from a regulator-independent
   topological invariant of `Z^4`"** — negated: the BZ-corner count of
   `Z^d` is `2^d` at `d=4`, but it is a property of the **naive**
   lattice action only. Wilson, twisted-mass, staggered, domain-wall,
   overlap all have different actions and different physical species
   counts. The `2^d` count belongs to one specific operator, not to a
   regulator-independent feature of `Z^4`.

4. **"The bridge `16 = hierarchy exponent` can be promoted to a
   theorem by closing the staggered-Dirac realization gate"** —
   negated as a sufficient route: closing the gate would force the
   substrate selection (gate input O1 or O2 in §5), but would not by
   itself remove the regulator-dependence of the identification (still
   O1/O2/O3). The honest outcome under any gate closure is that the
   substrate selection itself is the substrate-imposed input, and the
   hierarchy formula reads `16` because the substrate selects the naive
   regulator, not because `16` is a regulator-independent QFT integer.

The counterfactual exercise confirmed the no-go as a class B structural
result on the regulator-independence question, with gate inputs (O1, O2,
O3) enumerated exhaustively.

## 11. External references

- H. B. Nielsen and M. Ninomiya, "Absence of neutrinos on a lattice
  (I): Proof by homotopy theory", Nucl. Phys. B 185 (1981) 20-40;
  "(II): Intuitive topological proof", Nucl. Phys. B 193 (1981) 173-194.
- L. H. Karsten and J. Smit, "Lattice fermions: species doubling,
  chiral invariance and the triangle anomaly", Nucl. Phys. B 183 (1981)
  103-140.
- K. G. Wilson, "Confinement of Quarks", in "New Phenomena in
  Subnuclear Physics" (1977).
- R. Frezzotti and G. C. Rossi, "Chirally improving Wilson fermions",
  JHEP 04 (2004) 070, [arXiv:hep-lat/0306014](https://arxiv.org/abs/hep-lat/0306014).
- N. Kawamoto and J. Smit, "Effective Lagrangian and dynamical symmetry
  breaking in strongly coupled lattice QCD", Nucl. Phys. B 192 (1981)
  100-124.
- D. B. Kaplan, "A method for simulating chiral fermions on the
  lattice", Phys. Lett. B 288 (1992) 342, [arXiv:hep-lat/9206013](https://arxiv.org/abs/hep-lat/9206013).
- H. Neuberger, "Exactly massless quarks on the lattice", Phys. Lett. B
  417 (1998) 141, [arXiv:hep-lat/9707022](https://arxiv.org/abs/hep-lat/9707022).
- K. Symanzik, "Continuum limit and improved action in lattice theories.
  1. Principles and phi^4 theory", Nucl. Phys. B 226 (1983) 187-204.
- T. Reisz, "A power-counting theorem for Feynman integrals on the
  lattice", Commun. Math. Phys. 116 (1988) 81-126.
- M. Lüscher, "Selected topics in lattice field theory", in 'Fields,
  Strings and Critical Phenomena', Proc. Les Houches Summer School
  1988, eds. E. Brézin and J. Zinn-Justin (North-Holland 1990).
- S. R. Sharpe, "Rooted staggered fermions: good, bad or ugly?",
  PoS LAT2006 (2007) 022, [arXiv:hep-lat/0610094](https://arxiv.org/abs/hep-lat/0610094).
- C. Bernard et al., "Status of staggered simulations", PoS LAT2007
  (2007) 090.
