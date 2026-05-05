"""Migdal-Makeenko equation for the 1×1 plaquette in SU(3) Wilson lattice.

Derived from path-integral invariance under U_l → e^{iε t_a} U_l for each link
l in the plaquette boundary, summed over a = 1..8 (SU(3) generators).

Standard derivation (see Migdal 1968, Wilson 1974, Anderson-Kruczenski 2017):

For Wilson loop W(C) and link l ∈ C:
  0 = ∫DU ∂_l (W(C) e^(-S))
  = ⟨∂_l W(C)⟩ - (β/N) ⟨W(C) ∂_l S⟩

Using SU(N) Fierz identity Σ_a (T_a)_ij (T_a)_kl = (1/2)(δ_il δ_kj - (1/N) δ_ij δ_kl):

For 1×1 plaquette P:
  (N²-1)/(N) · ⟨P⟩ = (β/N) Σ_l Σ_p [⟨W(P ⊕ p)⟩ - (1/N) ⟨W(P) W(p)⟩]
                     - (boundary corrections for links shared with neighbors)

For SU(3) (N=3) at β=6:
  8/3 · ⟨P⟩ = (6/3) · [Σ_p_joined ⟨W(P ⊕ p)⟩ - (1/3) Σ_p ⟨P · W(p)⟩]
             = 2 · [Σ_joined - (1/3) ⟨P · ⟨P⟩⟩]

For each of the 4 links of P, there are 5 plaquettes other than P itself
that contain l (4D hypercubic). Of these:
  - 2 are in the same plane as P (forward/backward in perpendicular direction)
    → joining gives 1×2 rectangles (2 contributions per link)
  - 3 are in 3 different perpendicular planes (out-of-plane)
    → joining gives 3D L-shaped Wilson loops (3 contributions per link)

Total joined loops per plaquette:
  4 links × 5 other plaquettes = 20 joinings
  But many give the same loop by lattice symmetry:
    - All 4 in-plane joinings of same orientation → 1 type (1×2 rect)
    - 4 in-plane joinings of opposite orientation → 1 type (1×2 rect, reversed)
    - 12 out-of-plane joinings → 1 type (3D L-shape) at leading symmetry

So MM equation has at most a few distinct terms.
"""
import numpy as np
import cvxpy as cp
from scipy.special import iv

BETA = 6.0
N_C = 3
N_DIM = 4

def c_lambda(p, q, beta=BETA):
    arg = beta/3.0
    lam = [p+q, q, 0]
    tot = 0.0
    for m in range(-200, 201):
        mat = np.array([[iv(m+lam[j]+i-j, arg) for j in range(3)] for i in range(3)], dtype=float)
        tot += float(np.linalg.det(mat))
    return tot

c00 = c_lambda(0, 0)
c10 = c_lambda(1, 0)
ratio = c10 / (3 * c00)

print("="*68)
print("MIGDAL-MAKEENKO EQUATION FOR 1×1 PLAQUETTE")
print("="*68)
print(f"\nFramework primitives:")
print(f"  N_c = {N_C}, β = {BETA}, dim = {N_DIM}")
print(f"  P_1plaq(β=6) = c_(1,0)/(3·c_(0,0)) = {ratio:.4f}")

# Counting joined plaquettes per link in 4D hypercubic
# Each link is shared by 2(D-1) = 6 plaquettes (in D=4 dim)
# Of these, 1 is the original plaquette P itself
# So 5 "other" plaquettes per link
# 4 links × 5 = 20 joinings per plaquette

joinings_per_link = 2*(N_DIM-1) - 1  # 5 for D=4
total_joinings = 4 * joinings_per_link
print(f"\nLoop joining count:")
print(f"  Each link in 2(D-1) = {2*(N_DIM-1)} plaquettes (4D hypercubic)")
print(f"  Other plaquettes per link: {joinings_per_link}")
print(f"  Total joinings per plaquette: 4 × {joinings_per_link} = {total_joinings}")

# Classify joinings by topology
# In 4D, the 5 other plaquettes per link decompose:
# - Same plane as P, forward in perpendicular direction: 1
# - Same plane as P, backward: 1
# - Different plane (3 perpendicular planes), 1 plaquette each on each side: 3
# Total: 1+1+3 = 5 ✓

# Joining types:
# 1. In-plane forward (1×2 rectangle, same orientation as P)
# 2. In-plane backward (1×2 rectangle, opposite orientation = same physical loop)
# 3. Out-of-plane (3 perpendicular planes, "L-shape" 3D loops)

# By symmetry, all in-plane joinings give same Wilson loop value: ⟨W(1×2)⟩
# All out-of-plane joinings give same value: ⟨W(L-shape)⟩

n_inplane = 2  # 2 in-plane joinings per link (forward + backward)
n_outplane = N_DIM - 2  # 4-2 = 2 perpendicular planes... wait

# Recount more carefully for 4D:
# A link l is in a unique direction (say x)
# Plaquettes containing l: in planes (x,y), (x,z), (x,t) — that's 3 planes
# In each plane, l is on the boundary of 2 plaquettes (one on each side)
# Total: 3 planes × 2 sides = 6 plaquettes ✓

# Now, the original plaquette P has links in directions x,y,z (say P is in xy plane)
# Of the 6 plaquettes containing link l (x-link):
#   - In plane (x,y) (same as P): 2 plaquettes, one is P itself, one is opposite side
#   - In plane (x,z): 2 plaquettes (out-of-plane)
#   - In plane (x,t): 2 plaquettes (out-of-plane)

# So for link l ∈ P:
#   - In-plane joining: 1 (the other (x,y) plaquette adjacent to P)
#     This gives a 1×2 rectangle in xy plane
#   - Out-of-plane joinings: 2 (one each in xz and xt planes)
#     Each gives an L-shape 3D loop

n_inplane = 1   # one in-plane neighboring plaquette per link
n_outplane = 2 * (N_DIM - 2)  # 2 perpendicular planes × 2 sides... wait

# Let me recount once more:
# Link l is x-direction
# Plaquettes containing l in planes (x,μ) for μ = y, z, t (3 planes)
# In each (x,μ) plane: 2 plaquettes (l on either side of plaquette)
# For plane (x,y) — same as P: 1 is P, 1 is "other"
# For plane (x,z): 2 plaquettes (both "other", out-of-plane)
# For plane (x,t): 2 plaquettes (both "other", out-of-plane)
# Total "other" = 1 + 2 + 2 = 5 ✓

n_inplane = 1
n_outplane = 4  # 2 perpendicular planes × 2 sides each
print(f"\nPer-link breakdown:")
print(f"  In-plane joinings (1×2 rectangle): {n_inplane}")
print(f"  Out-of-plane joinings (3D L-shape): {n_outplane}")
print(f"  Total: {n_inplane + n_outplane} = 5 ✓")

# Now write MM equation for 1×1 plaquette in SU(3) at D=4:
# (N²-1)/(N) · 4 · ⟨P⟩ = (β/N) · 4 · [n_inplane · ⟨W(1×2)⟩ + n_outplane · ⟨W(L)⟩]
#                       - (β/N²) · 4 · 5 · ⟨P · W(p)⟩  (Fierz singlet)
#
# The factor 4 comes from summing over the 4 links of P (each gives same equation by symmetry)
#
# Simplifying (cancel 4):
# (N²-1)/N · ⟨P⟩ = (β/N) · [⟨W(1×2)⟩ + 4 ⟨W(L)⟩] - (5β/N²) · ⟨P · ⟨W(p)⟩⟩
#
# For SU(3), N=3, β=6:
# 8/3 · ⟨P⟩ = 2 · [⟨W(1×2)⟩ + 4 ⟨W(L)⟩] - (10/3) · ⟨P · W(p)⟩

print(f"\n{'='*68}")
print(f"MIGDAL-MAKEENKO EQUATION (1×1 plaquette in SU(3) at β=6, D=4)")
print(f"{'='*68}")
print(f"""
After SU(N) Fierz algebra and link-summing:

  (N²-1)/N · ⟨P⟩ = (β/N) · [n_inplane · ⟨W(1×2)⟩ + n_outplane · ⟨W(L)⟩]
                  - (β/N²) · (n_other_plaq_per_link) · ⟨P · ⟨W(p)⟩⟩

For SU(3), N=3, β=6, D=4 (n_inplane=1, n_outplane=4, n_other=5):

  (8/3) · ⟨P⟩ = 2 · ⟨W(1×2)⟩ + 8 · ⟨W(L_3D)⟩ - (10/3) · ⟨P · W(p)⟩_avg

Where:
  ⟨W(L_3D)⟩ = 3D L-shape Wilson loop (out-of-plane joining)
  ⟨P · W(p)⟩_avg = average two-plaquette product (Fierz singlet contribution)

REARRANGING:
  ⟨W(1×2)⟩ + 4 ⟨W(L_3D)⟩ = (4/3) · ⟨P⟩ + (5/3) · ⟨P · W(p)⟩_avg

THIS IS A LINEAR EQUALITY CONSTRAINT for the SDP bootstrap.
""")

# At β=6 with standard MC values:
# ⟨P⟩ = 0.5934, ⟨W(1×2)⟩ ≈ 0.357 (in-plane), ⟨W(L_3D)⟩ ≈ 0.225 (3D L-shape)
# ⟨P · W(p)⟩ ≈ ⟨P⟩² + ⟨P · P⟩_conn ≈ 0.5934² + small ≈ 0.353
P_mc = 0.5934
W12_mc = 0.357
WL_mc = 0.225  # estimate (3D L-shape similar to W(1×3))
P_pp_mc = 0.5934**2 + 0.005

LHS = W12_mc + 4 * WL_mc
RHS = (4/3) * P_mc + (5/3) * P_pp_mc

print(f"Verification with standard MC values:")
print(f"  LHS = ⟨W(1×2)⟩ + 4·⟨W(L_3D)⟩ = {W12_mc} + 4·{WL_mc} = {LHS:.4f}")
print(f"  RHS = (4/3)·⟨P⟩ + (5/3)·⟨P·W(p)⟩ = {(4/3)*P_mc:.4f} + {(5/3)*P_pp_mc:.4f} = {RHS:.4f}")
print(f"  Difference: {LHS - RHS:+.4f}")
print(f"  (NOTE: ⟨W(L_3D)⟩ estimate; actual value uncertain. The MM equation has additional")
print(f"   terms I may have approximated. For TIGHT SDP constraint, need more careful")
print(f"   coefficient derivation. This is the proof-of-concept structure.)")

print(f"\n{'='*68}")
print(f"NEXT IMPLEMENTATION STEPS")
print(f"{'='*68}")
print("""
1. **Verify MM coefficients rigorously** against Anderson-Kruczenski 2017:
   - The Fierz singlet term has specific (1/N²) coefficient I may have off
   - The total link factor and signs need careful sign-tracking
   - Out-of-plane "L-shape" loop matrix element needs explicit definition

2. **Add to SDP solver as equality constraint**:
   In CVXPY:
     constraints.append(W12 + 4*W_L == (4/3)*P + (5/3)*P_W_p_avg)

3. **Test how much it tightens the analytic bound**:
   - Currently [0.439, 1.000] (loose)
   - With one MM equation, expect tightening (maybe to [0.45, 0.85])
   - With multiple MM equations (1×2, 2×2 loops), tighter still

4. **Iterate on more MM equations** for larger Wilson loops:
   - Each new equation gives one more linear constraint
   - Gram matrix grows; SDP becomes tighter

5. **Cross-check against Anderson-Kruczenski / Kazakov-Zheng results**:
   - At N_loops=6, expect ~3% bound (matches their result)
   - Standard MC L→∞ value 0.5934 should fall in bound
""")
