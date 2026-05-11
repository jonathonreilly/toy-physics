# Probe Y-L1-Ratios: Wilson-Chain Heavy-Quark Ratio Comparator

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/cl3_koide_y_l1_ratios_2026_05_08_probeY_L1_ratios.py`](../scripts/cl3_koide_y_l1_ratios_2026_05_08_probeY_L1_ratios.py)
**Cache:** [`logs/runner-cache/cl3_koide_y_l1_ratios_2026_05_08_probeY_L1_ratios.txt`](../logs/runner-cache/cl3_koide_y_l1_ratios_2026_05_08_probeY_L1_ratios.txt)

## Claim

This note records a bounded observational-comparator diagnostic for the
Wilson-chain mass-ratio route. It asks whether the PDG comparator ratios
`m_q/m_tau` for `q in {t,b,c}` sit on an integer or simple-rational
power of the Wilson-chain scale

```text
alpha_LM = 0.090668
```

under the exponent definition

```text
Delta n(q) = log(m_q / m_tau) / log(alpha_LM).
```

Using the fixed comparator masses in the runner (`m_tau=1.77686 GeV`,
`m_t=172.69 GeV`, `m_b=4.18 GeV`, `m_c=1.27 GeV`), none of the three
heavy quarks passes a 5% mass-error gate for:

- integer `Delta n`; or
- simple rational `p/q` with `q <= 6`.

This is a bounded negative result for this comparator protocol only. It
does not derive quark masses, does not rule out other heavy-quark
mechanisms, and does not depend on or land any sibling absolute-mass
probe.

## Imports

The mass values are observational comparators, not derivation inputs.
The Wilson-chain scale `alpha_LM=0.090668` is used as a fixed numeric
context value for this diagnostic. No PDG value is promoted into a
framework axiom or retained theorem.

## Results

The runner verifies:

- `t`: best integer exponent is `-2`, with about 25% mass error;
- `b`: best integer exponent is `0`, with about 58% mass error;
- `c`: best integer exponent is `0`, with about 40% mass error;
- the best simple-rational `q <= 6` fits for all three heavy quarks
  still exceed the 5% gate;
- the near relation `m_b/m_c ~= alpha_LM^(-1/2)` is recorded only as a
  comparator observation, not as a derived theorem.

## Boundaries

This note does not:

- close a heavy-quark mass theorem;
- claim Wilson-chain routes are impossible outside this finite
  comparator protocol;
- cite an unmerged sibling PR as landed authority;
- assert retained or audited status;
- add a new axiom, new physics primitive, or new repo-wide theory
  language.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/cl3_koide_y_l1_ratios_2026_05_08_probeY_L1_ratios.py
```

Expected result:

```text
TOTAL: PASS=20 FAIL=0
```
