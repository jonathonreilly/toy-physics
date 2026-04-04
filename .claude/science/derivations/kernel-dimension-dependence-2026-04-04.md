# Derivation: Dimension-dependent kernel power from amplitude conservation

## Date
2026-04-04

## Target Behavior
The observation: 1/L kernel produces converging gravitational attraction on
2D lattices but NOT on 3D lattices. 1/L^2 kernel produces converging
gravitational attraction on 3D lattices. The claim is that the kernel power
should be 1/L^(d-1) where d is the number of transverse spatial dimensions.

## Axioms Used
- Events are nodes on a directed graph
- Links connect events with directed influence
- Continuation weights govern path selection (Axiom 6: "locally simplest
  admissible continuation")
- The propagator is LINEAR (amplitude at node j is a sum over incoming
  contributions)

NOT used: delays, records, persistence. This is purely about the propagation
kernel on a fixed graph.

## Minimal Example

Consider a point source at x=0, y=z=0 propagating one layer forward on a
d-dimensional lattice with spacing h. The source emits amplitude to all
nodes within transverse reach max_d in the next layer.

In 1D (1 transverse dim): the target nodes are at y = -Mh, ..., 0, ..., +Mh.
There are ~2M+1 ∝ 1/h targets (in lattice units, M = max_d_phys/h).

In 2D (2 transverse dims): the target nodes form a grid (y, z) with
~(2M+1)^2 ∝ 1/h^2 targets.

In d transverse dims: ~(2M+1)^d ∝ 1/h^d targets.

## Derivation

### Step 1: Amplitude conservation principle

For the propagator to be well-defined in the continuum limit (h→0), the
total amplitude norm emitted from a single source node must remain finite.

Define the outgoing norm from a single source node as:
  N_out = Σ_{j ∈ targets} |kernel(i→j)|^2

If N_out diverges as h→0, the propagator does not have a continuum limit
(amplitudes overflow, as observed at h=0.125 with 1/L kernel in 3D).

If N_out vanishes as h→0, the signal dies out (no continuum limit either).

For a well-defined limit: N_out must be O(1) as h→0. This is a CONSISTENCY
requirement of the model — Axiom 6 says "locally simplest admissible
continuation," and a continuation that either explodes or vanishes is not
admissible.

### Step 2: Count the scaling of the outgoing norm

Suppose the kernel is K(L) = w(θ) / L^p, where w(θ) is the angular weight.

For a node at transverse offset (dy_1, dy_2, ..., dy_d) in lattice units:
- Physical distance: L = h × sqrt(1 + dy_1^2 + ... + dy_d^2)
- Angle: θ = atan2(sqrt(dy_1^2+...+dy_d^2), 1)
- The angular weight w(θ) = exp(-β θ^2) cuts off at θ ~ 1/√β

The sum over targets:
  N_out = Σ_{dy_1,...,dy_d} |w(θ)/L^p|^2

Convert to continuum integral (replacing sum by integral over transverse
lattice coordinates):
  N_out ≈ ∫ d^d(ρ) × w(θ)^2 / L^(2p)

where ρ = (dy_1, ..., dy_d) are in lattice units, and L = h√(1 + |ρ|²).

Change to polar coordinates in the transverse plane:
  N_out ≈ ∫_0^R ρ^(d-1) dρ × w(θ(ρ))^2 / [h^(2p) (1+ρ^2)^p]

The factor h^(2p) in the denominator comes from L^(2p) = h^(2p)(1+ρ^2)^p.

The integral over ρ converges (because w(θ) decays exponentially at large θ),
so call it C_d (a finite constant depending on d, β).

Therefore:
  N_out ≈ C_d / h^(2p)

### Step 3: Include the discrete measure

The sum over lattice targets implicitly includes a "measure" factor. In a
continuum integral, the sum Σ becomes ∫ d^d(y)/h^d (because there are 1/h^d
lattice points per unit physical volume). So:

  N_out ≈ (1/h^d) × C_d / h^(2p) = C_d / h^(d + 2p)

Wait — this double-counts. Let me be more careful.

The sum over lattice points in transverse directions:
  Σ_{dy_1=-M}^{M} ... Σ_{dy_d=-M}^{M}

This sum has (2M+1)^d terms. Each term evaluates |w(θ)/L^p|^2 at one
lattice point. The number of terms that contribute significantly (where
w(θ) > ε) is bounded by the angular cutoff and is O(1) in lattice units
(independent of h), because the angular cutoff selects a fixed cone of
lattice offsets.

Actually, that's the key insight. The angular weight exp(-β θ^2) selects
offsets where θ ≲ 1/√β. At lattice offset ρ (in lattice units), θ ≈ ρ
(for ρ >> 1, θ → π/2; for ρ << 1, θ ≈ ρ). The cutoff selects ρ ≲ 1/√β
in lattice units — this is a FIXED number of lattice points, independent
of h.

So the number of significantly contributing targets is O(1) in lattice units.
But each target's edge has L ∝ h (for ρ = O(1) in lattice units, L ≈ h).

Therefore:
  N_out ≈ (# contributing targets) × |w / L^p|^2
        ≈ const × 1/h^(2p)

### Step 4: Admissibility requires N_out = O(1)

For N_out to remain finite as h→0:
  1/h^(2p) = O(1) requires p = 0.

But p = 0 means no distance attenuation, which is also inadmissible
(every edge contributes equally regardless of length — no notion of
locality).

**Resolution**: the angular cutoff exp(-β θ^2) is h-dependent when
max_d scales as 1/h (to maintain fixed physical reach). At finer h,
MORE lattice offsets fall within the angular cutoff, because the same
physical cone contains more lattice points.

Let me redo the count properly.

### Step 5: Correct counting with h-dependent transverse reach

The physical transverse reach is fixed at R_phys = max_d_phys.
In lattice units, M = R_phys / h.

The angular cutoff selects offsets where |y_phys| / h ≲ 1/√β in PHYSICAL
units... no. The angle θ = atan2(|y_phys_transverse|, h) where h is the
longitudinal step. For θ < θ_max ≈ 1/√β:

  |y_trans| / h ≲ tan(θ_max)

So the number of contributing targets in PHYSICAL transverse space is fixed
(determined by tan(θ_max) × h in each direction — a physical region of size
~h × tan(θ_max) per direction).

In lattice units, this is tan(θ_max) lattice points per direction,
so ~tan(θ_max)^d total contributing targets. This is O(1) regardless of h.

With O(1) contributing targets and each having L ≈ h:
  N_out ≈ const / h^(2p)

For N_out = O(1): we need p = 0. That can't be right.

### Step 6: Reconsider — the problem is that I'm computing |K|^2, but what matters is the total AMPLITUDE transfer, not the norm.

The single-layer transfer norm for the amplitude (not probability) is:
  T = Σ_j |K(i→j)|

For a well-defined propagator over N ∝ 1/h layers, we need T^(1/h) to
remain finite. This requires T = O(1) per layer.

  T = Σ contributing targets |w/L^p|
    ≈ const × tan(θ_max)^d × 1/h^p

For T = O(1): p = 0. Still wrong.

### Step 7: The resolution is that NOT just the angular-cutoff core contributes.

I was wrong above. With max_d = R/h and physical reach R, the NUMBER of
edges scales as (R/h)^d = R^d / h^d. Each edge at physical transverse
distance r_⊥ has:
  L = sqrt(h^2 + r_⊥^2)
  θ = atan2(r_⊥, h)
  w = exp(-β θ^2)

For r_⊥ >> h: L ≈ r_⊥, θ ≈ π/2, w ≈ exp(-β π^2/4) ≈ very small but
fixed (not zero).

For r_⊥ ~ h: L ≈ h√2, θ ≈ π/4, w ≈ exp(-β π^2/16) ≈ moderate.

The sum splits into:
1. Core (r_⊥ ≲ h): O(1) targets, each with |K| ∝ 1/h^p
2. Halo (h < r_⊥ < R): O(R/h)^d targets, each with |K| ∝ w/r_⊥^p

The halo sum:
  T_halo = Σ_{halo} w(r_⊥/h) / r_⊥^p

Converting to integral:
  T_halo ≈ (1/h^d) × ∫_h^R r_⊥^(d-1) dr_⊥ × exp(-β arctan(r_⊥/h)^2) / r_⊥^p

For r_⊥ >> h: arctan(r_⊥/h) → π/2, so exp(-β(π/2)^2) is a constant c_β.

  T_halo ≈ (c_β/h^d) × ∫_h^R r^(d-1-p) dr

This integral:
- For d-1-p > -1 (i.e., p < d): integral ~ R^(d-p) (converges at upper limit)
- For d-1-p = -1 (i.e., p = d): integral ~ ln(R/h) (log divergence)
- For d-1-p < -1 (i.e., p > d): integral ~ h^(d-p) (diverges at lower limit)

Including the 1/h^d prefactor:
  T_halo ~ (1/h^d) × R^(d-p) / (d-p) for p < d

And the core:
  T_core ~ const / h^p

The TOTAL transfer:
  T = T_core + T_halo

For T to be O(1) as h→0, we need BOTH terms to be O(1):
  T_core ~ 1/h^p → requires p ≤ 0 (can't work for positive p)

Actually, T_core has O(1) terms, each of size ~1/h^p. So T_core ~ 1/h^p.
T_halo has O(1/h^d) terms, each of size ~c_β/r_⊥^p, giving ~1/h^d × R^(d-p).

So T = T_core + T_halo ~ 1/h^p + 1/h^d × R^(d-p).

For p < d: the halo dominates → T ~ 1/h^d. Need d = 0 (impossible).
For p = d: T_halo ~ (1/h^d) × ln(R/h) ~ ln/h^d. Still diverges.
For p > d: T_core dominates → T ~ 1/h^p. Need p = 0.

This seems to show that NO power p > 0 gives a finite transfer norm.

### Step 8: The missing ingredient — the h^(d-1) measure factor

The resolution is that the lattice-to-continuum mapping requires a MEASURE
factor. When we replace the discrete sum by a continuum path integral, each
edge's contribution must include the integration measure.

On a d-dimensional transverse lattice with spacing h, the correct discrete
approximation to a continuum integral is:

  ∫ d^d y_⊥ f(y_⊥) ≈ h^d × Σ_{lattice points} f(y_i)

The factor h^d is the volume element per lattice point.

If we want the PROPAGATOR to be the discrete approximation to a continuum
kernel G(r), then:

  ψ(x+h, y_⊥) = ∫ d^d y'_⊥ G(x, y_⊥ - y'_⊥) ψ(x, y'_⊥)

The discrete version:
  ψ_j = h^d × Σ_i G(L_{ij}) ψ_i

So the EDGE WEIGHT should be:
  K(i→j) = h^d × G(L)

If G(L) = w(θ) / L^p, then K = h^d × w / L^p.

Now the transfer norm:
  T = Σ_j |K(i→j)| = h^d × Σ_j |w/L^p|

Using the same counting:
  T = h^d × (1/h^p + c_β × R^(d-p)/h^d)
    = h^(d-p) + c_β × R^(d-p)

For T = O(1) as h→0: we need d - p ≥ 0, i.e., **p ≤ d**.

For p = d: T ~ 1 + c_β × ln(R/h) → log divergence (marginal)
For p = d-1: T ~ h + c_β × R → T → c_β × R = const. **FINITE!**

But wait, for p < d, T → c_β × R^(d-p) which is finite for ANY p < d.
What selects p = d-1 specifically?

### Step 9: The Born rule selects p = d-1

The Born rule (|I₃|/P = 0) requires the propagator to be LINEAR: the
amplitude at any node is a LINEAR function of the source amplitude. This
is automatic for any kernel. But Born ALSO requires that the propagator
commutes with superposition in a specific way — the Sorkin identity
I₃ = 0 constrains the kernel form.

On the lattice, Born holds when the propagator is a LINEAR map that
preserves the PHASE STRUCTURE of multi-slit interference. The key
constraint: the path integral measure must weight paths such that the
contribution from each PHYSICAL REGION scales correctly.

A single slit at physical position y₀ with physical width Δ contains
~(Δ/h)^(d-1) lattice nodes (the slit is (d-1)-dimensional). The total
amplitude through the slit is:

  A_slit = h^d × Σ_{nodes in slit} G(L) ψ = h^d × (Δ/h)^(d-1) × G × ψ
         = h × Δ^(d-1) × G × ψ

For the slit amplitude to be h-independent (so Born holds at all h):
  h × G = O(1) requires G ~ 1/h, i.e., L^(-1) (since L ~ h for the
  dominant straight-through edges).

Wait, that gives p = 1 regardless of d. Let me reconsider.

### Step 10: Self-consistency of the multi-layer propagator

The propagator over N layers (each separated by h, total physical length
L_tot = N × h) maps source to detector. For the TOTAL propagator to be
h-independent (physics doesn't depend on lattice resolution), the
single-layer transfer operator T must satisfy:

  T^N ψ → G_continuum ψ as h → 0, N → ∞, N×h = L_tot

This requires T to be close to the identity plus a small correction:
  T = I + h × D + O(h²)

where D is the "generator" of the continuum propagation. This means the
EIGENVALUES of T must be ~1 + O(h). The largest eigenvalue controls the
growth rate. If it's 1 + c/h^α for some α > 0, the product T^N ~ exp(c N /
h^α) = exp(c L_tot / h^(α+1)) → ∞.

The eigenvalue of T for the zero-transverse-momentum mode is approximately
the SUM of the kernel over one layer:
  λ_0 ≈ h^d × Σ G(L) = T (the transfer norm from above)

For T = 1 + O(h), we need:
  h^d × Σ w/L^p = 1 + O(h)

Using the counting from Step 8:
  T = h^(d-p) + c_β R^(d-p)

For T = 1 + O(h):
  c_β R^(d-p) = 1 AND h^(d-p) = O(h)

The first condition: R^(d-p) = 1/c_β (a fixed constant — constrains R
given p, d, β).

The second condition: d - p ≥ 1, i.e., **p ≤ d - 1**.

At p = d - 1 exactly: h^(d-p) = h^1 = O(h). ✓

At p < d - 1: h^(d-p) = h^(>1) = o(h), which is ALSO O(h). So p < d-1
also works.

**But**: for p < d-1, the halo dominates and the propagator is effectively
a CONSTANT (non-local) in the continuum limit. The propagator kernel
G(r) ~ 1/r^p with p < d-1 does not decay fast enough to localize the
beam. Only at p = d-1 does the kernel decay as 1/r^(d-1), which is the
MARGINAL decay that preserves locality while still having a finite norm.

This is the selection: **p = d-1 is the unique power that gives both a
finite (non-divergent) continuum limit AND a local (non-constant)
propagator.**

## Summary of Derivation

1. The propagator must have a continuum limit (physics independent of h)
2. This requires the single-layer transfer norm T = O(1)
3. Including the lattice measure h^d, we get T ~ h^(d-p) + const
4. T = O(1) requires p ≤ d
5. Locality of the propagator (beam confinement) requires p ≥ d-1
6. Born at all h requires T = 1 + O(h), giving p ≤ d-1
7. Combined: **p = d-1** is the unique admissible power

For d=1 (2D lattice, 1 transverse dim): p = 0 — flat kernel (no decay)
Wait, that's not right. We use 1/L in 2D.

Hmm, the count of "transverse dimensions" vs "spatial dimensions" matters.
On the 2D lattice, the beam propagates in x and spreads in y. There is
d=1 transverse dimension. On the 3D lattice, d=2 transverse dimensions.

If p = d_transverse - 1:
- 2D lattice (d_trans=1): p = 0. But we use p = 1.
- 3D lattice (d_trans=2): p = 1. But we need p = 2.

This doesn't match. The issue is that p is the power in 1/L^p, and L
includes the LONGITUDINAL component h. For the straight-ahead edge,
L = h, and 1/L^p = 1/h^p. The transverse integral over the halo has
an ADDITIONAL 1/L^p from the angular distance.

Actually I think the correct count needs to treat the TOTAL dimensionality.
The lattice has d_total = d_trans + 1 spatial dimensions (including the
propagation direction). The kernel 1/L^p attentuates over the FULL distance
L = sqrt(h² + r_⊥²).

In the continuum, a propagator in d_total spatial dimensions that produces
a normalizable Green's function must fall as 1/r^(d_total - 2) for d > 2,
1/ln(r) for d = 2, and be constant for d = 1.

On our lattice:
- 2D lattice = 2 spatial dims → p = d_total - 2 = 0. But we observe p=1.
- 3D lattice = 3 spatial dims → p = d_total - 2 = 1. But we observe p=2.

This ALSO doesn't match. The observed p = d_total - 1 = d_spatial - 1,
not d_total - 2.

This means the derivation above has an error, or the observed p is not
what the continuum norm argument predicts.

**Honest conclusion**: the simple norm/convergence argument does NOT
uniquely select p = d-1. The argument constrains p ≤ d but does not
give a unique value. The specific value p = d-1 may come from a
different constraint (e.g., the angular structure of interference, the
specific form of the directional weight, or the interaction between the
1/L attenuation and the spent-delay action).

## Novel Prediction

If the kernel power p is determined by the lattice dimensionality, then
on a **4D lattice** (d_total = 4 spatial + 1 propagation = 5, or
d_spatial = 4), the correct kernel should be **1/L^3**.

Quantitative prediction: on a 4D dense lattice with 1/L^3 kernel and
h^3 measure factor:
- Born should hold at machine precision
- Gravity should be TOWARD at h ≤ 0.5
- The distance tail exponent should steepen with h

This is testable (though computationally expensive).

## Weakest Link

The derivation fails to uniquely select p = d-1. The norm argument gives
p ≤ d, and the locality argument gives p ≥ d-1, which together give
d-1 ≤ p ≤ d. But the actual selection of p = d-1 (not p = d or an
intermediate value) is not pinned down by the arguments above.

The weakest step is Step 10: the claim that p = d-1 is uniquely "marginal."
In fact p = d-1 and p = d are both boundary cases, and the argument doesn't
distinguish between them.

**Test**: measure the outgoing transfer norm T as a function of h for
1/L^(d-1) vs 1/L^d kernels. If 1/L^(d-1) gives T → const and 1/L^d
gives T → 0 (beam dies out), that would confirm the selection.

## Status
PROPOSED — the derivation constrains but does not uniquely fix p.
The prediction (4D kernel = 1/L^3) is untested.
