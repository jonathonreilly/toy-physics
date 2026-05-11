# SU(3) Wilson Plaquette Closed-Form Fan-Out at β = 6

**Date:** 2026-05-04
**Claim type:** bounded_theorem
**Status:** bounded support theorem — closed-form fan-out, unaudited.
**Primary runner:** `scripts/frontier_su3_wilson_closed_form_fanout_2026_05_04.py`
**Predecessor:** `docs/SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md` (PR #501)

## 0. Headline

Per physics-loop deep-work / stuck-fan-out guidance, this note runs **4 orthogonal
closed-form attack frames** for `<P>(β=6)` on standard SU(3) Wilson primitives.
The point is to record the bounded fan-out result so that future work does
not reopen these four paths blindly. **The MC reference value 0.5934 and
the `epsilon_witness = 3.03e-4` target are external comparator-only inputs
to this note**; they are not derived here and the note's bounded scope
does not depend on them being audit-clean.

### Honest narrowing 2026-05-10

The original framing said the comparison "rules out" the four closed-form
methods. That phrasing is comparator-conditional: the only structural
content of this note that does not depend on the imported MC value is the
quartet of derived numbers `(M1, M2, M4, M5) = (0.4225, 0.3333, 0.8740, 0.9259)`,
each computed from framework-allowed primitives. The "ruling out at
`epsilon_witness`" reading is conditional on the comparator and is no
stronger than the comparator's own provenance. This note is therefore
narrowed to:

- a bounded record of the four closed-form numerical values at `β = 6`
  (these are framework-internal and do not depend on imported data); and
- a bounded comparator note that, if `<P>_MC(β=6) = 0.5934` is taken as
  given, then the four methods are far-misses at the `epsilon_witness`
  scale.

The bounded record is internal to the framework. The comparator note
inherits the provenance of its inputs and is not promoted as a standalone
ruling-out theorem.

| Method | `<P>(β=6)` | gap to MC | gap / ε_witness |
|---|---:|---:|---:|
| M1: single-plaquette character (Haar) | 0.4225 | 0.171 | 564× |
| M2: strong-coupling leading β/(2N²) | 0.3333 | 0.260 | 858× |
| M4: mean-field self-consistency | 0.8740 | 0.281 | 926× |
| M5: weak-coupling 1-loop | 0.9259 | 0.333 | 1097× |
| **MC reference (canonical)** | **0.5934** | 0 | 0× |

All 4 closed-form estimates are **far-misses** (gap ≥ 0.05). β=6 is the SU(3) crossover regime: strong-coupling estimates undershoot (M1, M2), weak-coupling estimates overshoot (M4, M5), and the MC value 0.5934 sits between them. No single-plaquette / leading-perturbative method captures the connected multi-plaquette structure that drives `<P>` to ~0.59.

**Verdict:** among the tested simple closed-form attacks, none closes
the plaquette value. The L_s ≥ 3 Wigner-Racah engine remains the next
exact-cube route rather than an already completed closure.

## 1. Methods

### 1.1 M1 — single-plaquette character expansion

```text
<P>_1plaq = (1/N) Re[c_(1,0)(β) / c_(0,0)(β)]
         = c_(1,0)(6) / (3 c_(0,0)(6))
         = 0.422532
```

Exact one-plaquette-in-isolation Haar-integrated Wilson observable. Uses the framework's `wilson_character_coefficient` routine (Bessel-determinant). The single-plaquette character expansion sums to all orders in the one-plaquette Haar measure; what it misses is **inter-plaquette correlation**.

This value 0.4225 matches the framework's existing `P_triv` reference (`rho = delta`) reported in `docs/GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md` and `docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md` — which is the same single-plaquette structure under a different framework alias.

### 1.2 M2 — strong-coupling leading order

```text
<P>_SC1 = β / (2 N²) = 6 / 18 = 0.333333
```

Universal first-order strong-coupling formula for SU(N) Wilson lattice. Strict leading-order; ignores all corrections.

### 1.3 M3 — single-plaquette all-order strong coupling

Same as M1. The single-plaquette character expansion is the all-order strong-coupling result restricted to the one-plaquette Haar measure. A genuine 2nd-order improvement would require enumerating connected small-loop Wilson contributions (2×1, 1×2, etc.), beyond this fan-out's scope.

### 1.4 M4 — single-plaquette mean-field self-consistency (Drouffe-Itzykson)

```text
<P>_MF = (1/N) c_(1,0)(β_eff) / c_(0,0)(β_eff),
β_eff  = z β <P>_MF,    z = 6 (3+1D coordination).
```

Fixed-point iteration converges in 12 steps to:

```text
<P>_MF = 0.874049.
```

The mean-field self-consistency adds the coordination effect of `z = 6` neighboring plaquettes per link, promoting `β_eff` from the bare `β = 6` to `β_eff = 6 · 6 · 0.87 = 31.5`, deep into the weak-coupling regime where the single-plaquette character ratio saturates near 1. **M4 overshoots**: mean-field is too aggressive at β = 6 (the crossover regime).

### 1.5 M5 — weak-coupling 1-loop

```text
<P>_WC = 1 - (N²-1)/(8 N²) · 4/β
       = 1 - 4/54
       = 0.925926.
```

Standard 4D Wilson lattice perturbation theory at one loop. **M5 overshoots**: weak coupling is not yet asymptotic at β = 6.

## 2. Theorem statement

**Bounded numerical statement (closed-form fan-out at β = 6).** The runner
`scripts/frontier_su3_wilson_closed_form_fanout_2026_05_04.py` evaluates
four standard closed-form approximations for the SU(3) Wilson plaquette
expectation value at β = 6:

(a) M1 (single-plaquette character expansion): `<P>_1plaq = 0.4225`;
(b) M2 (strong-coupling leading order): `<P>_SC1 = 0.3333`;
(c) M4 (mean-field self-consistency, z = 6): `<P>_MF = 0.8740`;
(d) M5 (weak-coupling 1-loop): `<P>_WC = 0.9259`.

**Bounded comparator (conditional on imported `<P>_MC = 0.5934` and
`epsilon_witness = 3.03e-4`).** Under the comparator-only assumption
that the canonical lattice MC value at β = 6 is 0.5934, all 4 estimates
have gaps to MC of ≥ 0.05 (≥ 564× ε_witness). The "ruling-out at
ε_witness" reading is conditional on this comparator; the note does not
derive the MC value or the ε_witness target.

**Proof sketch (numerical part).** Each method is a closed-form
evaluation on framework-allowed primitives (Bessel-determinant
character coefficients for M1, M3, M4; pure SU(N) algebra for M2, M5).
Numerical evaluation gives the four numbers above. The gap-to-MC values
are computed by the runner from the imported comparator. The bounded
internal content is the quartet `(0.4225, 0.3333, 0.8740, 0.9259)`; the
comparator wing is conditional. ∎

## 3. Interpretation

β = 6 sits in the **SU(3) crossover regime**: it is the boundary where the correlation length ξ exceeds 2 lattice spacings (so L_s = 2 PBC fails, per the SU(3) Wigner L_s=2 orientation verdict, legacy Block 5) and where neither strong-coupling expansion (M1, M2) nor weak-coupling perturbation (M5) is a good asymptotic. Mean-field (M4) sits awkwardly between because its self-consistent β_eff jumps deep into weak coupling.

The MC value 0.5934 is **sandwiched** between strong-coupling estimates (0.33, 0.42) and weak-coupling estimates (0.87, 0.93). Closing this gap requires the full **connected multi-plaquette tensor-network structure** that:

- L_s = 2 PBC cannot host (SU(3) Wigner L_s=2 orientation verdict, legacy Block 5);
- No single-plaquette closed form captures (this Block);
- Only the L_s ≥ 3 Wigner-Racah engine (Blocks 1-4) is engineered to compute.

This is consistent with the gauge-scalar bridge no-go theorem
(`GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`;
contextual reference, not a load-bearing dependency): the current
Wilson-framework primitive stack does not derive `<P>(β=6)`. To escape
the no-go, additional independently audited primitives such as the
L_s ≥ 3 cube Wigner-Racah Perron data would be needed.

## 4. Scope

### 4.1 In scope

- 4 closed-form Wilson plaquette estimates at β = 6 (M1, M2, M4, M5).
- Comparison to canonical MC reference and ε_witness.
- Strengthened verdict that L_s ≥ 3 Wigner-Racah work is the next
  exact-cube route after these simpler frames fail.

### 4.2 Out of scope

- Genuine 2nd-order strong-coupling improvement (needs enumeration of connected small-loop contributions).
- Higher-loop weak-coupling perturbation (needs 2-loop, 3-loop coefficients with proper resummation).
- Bootstrap, holography, exact-renormalization-group, or other multi-week analytic methods.
- Closure of the gauge-scalar bridge.

### 4.3 Not making the following claims

- Does NOT promote the gauge-scalar bridge parent theorem.
- Does NOT claim 0.5934 as derived from framework primitives.
- Does NOT use forbidden imports: MC reference is comparator only, not derivation input.
- Does NOT claim a free-standing "ruling-out" theorem at `epsilon_witness`.
  The ruling-out language is comparator-conditional and inherits the
  provenance of `<P>_MC = 0.5934` and `epsilon_witness = 3.03e-4`. The
  bounded internal content of this note is the four derived numbers
  `(0.4225, 0.3333, 0.8740, 0.9259)`.

## 5. Audit queue seed (review-only)

The independent audit lane owns verdict and effective-status authority.
This block only gives the seeder the intended claim boundary.

```yaml
claim_id: su3_wilson_closed_form_fanout_theorem_note_2026-05-04
note_path: docs/SU3_WILSON_CLOSED_FORM_FANOUT_THEOREM_NOTE_2026-05-04.md
runner_path: scripts/frontier_su3_wilson_closed_form_fanout_2026_05_04.py
claim_type: bounded_theorem
deps:
  - su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03  # PR #501
  - gauge_scalar_temporal_observable_bridge_no_go_theorem_note_2026-05-03
review_scope: |
  Bounded internal record of 4 closed-form Wilson <P>(beta=6)
  estimates. M1 (single-plaq char) = 0.4225, M2 (SC leading) = 0.3333,
  M4 (mean-field) = 0.8740, M5 (WC 1-loop) = 0.9259; MC = 0.5934.
  The gap-to-MC reading is comparator-conditional on the imported MC
  value and epsilon_witness target.

  Provides bounded support adjacent to the SU(3) Wigner intertwiner
  L_s=2 PBC orientation verdict (legacy Block 5) without changing that
  parent verdict.

  Does not promote bridge parent chain. Does not claim MC value as
  derived. No forbidden imports (numpy + scipy.special only; MC
  comparator is reported, not used as derivation input).
```

## 6. Cross-references

- SU(3) Wigner intertwiner L_s=2 PBC orientation verdict (legacy Block 5):
  [`SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md)
  (PR #501).
- Bridge no-go:
  [`GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`](GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md).
- Framework `P_triv` reference (= M1 here under different alias):
  [`GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md),
  [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md).

## 7. Command

```bash
python3 scripts/frontier_su3_wilson_closed_form_fanout_2026_05_04.py
```

Expected summary:

```text
SUMMARY: THEOREM PASS=4 SUPPORT=1 FAIL=0
```
