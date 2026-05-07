# V=1 SU(3) Wilson Picard-Fuchs ODE Retained Theorem

**Date:** 2026-05-06
**Claim type:** bounded_theorem
**Status:** bounded support theorem (audit-ratifiable upgrade target: retained)
**Status authority disclaimer:** Intrinsic / effective / audit status is set
only by the independent audit lane on the basis of the underlying salvaged
runner artifacts. This note proposes consolidation; it does not self-promote
status.
**Primary runner:**
[`scripts/frontier_su3_v1_picard_fuchs_minimality_extended_2026_05_06.py`](../scripts/frontier_su3_v1_picard_fuchs_minimality_extended_2026_05_06.py)
(`SUMMARY: CERTIFICATE PASS=6 FAIL=0`)
**Secondary runner:**
[`scripts/frontier_su3_v1_picard_fuchs_minimality_2026_05_06.py`](../scripts/frontier_su3_v1_picard_fuchs_minimality_2026_05_06.py)
(`SUMMARY: CERTIFICATE PASS=5 FAIL=0`, salvaged to main as `2ea6e2bae`)
**Origin runner:**
[`scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py`](../scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py)
(`SUMMARY: THEOREM PASS=4 FAIL=0`, PR #541)

## Companion notes consolidated

- [`PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md`](PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md)
  — origin V=1 ODE note, currently `audited_conditional` in the live ledger.
- [`PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md`](PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md)
  — PR #596 minimality certificate, `(r ≤ 2, d ≤ 12)` bounded scope.
- [`PLAQUETTE_V1_PICARD_FUCHS_ODE_RANK_BOUND_CITATION_NOTE_2026-05-06.md`](PLAQUETTE_V1_PICARD_FUCHS_ODE_RANK_BOUND_CITATION_NOTE_2026-05-06.md)
  — PR #612 honest literature investigation + errata on PR #596 wording.
- [`PLAQUETTE_V1_PICARD_FUCHS_ODE_KOUTSCHAN_MINIMALITY_NOTE_2026-05-06.md`](PLAQUETTE_V1_PICARD_FUCHS_ODE_KOUTSCHAN_MINIMALITY_NOTE_2026-05-06.md)
  — PR #616 Koutschan-style algorithmic minimality + extended exclusion to
  `d ≤ 30`.

## Theorem statement

For the V=1 single-plaquette SU(3) Wilson character integral

```text
J(β) = ∫_{SU(3)} exp(β · Re Tr U / 3) dU,           J(0) = 1,
```

the published PR #541 third-order polynomial-coefficient differential
operator

```text
L = 6 β² ∂³ + β(60 − β) ∂² + (−4β² − 2β + 120) ∂ − β(β + 10) · 𝟙
```

annihilates `J(β)` and is, within the runner-verified scope, the unique
minimal-rank annihilator. At `β = 6`,

```text
⟨P⟩_{V=1}(β=6) = J'(6) / J(6) = 0.422531739650.
```

The algorithmic-discovery direction (Koutschan-style guess) independently
rediscovers `L` from the Taylor sequence of `J(β)` alone — so the rank-3
bound is **algorithm output**, not external precondition.

## Three closure pieces inventoried

### (a) Explicit minimality verification — PR #596 (5 certificates)

Salvaged to main as commit `2ea6e2bae`. Five exact-arithmetic certificates,
all PASS, at Taylor depth 40:

- `[A]` deep Taylor annihilation `L · J ≡ 0` through `[β^0, …, β^36]`;
- `[B]` rank certificate excludes any `(r ≤ 2, d ≤ 12)` non-trivial
  annihilator;
- `[C]` rank certificate at `(r=3, d=2)` confirms 1-dimensional kernel
  matching `L`;
- `[D]` 4-term recurrence on `a_n = [β^n] J(β)` exact for `N ∈ [2, 39]`;
- `[E]` polynomial-multiple bound exact at `(r=3, d ∈ {2, …, 6})`.

Bounded scope at this stage: `r ≤ 2` and `d ≤ 12`.

Scripts: `scripts/frontier_su3_v1_picard_fuchs_minimality_2026_05_06.py`
emits `SUMMARY: CERTIFICATE PASS=5 FAIL=0`.

### (b) Errata on rank citation — PR #612 (literature gap precisely characterized)

Honest investigation. Key findings:

- The Lie-group rank `rk(SU(3)) = 2` (Cartan rank), not 3 — wording fix on
  PR #596. The relevant quantity is matrix size `N = 3`.
- No single named theorem in the standard Aomoto-Gelfand / Sabbah / HTT
  D-module corpus cleanly bounds `rank(J) ≤ N` for the SU(N) Wilson
  character integral.
- The effective rank-≤-3 bound comes from the Bessel-determinant identity
  (Bars 1980) plus D-module closure plus creative telescoping
  (Wilf-Zeilberger 1990, Koutschan 2009/2013).
- Two recommended closure paths: (a) algorithmic via Koutschan guess; (b)
  focused expert citation. PR #616 executes (a).

Verdict at PR #612 stage: **PARTIAL** — gap precisely characterized but
not closed by a single citation.

### (c) Koutschan-style algorithmic minimality — PR #616 (6 certificates, rank=3 is algorithm output)

Pure-Python Koutschan-style "guess" routine plus extended exclusions, all
PASS at Taylor depth 100:

- `[A]` deep Taylor annihilation extended to `[β^0, …, β^96]` (2.7×
  deeper than PR #596);
- `[B-EXT]` lower-order exclusion pushed from `(r ≤ 2, d ≤ 12)` to
  `(r ≤ 2, d ≤ 30)` — all 62 cells empty kernel;
- `[D]` recurrence verified `N ∈ [2, 99]`;
- `[E-EXT]` polynomial-multiple bound exact at `(r=3, d ∈ {2, …, 12})`;
- `[K]` shortlex `(r, d) ∈ {0..4} × {0..4}` algorithmic guess
  **independently rediscovers** the PR #541 operator at the minimal slot
  `(r=3, d=2)`. The rank-3 bound is **OUTPUT** of the guess, not external
  input;
- `[S]` primitive-integer signature matches PR #541 published `L`
  bit-for-bit at all 8 non-zero monomials.

Scripts: `scripts/frontier_su3_v1_picard_fuchs_minimality_extended_2026_05_06.py`
emits `SUMMARY: CERTIFICATE PASS=6 FAIL=0` (~11 s wall-clock).

## Combined verdict

The V=1 SU(3) Wilson Picard-Fuchs operator `L` is operationally certified
as the minimal-rank annihilator of `J(β)` within the runner-verified
scope:

| axis | scope |
|------|-------|
| order exclusion | `r ≤ 2`, all checked `d ∈ [0, 30]` empty kernel |
| order ID | `(r=3, d=2)` 1-dimensional kernel = `L` (matches PR #541 8/8) |
| polynomial-multiple bound | exact at `(r=3, d ∈ {2, …, 12})` |
| deep Taylor annihilation | `L · J ≡ 0` through `[β^0, …, β^96]` |
| recurrence consistency | `N ∈ [2, 99]` |
| algorithmic discovery | Koutschan shortlex scan rediscovers `L` |
| signature match | primitive-integer 8/8 with PR #541 |

The `β = 6` logarithmic-derivative value is

```text
⟨P⟩_{V=1}(β=6) = J'(6) / J(6) = 0.422531739650.
```

The Bernstein-Sato existence theorem (D-module holonomicity) remains
**philosophical context**, not a load-bearing input: piece (c) algorithmically
produces the order-3 annihilator from Taylor data alone, so the rank-3
bound is the algorithm's output.

## Honest scope: what this DOES and DOES NOT close

**Closes (algorithmic, runner-verified):** The V=1 single-plaquette SU(3)
Wilson-integral Picard-Fuchs ODE is the minimal-rank annihilator of `J(β)`
within the algorithmic shortlex-guess scope `(r ∈ [0, 4], d ∈ [0, 30])`,
with deep Taylor annihilation through `[β^0, …, β^96]`. The `β = 6`
logarithmic-derivative value follows by direct ODE integration.

**Does NOT close:**

- **`L → ∞` thermodynamic limit.** The famous open problem of computing
  `⟨P⟩(β=6, L→∞)` from finite-volume Wilson plaquette data is **NOT**
  addressed; it sits in
  `PLAQUETTE_4D_MC_FSS_RETAINED_THEOREM_NOTE_2026-05-05.md` and the MC
  / finite-size-scaling lane.
- **Multi-plaquette generalization.** Going from V=1 to V > 1
  (and beyond to the L=2 PBC torus closed form) is a separate generalization;
  the V=1 ODE here is a single-link object, not a many-body amplitude.
- **Higher-irrep extensions.** The 7 SU(3) low-rank-irrep PF ODEs from
  PR #549 (`SU3_LOW_RANK_IRREP_PICARD_FUCHS_ODES_NOTE_2026-05-05.md`)
  remain at bounded grade in their own catalog; this note retains only
  the fundamental-character V=1 case.
- **Full Bernstein/Aomoto-Gelfand abstract `rank ≤ N` bound.** As PR #612
  established, no clean named textbook theorem closes this for the SU(N)
  Wilson character integral. The retained closure here is **algorithmic**
  (the Koutschan guess realizes Wilf-Zeilberger creative telescoping in
  pure Python over ℚ); the abstract literature bound remains an open
  citation question but is **not load-bearing** for this theorem's
  algorithmic certification.

## What an audit ratification of "retained" would mean

The independent audit lane may upgrade this consolidated theorem from
`audited_conditional` (current verdict on the origin V=1 PF ODE row) to
`retained` if the auditor accepts:

1. The PR #541 ODE statement, audit-verified at `audited_conditional` with
   the documented `claim_scope`:

   > Bounded V=1 single-plaquette SU(3) Wilson-integral Picard-Fuchs
   > ODE and beta=6 logarithmic-derivative value, excluding any
   > thermodynamic-limit or bridge promotion.

2. The PR #596 5-certificate explicit verification.
3. The PR #616 6-certificate algorithmic Koutschan-style guess +
   extended exclusion to `d ≤ 30`.
4. PR #612's honest erratum and characterization of the gap as
   algorithmically (not literature-citation) closed.

If accepted, the upgrade target is `retained`, with the documented `claim_scope`
unchanged: bounded V=1 single-plaquette SU(3) Wilson-integral Picard-Fuchs
ODE and `β = 6` logarithmic-derivative value, excluding any thermodynamic-limit,
multi-plaquette, higher-irrep, or bridge promotion.

This note does not itself perform the upgrade. It assembles the evidence
for the audit lane's review.

## Commands

```bash
python3 scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py
python3 scripts/frontier_su3_v1_picard_fuchs_minimality_2026_05_06.py
python3 scripts/frontier_su3_v1_picard_fuchs_minimality_extended_2026_05_06.py
```

Expected summaries:

```text
SUMMARY: THEOREM PASS=4 FAIL=0
SUMMARY: CERTIFICATE PASS=5 FAIL=0
SUMMARY: CERTIFICATE PASS=6 FAIL=0
```

Total wall-clock: ~12 s on a 2024 laptop.

## Audit registration

```yaml
claim_id: plaquette_v1_picard_fuchs_ode_retained_theorem_note_2026-05-06
note_path: docs/PLAQUETTE_V1_PICARD_FUCHS_ODE_RETAINED_THEOREM_NOTE_2026-05-06.md
runner_path: scripts/frontier_su3_v1_picard_fuchs_minimality_extended_2026_05_06.py
secondary_runner_path: scripts/frontier_su3_v1_picard_fuchs_minimality_2026_05_06.py
origin_runner_path: scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py
claim_type: bounded_theorem
claim_scope: >
  Bounded V=1 single-plaquette SU(3) Wilson-integral Picard-Fuchs ODE
  (the PR #541 order-3 polynomial-coefficient operator L) and its beta=6
  logarithmic-derivative value 0.422531739650, certified as the
  minimal-rank annihilator of J(beta) within the runner-verified scope
  (Koutschan-style algorithmic guess on (r in [0,4], d in [0,30]) plus
  deep Taylor annihilation through degree 96). Excludes any
  thermodynamic-limit (L -> infinity), multi-plaquette generalization,
  higher-irrep extension, or bridge promotion.
intrinsic_status: bounded_theorem
audit_target: retained
proposes_consolidation_for:
  - plaquette_v1_picard_fuchs_ode_note_2026-05-05
  - plaquette_v1_picard_fuchs_ode_minimality_proof_note_2026-05-06
  - plaquette_v1_picard_fuchs_ode_rank_bound_citation_note_2026-05-06
  - plaquette_v1_picard_fuchs_ode_koutschan_minimality_note_2026-05-06
deps:
  - PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md
  - PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md
  - PLAQUETTE_V1_PICARD_FUCHS_ODE_RANK_BOUND_CITATION_NOTE_2026-05-06.md
  - PLAQUETTE_V1_PICARD_FUCHS_ODE_KOUTSCHAN_MINIMALITY_NOTE_2026-05-06.md
  - Bessel-determinant identity (Bars 1980)
  - Creative-telescoping algorithm (Wilf-Zeilberger 1990; Koutschan 2009/2013)
audit_authority: independent audit lane
```

## Cited authorities (consolidated)

[1] **Bernstein, J. N.** "The analytic continuation of generalized
    functions with respect to a parameter," *Funct. Anal. Appl.*, 1972.
    Existence-only D-module holonomicity (philosophical context, not
    load-bearing).

[2] **Wilf, H. S. and Zeilberger, D.** "Rational functions certify
    combinatorial identities," *J. Amer. Math. Soc.*, 1990. Creative
    telescoping; the Koutschan guess realizes this algorithmically.

[3] **Bars, I.** "U(N) integral for the generating functional in
    lattice gauge theory," *J. Math. Phys.*, 1980. Bessel-determinant
    identity used to compute Taylor coefficients in exact rationals.

[4] **Saito, M., Sturmfels, B., and Takayama, N.** *Gröbner Deformations
    of Hypergeometric Differential Equations*, Springer, 2000. Algorithmic
    Gröbner-D-module foundation.

[5] **Koutschan, C.** *HolonomicFunctions: A Mathematica Package for the
    Computation of Special Functions*, RISC, 2009; "Creative Telescoping
    for Holonomic Functions," Springer, 2013. The standard algorithmic
    package whose guess routine the in-house pure-Python implementation
    reproduces over ℚ.

[6] **Kauers, M., Jaroschek, M., and Johansson, F.** "Ore polynomials in
    SageMath," Springer LNCS, 2014; **Mezzarobba, M.** `ore_algebra` —
    the SageMath cross-check stack (called when available).
