# Gravity Sign Audit — Corrected Assessment

**Date:** 2026-04-10
**Revised:** 2026-04-10 (after spot-check verification)
**Audit-status note added:** 2026-05-10

**Purpose:** Determine whether the TOWARD gravity results across all retained harnesses
are genuine physical predictions or tautological consequences of sign conventions.

## Audit-status note (2026-05-10)

The 2026-05-04 audit verdict (`audited_conditional`, `chain_closes=false`)
confirmed that the runner does instantiate Hamiltonians and evolve states,
so it supports the narrow statement that the chosen couplings (parity and
lapse) distinguish well from hill in the configured 1D external-potential
test. The verdict flagged a missing bridge theorem: the load-bearing
identification of the parity / lapse coupling is asserted from the
literature (Zache 2020; Dempsey 2025) and not derived from the repository
axioms inside the audit packet, and the irregular-graph directional
observable scope is honestly admitted as a separate open lane.

> "the load-bearing coupling identification is asserted rather than
> derived from provided inputs ... missing_bridge_theorem: provide a
> restricted retained derivation of the parity/lapse coupling from the
> repository axioms, then separately audit the bounded irregular graph
> directional observable scope."

Admitted-context inputs (carrier framework, not derived in this note):

- the parity coupling `H_diag = (m + Phi) * epsilon(x)` — imported from
  Zache et al. 2020 and Dempsey et al. 2025 as the literature-correct
  staggered-fermion scalar coupling; the algebraic form and the
  per-site distinction from the additive identity coupling is now
  recorded as a one-hop ledger cite-form source-theorem note in
  `STAGGERED_SCALAR_PARITY_LAPSE_COUPLING_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-16.md`
  (paired runner
  `scripts/frontier_staggered_scalar_parity_lapse_coupling_external_narrow.py`,
  18/18 PASS). That source-theorem note carries only the lattice-algebraic
  form of (P) and (L); it does NOT derive the parity coupling from the
  restored framework axiom set (A1 + A2; see
  `MINIMAL_AXIOMS_2026-05-03.md`), and it does NOT close the open
  `staggered_dirac_realization_gate_note_2026-05-03` gate, which is the
  strictly stronger question of whether A1 + A2 forces the staggered
  formulation itself.
- the Hermitian lapse coupling
  `H_grav = sqrt(N) * H_flat * sqrt(N)`, `N = 1 + Phi/m` — imported as
  the full-GR scalar variant, with the lattice-algebraic Hermitian
  symmetrization recorded in the same source-theorem note above
- the screened Poisson `(L + mu^2 I) Phi = G * rho` framework operator,
  and the retarded wave equation with `beta > 0`

Configured probe parameters (proxy thresholds, not derived):

- the configured 1D exact-lattice external-potential test
  (`scripts/frontier_correct_coupling.py`, well `V<0` vs hill `V>0`)
- the configured irregular random-geometric external-source test
  (`scripts/frontier_two_sign_parity.py`)
- the configured endogenous same-surface directional probe
  (`scripts/frontier_irregular_directional_observable.py`),
  reporting `0/9`, `0/9`, `4/9` and recorded as a blocker
- the centered core-packet bounded reopen
  (`scripts/frontier_irregular_sign_core_packet_gate.py`),
  reporting `30/30`, `30/30`, `30/30` at `mu^2=0.1` and `28/30`, `30/30`,
  `28/30` at `mu^2=0.001` — recorded as bounded reopen, not universal closure

Blocked-on: this row stays `audited_conditional` until either a retained
restricted-packet derivation is supplied that fixes the staggered-fermion
parity / lapse scalar coupling from the repository axioms (which is
strictly stronger than the lattice-algebraic source-theorem cite-bridge
landed on 2026-05-16 in
`STAGGERED_SCALAR_PARITY_LAPSE_COUPLING_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-16.md`,
and which would require closing the open
`staggered_dirac_realization_gate_note_2026-05-03` gate end-to-end), or
the irregular-graph directional observable lane lands a graph-native
sign-selective observable that closes the universal-portability gap on
families beyond the audited centered core-packet surface. The bounded
computational diagnostic — under the parity and lapse couplings, the
configured exact-lattice external-potential test splits well from hill,
the canonical exact-force staggered card stays `17/17`, and the centered
core-packet probe recovers a same-surface separator on the audited
families — is unaffected by this status note.

The 2026-04-25 Planck Pin retained closure provides an independent
restricted-packet derivation of `c_cell = 1/4` from a discrete
Wald-Noether charge on the framework's retained discrete GR action; that
closure handles the BH coefficient and `G_Newton,lat = 1` boundary, but
does not by itself fix the staggered-fermion scalar coupling sign on
load-bearing irregular families and so does not retire this row's
blocker.

## Executive Summary

The old identity coupling `H_diag = m·ε − m·Φ` was physically wrong for the
staggered scalar channel. It treated `Φ` as a plain diagonal energy shift and
is exactly why the earlier two-sign comparison could leave the irregular graph
sign rows inward under both coupling signs.

The literature-correct scalar coupling is the **parity coupling**
`H_diag = (m + Φ)·ε(x)`. A Hermitian lapse-style coupling is also possible via
`H_grav = √N · H_flat · √N`, `N = 1 + Φ/m`.

Direct sign tests now split cleanly:
- under the corrected parity and lapse couplings, well vs hill are
  distinguishable in the exact-lattice external-potential test
- the canonical exact-force staggered card survives unchanged at `17/17`
- graph portability (`7/7`), self-gravity (`5/5`), the rerun-corrected wave
  coupling (`4/5`, `5/5`, `4/5`), and the layered DAG-derived control (`6/6`)
  all survive numerically under the parity rewrite
- the cycle battery now closes `9/9` on all three retained cycle-bearing
  families
- the scaled sibling now closes `9/9` on all nine retained larger-size runs
- the retarded family-closure sibling now closes `9/9`, `9/9`, `9/9`, `8/9`
- the endogenous same-surface directional probe failed (`0/9`, `0/9`, `4/9`)
- later bounded follow-ups on current `main` recover:
  - a retained weak-coupling sign-sensitive regime on the audited irregular
    family/size/seed surface
  - a bounded centered core-packet same-surface sign separator across the
    audited irregular families at both `mu^2 = 0.1` and `mu^2 = 0.001`

So the sign story is reopened, but not fully closed:
- the old two-sign comparison is now a **negative control** that invalidates the
  identity coupling
- the corrected coupling restores sign-sensitivity in direct well/hill tests
- irregular self-generated graph batteries still need portability beyond the
  new bounded centered-packet surface; one universally frozen graph-native
  directional observable across broader packet/transport surfaces is still not
  in hand

## Observable Hierarchy

| Observable | Definition | Status |
|-----------|------------|--------|
| **Exact lattice force** F = −Σ ρ·dV/dx | Exact expectation on regular lattice | Cleanest. Used in `frontier_staggered_17card.py` |
| **Edge-radial force** | Σ edges w·(Φⱼ−Φᵢ)·ρᵢ·cos(θ) | Exact per-edge, radial projection | Stronger proxy for irregular graphs |
| **Probability-weighted shell force** | Σ_shells P_shell · ΔΦ/Δd | Stronger radial proxy | Audit cross-check / recommended irregular-graph gate |
| **Shell-mean force** | Σ_shells ⟨ρ⟩_shell · ΔΦ/Δd | Weaker proxy; shell size enters explicitly | Current implementation in cycle/self-gravity/retarded batteries |
| **Centroid** | d⟨x⟩/dt | Broken on staggered lattices (period-4) | Not usable |

**Standard going forward:**
- Regular lattices: use exact F = −⟨dV/dx⟩
- Irregular graphs: require BOTH probability-weighted shell force AND edge-radial
  force to agree in sign before claiming gravity direction
- Treat shell-mean and centroid as diagnostics only

## The Sign Chain

### Link 1: Field Equation → Positive Φ

The screened Poisson `(L + μ²I)Φ = G·ρ` with positive-definite operator and
ρ = |ψ|² ≥ 0 necessarily gives Φ ≥ 0. This is mathematical, not a physics choice.
The retarded wave equation with β > 0 likewise drives Φ positive.

### Link 2: Hamiltonian Coupling (THE CRITICAL CORRECTION)

The earlier retained graph harnesses used the identity coupling

```python
H.setdiag(mass * parity - mass * phi)
```

That is not the correct scalar coupling for staggered fermions.

The literature-correct scalar channel is:

```python
H.setdiag((mass + phi) * parity)
```

and the Hermitian lapse-style variant is:

```python
H_grav = sqrt_lapse @ H_flat @ sqrt_lapse
```

with `sqrt_lapse = sqrt(1 + Φ/m)`.

### Link 3: Force Measurement

**17card (exact):** F = −⟨dV/dx⟩ on the lattice coordinates. Clean, unambiguous.

**Graph batteries (proxy):** Shell-mean radial gradient from BFS-depth shell
averages of `Φ` and `ρ`. This is a radial proxy — shell volume enters the
averaging. It should be described as "radial force proxy" rather than "exact
force."

### What the Corrected Coupling Buys

Given the corrected parity coupling, the direct well/hill sign test is no
longer tautological. The non-trivial content is now:

1. **The exact-lattice directional response survives** — the `17-card` stays `17/17`
2. **The sign test becomes dynamical** — well vs hill split under parity/lapse
3. **Self-gravity contracts much more strongly** — width ratios now land well below `1`
   across all retained scaling families
4. **Portability survives** — the `7/7` graph-portability probe still closes
5. **Some irregular batteries now fail honestly** — layered-cycle linearity and
   growing-family retarded stability are real post-rewrite misses

## Direct Sign Tests

### Exact Lattice External-Potential Test

`frontier_correct_coupling.py` now gives:

| Coupling | Well (V<0) | Hill (V>0) | Distinguishes? |
|----------|-----------|-----------|----------------|
| identity | TOWARD | TOWARD | NO |
| parity | TOWARD | AWAY | YES |
| lapse | TOWARD | AWAY | YES |

### Irregular Random-Geometric External-Source Test

`frontier_two_sign_parity.py` shows the corrected parity coupling also flips
the shell-force sign when the external source is inverted:

| External field | Parity-coupled shell sign |
|----------------|---------------------------|
| `Φ > 0` | TOWARD |
| `Φ < 0` | AWAY |

This is enough to say the old identity-coupling sign audit no longer governs
the retained stack.

### Endogenous Same-Surface Directional Probe

`frontier_irregular_directional_observable.py` and
`IRREGULAR_DIRECTIONAL_OBSERVABLE_NOTE_2026-04-11.md` try to distinguish
attractive from repulsive coupling on the same irregular graph families using
dynamical observables rather than shell-profile positivity.

| Metric | Sign-separated parity-vs-identity cases |
|--------|-----------------------------------------|
| `Δ<depth>` | `0/9` |
| signed cut flux | `0/9` |
| frontier current bias | `4/9` |

**Verdict:** blocker. The endogenous same-surface observable does not yet
provide a frozen sign-selective irregular-graph direction claim.

### Later Bounded Same-Surface Reopen

`frontier_irregular_sign_core_packet_gate.py` and
`IRREGULAR_SIGN_CORE_PACKET_GATE_NOTE.md` later recover a narrower bounded
same-surface separator by switching to a centered non-oscillating core packet
and auditing both `mu^2 = 0.1` and `mu^2 = 0.001`:

| Screening | ball1 positive | ball2 positive | depth positive | min fraction |
|-----------|----------------|----------------|----------------|--------------|
| `mu^2=0.1` | `30/30` | `30/30` | `30/30` | `100%` |
| `mu^2=0.001` | `28/30` | `30/30` | `28/30` | `93.3%` |

**Verdict:** bounded reopen, not universal closure. The centered core-packet
surface is now a real same-surface irregular sign separator on the audited
families, but the older off-center / transport-style blocker still explains
why the lane remains scoped narrowly.

## Emergent Geometry — Corrected

The v2 emergent geometry script plus the new G sweep now report:

| Measure | Value | Sign |
|---------|-------|------|
| `G=100` audit | robust TOWARD | narrow high-`G` window |
| shell_mean | −1.94e-3 | AWAY |
| shell_prob | −3.30e-2 | AWAY |
| edge_radial | +3.52e-3 | TOWARD |

**Verdict:** partial reopen only. The old one-number "AWAY" readout was
overclaimed, and the new sweep only opens a narrow high-`G` window rather than
a retained closure. Do not promote the emergent-geometry gravity sign story
until it passes the two-metric gate across seeds and sizes.

## What IS Genuinely Non-Trivial

| Test | What it shows | Why non-trivial |
|------|---------------|-----------------|
| Norm conservation ~1e-15 | CN is exactly unitary | Numerical correctness |
| Self-gravity contraction | Width shrinks under self-gravity | Magnitude is non-trivial |
| Iterative stability (20/20) | Backreaction loop converges | Could blow up; it doesn't |
| G_eff = 0.4–0.6 | Retarded field coupling strength | Quantitative, not sign-dependent |
| Multi-measure sign agreement | Shell and edge-radial agree on admissible families | Cross-validates proxy, but not sign-selective |
| Critical exponent β | Topology-dependent onset | Phase transition existence is real |
| Gauge current J(A) | Persistent current on graph cycles | Unrelated to gravity sign |
| Born rule I₃ | Three-slit interference | Unrelated to gravity sign |
| Lieb-Robinson cone | 97% inside | Unrelated to gravity sign |
| d_eff = 2.03 | Growth rule makes 2D geometry | Genuine geometric result |

## What Would Strengthen the Gravity Story

### Option A: Derive the Coupling Sign ← PARTIALLY CLOSED

The literature (Zache et al. 2020, Dempsey et al. 2025) shows that a scalar
potential in the staggered Hamiltonian must couple through the SAME parity
factor ε(x) as the mass (both are 1⊗1 in spin-taste):

    CORRECT:  H_diag = (m + Φ) · ε(x)      ("parity coupling")
    WRONG:    H_diag = m·ε ± m·Φ            ("identity coupling" — all current scripts)

The full GR coupling via the lapse function gives:

    H_grav = √N · H_flat · √N,   N = 1 + Φ/m   ("lapse coupling")

**Result: Both correct couplings distinguish well from hill in the direct sign test.**

| Coupling | Well (V<0) | Hill (V>0) | Distinguishes? |
|----------|-----------|-----------|----------------|
| identity (current) | TOWARD +0.61 | TOWARD +0.48 | NO |
| parity (correct) | TOWARD +2.08 | AWAY −0.78 | YES |
| lapse (full GR) | TOWARD +0.61 | AWAY −1.78 | YES |

Under parity coupling, `V<0` narrows the mass gap locally and `V>0` widens it.
That is enough to make the direct external sign test dynamical rather than
conventional.

What is **not** closed yet is the final irregular-graph claim:
the retained shell/edge-radial graph observables are still proxy measures, and
the self-generated graph field story has not yet been reduced to one exact,
graph-native directional observable. The endogenous same-surface probe is the
current blocker, not the exact-cubic sign test.

**Script:** `frontier_correct_coupling.py`

**Action completed in part:** the retained stack is being rewritten around the
parity coupling; the canonical card, portability, self-gravity, rerun-corrected
wave note, and layered DAG-derived control
probes survive, while some cycle/retarded rows now fail honestly.

### Option B: Sign-Agnostic Observables
Reframe around contraction magnitude, binding energy, correlation length —
compare to GR quantitatively without invoking force direction.
**Status:** Partially done (G_eff), not systematically framed.

### Option C: Two-Sign Comparison ← DONE
Run both `−mass·Φ` and `+mass·Φ` through the full battery. If repulsive coupling
is pathological (divergent norm, unstable backreaction), that selects the sign.

**Result: BOTH SIGNS ARE COMPLETELY STABLE.**
- Norm drift: identical (machine epsilon)
- Width: both expand comparably (no contraction under either sign at G=50, N=20)
- Φ convergence: both stable
- Energy: bounded under both (attractive E<0, repulsive E>0 — just the diagonal shift)
- Spectral range: comparable
- **Force sign: BOTH give TOWARD on all three measures.**

The last point is the most damning: even repulsive coupling gives positive
shell/edge-radial force. The force observables are measuring the Φ profile
shape (positive, peaked at source), not the wavepacket's dynamical response
to the potential. The shell force `Σ ρ·∇Φ` is always positive because Φ
is always positive and peaked inward — regardless of whether Φ enters the
Hamiltonian with + or − sign.

**Conclusion:** Consistency does NOT select the coupling sign at these parameters.
The sign is a free parameter. The force observables do not distinguish the signs
because they measure the field shape, not the dynamical response.

**Script:** `frontier_two_sign_comparison.py`

## For a Nature Referee

A referee will now ask a narrower question:

> "Did you merely fix a wrong coupling, or did you also close directional
> gravity on the irregular graph families?"

Honest answer:
- yes, the old identity coupling was wrong and had to be retired
- yes, the corrected parity/lapse couplings restore sign-sensitivity in the
  direct external-potential tests
- no, the irregular graph story is not fully closed yet, because the retained
  graph-family directional observables are still proxy measures and the
  endogenous same-surface probe failed honestly after the rewrite

What now survives cleanly:
- exact-lattice directional response on the canonical `17-card`
- graph portability `7/7`
- self-gravity `5/5` with strong contraction across all retained scaling families
- rerun-corrected wave two-field `4/5`, `5/5`, `4/5`
- layered DAG-derived control `6/6`
- cycle battery `9/9` on all three retained cycle-bearing families
- scaled sibling `9/9` on all nine retained larger-size runs
- retarded family-closure sibling `9/9`, `9/9`, `9/9`, `8/9`
- topology-dependent onset behavior

What is still open:
- one graph-native directional observable that stands up on irregular graphs
- the emergent-geometry high-`G` window is a partial reopen, not retained closure

**Scripts:** `frontier_correct_coupling.py`, `frontier_two_sign_comparison.py`,
`frontier_two_sign_parity.py`
