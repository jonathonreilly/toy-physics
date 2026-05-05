# PR230 Missing Bridge Literature And Assumption Exercises

Date: 2026-05-05

Status: bounded support / targeted literature and assumption exercises complete;
missing `O_s/O_sp -> O_H` bridge remains open.

Runner:
`scripts/frontier_yt_pr230_missing_bridge_literature_assumption_exercises.py`

Certificate:
`outputs/yt_pr230_missing_bridge_literature_assumption_exercises_2026-05-05.json`

## Target

The missing bridge is narrow:

```text
source pole O_s / O_sp  -> canonical Higgs radial operator O_H
source-only Z(s,0)      -> two-source Z(s,h), C_sH, C_HH
```

The exercise deliberately searched beyond standard lattice-QCD habits:
matrix-valued Herglotz theory, moment problems, realization theory,
phase retrieval, latent-variable identifiability, positive-operator spectral
theory, Tannakian reconstruction, D-modules, Picard-Fuchs equations, and Prony
methods.

## Literature Exercise

The survey result is not a hidden closure theorem.  It sharpens the route map.

| Literature family | What it gives | PR230 status |
|---|---|---|
| FMS / gauge-invariant Higgs spectroscopy | Correct physical language for `O_H` as a gauge-invariant composite | Conditional: needs same-source EW/Higgs action or canonical `O_H` certificate |
| Matrix-valued Herglotz / matrix moment problem | Exact language for `C_ss/C_sH/C_HH` as a matrix spectral measure | Source-only no-go; strong future row framework |
| Ho-Kalman minimal realization | Input-output data determine hidden state only up to coordinate similarity | Explains source-coordinate ambiguity; supports multi-output rows |
| Phase retrieval / latent identifiability | One marginal/view is usually insufficient; extra masks/views restore identifiability | Need `O_H`, W/Z, or neutral projector view |
| Krein-Rutman / Perron-Frobenius | Positivity-improving operator can yield unique first eigenvector | Best derivation-preferred route if current-surface cone/irreducibility can be proved |
| Tannaka-Krein / Doplicher-Roberts | Reconstruct symmetry/field structure from rich observable categories | Long-horizon; current scalar rows are far too small |
| Holonomic D-modules / Picard-Fuchs / creative telescoping | Exact compute after a finite-volume functional is defined | Cannot define `h`, `O_H`, or `kappa_s` |
| Prony / sparse moment reconstruction | Can recover finite sparse measures under exact finite-rank/separation assumptions | Conditional scalar-LSZ support only; current finite prefixes are insufficient |

Representative sources:

- FMS original preprint:
  `https://archives.ihes.fr/document/P_81_12.pdf`
- Maas/Sondenheimer gauge-invariant Higgs resonance:
  `https://arxiv.org/abs/2009.06671`
- Fradkin/Shenker lattice gauge-Higgs phase structure:
  `https://www.osti.gov/biblio/6248890`
- Matrix-valued Herglotz functions:
  `https://arxiv.org/abs/funct-an/9712004`
- Matrix moment Nevanlinna parametrization:
  `https://www.mscand.dk/article/view/14340`
- Ho/Kalman minimal realization:
  `https://ntrs.nasa.gov/citations/19670049337`
- Phase retrieval uniqueness/stability:
  `https://epubs.siam.org/doi/10.1137/19M1256865`
- Latent-structure identifiability:
  `https://arxiv.org/abs/0809.5032`
- Krein-Rutman positive semigroups:
  `https://arxiv.org/abs/2305.06652`
- Doplicher-Roberts reconstruction:
  `https://annals.math.princeton.edu/1989/130-1/p03`
- Abstract compact-group duality:
  `https://link.springer.com/article/10.1007/BF01388849`
- Holonomic systems:
  `https://sites.math.rutgers.edu/~zeilberg/mamarim/mamarimhtml/holonomic.html`
- Picard-Fuchs equations for integrals:
  `https://arxiv.org/abs/1212.4389`
- Multivariate Prony:
  `https://www.sciencedirect.com/science/article/pii/S0024379515006187`

## Assumption Questioning Exercise

The load-bearing assumptions tested were:

| Assumption | Current result | Repair target |
|---|---|---|
| Same-source label fixes physical Higgs coordinate | False on current surface | derive `k_top/k_gauge = 1` or measure joint response |
| Exact `Z(s,0)` determines `C_sH/C_HH` | False | define `O_H` and measure matrix spectral rows |
| FMS supplies `O_H` without EW/Higgs action | False | same-source EW/Higgs action or independent `O_H` theorem |
| Holonomic methods define missing source | False | define `Z(beta,s,h)` first |
| One neutral scalar pole is automatic | Unproved | primitive cone / positivity-improving rank-one theorem |
| `v` input fixes source-Higgs normalization | False | source-Higgs Gram purity or W/Z response |
| Invariant-ring uniqueness closes `O_s=O_H` | Conditional only | derive same-surface Higgs doublet/action first |
| Tannakian reconstruction works with current rows | False now | build actual tensor-category/fiber-functor data |
| Finite moment prefixes are scalar-LSZ authority | False | finite-rank or threshold/FV/IR theorem |
| Measured target value can select bridge | Forbidden | use only current-surface derived/measured rows |

## Ranked Next Routes

1. Multi-output physical response.  Measure same-source top plus W/Z or
   `O_H` rows so the hidden overlap becomes an observed covariance/ratio.
2. Positivity-improving neutral scalar rank-one theorem.  Derive a primitive
   cone and irreducible transfer operator so source-only scalar-pole data can
   become sufficient.
3. Same-source EW/Higgs action plus invariant/FMS `O_H`.  This is direct but
   still needs the action tied to the PR230 source coordinate.
4. Matrix-valued spectral measure.  Strong exact framework after `O_H` exists.
5. Tannaka/DR reconstruction.  Deep possible route, but far beyond current
   PR230 row data.

## Claim Boundary

This note does not claim retained or proposed-retained top-Yukawa closure.  It
does not define `y_t_bare`, does not use `H_unit` or `yt_ward_identity`, does
not use observed top/yukawa values, and does not identify `O_s` or `O_sp` with
`O_H`.

## Verification

```bash
python3 scripts/frontier_yt_pr230_missing_bridge_literature_assumption_exercises.py
# SUMMARY: PASS=15 FAIL=0
```
