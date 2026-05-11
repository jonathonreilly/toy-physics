# Connes-Kreimer Partial-Sum Rota-Baxter on B4 External Bounded Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** source note only. Audit verdicts and effective status
are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_connes_kreimer_partial_sum_rb_b4_external_bounded.py`](../scripts/frontier_connes_kreimer_partial_sum_rb_b4_external_bounded.py)

## Scope

This note records an external algebraic bounded theorem for the
Connes-Kreimer rooted-tree setting of
[`CONNES_KREIMER_BIRKHOFF_FACTORIZATION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md`](CONNES_KREIMER_BIRKHOFF_FACTORIZATION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md).

Let `A_seq = C^N` with componentwise multiplication. Define the strict
prefix-sum operator

```text
P_strict(a)_n = a_1 + ... + a_{n-1},     P_strict(a)_1 = 0.
```

Then `P_strict` is a Rota-Baxter operator of weight `+1`:

```text
P(a) P(b) = P(P(a)b + aP(b) + ab).
```

The operator is not idempotent, so this target algebra supplies a
well-defined Rota-Baxter input for the Connes-Kreimer recursion but not a
projector-forced unique split.

## B4 Test Object

Let `B4` be the complete binary rooted tree of depth 4. It has 16 leaves,
31 nodes, and 30 edges. This is a valid external rooted-tree object in
`H_R`, but it is an external combinatorial choice. This note does not
derive `B4` from the framework lattice, from the physical `Cl(3)` local
algebra on the `Z^3` spatial substrate, or from a staggered taste-blocking
operator.

## Tautological Readout Boundary

For any character `phi: H_R -> A_seq`, the Connes-Kreimer recursion can be
run with the `P_strict` target above. If one chooses a character whose first
sequence slot assigns

```text
phi(B4)_1 = alpha_LM^16,
```

then the first slot of the regular part also reads `alpha_LM^16`, because
`P_strict(_)` has zero first slot. That is a tautological readout of the
chosen character value, not a derivation of `alpha_LM`, the exponent `16`,
or the hierarchy formula.

## Admissions

The bounded theorem has three explicit admissions:

1. `B4` is an external rooted-tree test object, not a derived framework
   taste-blocking tree.
2. `P_strict` is a non-idempotent Rota-Baxter operator; the resulting split
   depends on the chosen target and operator.
3. Any character value that reads `alpha_LM^16` imports that value into the
   target algebra. The recursion does not derive it.

## Non-Claims

- No framework-native Connes-Kreimer character is constructed.
- No bridge from staggered taste blocking to `H_R` is established.
- No derivation of `alpha_LM^16` is claimed.
- No new framework axiom, new lattice premise, or new retained status is
  introduced.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_connes_kreimer_partial_sum_rb_b4_external_bounded.py
```

Expected result: `PASS=9 FAIL=0`. A passing run supports only the external
bounded algebraic statement and the tautological-readout boundary above.
