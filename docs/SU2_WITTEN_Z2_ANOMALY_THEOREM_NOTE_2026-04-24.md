# SU(2) Witten Z₂ Global Anomaly Cancellation Theorem

**Date:** 2026-04-24
**Status:** **retained standalone structural-anomaly theorem** on `main`. Extracts and packages as its own theorem the global SU(2) Z₂ Witten-anomaly cancellation, which appears only as a single-line entry in [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) Step 1 ("Witten SU(2) (doublets) | 4 (even) | OK") and is not separately retained as a row. The Witten anomaly is *non-perturbative* and *topological* — distinct from the perturbative `Tr[Y]`, `Tr[Y³]`, `Tr[SU(3)² Y]`, `Tr[SU(2)² Y]` conditions already covered there — and so deserves its own retained status.
**Primary runner:** `scripts/frontier_su2_witten_z2_anomaly.py`

---

## 0. Statement

**Theorem (SU(2) Witten Z₂ global anomaly cancellation).** The fourth homotopy group of SU(2) is

```text
π_4(SU(2))  ≅  ℤ_2.
```

For an SU(2) gauge theory with `N_D` chiral Weyl fermion doublets (counted including colour multiplicities and any mirror/conjugate pairs), the path integral is well-defined as a **global** topological consistency condition iff

```text
N_D  ≡  0   (mod 2).                                              (W)
```

On the retained one-generation SM content, the SU(2) doublet count per generation is

```text
N_D^{(1 gen)}  =  3 (Q_L colours)  +  1 (L_L)  =  4    ⟹  4 ≡ 0 (mod 2).   ✓
```

Across the retained three generations:

```text
N_D^{(3 gen)}  =  3 × 4  =  12        ⟹  12 ≡ 0 (mod 2).                   ✓
```

The Witten Z₂ anomaly therefore vanishes identically on the retained three-generation SM content. SU(2) gauge invariance is consistent at the global topological level, and the framework is free of this non-perturbative obstruction.

## 1. Retained inputs

| Ingredient | Reference |
|------------|-----------|
| Native SU(2) gauge structure | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) |
| Retained Q_L, L_L SU(2)-doublet content | [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) |
| Retained N_c = 3 colours | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) |
| Retained three-generation structure | [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md) |
| Retained anomaly-forces-time existence of RH SU(2)-singlet completion | [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) |
| π_4(SU(2)) = ℤ_2 | classical homotopy theory; Witten 1982, "An SU(2) anomaly", Phys. Lett. B 117, 324 |

## 2. Background: Witten's argument

Witten (1982) showed that the SU(2) path integral picks up a sign under a "large" gauge transformation associated with the non-trivial element of `π_4(SU(2)) = ℤ_2`. For a single Weyl fermion doublet, this contributes a factor of `−1` to the partition function, rendering it ill-defined. With `N_D` doublets, the factor is `(−1)^{N_D}`. Cancellation requires `N_D` even.

This is a **non-perturbative** anomaly. Unlike the Adler–Bell–Jackiw perturbative anomalies, it does *not* show up at any finite order in Feynman diagrams. It is invisible to the standard `Tr[T^a T^b T^c]` calculation.

The cancellation condition is binary (mod 2). Adding any odd-multiplicity SU(2)-doublet matter content breaks consistency.

## 3. Derivation on retained content

### 3.1 Per-generation count

The retained one-generation SU(2) doublet content is exactly:

| Field | SU(3) | SU(2) | colour mult | weak doublet count |
|-------|-------|-------|-------------|--------------------|
| `Q_L` | 3 | 2 | 3 | **3** (one doublet per colour) |
| `L_L` | 1 | 2 | 1 | **1** |
| `u_R` | 3 | 1 | 3 | 0 (singlet) |
| `d_R` | 3 | 1 | 3 | 0 |
| `e_R` | 1 | 1 | 1 | 0 |
| `ν_R` | 1 | 1 | 1 | 0 |

Per-generation total of SU(2) doublets:

```text
N_D^{(1 gen)}  =  3 + 1  =  4
```

`4 ≡ 0 (mod 2)`. The Witten Z₂ anomaly cancels per generation.

### 3.2 Three-generation count

The retained three-generation structure replicates the one-generation content three times (per [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md) orbit algebra `8 = 1 + 1 + 3 + 3`):

```text
N_D^{(3 gen)}  =  3 × 4  =  12.
```

`12 ≡ 0 (mod 2)`. The Witten Z₂ anomaly cancels at the three-generation level.

### 3.3 Cancellation per generation is structurally automatic

Because `Q_L` has colour 3 (odd) and `L_L` has colour 1 (odd), each generation contributes `3 + 1 = 4` doublets. The sum of two odd integers is always even, so:

```text
N_D^{(1 gen)}  =  N_c + 1  =  3 + 1  =  4   (always even when N_c is odd).
```

This is a **structural** parity coincidence: it works because of the precise interplay between the retained `N_c = 3` colour count (odd) and the lepton sector's single doublet (also odd). If the framework had had `N_c = 4` colours (even), the per-generation count would be `4 + 1 = 5` (odd), giving Witten anomaly = 1 mod 2 — the theory would be inconsistent. So the parity cancellation is non-trivial.

## 4. Falsification scenarios

The theorem is binary, so the falsification surface is sharp:

| Hypothetical content | `N_D` per gen | mod 2 | Witten consistent? |
|-----------------------|----------------|-------|---------------------|
| Standard SM (this theorem): Q_L + L_L | 4 | 0 | ✓ |
| Add a 4th-gen quark doublet (no lepton) | 7 | 1 | ✗ ANOMALOUS |
| Add only an extra L_L | 5 | 1 | ✗ ANOMALOUS |
| Add a Q_L + a singlet (e.g. dark quarks) | 7 | 1 | ✗ ANOMALOUS |
| Mirror world: Q_L + L_L + Q_R + L_R as doublets | 8 | 0 | ✓ (mirror cancels) |
| 4-color extension with N_c = 4: Q_L^{(4-col)} + L_L | 5 | 1 | ✗ ANOMALOUS |

The retained `N_c = 3` is structurally pinned by the graph-first SU(3) closure ([`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)) and three generations is retained ([`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md)). So the falsification surface is precisely those alternatives — none of which are realized in the retained framework.

## 5. Bosonic Higgs doublet does NOT enter

The Higgs is an SU(2) doublet, but it is a **boson**, not a Weyl fermion. The Witten anomaly arises specifically from the chiral path-integral measure of Weyl fermions in the SU(2) doublet representation. Bosonic doublets contribute to other anomalies (e.g., gauge boson loops in perturbative anomalies) but **not** to the Witten Z₂.

So adding the SM Higgs doublet does not change the Witten count: `N_D^{Witten} = 12` (fermionic only) on the retained three-generation content.

## 6. Consequences

### 6.1 SU(2) consistency at global topological level

The retained framework's SU(2) gauge sector is consistent at the **non-perturbative, global, topological** level — distinct from the perturbative anomaly cancellation already retained in [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md).

### 6.2 Restriction on extensions

Any retained-framework extension that adds chiral SU(2)-doublet content must add an even number of doublets per generation. This rules out:
- Single 4th-generation quark doublet (without companion lepton)
- Sterile SU(2)-doublet "dark sector"
- Any unbalanced doublet addition

### 6.3 Consistency check on three-generation closure

The retained three-generation structure (`8 = 1 + 1 + 3 + 3` orbit algebra) gives 3 generations, with each carrying 4 SU(2) doublets, totalling 12. Since 12 is even, three-generation closure is automatically Witten-consistent.

A *one-generation* framework would also be Witten-consistent (4 ≡ 0 mod 2), as would any *odd-number-of-generations* framework. The integer count must merely be even.

### 6.4 The bosonic Higgs is not constrained by Witten

The Higgs doublet is bosonic and does not add to `N_D^{Witten}`. So the Witten anomaly cancellation does not constrain the number of Higgs doublets (1 in standard SM, 2 in 2HDM, etc.).

## 7. Scope and boundary

**Claims:**

- (W) `N_D ≡ 0 (mod 2)` is the necessary global topological condition.
- Per-generation `N_D = 4` on retained content.
- Three-generation total `N_D = 12 ≡ 0 (mod 2)`.
- Cancellation is automatic and structural at the per-generation level.

**Does NOT claim:**

- Cancellation in non-SU(2) sectors (other group anomalies are separate).
- Anything about the Higgs doublet (bosonic).
- Constraints on SU(3)³ or other gauge-only cubic anomalies (which vanish for separate reasons — vector-like content).
- Native-axiom uniqueness of `N_c = 3` (that's [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)).
- That `N_D = 4` per gen is the *minimum* — adding more even counts would also work.

## 8. Falsifiability

Sharp and binary:

- Discovery of any new chiral SU(2)-doublet matter giving an odd total `N_D` would falsify the framework's gauge consistency.
- Current LHC data: no fourth-generation quark or anomalous SU(2)-doublet content beyond the SM. Framework consistent.
- LHC + future colliders sharpen the bound; any unbalanced doublet addition at high luminosity is excluded by direct search.

## 9. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_su2_witten_z2_anomaly.py
```

Expected: all checks pass.

The runner:

1. Enumerates the retained one-generation SU(2)-doublet content with multiplicities.
2. Verifies `N_D^{(1 gen)} = 4` and `4 ≡ 0 (mod 2)`.
3. Multiplies by 3 generations: `N_D^{(3 gen)} = 12`, verifies even.
4. Tests falsification scenarios (4th-gen quark only, dark doublet only, etc.) and confirms each gives odd `N_D` → anomaly.
5. Verifies the structural parity argument: `N_c + 1 = 3 + 1 = 4` always even when `N_c` odd.
6. Confirms bosonic Higgs doublet does not enter the count.

## 10. Cross-references

- [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) — Witten Z_2 mentioned as a single line in the table; full theorem packaging is here
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) — covers the perturbative anomaly conditions
- [`BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md`](BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md) — parallel B-L global symmetry anomaly closure (perturbative not Witten)
- [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) — retained native SU(2)
- [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md) — retained 3-generation
- Witten 1982, "An SU(2) anomaly", Phys. Lett. B 117, 324 — original paper
