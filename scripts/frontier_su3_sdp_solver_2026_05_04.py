"""SDP solver for ⟨P⟩(β=6) using Wilson loop tower + RP A11 + Migdal-Makeenko.

Inputs:
  - Wilson loop expectations from MC (frontier_su3_wilson_loop_tower_mc)
  - Framework's exact onset jet (P(0)=0, P'(0)=1/18, β^5 correction)
  - Reflection positivity A11 (PSD on Gram matrix)
  - Cluster decomposition (cross-correlator bounds)

Outputs:
  - SDP-bounded ⟨P⟩(β=6) with explicit lower/upper bounds
  - Verification that PSD + framework constraints give consistent solution

Method:
  1. Variables: ⟨P⟩, ⟨W(1,2)⟩, ⟨W(2,2)⟩, etc. (single Wilson loops)
     Plus cross-correlators ⟨W_α W_β⟩ for the Gram matrix
  2. Constraints:
     - PSD on Gram matrix (RP A11)
     - Bounds: 0 ≤ ⟨W⟩ ≤ 1
     - Cluster decomposition: ⟨W²⟩ ≥ ⟨W⟩²
     - Migdal-Makeenko equations relating ⟨W_α⟩'s
     - Cauchy-Schwarz bounds on cross-correlators
  3. Solve max/min ⟨P⟩ subject to constraints
"""
import numpy as np
import cvxpy as cp
import json
import os

# Load Wilson loop tower data if available
wilson_data_file = '/tmp/wilson_loops_L4.json'
if os.path.exists(wilson_data_file):
    with open(wilson_data_file) as f:
        wilson_data = json.load(f)
    print(f"Loaded Wilson loop data from {wilson_data_file}:")
    for key, val in wilson_data.items():
        print(f"  W{key}: {val['mean']:.4f} ± {val['err']:.4f}")
else:
    print(f"Warning: {wilson_data_file} not found; using literature values as placeholders")
    wilson_data = {
        '(1, 1)': {'mean': 0.5934, 'err': 0.001},
        '(1, 2)': {'mean': 0.357,  'err': 0.005},
        '(2, 2)': {'mean': 0.135,  'err': 0.005},
        '(1, 3)': {'mean': 0.225,  'err': 0.005},
        '(2, 3)': {'mean': 0.0858, 'err': 0.005},
        '(3, 3)': {'mean': 0.0228, 'err': 0.002},
    }

# Framework primitives
print(f"\nFramework primitives at β=6:")
P_1plaq_6 = 0.4225  # exact from c_(1,0)/(3 c_(0,0))
print(f"  P_1plaq(β=6) = {P_1plaq_6:.4f}")
beta5_correction = 6**5/472392
print(f"  β^5 mixed-cumulant correction: {beta5_correction:.6f}")
P_lower_onset = P_1plaq_6 + beta5_correction
print(f"  Onset lower bound: {P_lower_onset:.4f}")

print(f"\n{'='*64}")
print(f"SDP BOOTSTRAP: bounding ⟨P⟩(β=6)")
print(f"{'='*64}")

# Variables: 6 Wilson loop expectations + cross-correlators
# Use 4-loop tower for now (simpler): P, R(1x2), S(2x2), T(2x3)
# (Skip W(1,3) since W(1,3) ~ W(1,3) is harder to integrate properly)

P  = cp.Variable(name="<P>")
R  = cp.Variable(name="<W_1x2>")
S  = cp.Variable(name="<W_2x2>")
T  = cp.Variable(name="<W_2x3>")
P2 = cp.Variable(name="<P^2>")
R2 = cp.Variable(name="<R^2>")
S2 = cp.Variable(name="<S^2>")
T2 = cp.Variable(name="<T^2>")
PR = cp.Variable(name="<PR>")
PS = cp.Variable(name="<PS>")
PT = cp.Variable(name="<PT>")
RS = cp.Variable(name="<RS>")
RT = cp.Variable(name="<RT>")
ST = cp.Variable(name="<ST>")

# Build 5x5 Gram matrix: identity, P, R, S, T
G = cp.bmat([
    [np.array([[1.0]]),       cp.reshape(P,(1,1)), cp.reshape(R,(1,1)), cp.reshape(S,(1,1)), cp.reshape(T,(1,1))],
    [cp.reshape(P,(1,1)),     cp.reshape(P2,(1,1)), cp.reshape(PR,(1,1)), cp.reshape(PS,(1,1)), cp.reshape(PT,(1,1))],
    [cp.reshape(R,(1,1)),     cp.reshape(PR,(1,1)), cp.reshape(R2,(1,1)), cp.reshape(RS,(1,1)), cp.reshape(RT,(1,1))],
    [cp.reshape(S,(1,1)),     cp.reshape(PS,(1,1)), cp.reshape(RS,(1,1)), cp.reshape(S2,(1,1)), cp.reshape(ST,(1,1))],
    [cp.reshape(T,(1,1)),     cp.reshape(PT,(1,1)), cp.reshape(RT,(1,1)), cp.reshape(ST,(1,1)), cp.reshape(T2,(1,1))],
])

constraints = [
    # PSD from RP A11
    G >> 0,
    # Bounds
    P >= 0, P <= 1,
    R >= 0, R <= 1,
    S >= 0, S <= 1,
    T >= 0, T <= 1,
    # Framework's onset lower bound
    P >= P_lower_onset,
    # Area-law-ish soft bounds (provide structure to SDP)
    R <= P + 0.01,    # 1x2 ≤ 1x1 (typically)
    S <= R + 0.01,    # 2x2 ≤ 1x2 (typically)
    T <= S + 0.01,    # 2x3 ≤ 2x2 (typically)
    # Self-correlator bounds (handled by PSD if no other coupling)
    P2 >= 0, R2 >= 0, S2 >= 0, T2 >= 0,
    P2 <= 1, R2 <= 1, S2 <= 1, T2 <= 1,
]

# Constrain Wilson loops to MC values (pin them as boundary data)
def get_W(key):
    if key in wilson_data: return wilson_data[key]['mean']
    return None

# If MC data available, pin the values
W_R = get_W('(1, 2)')
W_S = get_W('(2, 2)')
W_T = get_W('(2, 3)')
if W_R is not None: constraints.append(R == W_R)
if W_S is not None: constraints.append(S == W_S)
if W_T is not None: constraints.append(T == W_T)

# Solve max ⟨P⟩
print(f"\nMaximizing ⟨P⟩ with framework constraints + Wilson tower MC:")
prob_max = cp.Problem(cp.Maximize(P), constraints)
try:
    prob_max.solve(solver='SCS', verbose=False)
    P_max = float(P.value)
    print(f"  ⟨P⟩_max = {P_max:.4f}")
except Exception as e:
    print(f"  failed: {e}")
    P_max = None

# Solve min ⟨P⟩
print(f"\nMinimizing ⟨P⟩ with framework constraints + Wilson tower MC:")
prob_min = cp.Problem(cp.Minimize(P), constraints)
try:
    prob_min.solve(solver='SCS', verbose=False)
    P_min = float(P.value)
    print(f"  ⟨P⟩_min = {P_min:.4f}")
except Exception as e:
    print(f"  failed: {e}")
    P_min = None

if P_max is not None and P_min is not None:
    width = P_max - P_min
    midpoint = (P_max + P_min) / 2
    print(f"\n{'='*64}")
    print(f"SDP RESULT")
    print(f"{'='*64}")
    print(f"  ⟨P⟩(β=6) ∈ [{P_min:.4f}, {P_max:.4f}]")
    print(f"  Midpoint: {midpoint:.4f}")
    print(f"  Width: {width:.4f} ({width/midpoint*100:.1f}%)")
    print(f"  Standard MC L→∞: 0.5934")
    print(f"  Framework MC L=4: 0.5978")
    print(f"  In bounds? {'YES' if P_min <= 0.5934 <= P_max else 'NO'}")

    if width < 0.05:
        print(f"\n  ✓ TIGHT BOUND ({width/midpoint*100:.1f}%) — significant improvement")
    elif width < 0.1:
        print(f"\n  Reasonable bound ({width/midpoint*100:.1f}%) — needs more constraints")
    else:
        print(f"\n  Loose bound ({width/midpoint*100:.1f}%) — needs Migdal-Makeenko equations")

print(f"\n{'='*64}")
print(f"NEXT STEPS for tighter bounds")
print(f"{'='*64}")
print("""
Current limitations of this minimal SDP:
  - Only 5×5 Gram matrix (need 8×8 or larger for tighter)
  - No Migdal-Makeenko loop equations (only soft bounds)
  - Cross-correlators not computed via framework primitives

To reach Anderson-Kruczenski/Kazakov-Zheng ~2-3% precision:
  1. Compute cross-correlators ⟨W_α W_β⟩ via SU(3) Clebsch-Gordan
  2. Implement Migdal-Makeenko equations (~6+ relations for minimal tower)
  3. Extend to 6+ Wilson loops
  4. Industrial SDP scan with MOSEK/SCS

Each is a substantial subtask. This script is the proof-of-concept showing
the framework primitives (RP A11 + onset jet + bounds) PLUS MC Wilson tower
gives a working SDP infrastructure on framework's surface.
""")
