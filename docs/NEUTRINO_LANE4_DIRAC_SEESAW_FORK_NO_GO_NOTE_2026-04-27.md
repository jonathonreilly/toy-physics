# Lane 4 Neutrino Dirac/Seesaw Fork No-Go

**Date:** 2026-04-27
**Status:** proposed_retained exact negative boundary for Lane 4 claim
accounting. This is not full neutrino closure, not a global no-go against
Majorana neutrinos, and not a global no-go against Dirac neutrinos.
**Script:** `scripts/frontier_neutrino_lane4_dirac_seesaw_fork_no_go.py`
**Lane:** Lane 4 neutrino quantitative closure

## Question

Can the current-stack Majorana zero law, the diagonal seesaw atmospheric-scale
benchmark, and the retained local coefficient `y_nu^eff = g_weak^2/64` be
treated as one global quantitative neutrino-mass closure?

## Result

No.

They live on a forked claim surface unless an extra activation law is supplied.

The current retained stack gives the exact Majorana activation law

```text
mu_current = 0.
```

Therefore the current-stack right-handed Majorana matrix is non-invertible on
the type-I seesaw surface. The diagonal atmospheric-scale benchmark instead
uses a nonzero right-handed Majorana spectrum

```text
M_1 = B(1 - alpha_LM/2),
M_2 = B(1 + alpha_LM/2),
M_3 = A,
```

with `A = M_Pl alpha_LM^7` and `B = M_Pl alpha_LM^8`. That benchmark is useful
and numerically successful for the atmospheric scale, but it is not the same
surface as the current-stack `mu_current = 0` theorem.

Conversely, using `y_nu^eff` directly as a one-Higgs Dirac Yukawa eigenvalue
does not close the Dirac lane. With the Standard Model one-Higgs convention,

```text
m_D = y_nu^eff v/sqrt(2)
```

is GeV-scale, not meV-scale. A pure Dirac closure for the atmospheric mass
would need a separate tiny Yukawa activation law of order `10^-13`.

## Theorem

**Theorem (Lane 4 Dirac/seesaw fork no-go).** Assume the current retained
Majorana zero law `mu_current = 0`, the retained one-Higgs Yukawa gauge
selection convention, and the existing diagonal atmospheric-scale benchmark.
Then there is no single current-stack quantitative neutrino-mass closure that
simultaneously:

1. keeps the current-stack right-handed Majorana matrix at zero;
2. uses the type-I seesaw formula with an invertible right-handed Majorana
   matrix;
3. reuses `y_nu^eff = g_weak^2/64` as a direct Dirac mass eigenvalue; and
4. claims the Lane 4 absolute-mass target is retained.

At least one additional positive premise is required:

- a nonzero charge-2 Majorana primitive or equivalent admitted Majorana/seesaw
  extension, or
- a separate tiny Dirac `Y_nu` activation law on the surviving Dirac lane.

## What This Retires

This retires one hidden-closure conflation:

```text
current-stack mu=0
  + diagonal seesaw atmospheric benchmark
  + retained local y_nu^eff
  => full quantitative neutrino closure
```

That implication is false. The three inputs are individually useful, but they
do not by themselves close the global Lane 4 target.

## What Remains Open

The lane remains open. The exact fork is now sharper:

- **Majorana/seesaw route:** derive a nonzero charge-2 primitive, then derive
  the full right-handed Majorana texture, including the solar gap.
- **Dirac route:** derive the small Dirac Yukawa activation law on the minimal
  surviving Dirac lane. The current exact reductions already compress this
  target, but they do not supply the seven required quantities.

The existing atmospheric benchmark remains a bounded/support surface, not a
global retained neutrino-mass closure.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_neutrino_lane4_dirac_seesaw_fork_no_go.py
```

Expected result:

```text
PASS=10 FAIL=0
```

## Inputs And Import Roles

| Input | Role | Import class | Source |
|---|---|---|---|
| `mu_current = 0` | current-stack Majorana zero law | exact current-stack theorem | `docs/NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md` |
| `y_nu^eff = g_weak^2/64` | retained local coefficient used by the benchmark | retained support | `docs/NEUTRINO_MASS_DERIVED_NOTE.md` |
| `M_1 = B(1 - alpha_LM/2)` | diagonal seesaw benchmark scale | bounded/support Majorana extension surface | `docs/DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md` |
| one-Higgs Dirac mass convention `m = y v/sqrt(2)` | Dirac misuse guard | retained/exact SM gauge-selection convention | `docs/SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md` |

No observed neutrino mass, solar splitting, PMNS angle, or cosmological bound
is used as a derivation input in this no-go.

## Safe Wording

Can claim:

- the current-stack Dirac and seesaw routes are forked unless an extra
  activation law is supplied;
- the diagonal seesaw atmospheric benchmark cannot be silently upgraded to
  global Lane 4 closure while retaining `mu_current = 0`;
- `y_nu^eff` is not a direct one-Higgs Dirac neutrino eigenvalue.

Cannot claim:

- full neutrino quantitative closure;
- a final no-go against all Majorana extensions;
- a final no-go against all Dirac neutrino masses;
- that the atmospheric-scale benchmark is useless.
