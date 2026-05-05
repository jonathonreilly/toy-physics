# YT Top/W Factorization-Independence Gate

Status: exact negative boundary / same-source factorization not derived on
current PR230 surface; proposal_allowed=false.

This note records the next non-chunk derivation check after the matched
top/W covariance marginal no-go.  The tested shortcut was:

```text
Cl(3)/Z^3 same-source label + 3 spatial + 1 derived-time locality
  -> top/W response factorization or independence
  -> fixed cov_dE_top_dM_W without matched rows
```

That shortcut is rejected on the current PR230 surface.  The work remains
framework-native, but native bookkeeping is not itself a product-measure or
conditional-independence theorem.

## Runner

```text
scripts/frontier_yt_top_wz_factorization_independence_gate.py
```

Current output:

```text
outputs/yt_top_wz_factorization_independence_gate_2026-05-05.json
```

Scout output:

```text
outputs/yt_top_wz_factorization_independence_gate_scout_2026-05-05.json
outputs/yt_top_wz_factorization_independence_gate_scout_certificate_2026-05-05.json
```

## Framework-Native Scope

The gate is scoped to the PR230 native surface:

- substrate: `Cl(3)/Z^3`;
- geometry: three spatial directions plus the framework's derived-time source
  surface;
- source convention: same scalar source coordinate for the top and W response
  objects;
- no PDG, Sommer scale, SM RGE, observed `y_t`, observed W/Z/top values, or
  matrix-element identity enters the proof boundary.

## Boundary

The runner constructs a same-source latent configuration family.  All cases
share the native labels and the same source coordinate, but the W response can
depend on the shared configuration coordinate with positive, negative, or zero
correlation relative to the top response.  The resulting
`cov_dE_top_dM_W` therefore changes sign while the native bookkeeping remains
unchanged.

This does not prove that no future same-surface theorem can fix the covariance.
It proves the narrower current-surface fact: Cl(3)/Z^3 same-source bookkeeping
and 3+derived-time locality do not, by themselves, imply top/W independence.

## What Would Be Enough

A future strict pass needs one of:

- measured matched top/W response rows on the same configuration set;
- a product-measure factorization theorem for the top and W response
  functionals;
- a conditional-independence theorem strong enough to fix
  `cov_dE_top_dM_W`;
- a deterministic W-response theorem plus a validated finite-sample covariance
  rule;
- a closed covariance formula derived on the same Cl(3)/Z^3 3+derived-time
  surface.

The deterministic-response option is now separately gated by
[`YT_TOP_WZ_DETERMINISTIC_RESPONSE_COVARIANCE_GATE_NOTE_2026-05-05.md`](YT_TOP_WZ_DETERMINISTIC_RESPONSE_COVARIANCE_GATE_NOTE_2026-05-05.md):
deterministic W response alone is not covariance authority without paired top
rows or a closed same-surface covariance formula.

## Non-Claims

This note does not claim retained or proposed_retained top-Yukawa closure.  It
does not create matched production rows, define `y_t` through a matrix element
or `y_t_bare`, or use observed W/Z/top/`y_t`/`g_2` selectors, `H_unit`,
`yt_ward_identity`, `alpha_LM`, plaquette/u0, `kappa_s=1`, `c2=1`,
`Z_match=1`, or `cos(theta)=1`.

## Next Action

The non-chunk W/Z route now has a clean fork.  Either build the matched
top/W rows, or derive one of the allowed same-surface factorization mechanisms
and rerun the gate in strict mode.  Do not treat framework-native labels as
independence authority.
