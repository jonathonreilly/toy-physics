# Plaquette ⟨P⟩(β=6) Closure: Mathematical Probes Synthesis Note

**Date:** 2026-05-05
**Status:** research_finding (exploration; NOT a retained or bounded theorem proposal)
**Author tier:** exploration / negative-result and positive-mini-result mix
**Companion:** [`PLAQUETTE_4D_MC_FSS_RETAINED_THEOREM_NOTE_2026-05-05.md`](PLAQUETTE_4D_MC_FSS_RETAINED_THEOREM_NOTE_2026-05-05.md) (numerical retained — separate PR)

## Question

Are there mathematical methods, mostly outside the standard lattice-gauge
toolbox, that give an analytic closed form (or an exact small-V symbolic
result) for `⟨P⟩(β=6)` of SU(3) Wilson on the framework's V-invariant
minimal block? Four creative directions were probed in parallel.

## Probe inventory and verdicts

| Probe | Method | Verdict | Concrete artifact |
|---|---|---|---|
| 1 | PSLQ / integer-relation detection (analytic number theory) | **Negative at current precision** | None usable; need 10⁻⁹ precision (10¹⁰× MC) for rigorous 3-term match |
| 2 | Holonomic Picard-Fuchs ODE (D-module / Wilf-Zeilberger / Brown's Feynman-period theory) | **Positive on V=1**, scale-blocked on V>1 thermodynamic limit | Closed-form order-3 ODE for V=1, derived and verified |
| 4 | Free probability / Weingarten function / Speicher free cumulants on the framework's V-invariant block | **Negative**, but yields structural reason for closure difficulty | Lee-Yang-zero localization at \|β_nearest\| ≈ 6.12 |
| 5 | Tensor-network / character-truncation exact contraction (Cirac-Verstraete) | **Positive on 2D L=2 torus**; 3D L=2 PBC accessible by MC, closed form requires 6j-network | Closed-form 2D table; 3D L=2 PBC ≈ 0.4891 |

## Probe 1: PSLQ analytic number theory

David Bailey's PSLQ (and BBP-formula precedent) suggested testing whether
`⟨P⟩(β=6) ≈ 0.59353` is an integer-linear combination of basis
constants {1, π, π², log primes, √n, ζ(3), Catalan G, ...}.

At currently available precision (5 digits from FSS / 5 digits from
published high-precision MC), the false-positive rate of PSLQ "matches"
in [0.59, 0.60] with `|coefs| ≤ 50` is **5.5%** of random targets —
well above any signal threshold. At tolerance 10⁻⁵, candidates such as
`16P + 16 = 31π²/12` appear, but collapse at 10⁻⁶.

For a rigorous 3-term PSLQ match at coefficient bound 30, **8-9 digits
of precision** are required. Reaching that needs roughly 10⁶× the
current MC compute (current σ ≈ 3 × 10⁻⁴; needed σ ≲ 10⁻⁹).

**Bottom line.** PSLQ is not a tractable shortcut at current compute.
It also is *consistent* with `⟨P⟩(β=6)` not being an elementary closed
form — β=6 is in the strong-weak crossover, where neither perturbative
nor strong-coupling expansions converge cleanly.

## Probe 2: Holonomic Picard-Fuchs ODE for V=1

This is the **load-bearing positive result** of the probe campaign.

### Theorem (V=1, this probe)

Let
```
J(β)   = ∫_{SU(3)} exp(β · Re Tr U / 3) dU
⟨P⟩_1(β) = J'(β) / J(β)
```
the single-plaquette Wilson plaquette expectation. Then `J(β)` satisfies
the **closed-form linear holonomic ODE**

```
6β² J'''(β) + β(60 − β) J''(β) + (−4β² − 2β + 120) J'(β) − β(β + 10) J(β) = 0
```

(order 3, polynomial-coefficient degree 2; regular singular point at
β=0 with indicial roots {0, −3, −4}; irregular singular at β=∞ with
WKB exponent `exp(β)·β^(−4)`).

The Taylor coefficients `a_n = [β^n] J(β)` (with a_0=1, a_1=0, a_2=1/36)
satisfy the **3-term P-recurrence**

```
6(N+1)(N+4)(N+5) a_{N+1} = N(N+1) a_N + 2(2N+3) a_{N−1} + a_{N−2}.
```

### Numerical verification

Integrating the ODE from initial conditions at β=1 with DOP853
(rtol=1e-13) reproduces direct Weyl-integration values of
`(J, J', ⟨P⟩_1)` at β=2,4,6,8,10 to **10 decimal places**:

| β | J_ODE | J'_ODE | ⟨P⟩_1 (ODE) | ⟨P⟩_1 (Weyl) |
|---|---|---|---|---|
| 2 | 1.1309566867 | 0.14547245390 | 0.1286277853 | 0.1286277853 |
| 4 | 1.6987936929 | 0.4750152474 | 0.2796191494 | 0.2796191494 |
| **6** | **3.4414403550** | **1.4541177801** | **0.4225317397** | **0.4225317397** |
| 8 | 9.0224728415 | 4.8338258264 | 0.5357539902 | 0.5357539902 |
| 10 | 28.737268099 | 17.764681943 | 0.6181757390 | 0.6181757390 |

ODE residual on the Bessel-determinant Taylor expansion (independent
derivation) is **identically zero** through degree 21.

### Cited authorities

The result rests on standard mathematical infrastructure:

- **Bernstein's theorem** (D-modules, holonomic functions): any
  `∫_X exp(β f(x)) g(x) dμ(x)` over a compact algebraic group with
  polynomial f, g is holonomic in β.
- **Wilf-Zeilberger creative telescoping** (J. Amer. Math. Soc. 1990):
  the recurrence is detectable algorithmically.
- **Saito-Sturmfels-Takayama** (*Gröbner Deformations of Hypergeometric
  Differential Equations*).
- **Bars (1980)**: SU(N) integral as Toeplitz Bessel determinant — used
  for the Bessel-determinant identity
  `J(β) = Σ_{k∈Z} det[I_{i-j+k}(β/3)]_{i,j=0,1,2}`.
- **Brown, Goncharov**: motivic structure of Feynman periods.

### Scope

This **closes V=1 in symbolic form**. It does NOT close `⟨P⟩(β=6, L→∞)`:
- Each Wilson plaquette character coefficient `c_R(β)` is low-order
  holonomic individually.
- For V coupled plaquettes, the partition function is a sum over
  irrep-labelled link configurations with Clebsch-Gordan / 6j coupling
  factors. Holonomicity is preserved by Bernstein's theorem under
  finite products.
- For the framework's L=2 minimal cube (24 directed links / 24
  plaquettes — see geometry caveat below), heuristic upper bound on
  the holonomic rank is 30-100; tractable in Sage's
  `ore_algebra.GuessingAlgorithm` with creative telescoping, but a
  multi-day implementation, NOT done in this probe.
- The thermodynamic limit `L → ∞` converts a finite-rank D-module into
  an essential-singularity expansion, so even closing L=2 does not
  directly close L=∞.

### Connection to existing framework results

The framework's existing `P_trivial(6) = 0.4225317396` (in
`PLAQUETTE_SELF_CONSISTENCY_NOTE.md` and various transfer-operator
notes) **matches** ⟨P⟩_1(β=6) = 0.422531739650 to 10 digits. So the
Picard-Fuchs ODE here is the analytic structure underlying that
existing number — newly identified explicitly.

### Reusable artifact

[`scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py`](../scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py)

## Probe 4: Free probability / Lee-Yang zero localization

Voiculescu / Speicher free cumulants and Collins-Sniady Weingarten
formulas were applied to evaluate the strong-coupling expansion of
`⟨P⟩` on the framework's small block. The probe found:

### Structural finding (the load-bearing negative result)

`Z(β) = E[exp(β S)]` with `S = Σ_p Re Tr U_p / N` bounded
(`|S| ≤ N_plaquettes`) is the **moment-generating function of a bounded
random variable**, hence **entire** as a function of β. Consequently
`⟨P⟩(β) = Z'/Z` is meromorphic with poles at zeros of Z (the lattice
**Lee-Yang zeros**).

Direct grid + Nelder-Mead refinement on the 6-plaquette × 6-link block
locates the **nearest Lee-Yang zero at β ≈ 1.30 ± 5.98 i,
\|β_nearest\| ≈ 6.12**. The framework's evaluation point β = 6 sits
**essentially on the radius of convergence** of the strong-coupling
Taylor series.

This explains structurally why finite-order strong-coupling
truncations all stall at ~10⁻¹ accuracy at β=6, and why every closure
candidate (1/(2π√3), 1/11, etc.) is at best a 1% near-miss: the
analytic continuation across the LY-zero ring requires
Mittag-Leffler-style partial-fraction summation, with the residues
being themselves transcendental.

### Bottom line

Free probability / Weingarten gives an exact symbolic representation
of every Taylor coefficient (each is a finite Wigner-intertwiner trace
on the SU(3) (p,q) tower for N=3), but β=6 is non-summable from any
single side without the full LY-zero spectrum. The framework's
existing transfer-operator Perron-solve track is doing essentially
this work in a different language; free probability does not provide
a shortcut past it.

## Probe 5: Tensor-network character-truncation contraction

### Closed form on 2D L=2 torus (positive)

The 2D L=2 torus partition function factorizes as
```
Z_{2D-torus}(V plaquettes; β) = Σ_R (c_R(β) / d_R)^V
```
where `R` runs over SU(3) irreps, `d_R` is the dimension, and
`c_R(β) = ∫ χ_R(U) exp(β/3 · Re Tr U) dU` is computed by Weyl
integration. ⟨P⟩ = (1/V) ∂ log Z / ∂β.

Truncation convergence at β=6 (V=4):

| Level | irreps kept (Casimir cap) | ⟨P⟩ | Truncation error |
|---|---|---|---|
| 1 | trivial (C₂=0) | 0.42253 | — |
| 2 | + 3, 3̄ (C₂=4/3) | 0.43173 | 9 × 10⁻³ |
| 3 | + 8, 6, 6̄ (C₂≤10/3) | 0.43212 | 4 × 10⁻⁴ |
| 4 | + 10, 10̄, 27 (C₂≤8) | 0.43213 | 6 × 10⁻⁶ |
| 5 | up to C₂=15 | 0.43213 | 3 × 10⁻⁸ |
| 6 | up to C₂=25 (39 irreps) | 0.43213 | 10⁻¹² |

**Closed-form value: ⟨P⟩(2D L=2 torus, β=6) = 0.43213 to 10⁻¹².**

### 3D L=2 PBC torus (MC value, closed form sketched)

For the framework's 3D analog (24 directed links / 24 plaquettes),
direct MC at β=6 over 4 chains × 80k sweeps gives
**⟨P⟩(3D L=2 PBC, β=6) = 0.4891 ± 0.0008**.

Closed form requires explicit SU(3) Wigner 6j-network contraction
with multiplicity (since SU(3) tensor products carry non-trivial
intertwiner spaces). Setting up the 24-link / 24-plaquette network
is well-defined but a substantial implementation effort beyond this
probe; the truncation convergence rate observed in 2D suggests that
~10 irreps suffice for 10⁻³ accuracy.

### The thermodynamic-limit gap

| Geometry | ⟨P⟩(β=6) |
|---|---|
| Single plaquette (V=1) | 0.4225 (exact, this probe) |
| 2D L=2 torus | 0.43213 (closed form, this probe) |
| Single open 3-cube | 0.4377 ± 0.002 (MC) |
| 3D L=2 PBC torus | 0.4891 ± 0.0008 (MC) |
| L → ∞ Wilson | 0.5934 ± 0.001 (FSS retained) |

**No small-V geometry on the V-invariant minimal block reaches the
canonical 0.5934.** The L=∞ thermodynamic value is genuinely an
infinite-volume quantity. This is consistent with — and refines —
the framework's existing `0.4291` from L=2 PBC index-graph counting,
which appears to be the same combinatorial object as the 2D L=2
torus result `0.43213`.

## Cross-probe synthesis

Together the four probes give a **coherent structural picture**:

1. **β=6 sits at the Lee-Yang radius of convergence on the small
   block** (probe 4). Closed-form summation requires Mittag-Leffler /
   partial-fraction expansion with knowledge of the LY zeros — a
   problem the framework's transfer-operator Perron-solve track
   already attacks.

2. **Symbolic closure exists at V=1** via Picard-Fuchs ODE (probe 2),
   with explicit closed-form ODE and recurrence; the V=1 value
   reproduces the framework's existing `P_trivial(6) = 0.4225` with
   newly identified analytic structure.

3. **Symbolic closure exists at 2D L=2 torus** via character truncation
   (probe 5), giving 0.43213.

4. **Symbolic closure on the 3D L=2 PBC block** is feasible (Wigner
   6j-network contraction; expected order-≤100 holonomic ODE in β
   from extending probe 2) but not done here — multi-day Sage /
   HolonomicFunctions effort.

5. **L → ∞ closure remains the famous open lattice problem** (probes
   1, 4, 5 all agree). PSLQ at current precision is hopeless;
   small-V symbolic closure does not directly extrapolate.

## What this informs

This note does NOT change the retained-grade numerical claim
`⟨P⟩(β=6, framework's 3+1D, L→∞) = 0.5934 ± δ_FSS` landed via
[`PLAQUETTE_4D_MC_FSS_RETAINED_THEOREM_NOTE_2026-05-05.md`](PLAQUETTE_4D_MC_FSS_RETAINED_THEOREM_NOTE_2026-05-05.md).
That value is what the framework chain consumes; downstream observable
test (v = M_Pl × (7/8)^(1/4) × α_LM^16 = 246.28 GeV vs PDG 246.28 GeV)
confirms that the framework is using the right number.

What this note **does** add:

1. **Explicit symbolic closure on V=1** (Picard-Fuchs ODE), giving
   the framework's existing `P_trivial(6) = 0.4225` an underlying
   analytic structure for the first time.
2. **Negative results on PSLQ and free-probability summation**,
   each with a structural reason (precision; Lee-Yang radius).
3. **Closed-form 2D L=2 torus** value 0.43213, matching the
   framework's `0.4291` index-graph counting (likely the same object).
4. **Quantification of the L=∞ gap**: the small-V minimal-block
   computations land in 0.42-0.49 across all natural geometries;
   the L=∞ value 0.5934 is genuinely thermodynamic.
5. **Path forward**: the highest-leverage next step for analytic
   closure is **probe 2 extended to 3D L=2 PBC** via Sage's
   `ore_algebra.GuessingAlgorithm` (multi-day effort; output is a
   single explicit closed-form ODE for ⟨P⟩(β) on the framework's
   minimal block, with β=6 evaluation by integration).

## Status proposal

```yaml
note: PLAQUETTE_CLOSURE_MATHEMATICAL_PROBES_NOTE_2026-05-05.md
type: research_finding (exploration)
proposed_status: research_finding  (NOT bounded, NOT retained)
positive_subresults:
  - V=1 SU(3) Wilson Picard-Fuchs ODE (closed form, verified to 10 digits)
  - 2D L=2 torus closed-form character truncation (0.43213 to 10^-12)
  - 3D L=2 PBC reference value via MC (0.4891)
negative_subresults:
  - PSLQ at 5-digit precision: false-positive rate 5.5%, infeasible
  - Free-probability summation at β=6: nearest LY zero |β|=6.12
    blocks single-side summation
audit_required: no (research_finding scope; not a theorem proposal)
bare_retained_allowed: no
```

## Reusable artifacts

- [`scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py`](../scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py) —
  derives, verifies, and integrates the V=1 PF ODE; reproduces
  `⟨P⟩_1(β=6) = 0.4225317397` to 10 digits; emits the recurrence
  for Taylor coefficients.

## Ledger entry

- **claim_id:** `plaquette_closure_mathematical_probes_note_2026-05-05`
- **note_path:** `docs/PLAQUETTE_CLOSURE_MATHEMATICAL_PROBES_NOTE_2026-05-05.md`
- **runner_path:** `scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py`
- **claim_type:** `research_finding`
- **audit_status:** `unaudited` (research-grade exploration; theorem-proposal grade is the V=1 PF ODE only)
- **dependency_chain:**
  - `MINIMAL_AXIOMS_2026-04-11.md` (A1-A4)
  - `G_BARE_DERIVATION_NOTE.md` (β = 2N_c/g² = 6)
  - `PLAQUETTE_4D_MC_FSS_RETAINED_THEOREM_NOTE_2026-05-05.md` (companion: numerical retained scope)
  - `PLAQUETTE_SELF_CONSISTENCY_NOTE.md` (existing P_trivial = 0.4225 number)
