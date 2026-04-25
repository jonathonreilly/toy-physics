# Fractional Charge Denominator From N_c Theorem

**Date:** 2026-04-24

**Status:** Retained structural corollary on the matter/gauge surface. This
packages the exact relation between the left-handed color multiplicity `N_c`
and the denominator of quark electric charge. It is implicit in
[`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
and in the `{1, 3}` denominator corollary of
[`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md),
but was not previously isolated as a named theorem.

**Primary runner:** `scripts/frontier_fractional_charge_denominator_from_n_c.py`

## Statement

Consider the retained left-handed template with one weak quark doublet carrying
`N_c` color copies and one weak lepton doublet carrying no color. A diagonal
commutant `U(1)` generator with eigenvalue `a` on `Q_L` and `b` on `L_L`
is traceless on the `2 N_c + 2` left-handed states iff

```text
2 N_c a + 2 b = 0.
```

Therefore

```text
Y(Q_L) : Y(L_L) = 1 : -N_c.
```

Fixing the conventional lepton normalization `Y(L_L) = -1` gives

```text
Y(Q_L) = 1/N_c.
```

With the standard doubled-hypercharge convention used throughout the retained
notes,

```text
Q = T_3 + Y/2,
```

the left-handed electric charges are

```text
Q(u_L)  = (N_c + 1)/(2 N_c),
Q(d_L)  = (1 - N_c)/(2 N_c),
Q(nu_L) = 0,
Q(e_L)  = -1.
```

After reducing fractions, the nonzero quark-charge denominator is

```text
denominator = N_c      if N_c is odd,
denominator = 2 N_c    if N_c is even.
```

For the retained graph-first color value `N_c = 3`,

```text
Y(Q_L) = 1/3,
Q(u_L) = 2/3,
Q(d_L) = -1/3.
```

Thus the third-integer quark-charge denominator is exactly the retained
`N_c = 3` denominator.

## Derivation

The left-handed multiplicities are:

| Field | weak multiplicity | color multiplicity | total |
|---|---:|---:|---:|
| `Q_L` | 2 | `N_c` | `2 N_c` |
| `L_L` | 2 | 1 | 2 |

Tracelessness gives

```text
Tr(Y) = (2 N_c) a + 2 b = 0
      = 2 (N_c a + b).
```

Hence `b = -N_c a`, so the eigenvalue ratio is `a:b = 1:-N_c`. Setting
`b = -1` fixes `a = 1/N_c`.

The charge formulas then follow directly:

```text
Q(u_L)  =  1/2 + 1/(2 N_c) = (N_c + 1)/(2 N_c),
Q(d_L)  = -1/2 + 1/(2 N_c) = (1 - N_c)/(2 N_c),
Q(nu_L) =  1/2 - 1/2       = 0,
Q(e_L)  = -1/2 - 1/2       = -1.
```

For odd `N_c`, both `N_c + 1` and `N_c - 1` are even, and the reduced quark
charge denominators are `N_c`. For even `N_c`, `N_c +/- 1` is odd and shares
no common factor with `2 N_c`, so the reduced denominator is `2 N_c`.

## N_c Scan

| `N_c` | parity | `Y(Q_L)` | `Q(u_L)` | `Q(d_L)` | denominator |
|---:|---|---:|---:|---:|---:|
| 1 | odd | 1 | 1 | 0 | 1 |
| 2 | even | 1/2 | 3/4 | -1/4 | 4 |
| 3 | odd | 1/3 | 2/3 | -1/3 | 3 |
| 4 | even | 1/4 | 5/8 | -3/8 | 8 |
| 5 | odd | 1/5 | 3/5 | -2/5 | 5 |

The retained `N_c = 3` case is the first nontrivial colored case with the
observed third-integer denominator.

## Joint Constraint With Witten Z_2

[`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md)
shows that a retained-style generation has weak-doublet count

```text
N_D = N_c + 1.
```

The Witten global anomaly cancels per generation iff this count is even, hence
iff `N_c` is odd. Combined with the denominator theorem:

```text
Witten-consistent retained-style one-generation template
  => N_c odd
  => quark-charge denominator = N_c.
```

This does not by itself derive `N_c = 3`; it says that on the Witten-consistent
retained-style template, the fractional-charge denominator tracks `N_c`.
The separate graph-first color lane supplies the retained `N_c = 3` value.

## Relation To Hypercharge Uniqueness

This theorem covers the left-handed denominator source:

```text
Tr(Y)_LH = 0  =>  Y(Q_L) = 1/N_c.
```

The right-handed hypercharges are not derived here. They are fixed by
[`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
after adding the retained singlet right-handed completion, anomaly equations,
`Y(nu_R)=0`, and the positive up-type label. At `N_c = 3`, the two theorems
combine to give the full one-generation charge set

```text
{0, +/-1/3, +/-2/3, +/-1}.
```

## Observational Surface

Within the retained left-handed template, a fundamental fermion with a
non-third-integer fractional charge would be incompatible with the retained
`N_c = 3` denominator. The observed quark flavors repeat the same
third-integer pattern:

```text
u, c, t:  +2/3
d, s, b:  -1/3
```

This is a denominator-pattern check, not an independent derivation of
`N_c = 3`.

## Scope

This note claims:

- the exact trace relation `Y(Q_L):Y(L_L) = 1:-N_c`;
- the exact quark-charge denominator rule `N_c` for odd `N_c` and `2 N_c`
  for even `N_c`;
- the retained `N_c = 3` specialization to third-integer quark charge;
- the joint Witten corollary that Witten-consistent retained-style templates
  have denominator `N_c`.

This note does not claim:

- native-axiom uniqueness of `N_c = 3`;
- a derivation of the right-handed hypercharges;
- a classification of all anomaly-free or beyond-Standard-Model matter
  extensions;
- exclusion of altered left-handed templates, mirror/vectorlike matter, extra
  `U(1)` factors, or nonretained charge conventions.

## Reproduction

```bash
python3 scripts/frontier_fractional_charge_denominator_from_n_c.py
```

The runner uses exact `fractions.Fraction` arithmetic to verify the trace
equation, the retained `N_c = 3` charge spectrum, the denominator parity scan,
the Witten parity relation, and the combined full one-generation charge set
when paired with the retained right-handed hypercharge uniqueness theorem.

## Cross-References

- [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
  - the `6a + 2b = 0` specialization at `N_c = 3`.
- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  - retained left-handed `Q_L` and `L_L` charge surface.
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
  - retained graph-first `N_c = 3` color structure.
- [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md)
  - Witten parity constraint on weak doublets.
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
  - right-handed hypercharge uniqueness and full one-generation electric
    charge set.
