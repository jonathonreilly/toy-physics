# Physics Autopilot Handoff

## 2026-03-30 12:48 America/New_York

### Seam class
- interference geometry sweep
- two-slit fringe contrast vs network geometry
- PStack pipeline inaugural run

### Science impact
- First systematic geometry sweep of the two-slit interference setup
- Fringe contrast at y=0 is exactly 1.0 (coherent) / 0.0 (record) at all geometries — a symmetry property, not dynamics
- Distribution SHAPE varies dramatically with geometry and is the dynamically interesting observable

### Current state
- PStack science skills installed in `.claude/commands/` (14 skills)
- Science documents in `.claude/science/` (frontier map, hypothesis, theory-review, experiment design, analysis, sanity check)
- New script: `scripts/interference_geometry_sweep.py`
- New log: `logs/2026-03-30-interference-geometry-sweep.txt`
- Branch `claude/intelligent-jepsen` pushed to GitHub
- No detached science child is active.
- Lock: released.

### Active thread
- Interference regime geometry dependence — specifically the OFF-CENTER fringe pattern
- The center detector (y=0) contrast is trivially 1.0 by grid reflection symmetry
- The dynamically interesting measurement is fringe visibility V(y) at y != 0

### Strongest confirmed conclusion
- Fringe contrast at y=0 is EXACTLY 1.0 in coherent mode at all tested geometries, but this is a symmetry property of the setup (equal path lengths to center from symmetric slits), not a dynamical property of the model
- The record mechanism provides all-or-nothing suppression: binary toggle, no partial suppression, geometry-independent
- Distribution SHAPE varies dramatically with geometry and is the dynamically interesting observable for follow-up

### Files/logs changed
- New script: `scripts/interference_geometry_sweep.py`
- New result log: `logs/2026-03-30-interference-geometry-sweep.txt`
- New PStack skill files: `.claude/commands/` (14 skills)
- New PStack science documents: `.claude/science/` (frontier, hypotheses, experiments, analyses, sanity, theory-reviews)
- Updated: `AUTOPILOT_WORKLOG.md`, `logs/physics_autopilot_handoff.md`

### Remaining review seams
- open: off-center fringe visibility V(y) for y != 0 — does it depend on geometry?
- open: partial record mechanisms — probabilistic record creation sweeping probability 0→1
- open: attenuation_power sweep — could create partial decoherence-like effects
- open (prior thread): nearest still-fresh base or nearby non-base control beyond the paired ultra shoulders

### Exact next step
- Write a follow-up script measuring off-center fringe visibility V(y) for y != 0 across the geometry grid
- The symmetry protection only applies at y=0; off-center positions test the model's actual path-selection dynamics

### First concrete action
- Create `scripts/interference_offcenter_fringe_sweep.py` that computes V(y) = (P_max(y) - P_min(y)) / (P_max(y) + P_min(y)) across the full phase sweep for each screen position y, at each geometry point
