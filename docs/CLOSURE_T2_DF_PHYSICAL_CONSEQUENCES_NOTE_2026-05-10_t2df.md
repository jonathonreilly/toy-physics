# T2.7: Physical Consequences of D_F = Gamma_1 + Gamma_2 + Gamma_3

**Date:** 2026-05-10
**Claim type:** open_gate_narrowing
**Status authority:** source-note proposal only; audit verdict and effective
status are set by the independent audit lane.
**Primary runner:** [`scripts/cl3_t2_df_physical_consequences_2026_05_10_t2df.py`](../scripts/cl3_t2_df_physical_consequences_2026_05_10_t2df.py)
**Cached output:** [`logs/runner-cache/cl3_t2_df_physical_consequences_2026_05_10_t2df.txt`](../logs/runner-cache/cl3_t2_df_physical_consequences_2026_05_10_t2df.txt)

## Boundary

PR #1061 constructed the staggered finite Dirac candidate
`D_F = Gamma_1 + Gamma_2 + Gamma_3` on C^8 and admitted, as part of its
hostile-review accounting (HR3): "D_F = Gamma_1 + Gamma_2 + Gamma_3 does NOT
give SM observable Yukawa hierarchy; structural closure != observable
matching." This T2.7 note makes that admission precise and quantitative.

What this note does:

- compute the full spectrum of the constructed D_F;
- verify the KO-dim-6 J = omega K eigenstate-pairing structure;
- record the algebraic identity D_F^2 = 3 I on C^8 and its immediate
  consequence that the spectrum is degenerate;
- confront the predicted spectrum with PDG charged-lepton mass ratios and
  with the Koide Q identity;
- record the structural reason D_F's three-generation index is not
  D_F-invariant (the projector P_hw1 onto the hamming-weight-one triplet
  does not commute with D_F);
- enumerate the additional structure required to obtain the SM Yukawa
  hierarchy from D_F (Yukawa kernel Y_l, generation selector,
  order-one-compatible coupling, Majorana sector).

What this note does NOT do:

- claim D_F predicts SM lepton masses;
- claim the BAE-style |b|^2/a^2 = 1/2 relation holds;
- introduce new axioms;
- request retention;
- alter the audit status of any upstream dependency.

The runner deliberately tests against PDG charged-lepton mass values as
reference data for comparison ONLY; it does not import them as primitives,
does not fit them, and does not declare closure when they disagree with D_F
predictions.

## Source Dependencies

- PR #1061 minimal D_F construction:
  [`CLOSURE_C_STAGGERED_DIRAC_GATE_NOTE_2026-05-10_cStaggered.md`](CLOSURE_C_STAGGERED_DIRAC_GATE_NOTE_2026-05-10_cStaggered.md).
- Staggered Cl(3) embedding:
  [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md).
- Staggered chirality and BZ-corner structure:
  [`STAGGERED_CHIRAL_SYMMETRY_SPECTRUM_THEOREM_NOTE_2026-05-02.md`](STAGGERED_CHIRAL_SYMMETRY_SPECTRUM_THEOREM_NOTE_2026-05-02.md),
  [`STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md).
- Three-generation observable support:
  [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md).

The Brannen-Connes BAE / Koide construct is referenced as a standard-math
comparator and named target. It is not used as a retained primitive.

## Construction recap

The retained staggered Pauli-tensor realization is

```text
Gamma_1 = sigma_1 x I x I
Gamma_2 = sigma_3 x sigma_1 x I
Gamma_3 = sigma_3 x sigma_3 x sigma_1
```

on `H_F = C^8`, with `omega = Gamma_1 Gamma_2 Gamma_3` central in Cl(3),
`gamma_stag = sigma_3 x sigma_3 x sigma_3` the Hamming-weight parity, and
`J = omega K` the KO-dim-6 real structure.

PR #1061's minimal finite Dirac candidate is

```text
D_F = Gamma_1 + Gamma_2 + Gamma_3.
```

The Clifford relations (verified bit-exactly in the runner)
`{Gamma_i, Gamma_j} = 2 delta_ij I` imply

```text
D_F^2 = sum_i Gamma_i^2 + sum_{i<j} {Gamma_i, Gamma_j}
      = 3 I + 0 = 3 I.
```

Hence D_F has spectrum `{+sqrt(3), -sqrt(3)}` with each eigenvalue carrying
multiplicity four on C^8. The runner confirms this from a direct numerical
diagonalization.

## Result 1: The spectrum is degenerate

The eigenvalues of D_F on C^8 are exactly four copies of `+sqrt(3)` and
four copies of `-sqrt(3)` (runner section 1, all PASS). There is no
massless mode in the finite spectrum, and there is exactly one positive
"mass scale." Any candidate three-generation index must therefore live
inside the 4-dimensional `+sqrt(3)` eigenspace as a substructure that D_F
itself does not see.

## Result 2: J = omega K pairs states at the same eigenvalue

The KO-dim-6 real structure `J = omega K` is anti-linear and central in
Cl(3) commutes with D_F. The runner verifies (section 2) that for every
D_F eigenvector psi at eigenvalue lambda, J psi = omega conj(psi) is also
a D_F eigenvector at the same lambda (not at -lambda), and that
`|| J psi || = || psi ||`, with `J^2 = -I`. This is the standard KO-dim-6
pairing: it does not split eigenvalues into +/- pairs the way a charge
conjugation operator on a Lorentzian Dirac space would; the +/- pairing
of D_F eigenvalues here is supplied by the chirality grading
gamma_stag = sigma_3^{x3}, which anti-commutes with D_F.

## Result 3: No BAE relation emerges

The Brannen-Connes "BAE" structure parameterizes the finite Dirac as
`D_F = a I + b X` for some X and asks whether `|b|^2 / a^2 = 1/2` is
forced. With

```text
D_F(a, b) = a I + b (Gamma_1 + Gamma_2 + Gamma_3),
```

one obtains the spectrum `a +/- b sqrt(3)`, which is verified in the
runner. PR #1061's minimal candidate corresponds to `(a, b) = (0, 1)`. At
that choice the ratio `|b|^2 / a^2` is undefined (a = 0); it is not 1/2.
There is no algebraic constraint inside the retained framework that
selects a nonzero value of a relative to b. The "BAE relation" is
therefore NOT a derived consequence of the minimal D_F.

## Result 4: PDG charged-lepton mass-ratio comparison (negative)

At the PDG 2024 values

```text
m_e   = 0.51099895  MeV
m_mu  = 105.6583755 MeV
m_tau = 1776.86     MeV
```

the observed ratios are

```text
m_e  / m_tau = 2.875854e-04
m_mu / m_tau = 5.946353e-02.
```

If we identify "the three lepton masses" with three positive eigenvalues
of D_F (each equal to sqrt(3)), D_F predicts both ratios to be 1. The
relative miss is

```text
gap(m_e  / m_tau)  = 3.48e+03
gap(m_mu / m_tau)  = 1.58e+01.
```

So D_F is wrong by more than three orders of magnitude on the
electron/tau ratio and more than an order of magnitude on the muon/tau
ratio. PDG data is used here only as a comparison anchor.

## Result 5: Koide Q comparison (negative)

The Koide identity, in its standard form

```text
Q = (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2,
```

evaluates to `0.666661` at the PDG values above, famously close to `2/3`
to five significant digits.

With a degenerate D_F spectrum `{sqrt(3), sqrt(3), sqrt(3)}`, the same
formula reduces to `Q = (3 m) / (3 sqrt(m))^2 = 1/3`. So D_F predicts
`Q = 1/3`, not `2/3`. The gap is exactly 1/3 (verified in section 6 of
the runner).

This is a sharp falsification of "D_F gives the Koide identity" in the
minimal staggered form: even allowing the per-eigenvalue normalization
to absorb sqrt(3), the degeneracy alone forces Q = 1/3.

## Result 6: The hamming-weight-one triplet is not D_F-invariant

Define `P_hw1 = sum_{|x|=1} |x><x|`, the projector onto the
hamming-weight-one triplet that carries the M_3(C) summand. The runner
shows that

```text
D_F |001> = -|011> + |000> + |101>   (mix of hw = 0 and hw = 2)
```

and similarly for `|010>` and `|100>`. So `D_F` maps `P_hw1` into its
orthogonal complement; `[P_hw1, D_F] != 0`, with `|| [P_hw1, D_F] || =
4.2426 = 2 sqrt(3) sqrt(2)`. The three-generation index space `hw = 1`
and the D_F spectral content are NOT block-diagonal on the same C^8.

This is the structural reason PR #1061 sees the order-one violation for
nontrivial finite-Dirac perturbations: the M_3(C) summand acts on `hw =
1`, but D_F mixes `hw = 1` with `hw = 0, 2`. Any consistent finite
Dirac that respects the order-one condition must either preserve `hw =
1` or be supported on a different sector.

## Result 7: Required additional structure (open list)

For the staggered-Dirac line to predict the SM charged-lepton mass
hierarchy, the following components must be supplied, none of which is
derived in PR #1061 or here:

1. a Yukawa kernel `Y_l` acting on a flavor-indexed subspace, with
   eigenvalues spanning `m_e : m_mu : m_tau ~ 1 : 207 : 3477`;
2. a selector projecting onto a 3-dimensional generation subspace inside
   the 4-dimensional `+sqrt(3)` eigenspace of D_F;
3. an order-one-compatible coupling between `Y_l` and the
   `A_F = C + H + M_3(C)` algebra (PR #1061 already showed that
   Yukawa-like perturbations of `D_F` violate order-one in the runner's
   bounded test set);
4. a Majorana / right-handed neutrino structure for the neutrino mass
   tower (separate gate).

These are recorded as the standing TODO list for any subsequent attempt
to derive lepton masses inside this finite-triple lane.

## Hostile review

| ID | Question | Answer |
|---|---|---|
| HR1 | Does the runner fit PDG values? | No. The D_F spectrum is fixed by Cl(3) Clifford relations; PDG values appear only as comparison targets in sections 5 and 6. |
| HR2 | Is the "no SM hierarchy" verdict strong? | Yes. D_F has degenerate spectrum on C^8 with one positive eigenvalue at sqrt(3) of multiplicity 4. This is fully determined by D_F^2 = 3 I, an exact algebraic identity. |
| HR3 | Does the Koide-Q gap depend on the runner's choice of identification? | No. Any identification of "three lepton masses" with the four copies of `+sqrt(3)` gives Q = 1/3 because the formula depends only on equality of the three values, not on their absolute scale. |
| HR4 | Does this contradict PR #1061? | No. PR #1061 stated D_F does NOT give SM hierarchy; this note makes that quantitative. |
| HR5 | Does this introduce new axioms? | No. Uses Cl(3) Clifford algebra and the retained staggered embedding only. |
| HR6 | Is the KO-dim-6 J-pairing eigenvalue-preserving rather than eigenvalue-flipping? | Yes. The runner verifies J psi = omega conj(psi) preserves the D_F eigenvalue; the +/- splitting is supplied by gamma_stag, not J. |
| HR7 | Is the deliverable retention-bearing? | No. Source-only narrowing, audit lane decides. |

## What this note does not change

- The audit status of PR #1061 (closed in this repo's working tree per the
  PR-branch-dies-on-close rule). This note does not propose to reopen,
  amend, or rebase PR #1061.
- The retained primitives, retained theorems, or any upstream cl3 / staggered
  / generation primitives.
- The downstream lepton-mass derivation gate, which remains open with the
  enumerated additional structure required.

## Files

- `docs/CLOSURE_T2_DF_PHYSICAL_CONSEQUENCES_NOTE_2026-05-10_t2df.md`  (this file)
- `scripts/cl3_t2_df_physical_consequences_2026_05_10_t2df.py`  (38 PASS / 0 FAIL)
- `logs/runner-cache/cl3_t2_df_physical_consequences_2026_05_10_t2df.txt`  (cached output)

## Authority

closure_proposal_note follow-on. Audit lane retains all status decisions.
No retention requested.
