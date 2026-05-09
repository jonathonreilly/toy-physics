# Light Cone Framing — Lieb-Robinson is Standard Lattice QFT

**Status:** support - structural or confirmatory support note
**Date:** 2026-04-11 (math corrected 2026-05-01; CN LR bridge added 2026-05-09)
**Runners:**
  - `scripts/light_cone_staggered_dispersion.py` (dispersion validation)
  - `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` (Crank-Nicolson LR
    bridge runner — see CN bridge note below)

## The Concern

The Crank-Nicolson evolution gives a Lieb-Robinson cone (97% of probability
inside) rather than a strict v=1 light cone. Is this a blocker?

## The Answer: No

No lattice field theory has a strict v=1 light cone at finite spacing. This
is a well-known feature of lattice discretization. The staggered fermion
formulation used in lattice QCD (Kogut-Susskind, 1975) has exactly the
same Lieb-Robinson bound. The lattice QCD community has produced precise
predictions without a strict continuum light cone at finite spacing.

## The Staggered Dispersion Argument (corrected)

The 1+1d staggered Dirac dispersion in lattice units (a = 1) is:

    E² = m² + sin²(k),    k ∈ (-π, π]

The group velocity is:

    v_g(k, m) = dE/dk = sin(k) cos(k) / E = sin(2k) / (2E)

Maximizing over k at fixed m: setting dv_g/dk = 0 gives the implicit
condition

    sin²(k*) = m·(√(m²+1) − m)

Substituting back yields the closed-form maximum

    **v_max(m) = √(m² + 1) − m**

Limits:
  - **m → 0:** v_max → 1, attained at k* → 0 (the linear-dispersion regime
    near the band minimum, where E ≈ |sin k| ≈ |k| and v_g = cos k → 1).
  - **m → ∞:** v_max → 1/(2m), the heavy-mass non-relativistic limit.

Crucially, v_max(m) ≤ 1 for all m ≥ 0, with equality only in the strict
massless limit. The dispersion is **subluminal** for every nonzero mass —
no superluminal velocities are predicted at finite k or finite m.

This corrects two long-standing typos in earlier drafts of this note,
which (a) reported v_max = 1/(2m) as the m << 1 result (it is the m >> 1
limit), and (b) located the massless maximum at k = π/2, where in fact
cos(k) = 0 and v_g = 0. The runner cited in the header validates the
corrected formula numerically against the dispersion at fine k.

## The Lieb-Robinson Bound

The Lieb-Robinson theorem (Lieb-Robinson 1972) bounds signal propagation
in any local lattice Hamiltonian by an exponentially-suppressed cone

    v_LR ≤ 2 · ‖H_hop‖ · (lattice spacing)

For the staggered hopping with weight w = 1/(2a), this gives v_LR = 1/a in
lattice units, matching v_max(m=0) = 1 above. In the continuum limit
(a → 0, with m·a → 0), the LR cone approaches the strict relativistic
light cone from above. The 97% containment seen at finite lattice spacing
in the Crank-Nicolson evolution is the standard discretization artifact.

### Hamiltonian-side bounded support

The Hamiltonian-side support note
[`MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md`](MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md)
records bounded action-density support and a conservative local
coefficient budget:

    r_action <= 2,    J_action <= |m| + 30  (canonical action-density surface)

This is bounded support for the LR chain, not a retained exact theorem
for the reconstructed logarithmic Hamiltonian `H = -log(T)/a_tau`.

### Crank-Nicolson refinement

The framework's discrete-time evolution uses the **Crank-Nicolson
scheme** (Cayley transform of H):

    U_CN(a_τ)  =  (I − i a_τ H/2) · (I + i a_τ H/2)^{−1}

This is a different operator from the continuous evolution exp(−itH);
they agree only in the continuum limit. The Crank-Nicolson diagnostic
note
[`LIGHT_CONE_CRANK_NICOLSON_LIEB_ROBINSON_BRIDGE_NOTE_2026-05-09.md`](LIGHT_CONE_CRANK_NICOLSON_LIEB_ROBINSON_BRIDGE_NOTE_2026-05-09.md):
checks, on finite nearest-neighbor toy Hamiltonians, the bounded
velocity shape

    v_LR^CN(a_τ)  =  v_LR(H) / (1 − a_τ J / 2)
                  =  v_LR(H) · (1 + a_τ J / 2 + O((a_τ J)²))

with the bound

    ‖[α_t^CN(O_x), O_y]‖_op  ≤  2 ‖O_x‖ ‖O_y‖ · exp(−d(x,y) + v_LR^CN |t|).

The correction factor `1/(1 − a_τ J / 2)` is a bounded diagnostic
read of the Neumann-series resolvent expansion of
`(I + i a_τ H/2)^{−1}`. As `a_τ → 0`, the Crank-Nicolson evolution
converges to the continuous Hamiltonian evolution.

The companion runner
`scripts/light_cone_crank_nicolson_lr_2026_05_09.py` checks (CN-A)
unitarity, (CN-B) per-step Neumann-series decay, (CN-C) the n-step
velocity bound, and (CN-D) the `O(a_τ²)` continuum convergence
(`PASS=5 FAIL=0`).

## What This Architecture Does Provide

1. **Correct continuum dispersion** in the small-k regime: E ≈ √(m² + k²).
2. **Exponential suppression** of acausal signals (Lieb-Robinson bound).
3. **v_max → 1 in the massless limit** from staggered Dirac dispersion.
4. **v_max < 1 for massive particles**, as required by special relativity,
   with the explicit formula v_max(m) = √(m² + 1) − m.

## What It Does NOT Provide (and Why That Is Acceptable)

- **Strict v = 1 at finite lattice spacing** — no lattice FT does this.
- **Exact Lorentz invariance** — broken by the lattice, restored in the
  continuum limit. Standard lattice QFT.
- **Coin-based strict cone** — available but reintroduces a mixing period
  and is not used here.

## Scope and Limits of the Claim

This note is a *framing* note: it confirms that the observed Lieb-Robinson
cone is standard lattice QFT behavior, not an artifact of the framework.
The dispersion-side claim is exact for the 1+1d staggered Dirac operator,
and the runner validates the numeric v_max(m) = √(m²+1) − m to ~1e-8 across
m ∈ [0, 2].

The previously-flagged audit gap — that the note did not derive a
Lieb-Robinson constant from first principles for the specific Crank-
Nicolson operator used elsewhere in the repo — is now narrowed but not
closed:

  - **Hamiltonian-side action support/J budget** is recorded in
    [`MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md`](MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md)
    as bounded support: `r_action <= 2`, `J_action <= |m| + 30`.

  - **Crank-Nicolson-side finite-step behavior** is checked in
    [`LIGHT_CONE_CRANK_NICOLSON_LIEB_ROBINSON_BRIDGE_NOTE_2026-05-09.md`](LIGHT_CONE_CRANK_NICOLSON_LIEB_ROBINSON_BRIDGE_NOTE_2026-05-09.md):
    `v_LR^CN(a_τ) = v_LR(H) / (1 − a_τ J/2)` on tested finite
    nearest-neighbor toy models, with `U_CN^n -> exp(-itH)` as
    `a_τ -> 0`.

The remaining open bridge is an exact finite-range or quasilocal LR
estimate for the framework's reconstructed Hamiltonian and its
Crank-Nicolson kernel. The 97% containment remains evidence consistent
with an LR tail, not a closed theorem-grade identification.

## References

- Rothe, H.J. *Lattice Gauge Theories: An Introduction* (World Scientific).
- Montvay, I. and Münster, G. *Quantum Fields on a Lattice* (Cambridge UP).
- Kogut, J. and Susskind, L. "Hamiltonian formulation of Wilson's lattice
  gauge theories" Phys. Rev. D 11, 395 (1975).
- Lieb, E.H. and Robinson, D.W. "The finite group velocity of quantum
  spin systems" Commun. Math. Phys. 28, 251 (1972).
