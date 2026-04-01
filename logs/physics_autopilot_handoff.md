# Physics Autopilot Handoff

## 2026-04-01 04:39 America/New_York

### Seam class
- architecture integrity repair
- merged readout reconciliation

### What this loop did
- reconciled repo state first, then picked up the merged G2/two-scale readout-bug fix already on `main`
- reran `/Users/jonreilly/Projects/Physics/scripts/two_scale_architecture.py` so `/Users/jonreilly/Projects/Physics/logs/2026-03-31-two-scale.txt` matches the merged script output
- updated `/Users/jonreilly/Projects/Physics/README.md` so the architecture section matches the repaired two-scale numbers

### Current state
- no detached science child is running
- the architecture lane is now synchronized across script, tracked log, README, and work log
- corrected two-scale verdict:
  - `n_ybins = 6`: `R_2s +0.577 -> +0.925`, `pur_2s 0.8401 -> 0.9806`
  - `n_ybins = 8`: `R_2s +0.945 -> +1.195`, `pur_2s 0.8517 -> 0.9555`
- retained interference stop rule still applies: `V_g2 = 0.0000` at `k = 3.0, 5.0`

### Strongest confirmed conclusion
No tested architecture currently passes gravity scaling, interference, and decoherence scaling simultaneously. The merged readout repair changes some magnitudes, but not the qualitative closure: G2-style coarse-graining fixes gravity saturation, still kills interference, and the two-scale extension still wrong-scales on decoherence.

### Exact next step
- design one gravity-preserving compression that keeps microscopic phase contrast alive, then rerun the interference constraint before any new decoherence register variant

### First concrete action
- prototype a phase-preserving bundle rule that aggregates near-degenerate paths without averaging away their relative phases
