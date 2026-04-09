# Moonshot Honest Review — What Survived, What Didn't, What's Next

**Date:** 2026-04-09
**Commit:** 32e5931 (branch claude/sleepy-cerf)

## Adversarial self-review of all frontier experiments

### What ACTUALLY survived rigorous review

**Tier 1: Structurally sound, machine-precision results**

1. **Born rule is kernel-independent** — 7 kernels all give I₃/P < 10⁻¹⁴.
   This is structural: the linear path-sum guarantees pairwise interference
   regardless of the angular weight. No caveats needed.

2. **k=0 gravity control** — setting the phase coupling to zero kills gravity
   for all kernels, all dimensions, all field strengths. Structural.

3. **F∝M = 1.00 in 2+1D at the retained reference coupling** — valley-linear
   action on the 3D ordered lattice gives exact linear mass scaling with
   R²=1.0 in the benchmark attractive window. Existing closure card
   (lattice_3d_valley_linear_card.py) with 10 verified properties.

4. **Action constraint theorem** — Lorentz covariance + Newtonian limit
   constrains the leading-order action to a one-parameter family matching
   valley-linear. Spent-delay excluded by two axioms. Analytic.

**Tier 2: Positive signals with documented caveats**

5. **3+1D gravity feasibility** — TOWARD with F∝M=1.00 at h=0.5, W=3.
   Same-geometry refinement confirms resolution (not box size) is the
   variable. But: h=1.0 is AWAY, and this is a small box. Not closure.

6. **cos²(θ) passes all 10 properties in 2+1D** — including the multi-L
   companion checks. Trade-off: 30% weaker gravity, better isotropy
   (1.5% vs 16% in separate kernel sweep). At h=0.5 in 3+1D the two
   kernels converge to nearly identical gravity.

7. **Mass breaks propagator rank degeneracy** — free-space effective rank = 2
   (parity concentration). Mass pushes entropy from ln(2) to 1.45.
   Mechanism: field gradient breaks y-symmetry.

**Synthesis update from the later k-sweep, PN study, and 2D sign diagnosis**

The gravity-like response is best understood as a **coupling-window /
resonance phenomenon**, not as a universal geometric law of the propagator.
The retained `-1.40` lensing slope at `k·H=2.5` is a reference-configuration
value on an oscillatory response curve, not a structural constant. Within
specific attractive windows the model can look Newtonian-like; outside them
the same propagator can become shallower or even repulsive.

**Tier 3: Results that are real but overclaimed in the scripts**

8. **Gauge invariance** — U(1) gauge invariance of |ψ|² under node phases
   is mathematically trivial (|e^(iα)|² = 1). The AB effect test is a
   real interference phenomenon but in a confined geometry where the
   phase is on traversed edges, not in a flux tube the particle avoids.
   The SU(2) extension is custom code that needs verification against
   standard lattice gauge theory conventions.

   **What survives:** The path-sum naturally supports gauge connections.
   The AB phase modulation is real (cos²(φ/2), depth=1.0). But calling
   this "gauge invariance emerges" overstates it — it's a consequence
   of amplitude additivity, which was already assumed.

9. **Parity charge (spin analog)** — Z₂ parity IS a conserved quantum
   number. But the "Stern-Gerlach splitting" test compares different
   source configurations (source=0 for even, source=±1 for odd), not
   a single beam separated by a gradient. The differential deflection
   follows from source position, not from spin-like properties.

   **What survives:** Parity is a good quantum number. A field gradient
   creates odd components from even beams. But this is symmetry breaking,
   not spin splitting.

**Tier 4: Honest negatives and null results**

10. **Energy levels don't match n²** — the propagator is not the
    Schrödinger propagator. The spectrum is discrete but lattice-dominated.
    The corrected benchmark (first-excited degeneracy from square symmetry)
    is partially consistent.

11. **Rotational isotropy doesn't improve with h** — the angular kernel
    is intrinsic, not a lattice artifact. This blocks the Lorentz
    invariance frontier.

12. **Hawking T~1/M falsified** — thermal spectral shape exists (R² > 0.93)
    but T is constant across field strengths. No negative control shows
    whether ANY finite-lattice propagator has this shape. The thermal
    spectrum is likely geometric (lattice mode structure), not dynamical.

13. **PN f² correction is regime-dependent** — in the weak-field window it
    enhances gravity slightly, while at stronger coupling it can suppress
    or oscillate. The cleaner synthesis is that the f² term shifts the
    effective accumulated phase and moves the system along the same
    interference / resonance curve seen in the later k-sweep.

## Reframed approaches for the failures

### Energy levels → "What QM does this propagator produce?"

Instead of testing whether the existing propagator matches the Schrödinger
equation, compute the effective Hamiltonian H where M = exp(-iHT). The
transfer matrix already gives eigenvalues λₙ. Define H via
E_n = -i ln(λ_n) / T. Then examine: what IS the effective kinetic operator?
Is it a discrete Laplacian with corrections? What dispersion relation does
it give? This reframes from "does it match known physics" to "what physics
does it predict."

### Rotational isotropy → "What is the emergent metric?"

The angular kernel defines an effective metric on the lattice. Instead of
trying to eliminate anisotropy, COMPUTE the metric tensor:
g_ij = sum_edges w(θ) × (Δx_i)(Δx_j) / L²
If this tensor has Lorentzian signature (one negative eigenvalue), the
model has emergent Minkowski structure regardless of isotropy at finite h.
The anisotropy becomes a finite-lattice correction to an emergent
continuum metric, rather than a fundamental defect.

### Hawking → "What is the lattice temperature?"

If the thermal shape is geometric, then the lattice HAS a temperature
determined by its structure (spacing h, connectivity, number of modes).
This is analogous to the Unruh effect: an accelerating observer sees
thermal radiation at T = a/(2π). The lattice analogue would be:
what acceleration (field gradient) does the propagator "experience,"
and does the thermal temperature match a/(2π)?

Test: run with NO field but DIFFERENT lattice spacings h. If the thermal
temperature T scales with 1/h, the temperature is a lattice property.
If T is h-independent, it's something else.

### Spin → "What is the automorphism group of the DAG?"

Instead of forcing SU(2) from Z₂, study what the DAG's symmetry group
actually IS and what representations it has. On a rectangular DAG:
- Reflection y → -y (Z₂): gives parity charge ±1
- Translation y → y+1 (if periodic): gives momentum k
- Combined: can produce a richer representation theory

If the DAG is given a HEXAGONAL or TRIANGULAR lattice structure, the
symmetry group is larger (Z₆ or Z₃), potentially supporting more
internal degrees of freedom. Testing whether the number of "spin"
components tracks the lattice symmetry group would be a real result.

### Gauge invariance → "Can the model predict coupling constants?"

The AB effect IS real lattice gauge physics. Rather than debating
whether it's "trivial," ask: if we ADD a gauge field (link phases)
to the existing gravitational model, do the gauge field dynamics
(Wilson action / plaquette energy) have a natural value for the
coupling constant g? In lattice QCD, the coupling runs with the
lattice spacing. Does the same happen here?

## What to do next (priority order)

1. **Effective Hamiltonian analysis** — compute H from the transfer matrix
   and extract the dispersion relation. This is the most informative
   single experiment for understanding what physics the model produces.

2. **Emergent metric tensor** — compute from the angular kernel and check
   signature. This directly tests whether Lorentzian structure emerges.

3. **3+1D distance law** — run the actual b-sweep on the h=0.5 4D lattice
   with spatial-only field. This is the missing piece for the 3+1D story.

4. **Lattice temperature vs h** — test whether the thermal spectrum
   temperature depends on lattice spacing to identify its origin.

5. **Automorphism group representations** — compute the symmetry group
   of the DAG and its irreducible representations. Compare to particle
   content of the model.
