# Mac Mini Compute Backlog

Pull latest before running:
```bash
cd Physics-compute
git pull origin claude/youthful-neumann
```

## Priority 1: d=3 Selection Attacks (RUN ALL)

These test whether d=3 is uniquely selected. Run all four:

```bash
# 1a. Atomic bound states — no stable atoms at d≥5?
python3 scripts/frontier_bound_state_selection.py 2>&1 | tee ~/Desktop/bound_states.txt

# 1b. Transfer matrix spectral radius — propagator diverges at d>3?
python3 scripts/frontier_spectral_radius_dimension.py 2>&1 | tee ~/Desktop/spectral_radius.txt

# 1c. Wave stability — ringing at d=4? (already done on laptop, but rerun for confirmation)
python3 scripts/frontier_wave_stability_dimension.py 2>&1 | tee ~/Desktop/wave_stability.txt

# 1d. Self-energy critical dimension — d=3 is the UV/IR transition?
python3 scripts/frontier_self_energy_critical_dimension.py 2>&1 | tee ~/Desktop/self_energy.txt
```

Expected runtime: ~5-15 min total. The 4D/5D lattices (6⁴=1296, 4⁵=1024 sites) are the bottleneck.

**What to report:** For each script, the summary table showing which dimensions pass/fail. The key question: does anything FAIL at d≥4 that passes at d=3?

## Priority 2: Dimension Selection (if not already done)

```bash
python3 scripts/frontier_dimension_selection.py 2>&1 | tee ~/Desktop/dimension_selection.txt
```

## Priority 3: Background Independence

```bash
python3 scripts/frontier_background_independence.py 2>&1 | tee ~/Desktop/background_independence.txt
```

## Priority 4: Distance Law (if not already done)

```bash
python3 scripts/frontier_distance_law_definitive.py 2>&1 | tee ~/Desktop/distance_law.txt
```

## The d=3 question in one sentence

If ANY of the Priority 1 scripts shows a hard failure at d≥4 that doesn't occur at d=3, we can derive "space is 3-dimensional" from the framework's axioms. That eliminates the last free parameter and makes the framework truly 2 axioms, 0 parameters.
