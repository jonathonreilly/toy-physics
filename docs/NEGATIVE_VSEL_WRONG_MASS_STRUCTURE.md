# NEGATIVE: V_sel-Fermion Coupling Does Not Produce SM Three-Generation Mass Structure

**Status:** AIRTIGHT NEGATIVE — closed-form algebraic proof
**Method:** compute mass matrix eigenvalues from V_sel coupling at EWSB vacuum

## The claim

The natural fermion-V_sel coupling
```
L_int = y Σ_i φ_i (ψ̄ S_i ψ)
```
with S_i the canonical cube-shift operators, at the EWSB vacuum
φ_* = (0, 0, v), does NOT generate three hierarchical fermion mass
eigenvalues as required for SM generations.

## The derivation (pure algebra)

### Step 1: Tree-level mass from vacuum

At φ_* = (0, 0, v):
```
L_vacuum = y v (ψ̄ S_3 ψ)
```

Project onto hw=1 sector {X_1, X_2, X_3} = {|100⟩, |010⟩, |001⟩}:
```
⟨X_a | S_3 | X_b⟩ = 0 for all a, b in hw=1
```
(since S_3 flips the 3rd bit, moving hw=1 states to hw=0 or hw=2).

**Projected tree-level hw=1 mass matrix: M_tree = 0.**

### Step 2: One-loop effective mass from δφ exchange

```
M_eff(a, b) = y² Σ_{i,j} ⟨X_a | S_i S_j | X_b⟩ · Π_{ij}
```
with δφ propagators Π_{ij} = δ_{ij} / m²(δφ_i).

Mass spectrum of δφ at vacuum (0, 0, v) (from V_sel Hessian):
- m²(δφ_1) = m²(δφ_2) = 64 v² (massive, transverse)
- m²(δφ_3) = 0 (flat, along selected axis)

### Step 3: Matrix elements ⟨X_a | S_i S_j | X_b⟩

Direct algebra on the cube basis:

Diagonal (a = b):
- ⟨X_a | S_i² | X_a⟩ = 1 (since S_i² = I)
- ⟨X_a | S_i S_j | X_a⟩ = 0 for i ≠ j (S_j |X_a⟩ then S_i must return to |X_a⟩)

Off-diagonal (a ≠ b): only {i, j} = {a, b} gives non-zero entries.

### Step 4: Apply the flat-mode constraint

If δφ_3 is NOT a dynamical field (constrained by the SSB structure):
only δφ_1, δφ_2 exchanges contribute.

Then the non-zero off-diagonal entries involve {S_1, S_2}. Only
X_1 ↔ X_2 couples via S_1 S_2 (+ S_2 S_1).

X_1 ↔ X_3 (requires S_1 S_3 or S_3 S_1): FORBIDDEN (needs δφ_3).
X_2 ↔ X_3 (requires S_2 S_3 or S_3 S_2): FORBIDDEN.

### Step 5: The effective mass matrix

With α = y² / (64 v²)² as overall coefficient:
```
           [ 1   1   0 ]
M_eff = α  [ 1   1   0 ]
           [ 0   0   1 ]
```

### Step 6: Eigenvalues (closed form)

The upper-left 2×2 block [[1, 1], [1, 1]] has eigenvalues (2, 0).
The lower-right 1×1 block [1] has eigenvalue 1.

**Eigenvalues of M_eff:** {2α, α, 0}.

## The obstruction

The observed SM has three HIERARCHICAL masses (e.g., up-type:
m_u < m_c < m_t with m_t/m_u ~ 10^5). The V_sel mechanism gives
the structure {2α, α, 0} — a 2+1 pattern with ONE MASSLESS state,
not three hierarchical masses.

In particular:
- The antisymmetric combination (|X_1⟩ - |X_2⟩)/√2 has eigenvalue 0
  (massless)
- The symmetric combination (|X_1⟩ + |X_2⟩)/√2 has eigenvalue 2α
- The weak-axis state |X_3⟩ has eigenvalue α

**This structure does not correspond to the observed SM fermion mass
spectrum.**

## Conclusion

The V_sel selector potential, despite being airtight as an EWSB
mechanism, CANNOT serve as the sole generator of the SM three-
generation fermion mass matrix when coupled to fermions in the
natural form L_int = y Σ φ_i ψ̄ S_i ψ.

## What this does NOT rule out

1. V_sel + ADDITIONAL mechanism (e.g., explicit Yukawa couplings to
   a separate Higgs field with specific flavor structure).
2. More complex fermion-V_sel couplings (e.g., derivative couplings,
   or couplings involving S_i S_j tensors explicitly).
3. V_sel operating at a different role (e.g., providing the weak
   AXIS selection rather than generating mass hierarchy).

Any successful derivation of SM fermion masses from the framework
would require going BEYOND the simple V_sel-fermion coupling
analyzed here.

## What this establishes as rigorous negative

The natural minimal V_sel-fermion coupling is INSUFFICIENT for the
SM mass structure. Any framework claim relying on this specific
mechanism as the source of mass hierarchy is falsified.
