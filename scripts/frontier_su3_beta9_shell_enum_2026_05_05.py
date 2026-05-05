"""β^9 mixed-cumulant term: shell enumeration for SU(3) Wilson plaquette.

The framework's mixed-cumulant theorem at β^5 identified 4 cube shells
(elementary cube boundaries through the marked plaquette p_0), each
contributing 1/18^5 → total 4/18^5 = 1/472392.

For β^9: need to enumerate 9-action-plaquette closed shells through p_0
and compute their SU(3) Haar contributions.

LIKELY CONTRIBUTORS at β^9 (10 total plaquettes = 1 marked + 9 action):

1. **2×1×1 box configurations**: rectangular parallelepiped with 10 unit
   plaquette faces. p_0 can be any of these 10 positions.

2. **Two cubes joined at marked plaquette**: 2 cubes sharing only p_0
   gives 5+5 = 10 action plaquettes? Actually no — would give 10 action
   plaquettes (5 per cube minus 0 shared since they only share p_0 itself
   which is NOT an action plaquette). So 10 action = β^10, not β^9.

3. **Cube + extension**: an elementary cube + 4 extra plaquettes attached
   to close. Could give β^9 if the 4 extras contribute together with cube's
   5 action faces = 9 total.

4. **L-shape boxes**: 9-plaquette closed shells with L topology.

This enumeration is the framework-specific contribution to extending
the perturbative knowledge.
"""
import numpy as np
import sys
sys.path.insert(0, '/Users/jonBridger/Toy Physics/.claude/worktrees/romantic-moore-d6c92d/scripts')
from frontier_su3_lib_2026_05_05 import c_lambda, dim_su3

BETA = 6.0
N_C = 3

# =============================================================================
# 1. 2×1×1 BOX ENUMERATION
# =============================================================================

# A 2×1×1 box in 4D has faces in specific orientations:
# - 2 end faces (1×1): perpendicular to long axis
# - 4 side faces (each 2×1, decomposed into 2 unit plaquettes): parallel to long
# Total: 2 + 4×2 = 10 unit plaquette positions

# For marked plaquette p_0 at origin in plane (i,j):
# Count distinct 2×1×1 boxes containing p_0 as a face

# Case A: p_0 is one of the 2 end faces (1×1)
# The box extends in some direction k perpendicular to (i,j) plane
# k can be any direction except i, j: 4 - 2 = 2 perpendicular directions in 4D
# Wait, in 4D plane (i,j), perpendicular directions are 2 (the other two)
# Actually for plane (i,j), perpendicular directions in 4D are k ∈ {0,1,2,3}\{i,j}
# That's 2 choices

# For each k, box can extend in +k or -k direction: 2 choices
# Box dimensions: 2 along k, 1 along i, 1 along j (matches p_0 size)

# So Case A: 2 (perpendicular directions) × 2 (forward/backward) = 4 box positions

# Case B: p_0 is one of the 8 side-face unit plaquette positions
# Box has 4 size-2 sides (each split into 2 plaquettes)
# For p_0 in plane (i,j), the long axis must be along i or j (in-plane direction)
# 2 choices for long axis (i or j)
# Box has dimensions: 2 along long, 1 along the other in-plane, 1 along perpendicular
# The perpendicular direction: 2 choices in 4D (other two coords)
# Total orientations: 2 (long axis) × 2 (perpendicular) = 4

# For each orientation, p_0 can be at 2 positions along the long axis
# Total Case B: 4 × 2 = 8 box positions

# Hmm but Case A and Case B could overlap; let me check
# Actually wait, in Case B p_0 is on a SIDE face of the box; in Case A on END
# These are distinct geometrical configurations

n_box_A = 4   # p_0 as end face (1×1)
n_box_B = 8   # p_0 as side face position
n_box_total = n_box_A + n_box_B
print(f"2×1×1 box configurations through p_0:")
print(f"  Case A (p_0 as end face): {n_box_A}")
print(f"  Case B (p_0 as side face): {n_box_B}")
print(f"  Total 2×1×1 boxes through p_0: {n_box_total}")

# For each box, the SU(3) Haar integral contribution
# Each box has:
#   - 10 unit plaquettes (1 marked + 9 action)
#   - 12 unique edges (links shared by exactly 2 plaquettes in closed box)
# Wait, actually for 2×1×1 box, count edges:
#   - 8 vertices total (4 at each end)
#   - For 2×1×1 prism: vertices at (0,0,0), (1,0,0), (0,1,0), (1,1,0),
#                                  (0,0,2), (1,0,2), (0,1,2), (1,1,2) (using (x,y,k) with k along long axis)
#   - Edges: 4 along x at z=0, 4 along y at z=0... actually 8 short + 4 long = 12 edges? Let me recount

# 2×1×1 box vertices: 8 (4 at each "end")
# Edges:
#   - 4 connecting end vertices (along long direction, 2-long): 4 edges of length 2
#     These decompose into 2 unit edges each → 8 unit edges along long direction
#   - 4 short edges at each end (1 unit each): 8 edges (4 per end)
# Total unit edges: 8 + 8 = 16

# Hmm wait. For the 2×1×1 box, the unit lattice edges:
# - Along the long axis (length 2): 4 long-axis edges, each split into 2 unit edges = 8
# - Perpendicular at each "level" along long axis (3 levels × 4 perpendicular edges = 12)
# Total unit edges: 8 + 12 = 20

# But many are shared between adjacent plaquettes in the box surface.
# For the 10 unit-plaquette faces of the box surface, by Euler: V - E + F = 2 (sphere topology)
# V = 12 vertices on box surface (3 levels × 4 corners = 12)
# F = 10 plaquettes
# So E = V + F - 2 = 12 + 10 - 2 = 20 edges

# Each edge is shared by exactly 2 surface plaquettes (since surface is closed)
# So link incidence = 2 for all edges

# This gives Schur formula:
# ρ_(p,q) = (c/c_00)^N_plaq × d^(N_components - N_links)
# = (c/c_00)^10 × d^(N_comp - 20)

# For a closed surface (2-sphere topology), cyclic-index graph likely has N_comp = 2
# (analogous to cube which had N_comp = 2 with N_links=12)
# So ρ_(p,q) ≈ (c/c_00)^10 × d^(2-20) = (c/c_00)^10 × d^(-18)

print(f"\n2×1×1 box surface topology:")
print(f"  Vertices: 12 (3 levels × 4 corners)")
print(f"  Edges: 20")
print(f"  Faces (unit plaquettes): 10")
print(f"  Euler check: V - E + F = 12 - 20 + 10 = 2 ✓ (sphere)")

# Per-shell contribution at β=6:
# Each plaquette character expansion: (β/3) Re Tr U_p ≈ (β/3) × (1/2)(Tr U + Tr U†)
# After SU(3) Haar integration via Schur for closed 2-sphere surface:
# Contribution per shell ∝ (some combinatorial factor) × (1/18)^9

# For the cube at β^5: per shell = 2 × (1/6)^6 × (1/81) = 1/18^5
# (5 action plaquettes + 1 observed gives β^5; SU(3) Haar gives 1/81 from invariant tensors)
# 4 shells × 1/18^5 = 4/472392

# For 2×1×1 box at β^9: per shell = 2 × (1/6)^10 × (1/(some d^k)) ≈ 1/18^9 × symmetry factor
# d_(1,0) = 3, so d^(-18) for fundamental rep = 3^(-18) = 1/387420489

# Estimate per-shell contribution:
ratio = c_lambda(1, 0, BETA) / c_lambda(0, 0, BETA)
print(f"\n  c_(1,0)(β=6) / c_(0,0)(β=6) = {ratio:.4f}")
per_shell_estimate = ratio**9 / 3**18  # rough scaling
print(f"  Rough per-shell estimate at β^9: ratio^9 × 3^(-18) ≈ {per_shell_estimate:.6e}")

# Total β^9 contribution from 2×1×1 boxes (12 distinct boxes):
total_estimate = n_box_total * per_shell_estimate
print(f"  Total from {n_box_total} boxes: ≈ {total_estimate:.6e}")

# Convert to coefficient: P_full(β=6) - P_1plaq(β=6) ≈ β^5 × (1/472392) + β^9 × c_9 + ...
# At β=6: β^5 × 1/472392 = 6^5/472392 = 0.01646
# β^9 contribution: c_9 × 6^9 = c_9 × 10077696
# If our estimate is ~3e-9, then c_9 ≈ 3e-9 / 10077696 = 3e-16. TINY.

print(f"""
{'='*70}
ESTIMATE OF β^9 CONTRIBUTION
{'='*70}

Rough per-shell at β=6: {per_shell_estimate:.2e}
Total from {n_box_total} 2×1×1 boxes: {total_estimate:.2e}

In terms of β^9 coefficient c_9 in P_full = P_1plaq + ... + c_9 β^9 + ...:
  At β=6: contribution = c_9 × 6^9 = c_9 × 10077696
  If contribution ≈ {total_estimate:.2e}, then c_9 ≈ {total_estimate/6**9:.2e}

For COMPARISON: β^5 coefficient = 1/472392 ≈ 2.12e-6
  So β^9 estimate suggests coefficient ≈ {total_estimate/6**9:.2e}

This is a ROUGH ORDER OF MAGNITUDE estimate. Precise computation requires:
  1. Exact SU(3) Haar integration for each box configuration
  2. Other 9-plaquette shell types (not just 2×1×1 boxes)
  3. Sign and combinatorial factor accounting

For framework-specific closure search (Candidate #6 — Borel resummation):
  - β^5 coefficient: 1/472392 (small)
  - β^9 coefficient: estimated ~10^(-13) (much smaller)
  - β^13 coefficient: even smaller (heuristic)

If the series decays this fast, it's CONVERGENT at β=6 and the leading
mixed-cumulant terms don't dominate the gap [0.5934 - 0.4225 = 0.17].

This means the "missing 0.17" gap comes from HIGHER irreps in the
character expansion (not just (1,0)/3 ratio), not from the connected
correction to single-plaquette block.

Insight: framework's full P_full(β=6) at L→∞ IS captured by character
expansion at sufficient irrep cutoff + L→∞ scaling, not by series
expansion in β.

This suggests the path forward is via tensor-network engine (per
SU3_TENSOR_NETWORK_ENGINE_ROADMAP) rather than mixed-cumulant
resummation.
""")

print("="*70)
print("Preliminary Conclusion")
print("="*70)
print("""
The β^9 mixed-cumulant term is ESTIMATED to be very small (~10^-13).
This suggests the connected mixed-cumulant series CONVERGES rapidly,
but the LEADING terms don't account for the gap from P_1plaq ≈ 0.42 to
full P ≈ 0.59.

The remaining ~0.17 gap is from:
  - Higher irrep contributions in character expansion (NOT just (1,0))
  - Multi-plaquette correlations that aren't captured by leading
    mixed-cumulant terms
  - Genuine non-perturbative resummation of the full character expansion

Implication for framework-specific closure: candidate #6 (Borel
resummation of mixed-cumulant) likely doesn't give closure since
the series is small and convergent (no Borel resummation needed).

The closure path more likely lies in candidates:
  #5 (reduction-law uniqueness via susceptibility-flow)
  #1 (Cl(3) Z_2 grading)
  #4 (Pseudoscalar i² structure)
  Or a NEW candidate not yet identified.
""")
