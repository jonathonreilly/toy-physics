# Mac Mini Compute Backlog

These scripts may need more compute than the laptop can handle in agent timeouts.
Run them on the Mac Mini after pulling the latest branch.

## Setup

```bash
cd Physics-compute  # or wherever you cloned
git pull origin claude/youthful-neumann
pip3 install numpy scipy
```

## Run 1: Dimension Selection (Priority 2 — MOST IMPORTANT)

Tests whether self-consistency selects d_s=3. The 4D (6⁴=1296 sites) and 5D (4⁵=1024 sites) lattices need full eigendecomposition for the Poisson solver.

```bash
python3 scripts/frontier_dimension_selection.py 2>&1 | tee ~/Desktop/dimension_selection.txt
```

Expected runtime: ~5-10 min. The 4D/5D Poisson solves are the bottleneck.

**What to report:** The summary table showing which dimensions have all three properties (attractive + β≈1 + I₃=0). If only d=3 has all three, that's a Nature headline.

## Run 2: Hierarchy Ratio (Priority 3)

Tests gravity/EM coupling ratio constraints.

```bash
python3 scripts/frontier_hierarchy_ratio.py 2>&1 | tee ~/Desktop/hierarchy_ratio.txt
```

Expected runtime: ~3-5 min.

**What to report:** Whether there's a natural G/q² ratio, and what it is.

## Run 3: Background Independence (Priority 4)

Tests effective geometry ≠ input graph.

```bash
python3 scripts/frontier_background_independence.py 2>&1 | tee ~/Desktop/background_independence.txt
```

Expected runtime: ~2-3 min.

**What to report:** Whether the effective connectivity / distance / dimension change near a gravitational source.

## Run 4: Distance Law (if not already done)

```bash
python3 scripts/frontier_distance_law_definitive.py 2>&1 | tee ~/Desktop/distance_law_96.txt
```

## Priority Order

1. dimension_selection (biggest needle mover)
2. hierarchy_ratio
3. background_independence
4. distance_law (if not already run)
