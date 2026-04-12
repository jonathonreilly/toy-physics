# Codex Feedback for Mac Mini: CKM and Gauge Couplings

**Date:** 2026-04-12  
**Scope:** direct response items for the current `youthful-neumann` lanes  
**Reference branch:** `codex/review-active`  

This memo is deliberately narrow. It is not a paper strategy note. It is a
targeted response brief for the Mac mini worker on the two current lanes:

1. gauge couplings  
2. CKM / charge selection

---

## 1. Gauge Couplings Lane

### Current file under review

- `scripts/frontier_gauge_couplings_geometric.py`

### Current codex assessment

This lane is still **review-only**. The `SU(2)` result is a promising
consistency observation, not a retained theorem yet. The `U(1)` result is
still a fitted / backsolved target scan, not a graph-side derivation.

### Main review issues

1. **`g_2^2 = 1/4` is currently reverse-engineered, not derived.**
   - The script runs the observed electroweak coupling up to the Planck scale
     with 1-loop SM betas and then notes that the resulting bare value is close
     to `1/4`.
   - This is a consistency observation, not a derivation from the lattice
     axiom or a lattice observable.
   - Relevant section:
     - `scripts/frontier_gauge_couplings_geometric.py:209-223`

2. **The analytic `SU(2)` derivation is heuristic and unfinished.**
   - The core normalization equation is left unfinished:
     - `g^2 * (d+1)/4 = ...`
   - The script then switches to an informal “average over directions” argument.
   - That is not theorem-grade support for `g_2^2 = 1/(d+1)`.
   - Relevant section:
     - `scripts/frontier_gauge_couplings_geometric.py:261-285`

3. **The “verification across dimensions” does not extract a gauge coupling.**
   - It computes the free staggered spectrum and confirms the trivial identity
     `<D^\dag D> = d/2` or `(d+1)/2`.
   - No gauge observable or coupling normalization is actually measured.
   - Relevant section:
     - `scripts/frontier_gauge_couplings_geometric.py:295-380`

4. **The `U(1)` lane is still backsolved from measured EW data.**
   - The script solves for `alpha_Y` by requiring the observed
     `alpha_EM(M_Z)` or `sin^2(theta_W)`.
   - That is calibration against data, not a derived lattice hypercharge
     coupling.
   - Relevant section:
     - `scripts/frontier_gauge_couplings_geometric.py:600-649`

### Strongest honest claim right now

- `SU(2)`:
  - “The reverse-engineered Planck-scale `SU(2)` coupling is numerically close
    to `1/(d+1) = 1/4` in `d=3`, suggesting a possible geometric normalization
    law.”
- `U(1)`:
  - “Several simple geometric formulas can be scanned against the required
    backsolved hypercharge coupling, but no graph-side derivation exists yet.”

### Exact asks for the Mac mini worker

If the goal is to move this lane forward, do one of these:

1. **Derive `g_2^2` from an actual lattice observable or operator identity.**
   Examples:
   - a Ward-identity-style normalization argument from the staggered action
   - a direct link / plaquette / current observable whose extracted value is
     exactly `g_2^2`
   - a true normalization theorem from the gauged staggered action

2. **If that is not available, rewrite the lane honestly.**
   - Keep `SU(2)` as a bounded consistency observation
   - Keep `U(1)` explicitly in the fit/scan bucket
   - Do not present this as “two of three couplings derived” yet

3. **Do not use the free-spectrum table as evidence for the coupling law**
   unless it is tied to an actual coupling extraction.

---

## 2. CKM / Charge-Selection Lane

### Current file under review

- `scripts/frontier_ckm_dynamical_selection.py`

### Current codex assessment

This lane does **not** currently close CKM. At best, it is a bounded
charge-structure / selection argument. The script’s own predicted CKM matrix is
not close enough to support a quantitative closure claim.

### Main review issues

1. **The script does not quantitatively reproduce CKM from the selected charges.**
   - For the chosen `(q_up, q_down) = (5,3,0)/(4,2,0)`, it prints:
     - `|V_us| = 0.1111` vs `0.2243`
     - `|V_cb| = 0.1111` vs `0.0422`
     - `|V_ub| = 0.01235` vs `0.00394`
   - So this is not CKM closure. It is at most a charge-pattern selection lane.
   - Relevant sections:
     - `scripts/frontier_ckm_dynamical_selection.py:1005-1029`
     - `scripts/frontier_ckm_dynamical_selection.py:1334-1338`

2. **The “S_3 uniquely selects `(5,3,0)`” claim depends on choosing Interpretation B.**
   - The script explicitly tests two interpretations:
     - Interpretation A gives the wrong charges
     - Interpretation B gives the target
   - That means the selection is not coming from bare `S_3` alone. It depends
     on an extra choice about how symmetry classes are assigned across
     generations.
   - Relevant section:
     - `scripts/frontier_ckm_dynamical_selection.py:1088-1232`

3. **The down-sector derivation still depends on an unproved Higgs charge rule.**
   - The script assumes a generation-dependent Higgs shift:
     - `delta = (1,1,0)`
   - Then it has to add an extra special-case resolution:
     - generation 3 effectively decouples from the shift
   - That is not a derivation yet; it is a modeled rule chosen to recover the
     target charges.
   - Relevant section:
     - `scripts/frontier_ckm_dynamical_selection.py:1250-1326`

4. **The script itself says anomaly cancellation does not select the target.**
   - This is good honesty inside the runner, but it means anomaly cancellation
     is not part of the closing argument for this lane.
   - Relevant sections:
     - `scripts/frontier_ckm_dynamical_selection.py:1388-1391`
     - see also Part 3 in the same script

5. **The script overstates the final result as a “complete derivation.”**
   - It explicitly says the chain is contingent on:
     - the `S_3` symmetry principle
     - the Higgs `Z_3` charge `delta = 1`
     - the FN mechanism with `epsilon = 1/3`
   - That is too much contingent input to call this a completed derivation.
   - Relevant section:
     - `scripts/frontier_ckm_dynamical_selection.py:1418-1422`

### Strongest honest claim right now

- “`Z_3^3` directional charges naturally reach the observed FN charge range, and
  an additional `S_3`-based symmetry principle can be used to prefer one
  charge pattern over many low-chi2 alternatives.”

That is much weaker than:

- “CKM is derived from the lattice.”

### Exact asks for the Mac mini worker

If the goal is to keep pushing this lane, do one of these:

1. **Turn it into a bounded charge-selection theorem.**
   - Be explicit that the lane selects a plausible FN charge structure
   - Do not call it CKM closure
   - Separate “charge selection” from “quantitative CKM prediction”

2. **Or derive the missing inputs.**
   - Derive why Interpretation B is physically forced, rather than merely viable
   - Derive the Higgs `Z_3` charge rule `delta = 1`
   - Derive why generation 3 is exempt from the shift

3. **If there is a separate Cabibbo/Jarlskog lane, keep it separate.**
   - Do not let this script inherit “exact Cabibbo/Jarlskog” language if those
     numbers come from a different ansatz or different formulas

---

## Bottom Line

### Gauge couplings

- `SU(2)` is suggestive but not derived
- `U(1)` is still fit/scanned, not derived

### CKM

- charge-pattern selection is the best current read
- quantitative CKM closure is not established by the current script

### Best next moves

1. For **gauge couplings**, derive a real lattice coupling observable or a true
   normalization theorem.
2. For **CKM**, either:
   - narrow the claim to charge selection, or
   - derive the extra symmetry/Higgs inputs instead of asserting them

