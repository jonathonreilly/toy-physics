# Scaling Targets

## Gravity

**Current behavior:** centroid shift saturates at k × ΣΔS > π, producing a sign-threshold (±height) that is b-independent and M-independent.

**Target:** A dimensionless gravitational response R(b, M, N) where:
- R decreases with impact parameter b (at least as 1/b in 3D, 1/log(b) in 2D)
- R increases with mass M (at least linearly)
- R does not collapse to {-1, 0, +1} as graph size N grows
- R remains zero at k=0 (gravity = pure phase)

**Formal metric:**
```
R(b) = [⟨y⟩_mass(b) - ⟨y⟩_free] / σ_free
```
where σ_free is the free-beam width. This normalizes by beam spread.

**Success criterion:** d(log R)/d(log b) < 0 across at least one decade of b.

## Decoherence

**Current behavior:** detector-state purity Tr(ρ²) increases with graph size N (0.57 at N=126 → 0.89 at N=601 with fixed env; plateaus at 0.79 with depth-scaled env).

**Target:** Purity that stays bounded away from 1 or decreases as N grows, at fixed local environment density:
```
Tr(ρ²) ≤ C < 1  for all N > N₀
```
or ideally:
```
Tr(ρ²) → 0  as N → ∞  (complete decoherence in thermodynamic limit)
```

**Formal metric:** Purity conditioned on detector hits, measured at fixed env_region_fraction = (env layers)/(total layers).

**Success criterion:** d(Tr(ρ²))/d(N) ≤ 0 across N = 100..1000.

## Constraints (must not break)

| Property | Criterion |
|---|---|
| Born rule | I₃/P < 10⁻¹⁰ (3-slit amplitude mask on fixed DAG) |
| Interference | V > 0.5 at some k |
| k=0 → no gravity | shift < 10⁻¹⁰ at k=0 |
| Gravity sign | shift toward mass > 50% of seeds |
