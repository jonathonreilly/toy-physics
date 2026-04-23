# Axiom-Native Derivation — Starting Kit

**Status:** sole permitted inputs for the overnight axiom-native derivation
track on branch `claude/axiom-native-overnight-FtUl5`.
**Rule:** every `record()` PASS in every runner on this branch must trace to
either (i) this kit, or (ii) a previously-derived axiom-native lemma on this
same branch. No other inputs are allowed. Violations are rejected by the
hostile audit runner per iteration.

## The kit

### K1. Local algebra

The real Clifford algebra `Cl(3)` with unit generators `{e_0, e_1, e_2, e_3}`
satisfying

```
e_0 = 1,    e_i e_j + e_j e_i = 2 δ_ij  (i, j ∈ {1, 2, 3}),
```

and the induced basis `{e_0, e_1, e_2, e_3, e_1 e_2, e_2 e_3, e_1 e_3, e_1 e_2 e_3}`.
The pseudoscalar `ω = e_1 e_2 e_3` satisfies `ω² = −1` and is central.

### K2. Spatial substrate

The cubic lattice `Z³` with sites `n ∈ Z³` and nearest-neighbour edges in
directions `{±e_1, ±e_2, ±e_3}`. Lattice spacing `a > 0` is the one free
scale. All geometric structure on `Z³` is derived here from that — NO `M_Pl`,
NO `v_EW`, NO `α_LM`, NO observed masses.

### K3. Staggered-Dirac partition

On the free (non-interacting) retained surface, the partition function is

```
Z = ∫ 𝒟ψ̄ 𝒟ψ  exp(−S[ψ̄, ψ]),
S = a³ Σ_n Σ_μ η_μ(n) ψ̄(n) [ψ(n + μ̂) − ψ(n − μ̂)] / (2a),
```

with Kogut-Susskind staggered phases `η_μ(n) = (−1)^(n_1 + ... + n_{μ−1})`
and Grassmann fields `ψ(n) ∈ Cl(3)`. The measure `𝒟ψ̄ 𝒟ψ` is the standard
Grassmann Berezin measure.

(Interaction terms — gauge, Yukawa — are NOT part of the kit. If a target
requires them, they must be constructed from K1 + K2 + K3 on this branch.)

### K4. Allowed mathematical infrastructure

Only the following is assumed external:

- set theory, linear algebra over `R` and `C`;
- elementary group theory;
- finite-group representation theory and character orthogonality;
- Fourier analysis on finite abelian groups;
- elementary real analysis, elementary complex analysis, elementary calculus;
- the Berezin integral for Grassmann variables;
- sympy / numpy for symbolic/numerical verification.

**NOT allowed as external imports** (must be derived or avoided):

- any result from `docs/` or from `main` beyond this note;
- any Standard Model quantum-number assignment (`T`, `Y`, hypercharges);
- any continuum QFT convention (MS-bar, dim-reg, Ward identity);
- any rainbow/self-energy topology assumption;
- any Berry-phase formula (derive or do without);
- any PDG mass, coupling, or observational datum;
- any `v_EW`, `M_Pl`, `α_LM`, `I_loop`, `C_τ`;
- any "retained theorem" from the existing package;
- any appeal to "textbook QFT".

## Enforcement

Every iteration runs `scripts/frontier_axiom_native_hostile_audit.py` which:

1. Grep-scans every runner for citations of docs outside this kit and `main`-
   retained items treated as axioms. Any hit → iteration rejected.
2. Grep-scans for numeric constants that don't reduce to kit primitives.
   Any bare PDG-ish number → iteration rejected.
3. Counts `record(..., True, ...)` narrative assertions. Any → rejected.
4. Counts previously-derived facts that this iteration merely restates.
   If the iteration proves nothing new → rejected.

Iterations that pass the audit commit + push. Iterations that fail it do
NOT commit — they write a one-paragraph entry in
`docs/AXIOM_NATIVE_ATTEMPT_LOG.md` and try a different approach.

## Ledger of derived axiom-native facts

Populated as the loop proceeds. Format: fact / runner / commit hash.

- `2 * dim_R(Cl(3)) = 16` is a kit-derivable exact integer invariant
  on Cl(3) x Z^3, equal to the per-site real Grassmann generator count
  in the K3 partition; also = `|unit_cube(Z^3)|_sites * 2` and
  `dim_R(Cl(3)) * 2` / `frontier_axiom_native_cl3_z3_integer_inventory.py`
  / Target 1 sub-step 1a.
- Cl(3) is a closed real algebra of dimension 8 with every
  right-multiplication map `R_b` invertible on Cl(3) /
  `frontier_axiom_native_cl3_z3_integer_inventory.py` /
  Target 1 sub-step 1a.
