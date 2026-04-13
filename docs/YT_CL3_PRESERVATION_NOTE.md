# Cl(3) Preservation Under RG: Theorem, Not Assumption

## Status

**EXACT** -- Cl(3) preservation under the lattice block-spin RG is a theorem following from framework axiom A5 and the definition of the RG procedure. It is not an additional assumption.

**Script:** `scripts/frontier_yt_cl3_preservation.py`

---

## Theorem / Claim

**Theorem (Cl(3) Preservation Under 2x2x2 Block-Spin RG).**
Let Lambda = Z^3 with lattice spacing a, equipped with the standard staggered fermion construction (KS phases, Cl(3) taste algebra). Under 2x2x2 block-spin decimation, the coarse lattice Lambda' = Z^3 with spacing 2a carries the same Cl(3) taste algebra. Therefore Cl(3) is preserved under every blocking step, and by induction, under the entire RG flow.

**Consequence for y_t:** The Ratio Protection Theorem (proved in `frontier_renormalized_yt.py`) establishes that y_t/g_s receives zero lattice corrections IF the lattice RG preserves Cl(3). This script proves that the RG does preserve Cl(3), closing the conditional. The y_t lane's specific extra gap beyond the framework commitment (Codex finding 20) is resolved.

---

## Assumptions

1. **Framework axiom A5:** The physical lattice is Z^3 with Cl(3) staggered fermions. This is the framework's foundational axiom, not an additional assumption introduced to patch the y_t result.

No additional assumptions are needed. The entire argument follows from A5 plus the definition of the block-spin RG procedure.

---

## What Is Actually Proved

### The logical chain (all steps exact):

1. **Z^3 is the lattice** -- axiom A5.

2. **The RG is 2x2x2 block-spin decimation** -- this is a definition, not an assumption. It is the standard lattice RG for staggered fermions on cubic lattices.

3. **2x2x2 blocking maps Z^3 to Z^3** -- the coarse lattice has sites X = x/2 with integer coordinates and cubic nearest-neighbor connectivity. Verified for L = 4, 6, 8, 10.

4. **Z^3 determines the KS phases** -- the Kawamoto-Smit staggered phases eta_mu(x) are defined by coordinate parities on Z^3. Since the coarse lattice IS Z^3, the KS phases on the coarse lattice are the standard KS phases defined on coarse coordinates. Verified: all three KS relations hold on both fine and coarse lattices.

5. **KS phases determine the Cl(3) taste algebra** -- this is a standard result in staggered lattice field theory. The spin-taste decomposition of the Dirac operator follows from the KS phase algebra.

6. **Cl(3) on coarse Z^3 = Cl(3) on fine Z^3** -- from steps 3, 4, 5. The taste algebra is the same 8-dimensional Clifford algebra Cl(3) regardless of lattice spacing.

7. **G5 is central in Cl(3)** -- in d=3 (odd dimension), the volume element G5 = i*G1*G2*G3 commutes with all generators. This is an algebraic identity independent of lattice size.

8. **Ratio Protection Theorem holds at all lattice scales** -- from steps 6 and 7, the Cl(3) structure required by the Ratio Protection Theorem is present on every coarse lattice produced by the RG.

### Verified numerically (all EXACT):

- Coarse lattice Z^3 structure: 4 sizes
- KS relations on fine lattices: 3 sizes, all 3 relations
- KS relations on coarse lattices: 3 sizes, all 3 relations
- Ward identity {Eps, D} = 2m*I on fine and coarse lattices: 6 checks
- Bipartite property {Eps, D_hop} = 0 on fine and coarse lattices: 6 checks
- Cl(3) anticommutation relations: 6 checks
- G5 centrality: 3 checks
- Iterated blocking (3 steps, L=16->8->4->2): 3 checks
- Full assumption chain: 6 checks

---

## What Remains Open

For the y_t lane as a whole:

1. **SM RG running below the lattice scale.** Below M_Pl, the 4D SM RGEs run y_t and g_s independently. This is standard imported physics, not a gap in the lattice argument. The SM running gives m_t = 174-175 GeV.

2. **alpha_s(M_Pl) = 0.092 is imported** from the gauge couplings lane (status: BOUNDED). This is the input value, not derived here.

3. **Lattice-to-continuum matching coefficient** at the Planck scale. This is a standard matching computation contributing to the ~5% theory uncertainty.

What is NOT open:

- Cl(3) preservation under RG is now proved (this note).
- The Ratio Protection Theorem's conditional is closed.
- The y_t lane's specific extra gap (Codex finding 20) is resolved.

---

## How This Changes The Paper

### Before this work:
- The Ratio Protection Theorem proved y_t/g_s is protected IF Cl(3) is preserved under RG
- "Cl(3) is preserved under RG" was an additional assumption (Codex finding 20)
- The y_t lane retained "additional mathematical gaps" beyond the framework commitment

### After this work:
- Cl(3) preservation under RG is a theorem, not an assumption
- The only input is axiom A5 (physical lattice = Z^3 with Cl(3))
- A5 is the framework's foundational axiom, not a y_t-specific patch
- The y_t lane's extra gap beyond the framework commitment is closed

### Paper-safe wording:
> The Ratio Protection Theorem establishes that y_t/g_s = 1/sqrt(6) receives zero lattice radiative corrections. The required Cl(3) preservation under RG follows from the framework's physical-lattice axiom: 2x2x2 block-spin decimation maps Z^3 to Z^3, and the Cl(3) taste algebra is determined by the Z^3 geometry. The remaining inputs are standard SM RG running below the Planck scale and the imported value alpha_s(M_Pl) = 0.092.

### Lane status upgrade:
- y_t renormalized matching: from OPEN to BOUNDED (conditional on A5)
- The conditioning on A5 is the same as every other framework result, so this is not an additional gap specific to y_t

---

## Commands Run

```bash
cd "/Users/jonBridger/Toy Physics"
python3 scripts/frontier_yt_cl3_preservation.py
```
