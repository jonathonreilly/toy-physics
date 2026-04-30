# Lane 1 `sqrt(sigma)` B5 Framework-Link Audit

**Date:** 2026-04-30
**Status:** support / current-surface no-go; no theorem or claim
promotion. This note audits whether the current repo surface closes the
`(B5)` bridge that allows standard lattice-QCD static-energy and
string-tension values to be imported into the framework `SU(3)` gauge
sector.
**Script:** `scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py`
**Lane:** 1 - Hadron mass program, route 3E `sqrt(sigma)` retained
promotion.

---

## 0. Result

The current surface does **not close B5**.

It has meaningful structural support:

- graph-first `SU(3)` integration on the selected-axis surface;
- `g_bare = 1 -> beta = 6` on the accepted Wilson-plaquette action;
- canonical plaquette constants;
- a small-volume `4^4` pure-gauge consistency check.

But the B5 bridge needed by the B2 static-energy import is stronger:

```text
framework gauge substrate at beta=6
  -> same large-volume Wilson / Creutz / static-force observables
     as standard SU(3) lattice QCD, with uncertainty
```

The repo does not yet supply that large-volume framework-side ladder.
The current `4^4` check is useful but finite-volume and short-distance;
the `r0/a`, `sigma a^2`, Sommer-scale, and full-QCD static-energy values
remain standard lattice-QCD bridge inputs.

## 1. Current Support Surface

| Component | Current status | B5 role |
|---|---|---|
| `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` | structural `SU(3)` support | gives the compact semisimple color algebra |
| `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md` | conditional closure; Wilson action form imported | fixes coefficient once Wilson action is accepted |
| `canonical_plaquette_surface.py` | stores canonical beta=6 plaquette constants | evaluated surface, not volume-scaling proof |
| `CONFINEMENT_STRING_TENSION_NOTE.md` | bounded consistency story | imports standard `r0/a`, `sigma a^2`, and screening |
| `frontier_confinement_string_tension.py` | small-volume check plus bridge arithmetic | `L=4`, not asymptotic string-tension extraction |

This is enough to justify the **bounded** statement:

> Conditional on the framework gauge substrate matching standard
> `SU(3)` lattice QCD at `beta = 6`, standard static-energy inputs give a
> plausible `sqrt(sigma)` window.

It is not enough to retain the bridge.

## 2. Why B5 Does Not Close

### 2.1 Structural `SU(3)` is not lattice dynamics

The graph-first theorem closes the algebraic color-sector objection, but
it does not measure Wilson loops, Creutz ratios, force scales, or
static-energy correlators on the framework substrate.

### 2.2 `g_bare = 1 -> beta = 6` still assumes Wilson action form

The `g_bare` structural-normalization note is explicit: given the
standard Wilson plaquette action, the coefficient is forced. The action
form itself is an accepted kinetic ansatz, not derived uniquely from
`Cl(3)`.

This is not a defect in that theorem. It is exactly the residual B5 must
declare or reduce.

### 2.3 The current Monte Carlo check is too small

The confinement runner uses `L = 4`, and the confinement note already
states that `4^4` is far too small for quantitative asymptotic string
tension measurement. At that size, `chi(2,2)` is a short-distance
positive-tension diagnostic, not a large-distance `sigma a^2` extraction.

### 2.4 The bridge constants are still imported

The current runner hard-codes standard lattice-QCD bridge constants:

```text
p_lattice_qcd = 0.5934
r0/a = 5.37
sigma a^2 = 0.0465
```

Those constants are valid standard-QCD bridge material, but B5 asks why
they apply to this framework substrate beyond structural identification.

## 3. Closure-Gate Model

| Candidate | Framework-side measurement | Large-volume/asymptotic | Standard-QCD comparator | Action residual declared | Uncertainty | Closes? |
|---|---:|---:|---:|---:|---:|---:|
| current `4^4` plaquette/Wilson check | yes | no | yes | yes | no | no |
| graph-first `SU(3)` + `g_bare` normalization | no | no | no | yes | no | no |
| future Creutz/force-scale ladder | yes | yes | yes | yes | yes | yes |

So this block records a current-surface no-go, not a route failure in
principle.

## 4. Future Large-Volume Ladder

The next B5 science route should be a framework-side pure-gauge ladder:

```text
L = 4, 6, 8  (local machine feasible scout)
then L >= 12 or L >= 16 if compute budget allows
```

For each `L`, measure:

- plaquette mean and uncertainty at `beta = 6`;
- Wilson loops `W(R,T)` for as many `R,T` as signal allows;
- Creutz ratios `chi(R,T)`;
- optionally static-force proxies that can be compared to `r0` / `r1`.

The closure target is not to extract a publication-grade string tension
locally. It is to quantify the finite-volume residual and decide whether
the B5 uncertainty can be declared honestly or remains compute-blocked.

## 5. Claim-State Movement

Cycle 3 moves the lane by closing one possible shortcut:

```text
structural SU(3) + beta=6 + 4^4 check
  != retained framework-to-standard-QCD bridge
```

Safe statement:

> B5 is structurally supported but not retained. Current framework-side
> evidence is small-volume consistency; imported static-energy and
> string-tension constants must remain bounded bridge inputs until a
> large-volume Wilson/Creutz/force-scale ladder or equivalent theorem
> lands.

## 6. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py
```

Expected result:

```text
PASS=16 FAIL=0
```

## 7. Next Exact Action

Run a local B5 scout ladder on `L = 4, 6, 8` if runtime permits, or land a
compute-budget note proving that `L >= 12-16` is required before B5 can
be materially tightened.
