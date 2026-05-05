# YT Top/W Deterministic-Response Covariance Gate

Status: exact negative boundary / deterministic W-response covariance shortcut
not derived on current PR230 surface; proposal_allowed=false.

This note records the next non-chunk W/Z derivation check after the
top/W covariance marginal no-go and the factorization-independence gate.  The
tested shortcut was:

```text
deterministic W response on the same source surface
  -> fixed cov_dE_top_dM_W
  -> no matched top/W rows needed
```

That shortcut is rejected on the current PR230 surface.  A deterministic W
response can be useful, but only if it is tied to the same latent Cl(3)/Z^3
surface as the top response, with paired top rows or a closed covariance
formula.

## Runner

```text
scripts/frontier_yt_top_wz_deterministic_response_covariance_gate.py
```

Current output:

```text
outputs/yt_top_wz_deterministic_response_covariance_gate_2026-05-05.json
```

Scout output:

```text
outputs/yt_top_wz_deterministic_response_covariance_gate_scout_2026-05-05.json
outputs/yt_top_wz_deterministic_response_covariance_gate_scout_certificate_2026-05-05.json
```

## Framework-Native Scope

The gate is scoped to the PR230 native surface:

- substrate: `Cl(3)/Z^3`;
- geometry: three spatial directions plus the framework's derived-time source
  surface;
- source convention: same scalar source coordinate for the top and W response
  objects;
- no PDG, observed `y_t`, observed W/Z/top values, observed `g_2`, Sommer
  scale, SM RGE, or matrix-element identity enters the proof boundary.

## Boundary

The runner constructs a same-source latent configuration family.  The W
response is deterministic:

```text
R_W(h) = 0.516 + 0.003 h
```

Two allowed top-response functionals have the same top marginal but opposite
dependence on the same latent coordinate.  They therefore produce opposite
`cov_dE_top_dM_W` while keeping the deterministic W law unchanged.

This proves the narrow current-surface fact: deterministic W response alone is
not covariance authority.  A future positive theorem must also fix the top
response pairing/function on the same surface, or directly derive a closed
covariance formula.

## Future Acceptance Contract

A future strict pass needs:

- a same-surface `Cl(3)/Z^3` and 3+derived-time certificate;
- a deterministic W response proved on the same source coordinate;
- paired top response rows or a closed same-surface covariance formula;
- same-source EW action authority;
- W/Z mass-fit path or theorem authority;
- same-source top-response identity authority;
- non-observed electroweak `g_2` authority;
- sector/canonical-Higgs identity plus orthogonal correction control;
- the PR230 forbidden-import firewall.

## Non-Claims

This note does not claim retained or proposed_retained top-Yukawa closure.  It
does not create matched top/W rows, define `y_t` through a matrix element or
`y_t_bare`, or use observed W/Z/top/`y_t`/`g_2` selectors, `H_unit`,
`yt_ward_identity`, `alpha_LM`, plaquette/u0, `kappa_s=1`, `c2=1`,
`Z_match=1`, or `cos(theta)=1`.

## Next Action

To use the deterministic-response W/Z route, supply
`outputs/yt_top_wz_deterministic_response_covariance_certificate_2026-05-05.json`
with paired top rows or a closed covariance formula.  Otherwise produce matched
top/WZ response rows directly.
