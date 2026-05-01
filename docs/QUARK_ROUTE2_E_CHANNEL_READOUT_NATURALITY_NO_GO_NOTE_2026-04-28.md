# Quark Route-2 E-Channel Readout Naturality No-Go

**Date:** 2026-04-28

**Status:** proposed_no_go exact negative boundary for Lane 3 target 3B.
This note records a minimal-premise stretch attempt on the Route-2 up-type
amplitude scalar-law residual. It does not derive the E-channel law
`beta_E / alpha_E = 21/4`, and it does not claim retained `m_u` or `m_c`.

**Primary runner:**
`scripts/frontier_quark_route2_e_channel_readout_naturality_no_go.py`

## 1. Question

The current Route-2 readout stack has already reduced the up-sector scalar-law
problem to a sharp exact target:

```text
(beta_T / alpha_T, alpha_T / alpha_E, beta_E / alpha_E)
= (-1, -2, 21/4).
```

After granting the two `T`-side candidates,

```text
beta_T / alpha_T = -1,
alpha_T / alpha_E = -2,
```

the remaining irreducible entry is

```text
rho_E := beta_E / alpha_E = 21/4.
```

This note asks whether `rho_E = 21/4` is forced by minimal Route-2 carrier
naturality, without using observed quark masses, fitted CKM/`J` objectives, or
the live endpoint value as a hidden selector.

## 2. Minimal Premise Set

Allowed premises:

1. the exact restricted carrier columns from the Route-2 readout-map note;
2. the exact endpoint algebra
   `q_E = 1 + rho_E/6` and `q_T = 1 + rho_T/6`;
3. the exact T-side candidates `rho_T = -1` and `alpha_T/alpha_E = -2` as a
   conditional stretch premise;
4. standard linear algebra and exact rational arithmetic.

Forbidden proof inputs:

1. observed quark masses;
2. fitted Yukawa values;
3. minimizing CKM/`J` error against the live quark target;
4. selecting the nearest rational to the live E-channel endpoint as if that
   were a derivation;
5. adding a hidden E-center source weight.

## 3. Reduced Family

The exact readout-map note proves that the restricted carrier/readout class is
channelwise. With the two T-side candidates granted, the reduced family is:

```text
P(rho_E) =
[[1, 0, rho_E, 0],
 [0, -2, 0, 2]].
```

The exact E endpoint columns are:

```text
E-shell  = (1, 0, 0,   0)
E-center = (1, 0, 1/6, 0).
```

Therefore:

```text
P(rho_E) E-shell  = (1, 0),
P(rho_E) E-center = (1 + rho_E/6, 0).
```

Shell normalization, channelwise linearity, and the granted T-side data do not
select `rho_E`; every value of `rho_E` gives an exact admissible readout map
on the restricted carrier class.

## 4. What Would Force 21/4

The target value is equivalent to any of these exact statements:

```text
rho_E = 21/4,
q_E = gamma_E(center)/gamma_E(shell) = 15/8,
c_TE = gamma_T(center)/gamma_E(center) = -8/9
```

given the granted T-side values `q_T = 5/6` and
`gamma_T(shell)/gamma_E(shell) = -2`.

So `21/4` is not mysterious once the endpoint ratio chain

```text
{5/6, -2, -8/9}
```

is granted. The problem is that the current exact carrier does not derive the
third ratio `-8/9`. Granting `-8/9` is exactly equivalent to granting the
missing E-center lift.

## 5. Stuck Fan-Out Synthesis

The stretch attempt checked five orthogonal frames:

1. **Carrier-only frame.** Exact carrier columns plus shell normalization
   leave `rho_E` free.
2. **T-side transfer frame.** Granting `rho_T = -1` and
   `alpha_T/alpha_E = -2` fixes `q_T` and the shell T/E ratio, but still
   leaves `rho_E` free.
3. **Symmetry/naturality frame.** Simple natural choices such as no E-center
   lift (`rho_E = 0`) or T/E same-slope reuse (`rho_E = rho_T = -1`) are exact
   admissible maps, but they do not give `21/4`.
4. **Small-rational frame.** Low-rational grammar contains many admissible
   values. `21/4` is selected only after measuring distance to the live
   E-channel endpoint, which is bounded endpoint data, not a theorem.
5. **Endpoint-ratio-chain frame.** The chain derives `21/4` if `-8/9` is
   granted, but deriving `-8/9` is equivalent to deriving the missing E-center
   readout.

All five frames agree: the current retained/exact Route-2 primitives do not
force `rho_E = 21/4`.

## 6. Theorem

**Theorem (Route-2 E-channel readout naturality no-go).** In the exact
restricted Route-2 carrier/readout class, after granting the conditional
T-side candidates

```text
beta_T/alpha_T = -1,
alpha_T/alpha_E = -2,
```

the E-channel readout entry

```text
rho_E = beta_E/alpha_E
```

remains a free parameter unless an additional E-center endpoint ratio,
source-domain, or readout-map primitive is supplied. The value `rho_E = 21/4`
is equivalent to the endpoint ratio `gamma_T(center)/gamma_E(center) = -8/9`
under the granted T-side conditions, but it is not derived by carrier
linearity, shell normalization, T-side transfer, or low-rational naturality
alone.

## 7. What This Retires

This retires the direct naturality route:

```text
exact Route-2 carrier + T-side candidates + minimal naturality
=> beta_E/alpha_E = 21/4.
```

It also blocks the overread:

```text
nearest low rational to the live E endpoint => theorem-grade scalar law.
```

Nearest-rational selection is bounded candidate evidence unless the endpoint
ratio itself is derived.

## 8. What Remains Open

The right 3B theorem target is now sharper:

```text
derive gamma_T(center)/gamma_E(center) = -8/9
```

or equivalently derive the E-center lift

```text
gamma_E(center)/gamma_E(shell) = 15/8.
```

Possible next primitives:

1. a source-domain rule that fixes the E-center endpoint weight;
2. a tensor readout-map theorem beyond the restricted carrier columns;
3. a broader no-go proving that all endpoint-only naturality constraints leave
   `rho_E` free;
4. a different up-sector scalar-law route outside Route-2 readout.

## 9. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_route2_e_channel_readout_naturality_no_go.py
```

Expected result:

```text
TOTAL: PASS=28, FAIL=0
VERDICT: minimal Route-2 naturality does not derive rho_E = 21/4.
```

The runner verifies the reduced family, the exact equivalences, the
non-uniqueness of `rho_E`, the low-rational non-uniqueness, and the
comparator firewall.
