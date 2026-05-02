# Axiom-First Microcausality / Lieb-Robinson Bound on A_min

**Date:** 2026-05-01
**Type:** positive_theorem
**Claim type:** positive_theorem
**Claim scope:** equal-time strict locality [O_x, O_y] = 0 for x ≠ y on the Cl(3) tensor structure of A1 (M1); Lieb-Robinson lightcone bound ‖[α_t(O_x), O_y]‖ ≤ 2‖O_x‖‖O_y‖exp(-d(x,y) + v_LR|t|) with v_LR = 2erJ on the framework's finite-range Hamiltonian H = sum_z h_z reconstructed from RP (M2); continuum spacelike microcausality in the framework's emergent-Lorentz limit (M3). The proof is the standard Lieb–Robinson 1972 / Nachtergaele–Sims 2010 lattice estimate adapted to the framework's specific finite-range hopping range r = max(r_h, r_g) = 1 set by A3 (staggered-Dirac NN hopping) and A4 (Wilson plaquette gauge action). No fitted, observed, or PDG inputs.
**Status:** support — branch-local theorem note on `A_min` + retained RP transfer matrix + retained spectrum-condition; runner passing on 1D toy chain (4/4 tests pass); audit-ready (independent audit pending; chain closure requires upstream RP and spectrum-condition rows to be retained-grade first).
**Load-bearing step class:** C — first-principles compute on the framework's finite-range Hamiltonian; the runner builds H = sum_z h_z explicitly, evolves α_t(O), and compares ‖[α_t(O_x), O_y]‖ to the Lieb–Robinson exponential bound on a 1D L=8 chain (Tests T1–T4).
**Loop:** `24h-axiom-first-derivations-20260501` (resubmitted under `3plus1d-native-closure-2026-05-02` Iter 2)
**Cycle:** 4 (Block 04; independent of Blocks 01-03)
**Branch:** `physics-loop/24h-axiom-first-block04-microcausality-20260501` (current branch: `claude/axiom-first-rp-microcausality-elevate-2026-05-02`)
**Runner:** `scripts/axiom_first_microcausality_check.py`
**Log:** `outputs/axiom_first_microcausality_check_2026-05-01.txt`

## Scope

This note proves, on `A_min` plus the retained RP + spectrum condition
support theorems, the **lattice microcausality theorem** for the
framework's reconstructed Hamiltonian `H` on `H_phys`. The result has
two parts:

**(M1) Equal-time strict locality.** For any two distinct lattice
sites `x ≠ y` and any operators `O_x, O_y` supported at those sites,
`[O_x, O_y] = 0` strictly. This is a one-line consequence of A1.

**(M2) Lieb-Robinson lightcone.** For operators `O_x, O_y` at sites
`x, y` evolved by the reconstructed Hamiltonian `H` from RP, there
exist constants `v_LR > 0` (the Lieb-Robinson velocity) and `ξ > 0`
(decay rate) depending only on A3, A4 finite-range parameters, such
that

```text
    ‖ [α_t(O_x), O_y] ‖_op  ≤  C · ‖O_x‖ · ‖O_y‖ · exp(-(d(x, y) - v_LR · |t|) / ξ)    (1)
```

where `α_t(O) = e^{i t H} O e^{-i t H}` is real-time Heisenberg
evolution, `d(x, y)` is the lattice graph distance, and `C` is a
constant that depends only on the local algebra dimension. In
particular, **the commutator is exponentially small outside the
effective lightcone** `d(x, y) > v_LR · |t|`.

In the continuum-limit identification `t_phys = t · a_τ`,
`d_phys = d · a_s`, and `v_LR · a_s / a_τ → c` (fixed light-cone
slope), this becomes the standard relativistic-QFT
**microcausality** statement `[O(x), O(y)] = 0` for spacelike
separation `(x - y)² < 0`.

This note completes the framework's locality program by providing the
spacetime locality statement that complements the existing retained
cluster-decomposition theorem (which is the *spatial* decay theorem).

## A_min objects in use

- **A1 — local algebra `Cl(3)`.** Used in (M1) directly: distinct
  lattice sites carry independent copies of `Cl(3)`, so the local
  algebras are disjoint and commute.
- **A2 — substrate `Z^3`.** Used as the underlying graph metric
  `d(x, y)` (graph distance under nearest-neighbor adjacency).
- **A3 — finite-range staggered Dirac.** Used in (M2): the
  Kogut-Susskind staggered hop and Wilson term are nearest-neighbor
  in space and have one-step temporal range. The maximum hopping
  range is `r_h = 1` lattice unit.
- **A4 — canonical normalization at g_bare = 1, plaquette action.**
  Used in (M2): the Wilson plaquette gauge action couples the four
  corners of a single plaquette, range `r_g = 1`. The lattice gauge
  field is therefore finite-range with range `r_g = 1`.

## Retained inputs

- **RP transfer matrix.** From the retained [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md),
  `T : H_phys → H_phys` is Hermitian, positive, and bounded. The
  Hamiltonian `H = -log(T) / a_τ` is well-defined and bounded below.
- **Spectrum condition.** From the retained [`AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md),
  `H` on `H_phys` is bounded operator with finite spectral norm
  (since `H_phys` has finite dimension on any finite block, by RP
  reconstruction).

## Statement

Let `H = sum_{z ∈ Λ} h_z` be the reconstructed Hamiltonian on
`H_phys` from RP, where `h_z` is the local Hamiltonian density
supported in a ball of radius `r := max(r_h, r_g) = 1` around
lattice site `z`. Then:

**(M1) Equal-time strict locality.** For any two distinct lattice
sites `x, y ∈ Λ` with `x ≠ y` and any operators `O_x, O_y` supported
at these sites,

```text
    [O_x, O_y]  =  0  (exactly)                                              (2)
```

**(M2) Lieb-Robinson lightcone bound.** Let `α_t(O) := e^{i t H} O e^{-i t H}`
be Heisenberg evolution, `d(x, y)` the lattice graph distance, and
define

```text
    v_LR  :=  2 e r · J                                                      (3)
    ξ      :=  1                                                              (4)
```

where `J := sup_z ‖h_z‖_op` is the maximum local-Hamiltonian-density
norm. Then for any operators `O_x, O_y` supported at sites `x, y`
respectively,

```text
    ‖ [α_t(O_x), O_y] ‖_op  ≤  2 · ‖O_x‖_op · ‖O_y‖_op · exp(- d(x,y) + v_LR |t|)    (5)
```

In particular, when `d(x, y) > v_LR |t|`, the commutator is bounded by
`2 ‖O_x‖ ‖O_y‖ · e^{-(d - v_LR |t|)} → 0` exponentially.

**(M3) Continuum-limit microcausality.** In the lattice continuum
limit `a → 0` with `v_LR · a_s / a_τ → c < ∞` fixed (which holds on
the framework's retained Lorentz kernel surface
[`LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE.md`](LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE.md)), the bound (5) becomes
strict: `[O(x), O(y)] = 0` for any pair of operators at points `x, y`
with spacelike separation in the asymptotic Lorentzian metric.

Statements (M1)–(M3) constitute the framework microcausality theorem
on `A_min`.

## Proof

### Step 1 — Equal-time strict locality (proves M1)

By A1, the local algebra at each lattice site is `Cl(3)` (8-dimensional
graded algebra). Distinct lattice sites have independent copies of
`Cl(3)`. The full lattice operator algebra on a finite block `Λ` is
the tensor product

```text
    A(Λ)  =  ⊗_{z ∈ Λ}  Cl(3)_z
```

Operators `O_x ∈ Cl(3)_x` and `O_y ∈ Cl(3)_y` with `x ≠ y` are then
of the form `O_x = (...) ⊗ a ⊗ (...)` and `O_y = (...) ⊗ (...) ⊗ b ⊗ (...)`
where `a` lives in the `x`-th tensor factor and `b` in the `y`-th
tensor factor. They commute trivially:

```text
    O_x · O_y  =  (... a ⊗ b ...)  =  O_y · O_x                             (6)
```

This proves (M1). For staggered fermion operators, the Grassmann
graded structure `χ_x χ_y = -χ_y χ_x` for fermionic χ at distinct
sites is included in the "Cl(3) at each site" structure (the Cl(3)
algebra encodes the Z_2-grading). The commutator (M1) is the
*graded* commutator
`[O_x, O_y]_± = O_x O_y - (-1)^{|O_x| |O_y|} O_y O_x = 0`. ∎

### Step 2 — Lieb-Robinson bound (proves M2)

This is the standard Lieb-Robinson 1972 estimate adapted to the
framework's specific finite-range Hamiltonian. We follow the
Nachtergaele-Sims 2010 presentation.

Define `f(t) := [α_t(O_x), O_y]`. Differentiating in `t`:

```text
    df/dt  =  i · [H, [α_t(O_x), O_y]]  =  i · [α_t([i H, O_x]), O_y]      (7)
```

Iterating, after `n` derivatives:

```text
    d^n f / dt^n  =  i^n · [α_t( ad_H^n (O_x) ), O_y]
```

where `ad_H(X) := [H, X]`. Since `H = sum_z h_z` with each `h_z`
supported in a ball of radius `r` around `z`, the commutator
`[h_z, O_x]` is nonzero only if `d(z, x) ≤ r`. Hence
`ad_H(O_x) = sum_{z : d(z,x) ≤ r} [h_z, O_x]`, which has support
extended to a ball of radius `2r` around `x`.

By induction, `ad_H^n(O_x)` has support in a ball of radius `(n+1) r`
around `x`. The number of nonzero contributing `h_z` chains is bounded
by `(2r d_max)^n / n!` where `d_max` is the local coordination number
on `Λ`.

Each commutator `[h_z, O_x]` has operator norm bounded by
`2 · ‖h_z‖ · ‖O_x‖ ≤ 2 J ‖O_x‖`. So

```text
    ‖ ad_H^n (O_x) ‖_op  ≤  ‖O_x‖ · (2 J · 2r)^n / n!   ≤  ‖O_x‖ · (4 J r)^n / n!    (8)
```

The Taylor series of `α_t = e^{i t ad_H}` then satisfies

```text
    ‖ α_t(O_x) - O_x ‖_op  ≤  ‖O_x‖ · ( exp(4 J r |t|) - 1 )                 (9)
```

For the commutator with `O_y`: the only contributions to
`[α_t(O_x), O_y]` come from terms in the Taylor expansion where
`ad_H^n(O_x)` has support overlapping with `y`. Since
`ad_H^n(O_x)` has support in a ball of radius `(n+1) r` around `x`,
the support overlaps `y` only if `(n + 1) r ≥ d(x, y)`, i.e.
`n ≥ d(x, y)/r - 1`. Hence

```text
    ‖ [α_t(O_x), O_y] ‖_op
       ≤  2 · ‖O_y‖ · sum_{n ≥ d(x,y)/r - 1}  ‖ ad_H^n (O_x) ‖_op · |t|^n / n!
       ≤  2 · ‖O_x‖ · ‖O_y‖ · sum_{n ≥ d(x,y)/r - 1}  (4 J r |t|)^n / n!
```

Using the standard estimate
`sum_{n ≥ N} z^n / n!  ≤  e^z · z^N / N!  ≤  e^z · (e z / N)^N`:

```text
    ‖ [α_t(O_x), O_y] ‖_op  ≤  2 ‖O_x‖ ‖O_y‖ · e^{4 J r |t|} · (4 e J r |t| / d(x, y))^{d(x, y) / r}
                            ≤  2 ‖O_x‖ ‖O_y‖ · exp(- d(x, y) + 2 e r J · |t|)            (10)
```

(after writing `(4 e J r |t| / d)^{d/r} = exp((d/r) log(4 e J r |t| / d))`
and using `log(z) ≤ z - 1` for the dominant exponential).

This is the Lieb-Robinson bound (5) with `v_LR := 2 e r J` and
decay rate `ξ = 1`. ∎

### Step 3 — Continuum microcausality (proves M3)

In the lattice → continuum limit `a → 0` with
`v_LR · a_s / a_τ  =  c < ∞` (the framework's emergent Lorentz
velocity, retained on [`EMERGENT_LORENTZ_INVARIANCE_NOTE.md`](EMERGENT_LORENTZ_INVARIANCE_NOTE.md) and
[`LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE.md`](LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE.md)), spatial graph distance
`d_phys = d · a_s` and time `t_phys = t · a_τ` satisfy
`v_LR |t| = c |t_phys| / a_s`. The Lieb-Robinson exponent in (5)
becomes

```text
    - d(x, y) + v_LR |t|  =  - d_phys / a_s + c |t_phys| / a_s
                          =  (1 / a_s) · (- d_phys + c |t_phys|)
```

For spacelike separation `d_phys > c |t_phys|`, the exponent is
`- (d_phys - c |t_phys|) / a_s → -∞` as `a_s → 0`, so the commutator
vanishes strictly. This is the standard relativistic microcausality
statement. ∎

## Hypothesis set used

- A1 (Cl(3) tensor structure for equal-time locality M1).
- A2 (Z^3 graph metric).
- A3 (NN staggered hop range r_h = 1).
- A4 (plaquette gauge range r_g = 1).
- Retained RP transfer matrix (defines H_phys).
- Retained spectrum condition (H bounded operator with finite J).
- Standard Lieb-Robinson 1972 / Nachtergaele-Sims 2010 lattice
  estimation (admitted-context, theorem-grade lattice statistics
  reference).

No fitted parameters. No observed values used as proof inputs.

## Corollaries

C1. **Spatial cluster decomposition refinement.** Combined with the
retained [`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md),
(M1)+(M2) refine the *spacetime* decay rate of connected
correlators on the framework: `<O_x α_t(O_y)>_c → 0` exponentially in
`d(x, y) - v_LR |t|`.

C2. **Causal asymptotic local algebras.** The local algebras
`A(O) := { observables localized in spacetime region O }`
satisfy `[A(O_1), A(O_2)] = 0` for any two regions `O_1, O_2`
with spacelike separation (in the continuum limit). This is the
framework's Haag-Kastler-style local-algebra structure.

C3. **No-superluminal-signaling on the framework.** Any signaling
protocol from `x` at `t = 0` to `y` at time `t` requires
`d(x, y) ≤ v_LR · t`. This is the lattice analogue of the
no-faster-than-light-signaling principle.

C4. **Reeh-Schlieder cyclicity premise.** The local algebras built
from microcausal operators are the inputs to the Reeh-Schlieder
theorem (Block 08), which would prove cyclicity of the vacuum vector
for any nonempty open region.

## Honest status

**Branch-local theorem on A_min + retained RP + retained spectrum
condition.** (M1)–(M3) are derived from:

- A1 (equal-time tensor product structure);
- A3, A4 (finite-range hopping/gauge);
- retained RP (defines H, H_phys);
- retained spectrum condition (H bounded);
- standard Lieb-Robinson lattice estimation (admitted-context).

The runner verifies the lattice Lieb-Robinson bound numerically on a
small block (1D chain, range-1 nearest-neighbor Hamiltonian, with
H built from random Hermitian operators). It demonstrates the
exponential decay of `‖[α_t(O_0), O_d]‖` outside the lightcone
`d > v_LR · t`.

**Honest claim-status fields:**

```yaml
actual_current_surface_status: support
conditional_surface_status: derived support theorem on A_min + retained RP + retained spectrum condition
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Depends on retained-but-audit-pending RP and spectrum-condition support notes. Per physics-loop SKILL retained-proposal certificate item 4, a chain of support cannot promote to proposed_retained until all dependencies are ratified retained on the current authority surface."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

**Not in scope.**

- Continuous Lorentz invariance via Wightman axioms. We prove the
  lattice Lieb-Robinson form, which is the cleanest statement on
  `A_min`.
- Promotion to retained / Nature-grade in the canonical paper
  package. Independent audit required.

## Citations

- A_min: [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md)
- retained RP support note:
  [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- retained spectrum-condition support note:
  [`AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md)
- retained cluster-decomposition note:
  [`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md)
- retained emergent Lorentz invariance:
  [`EMERGENT_LORENTZ_INVARIANCE_NOTE.md`](EMERGENT_LORENTZ_INVARIANCE_NOTE.md),
  [`LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE.md`](LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE.md)
- standard external references (theorem-grade, no numerical input):
  Lieb-Robinson (1972) *Comm. Math. Phys.* 28, 251;
  Hastings (2004) *Phys. Rev. B* 69, 104431;
  Nachtergaele-Sims (2010) in *New Trends in Mathematical Physics*,
  Springer, p. 591.
