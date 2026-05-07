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

### Premises (A_min for substep 1)

| ID | Statement | Class |
|---|---|---|
| A1 | Local algebra is `Cl(3)` per [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) | retained axiom |
| A2 | `Z^3` spatial substrate | retained axiom |
| U2 | Cl(3) per-site uniqueness (chirality-aware): exactly two non-isomorphic complex spinor irreps, each dim 2 | retained per [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md) |
| U4 | Per-site Hilbert dim = 2 (chirality-independent) | retained per [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md) |
| S2 | Spin-statistics: bosonic 2nd-quantization on Cl(3) site → infinite-dim Fock incompatible with U4 | support per [`AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md) (S2) |

### Forbidden imports

- NO PDG observed values (no fermion masses, no mixing angles)
- NO lattice MC empirical measurements
- NO same-surface family arguments
- NO new axioms beyond A1+A2 (no-new-axiom rule)

## Theorem 1 (Grassmann partition forcing)

**Bounded theorem.** On A1 (Cl(3) local algebra) + A2 (Z³ substrate)
plus U2, U4, and the S2 spin-statistics support input:

```
The matter measure on the framework's Cl(3) ⊗ Z³ substrate must be
the finite Grassmann partition with one (χ_x, χ̄_x) pair per site.
Bosonic 2nd-quantization is RULED OUT by spin-statistics S2.
```

Specifically: there is no consistent matter measure on A1+A2
implementing the canonical staggered Dirac–Wilson operator that uses
**commuting** (bosonic) generators in place of the Grassmann pair.
Hence the staggered-Dirac realization's Grassmann content is
**forced**, not admitted as an independent axiom.

### Proof

The proof is a one-line repackaging of spin-statistics S2 specialized
to substep-1 of the staggered-Dirac realization gate.

**Step 1.** By U2 + U4, the per-site Hilbert space at every
`x ∈ Z³` is a finite-dimensional Cl(3) module of complex dimension
2 (Pauli realization on each chirality summand).

**Step 2.** Suppose for contradiction the matter generators were
**commuting** (bosonic) creation/annihilation operators `a_x, a_x^†`
satisfying `[a_x, a_y^†] = δ_{xy}, [a_x, a_y] = 0`. Build the
corresponding bosonic Fock space `F_B = ⊕_{n_1, n_2, ...} |n_1 n_2 ...⟩`
over the modes indexed by `Λ ⊂ Z³`.

**Step 3.** By the standard bosonic-Fock construction, each per-site
factor of `F_B` is the infinite-dimensional bosonic Fock tower
`H_x^B = ⊕_{n=0}^∞ |n⟩_x` with `dim_C H_x^B = ∞`.

**Step 4.** Per A1 + U4, the per-site Hilbert space MUST be the
faithful irreducible Cl(3) representation of complex dimension 2.
This is incompatible with `dim_C H_x^B = ∞` from Step 3.

**Step 5.** Contradiction. Hence the matter generators cannot be
bosonic. By the only remaining algebraic alternative (Grassmann),
the matter measure is forced to be the finite Grassmann partition
with one Grassmann pair per site, where `dim_C H_x^F = 2` (finite,
matches U4).

**Step 6.** The Grassmann implementation has `χ_x² = 0` and one
Grassmann pair `(χ_x, χ̄_x)` per site, giving per-site Hilbert
dimension exactly 2 (the two-state local Fock module). This matches
U4 and is the unique algebraic alternative to bosonic generators.

QED.

## Hypothesis set used

- A1 (Cl(3) local algebra)
- A2 (Z³ substrate)
- U2 (Cl(3) per-site uniqueness, chirality-aware)
- U4 (per-site Hilbert dim 2)
- S2 (spin-statistics: bosonic incompatibility argument)
- Standard finite Grassmann calculus (admissible standard math, narrow
  non-derivation role)

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
