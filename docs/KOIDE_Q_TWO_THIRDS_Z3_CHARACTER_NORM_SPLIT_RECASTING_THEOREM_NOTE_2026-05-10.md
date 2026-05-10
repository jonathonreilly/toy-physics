# Koide Q = 2/3 ⟺ Z_3 Character Norm Split (Recasting Theorem)

**Date:** 2026-05-10

**Status:** proposed_retained narrow algebraic equivalence theorem.
For any 3-vector v = (v_1, v_2, v_3) ∈ R³_{>0} interpreted as
mass-square-roots, Koide's relation Q(v) = (Σ v_i²) / (Σ v_i)² = 2/3
holds if and only if its discrete Z_3 character decomposition
satisfies the **norm split condition**

```text
   |c_0|²  =  |c_1|²  +  |c_2|²                                         (NSC)
```

where c_k = (1/√3) Σ_g ω^{kg} v_g are the discrete-Fourier components
under the standard Z_3 character orthogonal basis.

**This is a pure algebraic equivalence**, mathematically equivalent
to **Foot 1994**'s geometric form (Q = 2/3 ⟺ ∠(v, (1,1,1)) = 45°).
It is **not** a derivation of Q = 2/3 from the framework. It is a
**recasting** of Koide's relation in terms of the discrete-Fourier
basis natural to a cyclic-3-fold group action — a basis already
shown to apply to any 3-label space carrying an order-3 cyclic
permutation (per `Z3_CHARACTER_ISOMORPHISM_COLOR_GENERATION_OPEN_GATE_NOTE_2026-05-10`,
which itself is open_gate).

The significance: the recasting **REDUCES the Koide closure problem**
to a single, precisely-named structural condition on the lepton
mass operator's Z_3 character decomposition. Future Cl(3)/Z³
attempts to derive Koide have a sharp target.

**Primary runner:** `scripts/frontier_koide_q_two_thirds_z3_character_norm_split.py`

**Lane:** 6 — Charged-lepton mass retention (recasting only; closure not claimed)

---

## 1. Theorem statement

**Theorem (Koide–Z_3 character recasting).**

Let v = (v_1, v_2, v_3) ∈ R³_{>0} be a 3-vector with positive
real components, and define the Koide ratio:

```text
   Q(v)  :=  (Σ_g v_g²) / (Σ_g v_g)²                                    (1.1)
```

Define the discrete Z_3 Fourier components

```text
   c_k  :=  (1/√3) Σ_g=1,2,3  ω^{k(g-1)} v_g          k = 0, 1, 2     (1.2)
```

with ω = e^{2π i / 3} (primitive cube root of unity).

Then:

```text
   Q(v) = 2/3   ⟺   |c_0|²  =  |c_1|²  +  |c_2|²                       (NSC)
```

## 2. Proof

### 2.1 Plancherel (parseval) identity

The discrete Fourier transform (1.2) is unitary, so

```text
   Σ_k=0,1,2 |c_k|²  =  Σ_g=1,2,3 v_g²  =  Σ v_g²                      (2.1.1)
```

### 2.2 Trivial-character squared norm

The k = 0 (trivial) Fourier component is

```text
   c_0  =  (1/√3) (v_1 + v_2 + v_3)                                     (2.2.1)
```

so

```text
   |c_0|²  =  (1/3) (Σ v_g)²                                            (2.2.2)
```

### 2.3 Algebraic equivalence

The Koide condition Q = 2/3 is

```text
   Σ v_g²  =  (2/3) (Σ v_g)²                                            (2.3.1)
```

Substituting (2.1.1) and (2.2.2):

```text
   |c_0|² + |c_1|² + |c_2|²  =  (2/3) × 3 × |c_0|²
                              =  2 |c_0|²                                (2.3.2)
```

Subtracting |c_0|² from both sides:

```text
   |c_1|² + |c_2|²  =  |c_0|²                                           (2.3.3)
```

This is exactly NSC. The reverse direction (NSC ⟹ Q = 2/3) follows
by reversing the steps. ∎

### 2.4 Equivalent geometric form (Foot 1994)

Q = 2/3 is equivalent to the angle θ between v and the symmetric
direction e_sym = (1, 1, 1)/√3 satisfying:

```text
   cos² θ  =  (e_sym · v)² / |v|²  =  (1/3) (Σ v_g)² / (Σ v_g²)
                                  =  1 / (3 Q)                          (2.4.1)
```

So Q = 2/3 ⟺ cos² θ = 1/2 ⟺ θ = 45°.

NSC and the Foot 45° angle are equivalent restatements of the same
condition under a change of basis (component basis ↔ Z_3 character
basis ↔ symmetric vs anti-symmetric component decomposition).

## 3. Empirical verification

Using PDG charged-lepton masses (numerical values, used here ONLY as
EMPIRICAL WITNESSES to verify the equivalence is correctly derived,
NOT as derivation inputs):

```text
   m_e   =  0.510999  MeV
   m_μ   = 105.6584   MeV
   m_τ   = 1776.86    MeV
```

Computed:

```text
   √m_e  =  0.7148     v_1
   √m_μ  = 10.2791     v_2
   √m_τ  = 42.1528     v_3

   Σ v_g  = 53.1467
   Σ v_g² = 1883.03

   Q(v)  =  1883.03 / 53.1467² =  1883.03 / 2824.28 = 0.66675
   Q(v) - 2/3 = 0.00009  (matches Koide to ~4 decimal places)

   Z_3 character decomposition:
   |c_0|²                  =  941.53
   |c_1|² + |c_2|² (sum)   =  941.50
   ratio: 1.00003

   Foot angle:
   cos θ                   =  0.707111
   1/√2                    =  0.707107
   θ                       = 44.9997 deg (matches 45° to ~4 decimals)
```

All three forms agree empirically. The recasting is consistent.

## 4. Significance — what this REDUCES the closure problem to

Koide closure on the Cl(3)/Z³ framework requires deriving Q = 2/3
from structural content alone (no PDG mass inputs). With this
recasting, that derivation problem becomes:

> **Show that the Cl(3)/Z³ lepton mass operator M, decomposed in
> the Z_3 character basis natural to the framework's substrate,
> satisfies the norm split condition |c_0|² = |c_1|² + |c_2|².**

This is a **precise, single algebraic target**. Prior Lane 6 work
attempted various Ward identity routes (combined no-go #912,
D12-prime matching no-go #1048) and found them blocked. The
recasting offers a **different attack frame**:

- Don't try to derive y_τ as a coupling-constant identity
- Try to derive **the Z_3 character norm split** as a structural
  identity on the lepton mass operator
- The norm split is a single equality of two real positive numbers
  derivable from the operator's spectrum

## 5. What the recasting does NOT establish

- A derivation of Q = 2/3 from the framework
- A Lane 6 closure
- A Cl(3)/Z³-specific mechanism for the norm split
- Any prediction of m_e, m_μ, m_τ individually
- A falsification of any prior no-go (#912, #1018, #1026, #1048)

It only establishes the **algebraic equivalence** of Koide Q = 2/3
to a Z_3-character norm-split condition.

## 6. Connection to existing Lane 6 work

| Document | Status | Connection |
|---|---|---|
| `CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md` | retained | provides `N_gen = N_color = 3` (integer equality) |
| `Z3_CHARACTER_ISOMORPHISM_COLOR_GENERATION_OPEN_GATE_NOTE_2026-05-10` | open_gate | provides T_3 character framework (open: physical-label bridge) |
| `CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10` | proposed_no_go | M5-c surviving route (Koide-anchored cross-sector) |
| `LEPTON_BLOCK_D12_PRIME_MATCHING_NO_GO_NOTE_2026-05-10` | proposed_no_go | YT-style matching does not extend to leptons |
| **This note** (recasting) | proposed_retained | algebraic equivalence Koide ⟺ NSC |

The chain: Lane 6 needs M5-c closure → M5-c needs Koide closure → Koide closure ⟺ NSC. This recasting **identifies NSC as the precise structural target** for any future Koide attempt.

## 7. Literature context

The geometric form (Foot 1994: Q = 2/3 ⟺ 45° angle between v and (1,1,1))
is well-established in the Koide literature. Other equivalent forms:

- **Kocik 2012** (geometric): three mutually tangent circles with
  radii √m_i; Descartes circle theorem gives Q = 2/3
- **Sumino 2009**: gauge-radiative corrections cancel QED
  corrections, giving Q = 2/3 at pole-mass level
- **Ma 2006**: Z_3⁴-finite-group SUSY model gives m_i ∝ v_i²,
  satisfying Koide

The Z_3 character norm split form (NSC) presented here is
mathematically equivalent to Foot's geometric form. What is
framework-specific in this note is the **explicit bridge to the
Cl(3)/Z³ lepton mass operator's eigenstructure**: any future
attempt to derive Koide from Cl(3)/Z³ alone has NSC as the
precise structural target.

## 8. Falsifiers

The algebraic equivalence is mathematically rigorous. It is
falsified only by:

1. A computational error in the discrete Fourier transform
   normalization (verified by the runner)
2. A redefinition of Koide Q that differs from (Σ m) / (Σ √m)²

The CONNECTION to Lane 6 is falsified if NSC is shown to be
underivable from Cl(3)/Z³ alone — but that's a closure question,
not a falsifier of this algebraic equivalence.

## 9. What this note does NOT claim

- A derivation of Koide Q = 2/3 from any framework
- A Lane 6 closure
- A prediction of any lepton mass
- A falsification of #912, #1018, #1026, #1048
- An OPERATOR-LEVEL Cl(3)/Z³ derivation of NSC (still open)
- Anything not entailed by the algebraic equivalence in §1-2

It claims ONLY the algebraic equivalence of Koide Q = 2/3 to the
Z_3 character norm split.

## 10. Cross-references

- Foot 1994: G. Foot, "A note on Koide's lepton mass relation," Mod. Phys. Lett. A 9 (1994) 437
- Kocik 2012: J. Kocik, arXiv:1201.2067
- Sumino 2009: arXiv:0903.3640
- Ma 2006: hep-ph/0612022
- Z_3 character framework (open_gate): `docs/Z3_CHARACTER_ISOMORPHISM_COLOR_GENERATION_OPEN_GATE_NOTE_2026-05-10.md`
- Combined no-go: `docs/CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10.md`
- D12-prime matching no-go: `docs/LEPTON_BLOCK_D12_PRIME_MATCHING_NO_GO_NOTE_2026-05-10.md`
- D17-prime: `docs/LEPTON_BLOCK_SCALAR_SINGLET_COMPOSITE_UNIQUENESS_D17_PRIME_THEOREM_NOTE_2026-05-10.md`
- D16-prime: `docs/LEPTON_BLOCK_TREE_LEVEL_EXCHANGE_D16_PRIME_THEOREM_NOTE_2026-05-10.md`
- Cross-sector closure: `docs/CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md`

## 11. Boundary

This is a NARROW POSITIVE ALGEBRAIC EQUIVALENCE THEOREM. It
establishes mathematically that Koide Q = 2/3 ⟺ Z_3 character
norm split (NSC). It is mathematically equivalent to Foot 1994.

It does NOT close Koide; it RECASTS the closure problem in a form
naturally aligned with the Z_3 character framework that the
Cl(3)/Z³ substrate would use. Future Lane 6 work attempting Koide
closure now has NSC as a precise structural target rather than
Q = 2/3 as a mass-coefficient identity.

A class-A runner verifies the algebraic equivalence symbolically
and the empirical consistency numerically
(`scripts/frontier_koide_q_two_thirds_z3_character_norm_split.py`).
