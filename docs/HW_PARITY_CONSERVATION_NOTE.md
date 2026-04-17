# Hamming-Weight Parity Conservation Under Site-Phase Polynomials

**Status:** AIRTIGHT — combinatorial argument + Hamming-distance selection rule
**Runner:** `scripts/frontier_hw_parity_conservation.py` (68/68 PASS)
**Reusability:** high — parity-based block-decomposition of BZ-corner
operators built from site-phase products.

## Classical results applied

- **Z_2 projector decomposition** Π_± = (1 ± U)/2 for any involution
  U with U² = I (standard linear algebra).
- **Grading / parity argument** for polynomial algebras: even-degree
  monomials preserve a Z_2 grading and odd-degree monomials flip it
  (textbook).
- **Hamming-distance selection rule** from Batch 1 for the action of
  site-phase polynomials on BZ corners.

## Framework-specific step

- Identification of the total-parity involution T_1 T_2 T_3 on
  C^{L³} as the operator whose eigenspace decomposition coincides
  with the even/odd Hamming-weight decomposition of the BZ-corner
  subspace.

## Theorem

Let P_1, P_2, P_3 be the site-phase operators on C^{L³} (L even),
with (P_μ ψ)(x) = (−1)^{x_μ} ψ(x), and let M be a polynomial in them
with monomial expansion
```
M = Σ_k c_k · P_{μ_1^{(k)}} ... P_{μ_{n_k}^{(k)}}.
```
Then:

1. **Matrix-element parity:** for each monomial of order n,
   ⟨X_β | P_{μ_1} ... P_{μ_n} | X_α⟩ is nonzero only if
   α ⊕ β = ⊕_i e_{μ_i}; hence H(α ⊕ β) ≡ n mod 2.
   Equivalently, H(α) and H(β) have the same parity iff n is even.

2. **Even-order preservation:** if every monomial of M has even order,
   M preserves the hw-parity decomposition
   ```
   C^{L³}_{BZ corners} = C^8_{even-hw} ⊕ C^8_{odd-hw}
   ```
   (each of dimension 4).

3. **Odd-order swapping:** if every monomial has odd order, M swaps
   the two hw-parity subspaces.

4. **Explicit parity projectors:**
   ```
   Π_± = (1 ± T_1 T_2 T_3) / 2
   ```
   where T_μ is the translation operator (T_μ |X_α⟩ = (−1)^{α_μ}|X_α⟩
   from the translation-eigenvalue theorem).

## Proof

Key combinatorial fact (Part 1 of runner): for any index sequence
(μ_1, ..., μ_n), the XOR ⊕_i e_{μ_i} has Hamming weight of parity n
(because each e_{μ_i} has weight 1 and XOR cancellations come in pairs).

Combined with the Hamming-distance selection rule (⟨X_β|P_{μ_1}...
P_{μ_n}|X_α⟩ ≠ 0 iff α ⊕ β = ⊕_i e_{μ_i}), this gives:
```
⟨X_β|P^n(μ)|X_α⟩ ≠ 0 ⇒ H(α ⊕ β) ≡ n mod 2.
```

Since H(α) + H(β) ≡ H(α ⊕ β) mod 2 (twice-the-intersection is even),
nonzero matrix elements require H(α), H(β) to share parity ⇔ n even,
or differ in parity ⇔ n odd.

The parity projectors Π_± work because T_1 T_2 T_3 has eigenvalue
(−1)^{α_1 + α_2 + α_3} = (−1)^{H(α)} on |X_α⟩ (translation-eigenvalue
theorem). Projectors (1 ± T_1 T_2 T_3)/2 pick out the ±1 eigenspaces.

QED.

## Reusability

Cited wherever:
- Even/odd-order polynomials in site-phase operators appear (e.g., in
  gauge-induced effective operators at various loop orders)
- Block-diagonalization arguments separate hw-parity-preserving from
  hw-parity-flipping dynamics
- Selection rules from discrete parity symmetries constrain framework
  derivations
- Consistency constraints on operator structures (e.g., "X must be of
  even site-phase order because it preserves generation parity")

## Composition with earlier theorems

This theorem uses the translation-eigenvalue theorem (for the explicit
parity projectors Π_±) and the Hamming-distance selection rule (for the
matrix-element parity). It is itself a composition result strengthening
those two.

## Verification

```bash
python3 scripts/frontier_hw_parity_conservation.py
# Expected: TOTAL: PASS=68, FAIL=0
```
