# W/Z g2 Generator/Casimir Normalization No-Go

Status: exact negative boundary / SU2 generator-Casimir normalization does not certify PR230 g2.

This checkpoint closes a narrow shortcut in the same-source W/Z response route.
The normalized SU(2) generators fix representation data:

```text
[T_a,T_b] = i eps_abc T_c
Tr(T_a T_b) = delta_ab / 2
sum_a T_a^2 = 3/4 I
```

Those facts do not fix the physical low-scale electroweak coupling.  The
coupling is the coefficient of the canonically normalized gauge field in the
interacting action, so it needs an allowed action normalization,
matching/running bridge, or direct non-observed certificate.  Setting
`g2^2 = 1/4` from a generator convention is therefore not a PR230 `g2`
certificate.

Executable artifact:

```text
python3 scripts/frontier_yt_wz_g2_generator_casimir_normalization_no_go.py
# SUMMARY: PASS=8 FAIL=0
```

The runner constructs a fixed normalized SU(2) representation and an
algebraically indistinguishable family of candidate `g2` values.  The
commutators, trace normalization, and fundamental Casimir remain identical,
while `m_W/v = g2/2` and a fixed response-ratio readout
`y_t = (g2/sqrt(2)) dE_top/dM_W` vary with `g2`.

Claim boundary:

- This does not claim retained or proposed-retained top-Yukawa closure.
- It does not write `outputs/yt_electroweak_g2_certificate_2026-05-04.json`.
- It does not use observed electroweak values, `alpha_LM`, plaquette, `u0`,
  package `g_2(v)`, `H_unit`, or `yt_ward_identity` as proof authority.
- It does not set `c2`, `Z_match`, or `kappa_s` to one.

Next action: supply a strict non-observed `g2` authority with canonical
gauge-field/action normalization and allowed low-scale matching, then rerun
the electroweak `g2` certificate builder.
