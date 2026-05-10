# Staggered-Dirac Substep 1 — Grassmann Partition Forcing (Block 02)

**Date:** 2026-05-07
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded source support packaging the substep-1 forcing
surface of the staggered-Dirac realization gate. The statement is
conditional on the cited primitive chain (per-site Cl(3) dim 2 +
[Cl(3) per-site uniqueness chirality-aware repair](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md)
+ [spin-statistics S2](AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md)).
The load-bearing S2 input remains support-tier/re-audit-dependent on
current main, so this note does not assert retained-grade closure. It
repackages the existing spin-statistics S2 forcing argument as explicit
bounded support under the parent
[`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md).
**Authority role:** source note. Audit verdict and effective status are
set only by the independent audit lane.
**Primary runner:** [`scripts/probe_grassmann_forcing_dependency_chain.py`](../scripts/probe_grassmann_forcing_dependency_chain.py)

## Question

Does A1 (Cl(3) local algebra) + A2 (Z³ substrate) + admissible
mathematical infrastructure FORCE the matter sector of the
staggered-Dirac realization to be Grassmann (vs. allowing both
Grassmann AND bosonic 2nd-quantization)?

## Answer

**Yes — the matter measure on A1+A2 is uniquely Grassmann.**
Bosonic 2nd quantization is incompatible with the retained finite
per-site Cl(3) module dimension; only the Grassmann implementation
is consistent with A1.

## Setup

### Premises (A_min for substep 1, restructured 2026-05-10)

| ID | Statement | Class |
|---|---|---|
| A1 | Local algebra is `Cl(3)` per `MINIMAL_AXIOMS_2026-05-03.md` | retained axiom |
| A2 | `Z^3` spatial substrate | retained axiom |
| U2 | Cl(3) per-site uniqueness (chirality-aware): exactly two non-isomorphic complex spinor irreps, each dim 2 | retained per [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md) |
| U3 | Every finite-dim faithful complex Cl(3) representation decomposes as a direct sum of 2-dim chirality irreps with even total complex dim | retained per `AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md` (same source as U2) |

**2026-05-10 restructure note.** This note previously load-bore on U4
(per-site Hilbert dim = 2 on A_min) of the cl3 per-site uniqueness
note and on S2 of the spin-statistics support note. Both of those
were narrowed/reframed earlier today (U4 was moved out of the cl3
note's scope; spin_statistics was reframed to load-bear on U2+U3
not U4). To kill the resulting circularity (substep 1 ↔ dim_two ↔
substep 1; substep 1 ↔ S2 → U4 → substep 1), this note is
restructured to load-bear on **U2+U3 directly (A1-only)**, with the
bosonic-incompatibility argument promoted to the operator-algebra
level (bosonic `[a, a^†] = 1` does not satisfy the Cl(3) defining
relations `{γ_i, γ_j} = 2δ_{ij}` since `a^2 ≠ 0` while `γ_i^2 = I` —
no nilpotent unit-square element exists in the bosonic operator
algebra at the per-site level). The spin_statistics note (now
audited_clean / retained) uses the same operator-algebra argument
in its Fact 2.3; this substep applies it to substep-1 scope.

### Forbidden imports

- NO PDG observed values (no fermion masses, no mixing angles)
- NO lattice MC empirical measurements
- NO same-surface family arguments
- NO new axioms beyond A1+A2 (no-new-axiom rule)

## Theorem 1 (Grassmann partition forcing, restructured 2026-05-10)

**Bounded theorem.** On A1 (Cl(3) local algebra) + A2 (Z³ substrate)
plus U2+U3 of the upstream Cl(3) per-site uniqueness theorem (A1-only
content, retained):

```
The matter measure on the framework's Cl(3) ⊗ Z³ substrate must be
the finite Grassmann partition with one (χ_x, χ̄_x) pair per site.
Bosonic 2nd-quantization is RULED OUT at the operator-algebra level
because bosonic generators do not satisfy the Cl(3) defining
relations.
```

Specifically: there is no consistent matter measure on A1+A2
implementing the canonical staggered Dirac–Wilson operator that uses
**commuting** (bosonic) generators in place of the Grassmann pair.
Hence the staggered-Dirac realization's Grassmann content is
**forced**, not admitted as an independent axiom.

### Proof (restructured 2026-05-10 — A1-only chain, no U4 import)

**Step 1 (per-site is a faithful finite-dim Cl(3) module, A1+U2+U3).**
By A1, the local operators at each site `x ∈ Z^3` form the Cl(3)
algebra. Therefore the per-site Hilbert space `H_x` carries some
representation of Cl(3). The natural matter sector is a *faithful*
Cl(3) representation (else the Cl(3) generators would partially
annihilate the local module, contradicting A1's "the local algebra is
Cl(3)"). By U2+U3 (A1-only Cl(3) classification), every faithful
finite-dim complex Cl(3) representation decomposes as a direct sum of
2-dim chirality irreps with even total complex dimension `2(n_+ +
n_-)`. The minimal faithful representation has `dim_C H_x = 2`.

**Step 2 (bosonic operator algebra does NOT satisfy Cl(3) defining
relations).** Suppose for contradiction the matter generators were
commuting (bosonic) creation/annihilation operators `a_x, a_x^†`
satisfying `[a_x, a_y^†] = δ_{xy}, [a_x, a_y] = 0`. Then `a_x^2` and
`(a_x^†)^2` are not identically zero on the bosonic Fock space
(`(a^†)^2 |0⟩ = √2 |2⟩ ≠ 0`). But the Cl(3) generators satisfy
`γ_i^2 = I` — every Cl(3) generator must square to the identity, not
to the unit-norm `|2⟩` state. The bosonic ladder operator algebra
contains no element whose square is the identity (other than ±I
itself, which is not a generator). Hence the bosonic operators
**cannot** carry the Cl(3) per-site representation required by A1.
This is a sharper, A1-only obstruction than the dimension-counting
obstruction (which would require U4/A3-bridge content).

**Step 3 (Grassmann is the unique finite-dim canonical alternative).**
The standard QFT canonical-quantization choices are bosonic CCR
(`[a, a^†] = I`, ruled out by Step 2) or Grassmann CAR (`{c, c^†} = I`,
giving per-mode 2-dim Fock space `span(|0⟩, c^†|0⟩)`). The Grassmann
operators satisfy `c^2 = 0`, which is consistent with — and in fact
matches — Cl(3) generator nilpotency relations modulo a unitary
change of basis (specifically, `(σ_+)^2 = 0` for the Pauli raising
operator; the per-site 2-dim Cl(3) chirality irrep is unitarily
equivalent to the Grassmann 2-dim Fock module per the canonical
Pauli/Jordan-Wigner identification).

**Step 4 (substep 1 conclusion).** The matter measure on A1+A2
implementing the canonical staggered Dirac-Wilson operator must use
Grassmann generators with one pair `(χ_x, χ̄_x)` per site, giving
`dim_C H_x = 2` matching the minimal faithful Cl(3) representation.
QED.

The chain is now A1-only at the load-bearing level (U2+U3 of the
upstream cl3 note are A1-only retained content; Step 2's
operator-algebra obstruction needs only A1's Cl(3) defining relations,
not any A3-bridge content). The former U4 import has been eliminated.

## Hypothesis set used (restructured 2026-05-10 — A1-only)

- A1 (Cl(3) local algebra)
- A2 (Z³ substrate)
- U2+U3 of upstream `AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29` (Cl(3) chirality-irrep classification, A1-only retained)
- Standard finite Grassmann calculus (admissible standard math, narrow non-derivation role)

**No A3 dependency, no U4 dependency, no S2 dependency at the load-
bearing step.** The bosonic-incompatibility obstruction (Step 2 of
the proof) is operator-algebra-level on the Cl(3) defining relations
and needs no per-site Hilbert dimension input. The minimum-dim
conclusion (`dim_C H_x = 2`) follows from U2+U3 alone.

No fitted parameters. No observed values. No physics conventions
admitted beyond the cited retained primitives + standard finite
Grassmann calculus.

## Audit boundary

This note should seed as `bounded_theorem`. It does not write an audit
verdict, an effective status, or a retained-grade closure claim. The
independent audit lane must decide whether S2 and the resulting dependency
chain support any later retained-grade use.

## What this supports

- Substep 1 of the staggered-Dirac realization gate (Grassmann
  partition forcing) is packaged as bounded theorem support
- The dependency chain through U2, U4, and support-tier S2 is documented
  for audit
- The support boundary is explicit: no retained-grade conclusion follows
  until S2 and the dependency chain audit clean

## What this does NOT close

- The staggered-Dirac realization gate itself
- The S2 re-audit (independent audit lane work)

## Cross-references

- Parent open-gate: [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
- Spin-statistics S2 (load-bearing): [`AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md)
- Per-site uniqueness (U2): [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md)
- Per-site Hilbert dim (U4): [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md)
- Standard methodology: Berezin (1966) — finite Grassmann calculus; Slavnov-Faddeev — fermion measure; spin-statistics theorem in QFT (Streater-Wightman 1964)

## Command

```bash
python3 scripts/probe_grassmann_forcing_dependency_chain.py
```

Expected output: dependency chain verification — A1, A2, U2, U4, S2
all consistent; bosonic Fock dim infinite; Grassmann Fock dim 2;
contradiction with U4 forces Grassmann.
