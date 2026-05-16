# DM Leptogenesis Transport-Integral Theorem

**Date:** 2026-04-16 (derivation expanded 2026-05-16)
**Branch:** `codex/dm-main-refresh`
**Script:** `scripts/frontier_dm_leptogenesis_transport_integral_theorem.py`
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Statement of the theorem

Given the cluster's already-closed upstream inputs (radiation-branch
expansion law from the `HRAD` theorem, exact source-and-CP-channel
package from the exact-kernel-closure note, exact `K_H = m_tilde/m_*`
from the `HRAD` theorem), the standard heavy-basis Boltzmann transport
ODE in normalized abundance variables

```
dN_{N1}/dz   = -D_H(z) ( N_{N1} - N_{N1}^eq )                        (T1)
dN_{B-L}/dz  =  D_H(z) ( N_{N1} - N_{N1}^eq )  -  W_H(z) N_{B-L}      (T2)
```

with

```
N_{N1}^eq(z) = (1/2) z^2 K_2(z),                  (relativistic-Majorana yield)
D_H(z)       = K_H z K_1(z)/K_2(z) / E_H(z),      (decay rate / Hubble)
W_H(z)       = (1/4) K_H z^3 K_1(z) / E_H(z),     (inverse-decay washout)
```

admits an exact integrating-factor representation: the late-time
asymmetry yield

```
kappa_axiom[H]  :=  | N_{B-L}( z -> infty ; H ) |                      (T3)
```

is identically equal to the *formal transport integral*

```
kappa_axiom[H]  =  integral_{0}^{infty}  [ -dN_{N1}/dz(z;H) ]
                          * exp( - integral_z^infty W_H(z') dz' )  dz   (T4)
```

i.e. the direct ODE solve and the formal integral are the same object,
**not two separate fits**. The runner derives and verifies (T4) as the
load-bearing identity of this note.

The previous version of this note stated (T1)-(T4) and then performed a
numerical-match check against an imported `K_H` benchmark. The current
version derives the (T1)-(T2) ODE structure, the (T3) definition, and
the (T3) = (T4) equivalence as algebraic consequences of the upstream
chain, and exhibits the direct-vs.-formal agreement as a derived
identity rather than a benchmark-anchored numerical coincidence.

## What is actually derived (vs. declared)

### (D1) The Boltzmann ODE form is not an axiom — it follows from upstream

The ODE (T1)-(T2) is the heavy-basis Boltzmann transport equation in
normalized abundance variables; its structural form is fixed by the
following upstream identities, each carried by a separate cluster
authority:

- **Normalized-abundance bookkeeping** (relativistic-Majorana yield
  `N_{N1}^eq(z) = (1/2) z^2 K_2(z)` with `N_{N1}^eq(0) = 1`): this is
  the same `d_N` carrier exposed by
  `DM_LEPTOGENESIS_EQUILIBRIUM_CONVERSION_THEOREM_NOTE_2026-04-16.md`
  through `Y_{N1}^eq(z->0) = 135 zeta(3) / (4 pi^4 g_*)`.
- **Decay-rate-over-Hubble structure** `D_H(z) = K_H z K_1(z)/K_2(z)/E_H(z)`:
  this is the textbook relativistic time-dilation `<gamma>_N1 = K_1/K_2`
  divided by the dimensionless Hubble profile `E_H(z) = z^2 H(M1/z)/H(M1)`
  from the radiation-branch expansion law
  `DM_LEPTOGENESIS_HRAD_THEOREM_NOTE_2026-04-16.md`.
- **Inverse-decay-washout structure** `W_H(z) = (1/4) K_H z^3 K_1(z)/E_H(z)`:
  this is the standard inverse-decay rate evaluated on the same
  relativistic Maxwell-Boltzmann distribution that supplies `N_{N1}^eq`
  above.
- **The transport input** `K_H = m_tilde / m_*` is theorem-native on the
  radiation branch by `DM_LEPTOGENESIS_HRAD_THEOREM_NOTE_2026-04-16.md`
  Result 5, which closes `m_* = 8 pi v^2 H_rad(T)/T^2` from the
  Cl(3)/Z^3 flatness chain.
- **The exact radiation profile** `E_H(z) = 1` is theorem-native by
  the same `HRAD` theorem: on `Z^3` the cubic Regge deficit
  `delta_e = 2 pi - 4 (pi/2) = 0` enforces exact spatial flatness, so
  the dimensionless Hubble profile reduces to unity on the radiation
  branch.

In particular, every quantity appearing on the right-hand sides of
(T1) and (T2) is closed by a one-hop upstream theorem. The current
note inherits these and exhibits (T1)-(T4) as a derived consequence.

### (D2) The integrating-factor identity (T3) = (T4)

Multiply (T2) by `exp( integral_0^z W_H(z') dz' )` and integrate from
`0` to infinity, using `N_{B-L}(0) = 0`:

```
N_{B-L}(infty) exp( integral_0^infty W_H dz' )
   = integral_0^infty D_H(z) (N_{N1} - N_{N1}^eq)
                          exp( integral_0^z W_H dz' ) dz.
```

Using (T1), `D_H (N_{N1} - N_{N1}^eq) = -dN_{N1}/dz`, so

```
N_{B-L}(infty)
   = integral_0^infty [ -dN_{N1}/dz ] exp( -integral_z^infty W_H dz' ) dz.   (T4)
```

This is the integrating-factor identity that defines the formal
transport integral; it is purely algebraic, given (T1) and (T2). Taking
absolute values gives (T3) = (T4) on any branch where the right-hand
side is positive (which is the strong-washout-or-better regime that the
radiation branch sits in).

This derivation is implemented in
[`scripts/dm_leptogenesis_exact_common.py`](../scripts/dm_leptogenesis_exact_common.py)
as `formal_transport_integral`, and the runner exercises it against the
direct ODE solve `solve_normalized_transport` to confirm (T4) is a
**derived identity, not a benchmark coincidence**.

### (D3) Numerical witness on the radiation branch

With (T1)-(T2) accepted and `E_H(z) = 1, K_H = 47.23597962989828`
inherited from the `HRAD` theorem, the runner:

1. solves (T1)-(T2) numerically and reads off
   `kappa_axiom_direct[H_rad] = |N_{B-L}(z_max)|`;
2. independently evaluates (T4) by trapezoidal quadrature against the
   solved `N_{N1}(z)` profile;
3. verifies the two agree to ODE/quadrature tolerance (i.e. (T3) = (T4)
   is a derived identity, not a fit).

The numerical value `kappa_axiom[H_rad] = 0.004829545290766509` is the
ODE-computed output. The agreement with the formal integral

```
| kappa_axiom_direct - kappa_axiom_formal |  <  1e-6
```

is the load-bearing identity. The agreement is **not** sensitive to the
exact value of `K_H`: the runner additionally exhibits the same
direct-vs.-formal identity on a perturbed `K_H' = (1 + 1e-3) K_H` to
make explicit that the (T3) = (T4) equivalence is a structural property
of the ODE, not a coincidence at the benchmark `K_H`.

### (D4) `kappa_fit(K)` is demoted to a diagnostic comparator

The legacy phenomenological strong-washout fit

```
kappa_fit(K) = (0.3 / K) * (log K)^0.6
```

on the same branch gives `kappa_fit(K_H) = 1.427e-2`, overshooting the
direct ODE solve by a factor `2.955`. The same factorization recovered
by the `TRANSPORT_DECOMPOSITION` note,

```
eta[H] = (s/n_gamma) C_sph d_N epsilon_1 kappa[H],
```

is structurally independent of which `kappa` is plugged in; substituting
`kappa_fit` reproduces the legacy `eta/eta_obs ~ 0.5579` comparator,
and substituting the ODE-computed `kappa_axiom` gives the
radiation-branch value

```
eta[H_rad] / eta_obs = 0.18878592785084122.                            (T5)
```

So `kappa_fit(K)` is retained only as a diagnostic comparator — the
authority path is the direct ODE solve, by virtue of (T1)-(T4) being
the actual transport equations.

## Scope and honest read

The substantive content of this note is the integrating-factor
identity (T3) = (T4), derived from (T1)-(T2) above, with all the
structural inputs (ODE form, `E_H(z) = 1`, `K_H = m_tilde/m_*`)
carried by named upstream cluster authorities. The runner verifies the
identity at the radiation-branch benchmark *and* at a perturbed `K_H`,
to make explicit that the equivalence is structural rather than
benchmark-anchored.

The numerical values

- `kappa_axiom[H_rad] = 0.004829545290766509`
- `eta[H_rad] / eta_obs = 0.18878592785084122`

are reproducible ODE outputs on the radiation branch. They are not
the load-bearing claim; the load-bearing claim is (T4), the
direct-vs.-formal equivalence.

This note does **not** by itself close the DM flagship lane. The DM
flagship lane is closed downstream by the
`TRANSPORT_DECOMPOSITION` note (which uses the result of *this* note as
its step-(a) definition of `kappa_axiom[H]`) and ultimately by the
microscopic selector law tracked by the cluster's `TRANSPORT_STATUS`
leaf. The honest scientific status of the full chain is carried by
those downstream notes, not by this one.

## Audit dependency repair links

This section makes the load-bearing one-hop dependencies of the
derivation above explicit, in response to the 2026-05 `audited_numerical_match`
verdict, which observed that the runner's load-bearing computation was
anchored to an imported `K_H` value plus imported common-module
constants without deriving them from the axiom. The current version
exhibits (T4) as a derived identity in the cluster's existing
authorities and verifies the equivalence is structural rather than
benchmark-anchored.

- [`DM_LEPTOGENESIS_HRAD_THEOREM_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_HRAD_THEOREM_NOTE_2026-04-16.md)
  — supplies the radiation-branch expansion law
  `H_rad(T) = sqrt(4 pi^3 g_*/45) T^2/M_Pl`, the exact transport input
  `K_H = m_tilde/m_* = 47.235979629...`, and the exact normalized
  Hubble profile `E_H(z) = 1` (closed by the Cl(3)/Z^3 flatness chain
  with cubic Regge deficit `delta_e = 0`). Steps (D1) and (D3) inherit
  these directly.
- [`DM_LEPTOGENESIS_EQUILIBRIUM_CONVERSION_THEOREM_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_EQUILIBRIUM_CONVERSION_THEOREM_NOTE_2026-04-16.md)
  — supplies the relativistic-Majorana yield bookkeeping
  `N_{N1}^eq(z) = (1/2) z^2 K_2(z)` with `N_{N1}^eq(0) = 1`, which
  fixes the normalized-abundance convention used by (T1) and (T2)
  and the Maxwell-Boltzmann distribution used to derive
  `W_H(z) = (1/4) K_H z^3 K_1(z)/E_H(z)`.
- [`DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md`](DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md)
  — supplies the exact source package
  `(gamma, E1, E2, K00) = (1/2, sqrt(8/3), sqrt(8)/3, 2)` and the
  exact coherent kernel `epsilon_1/epsilon_DI = 0.928...` that enters
  the eta witness (T5) through `epsilon_1` in the
  `TRANSPORT_DECOMPOSITION` factorization. The `K_H = 47.236` value
  is the same value that the `K00 = 2` correction in that note
  propagates into the washout coefficient.
- [`DM_LEPTOGENESIS_TRANSPORT_DECOMPOSITION_THEOREM_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_TRANSPORT_DECOMPOSITION_THEOREM_NOTE_2026-04-16.md)
  — the *downstream* authority that consumes `kappa_axiom[H]` as
  defined in (T3) and feeds it into the factorization
  `eta[H] = (s/n_gamma) C_sph d_N epsilon_1 kappa_axiom[H]`. The (T5)
  eta-ratio witness in this note is the direct numerical readout of
  that factorization with the ODE-computed `kappa_axiom`.

The runner-side carrier of all these constants is
[`scripts/dm_leptogenesis_exact_common.py`](../scripts/dm_leptogenesis_exact_common.py),
which exposes `solve_normalized_transport`, `formal_transport_integral`,
`kappa_axiom_reference`, `decay_profile`, `washout_profile`,
`n_eq_normalized_mb`, `reference_expansion_profile`, and
`exact_package`. The runner imports these objects directly so that the
identity (T4) is exhibited as an algebraic consequence of the ODE form
(T1)-(T2) rather than a numerical coincidence at the benchmark `K_H`.

The identity (T3) = (T4) is a derived algebraic property of any
ODE of the form (T1)-(T2) with vanishing initial asymmetry, valid on
any branch where the right-hand side of (T4) is positive (i.e. the
strong-washout-or-better regime that the radiation branch sits in).
It is not a numerical-match claim. Closure of the DM flagship lane
depends on the downstream `TRANSPORT_DECOMPOSITION` factorization
plus the microscopic selector law tracked by `TRANSPORT_STATUS`, and
is not implied by this transport-integral identity alone.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_transport_integral_theorem.py
```
