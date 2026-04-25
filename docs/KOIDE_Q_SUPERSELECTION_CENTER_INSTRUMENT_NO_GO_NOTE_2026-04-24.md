# Koide Q superselection center-instrument no-go

## Theorem attempt

Maybe the charged-lepton observable is not asking for a trace state at all, but
for a retained superselection measurement of the two central `C_3` sectors.  If
the physical instrument only sees the center labels

```text
{plus, perp},
```

then perhaps measurement theory itself forces equal label weights, yielding
`K_TL=0` and the usual consequence chain:

```text
K_TL = 0 -> Y = I_2 -> E_+ = E_perp -> kappa = 2 -> Q = 2/3.
```

## Brainstorm/ranking

1. Sector-nondemolition instrument: strongest retained authority; it tests
   whether the measurement effects force the state.
2. Equal pointer-label prior: positive-looking, but likely imports the missing
   center-state law.
3. Lueders/nonselective update: tests whether measurement dynamics equalizes
   arbitrary central states.
4. Hilbert-trace instrument: retained representation-compatible but expected to
   give rank weights.
5. POVM rescaling by sector rank: can land on equal labels, but risks being an
   unexplained effect normalization.

The runner implements the first, third, and fourth variants exactly and exposes
the second/fifth as residual state choices.

## Exact result

The retained central projections satisfy

```text
rank(P_plus) = 1,
rank(P_perp) = 2.
```

A sector-nondemolition two-outcome POVM has effects

```text
F_plus = a P_plus,
F_perp = b P_perp.
```

Completeness forces

```text
a = b = 1,
```

so the instrument is the projective measurement `{P_plus, P_perp}`.  This fixes
the question being measured, not the pre-measurement central state.

Every normalized `C_3`-invariant central state can be written as

```text
rho(u) = u P_plus + (1-u) P_perp / 2,
```

with outcome probabilities

```text
p_plus = u,
p_perp = 1-u.
```

The source-neutral condition is the special state

```text
u = 1/2.
```

The retained Hilbert/rank state is instead `u=1/3`:

```text
rho_H = I/3,
(p_plus,p_perp) = (1/3,2/3),
Q = 1,
K_TL = 3/8.
```

The equal-label center state is

```text
rho_label = P_plus/2 + P_perp/4,
(p_plus,p_perp) = (1/2,1/2),
Q = 2/3,
K_TL = 0.
```

Both states are compatible with the same superselection instrument.

## Hostile review

- **Circularity:** requiring equal pointer labels is exactly the missing
  center-state/source law in measurement language.
- **Target import:** the runner uses `Q=2/3` and `K_TL=0` only as tested
  consequences of `u=1/2`, not as assumptions.
- **Hidden observational pin:** the audit stays symbolic; it never reads
  empirical mass tables, external witness values, or physical delta endpoint
  data.
- **Missing axiom link:** retained superselection fixes the PVM but does not
  select the central density state.
- **Overbroad claim avoided:** this no-go covers finite retained
  center-sector instruments; it does not exclude a future physical theorem that
  derives `rho_label`.

## Residual

```text
RESIDUAL_SCALAR = center_label_state_u_minus_one_half_equiv_K_TL
RESIDUAL_STATE = center_label_state_u_minus_one_half_equiv_K_TL
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_superselection_center_instrument_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_SUPERSELECTION_CENTER_INSTRUMENT_NO_GO=TRUE
Q_SUPERSELECTION_CENTER_INSTRUMENT_CLOSES_Q=FALSE
RESIDUAL_SCALAR=center_label_state_u_minus_one_half_equiv_K_TL
RESIDUAL_STATE=center_label_state_u_minus_one_half_equiv_K_TL
```
