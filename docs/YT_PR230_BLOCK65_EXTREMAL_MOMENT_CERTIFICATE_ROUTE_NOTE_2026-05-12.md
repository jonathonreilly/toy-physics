# PR230 Block65 Extremal Moment Certificate Route

**Status:** exact-support / strict extremal moment certificate route specified,
but current PR230 has no flat-extension/localizing certificate and therefore no
pole atom/residue authority
**Claim type:** open_gate
**Runner:** `scripts/frontier_yt_pr230_block65_extremal_moment_certificate_route.py`
**Certificate:** `outputs/yt_pr230_block65_extremal_moment_certificate_route_2026-05-12.json`

## Question

Block64 closed the shortcut

```text
finite source/Stieltjes moments => fixed pole atom/residue.
```

This block asks the stricter question: can an extremal truncated-moment
certificate make the shortcut valid?

The answer is conditional yes, current-surface no.  A flat-extension or
extremal localizing-matrix certificate would fix a finite atomic source
measure and hence its pole atom.  The current PR230 surface does not contain
that certificate, and the Block64 counterfamily still applies.

## Sufficient Certificate

Work in the shifted spectral variable

```text
lambda = s - m_pole^2.
```

After the scalar pole location and threshold side are certified, the pole atom
lives at `lambda=0` and the support condition is `lambda >= 0`.

A sufficient same-surface certificate is:

1. exact or interval-certified moments `m_0 ... m_{2d+2}` of the contact-
   subtracted PR230 scalar-source measure;
2. positive Hankel moment matrix `M_d` and support localizing matrices;
3. a rank-preserving flat extension `rank M_d = rank M_{d+1}`, or an extremal
   truncated-moment certificate with consistency;
4. localizing rank drop

```text
rank M_{d+1} - rank M_lambda = 1,
```

   proving one atom at `lambda=0`;
5. atom/residue extraction by declared atom list, recurrence/Vandermonde solve,
   or Christoffel-function bound, with a tight positive interval;
6. threshold/FVIR/contact authority and canonical `O_H`/source-overlap or
   same-surface physical W/Z response authority.

The runner verifies an exact rational witness where these checks recover a
`1/5` atom at `lambda=0`.

## Current Obstruction

The future certificate

```text
outputs/yt_pr230_strict_extremal_moment_certificate_2026-05-12.json
```

is absent.  Current parents also report:

- Block64: finite moment prefixes do not fix the pole atom/residue;
- Stieltjes moment gate: strict positive certificate absent;
- Pade/Stieltjes gate: strict moment-threshold certificate absent;
- Carleman/Tauberian route: infinite-tail/asymptotic determinacy absent;
- polefit8x8 `C_ss` proxy: current proxy fails Stieltjes monotonicity.

The runner replays the Block64 obstruction in extension form: two positive
measures agree on `m_0,m_1,m_2 = 1,1/2,1/3` but have different higher moments
and different pole atoms at `lambda=0`, namely `1/6` and `1/4`.  Since the
current prefix cannot even form the higher moment matrices needed for flatness,
it cannot certify extremality.

## Assumptions Exercise

| Assumption | If wrong | Test or derivation |
|---|---|---|
| A positive scalar-source Stieltjes measure exists for the same PR230 source object. | Moment theorems certify the wrong object or no positive measure. | Derive the contact-subtracted scalar measure from the compact source functional and rerun monotonicity/Hankel checks. |
| Finite source rows are actual moments, not shell-fit or contact-contaminated proxies. | The truncated moment problem does not apply. | Future certificate must include source coordinate, zero-source limit, contact subtraction, and covariance metadata. |
| Pole location and shifted support `lambda>=0` are same-surface. | Localizing rank drop at zero tests an arbitrary coordinate. | Derive thermodynamic pole/gap authority or direct pole rows first. |
| Moment order is high enough for flatness/extremality. | Block64-style completions remain possible. | Certify `rank M_d=rank M_{d+1}` or extremal rank/variety consistency. |
| PSD/rank decisions survive uncertainty. | Numerical near-flatness may hide nonflat positive families. | Use exact algebraic/rational moments or interval linear algebra with rank gaps. |
| The atom is isolated from continuum threshold effects. | A soft continuum can mimic finite-window pole behavior with zero atom. | Supply threshold and FVIR limiting-order authority. |
| Source-pole residue is physical scalar LSZ residue, or is bridged to it. | The result is only source-channel atom support, not canonical `O_H`. | Supply `C_sH/C_HH` pole rows, Gram purity, or same-surface physical response. |

## First-Principles Reduction

Load-bearing drivers only:

- `Cl(3)/Z3` compact scalar source fixes the source coordinate.
- Reflection positivity gives finite-volume positive source spectral sums.
- A positive Stieltjes scalar measure turns a pole residue into an atom mass.
- Truncated moment theory fixes that atom only under determinacy,
  flat-extension/extremality, or certified sharp Markov bounds with threshold
  authority.
- PR230 physics still needs canonical `O_H`/source-overlap or physical W/Z
  response authority.

Everything else is non-load-bearing here and forbidden: `H_unit`, Ward,
`y_t_bare`, `alpha_LM`, plaquette/`u0`, observed targets, `kappa_s=1`,
`c2=1`, and `Z_match=1`.

## Literature / Math Bridge

- Curto and Fialkow, [Truncated K-moment problems in several variables](https://arxiv.org/abs/math/0507067):
  flat extension plus localizing matrices gives a unique finite atomic
  representing measure and counts atoms in localizing zero sets.  This is a
  literature theorem, not a PR230 derivation.
- Curto, Fialkow, and Moeller, [The extremal truncated moment problem](https://arxiv.org/abs/math/0610882):
  positivity plus consistency is sufficient in the extremal
  rank-equals-variety case.  This supplies an alternate strict certificate
  class.
- Krein and Nudelman, [The Markov Moment Problem and Extremal Problems](https://bookstore.ams.org/MMONO/50):
  classical extremal moment bounds and canonical representations.  This
  supports the Markov/Chebyshev framing but does not provide current PR230
  moments.
- Pozza and Strakos, [Algebraic description of the finite Stieltjes moment problem](https://www.karlin.mff.cuni.cz/~strakos/download/2018_PozStr.pdf):
  finite Stieltjes moments link to spectral distributions, Jacobi matrices,
  Gauss quadrature, and Lanczos/orthogonal-polynomial extraction.
- Total positivity and Nevanlinna/Pick/Stieltjes theory are useful background:
  Hankel total positivity is another view of Stieltjes moment positivity, and
  Pick/Nevanlinna parametrization explains why indeterminate moment problems
  retain free spectral measures.  These do not close PR230 without the missing
  same-surface certificate fields.

## Non-Claims

This block does not claim retained or `proposed_retained` PR230 closure.  It
does not treat finite moment prefixes, Pade fits, finite-shell rows, or
source-carrier normalization as pole-residue authority.  It does not identify
source-pole residue with canonical `O_H` without a future bridge.

It does not use `H_unit`, Ward authority, `y_t_bare`, observed targets,
`alpha_LM`, plaquette/`u0`, `kappa_s=1`, `c2=1`, or `Z_match=1`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block65_extremal_moment_certificate_route.py
python3 scripts/frontier_yt_pr230_block65_extremal_moment_certificate_route.py
# SUMMARY: PASS=11 FAIL=0
```
