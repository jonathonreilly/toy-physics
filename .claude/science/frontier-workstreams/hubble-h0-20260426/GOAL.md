# Hubble Constant H_0 Derivation Workstream

**Goal:** retire `H_0 = 67.4 km/s/Mpc` from the external-input ledger and close
Lane 5 (Hubble constant `H_0` derivation) on the retained-cosmology surface.

**User invocation:**
`/frontier-workstream "go run the frontier workstream on hubble lane"
--mode run --runtime 10h`

**Target status:** `best-honest-status`. Retained closure if achievable;
substantial exact support, no-go, or import retirement otherwise. Pure prose
passes do not count.

## Reduced retained objective

The lane file
[`docs/lanes/open_science/05_HUBBLE_CONSTANT_DERIVATION_OPEN_LANE_2026-04-26.md`](../../../../docs/lanes/open_science/05_HUBBLE_CONSTANT_DERIVATION_OPEN_LANE_2026-04-26.md)
identifies the closure target:

> retained `H_0`, internal matter-density bridge, and a clear framework
> position on the low/high Hubble tension values.

Recent structural-identity landings collapse the late-time bounded cosmology
surface to **one open scalar plus one absolute-scale anchor**:

```text
L := (H_inf / H_0)^2 = Omega_Lambda    (matter-bridge theorem, 2026-04-22)
H_inf := c / R_Lambda                  (scale identification)
```

Closure of Lane 5 therefore reduces to one of:

1. retained derivation of `L`, OR
2. retained derivation of `R_Lambda` plus a separate derivation pinning either
   `H_0` or `L`, OR
3. proof that no retained derivation exists on the minimal accepted axiom
   stack — a useful program-bounding no-go.

## Workstream priorities

In order of next-cycle execution:

1. **R4 — Hubble Tension Structural Lock theorem** (Tier A). Formalize the
   framework's late-time `Lambda`CDM commitment as a publication-surface
   theorem with a real falsifier: any genuine `H_0` tension between
   distance-ladder and CMB measurements must arise from pre-recombination
   physics, not late-time modification.
2. **R3 — Open-number reduction theorem** (Tier A). Make explicit the
   parameter-count statement: every late-time bounded cosmology row
   (`Omega_Lambda`, `Omega_m`, `q_0`, `z_*`, `z_mLambda`, `H_inf`, `H(a)`) is a
   function of the single pair `(H_0, L)` on the retained surface.
3. **R5 — eta retirement audit** (Tier B). Survey existing DM leptogenesis
   support routes (`eta/eta_obs = 0.1888` exact one-flavor;
   `eta/eta_obs = 1.0` reduced-surface PMNS); identify the promotion gate
   that retires `eta` from the bounded `Omega_b` cascade.
4. **R6 — `R_Lambda` direct route** (Tier C, Planck-lane-blocked). `R_Lambda`
   from S^3 spatial topology + Planck-scale anchor; currently blocked by the
   Planck-lane open carrier identification.
5. **R7 — cosmology no-go** (Tier B). Prove that on the retained
   axiom stack alone, `L` cannot be derived without an additional structural
   premise (e.g. an absolute-scale axiom). Useful program-bounding negative.

## Delivery

Science-only on branch `frontier/hubble-h0-20260426`. Push that branch to
`origin`. Do not open a PR. Do not push to `main`. Proposed repo-wide weaving
recorded in `HANDOFF.md` for later review-and-integration.
