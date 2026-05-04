# Quark Endpoint Denominator Admissibility

**Date:** 2026-04-19
**Status:** exact denominator-admissibility theorem / no-go on the current
reduced quark endpoint atoms
**Primary runner:** `scripts/frontier_quark_endpoint_denominator_admissibility.py`

## Safe statement

The current quark endpoint denominator problem does **not** need another wide
expression search.

On the live reduced endpoint, the exact atoms already force a much smaller
multiplicative support grammar. After

1. stripping the fixed projector prefactor `sqrt(5/6)` down to its support
   denominator slot, and
2. excluding bridge ratios that still carry numerator contamination,

the smallest structurally admissible exact denominator generator class is

```text
{6, 7, sqrt(6), sqrt(7)}.
```

The datum-inclusive realized admissible class on the live endpoint atoms is

```text
{6, 7, 42, sqrt(6), sqrt(7), sqrt(42)}.
```

So the honest uniqueness statement is:

- `sqrt(7)` is **not** unique on the full admissible class;
- `sqrt(7)` is unique only in the pure seven-only irrational generator
  subclass.

That is a theorem-grade restriction on the denominator lane, not another
bounded fit scan.

## Exact endpoint atoms

The current lane starts from the exact endpoint atoms

```text
{delta_A1, 6/7, 1/6, 1/sqrt(42), 1/sqrt(7), sqrt(6/7), sqrt(5/6)}.
```

Write every atom on the exact support/projector exponent basis

```text
value = 5^(a5/2) 6^(a6/2) 7^(a7/2).
```

Then the live atoms are:

- `delta_A1 = 1/42 = 6^-1 7^-1`
- `6/7 = 6^1 7^-1`
- `1/6 = 6^-1`
- `1/sqrt(42) = 6^-1/2 7^-1/2`
- `1/sqrt(7) = 7^-1/2`
- `sqrt(6/7) = 6^1/2 7^-1/2`
- `sqrt(5/6) = 5^1/2 6^-1/2`

Two immediate facts matter:

1. every support exponent already lies on the half-integer `6/7` lattice;
2. `6/7` and `sqrt(6/7)` are **not** pure denominator atoms, because they
   still carry positive six-power numerator content.

So the denominator lane should be organized by support denominator slots, not
by every exact scalar that appears nearby.

## The admissibility restriction

Define the denominator-admissibility class by three exact rules:

1. keep only multiplicative exact forms; no additive mixing;
2. project away the fixed projector `sqrt(5)` numerator carried by
   `sqrt(5/6)`;
3. keep only pure reciprocal support slots, meaning no positive six- or
   seven-power numerator remains after simplification.

Under those rules:

- `1/6` contributes the exact denominator slot `6`;
- `1/sqrt(7)` contributes the exact denominator slot `sqrt(7)`;
- `1/sqrt(42)` contributes the exact denominator slot `sqrt(42)`;
- stripping `sqrt(5/6)` to the support side contributes the exact denominator
  slot `sqrt(6)`.

The missing rational seven-slot is then recovered exactly from the live support
atoms:

```text
delta_A1 / (1/6) = 1/7
```

and equivalently

```text
(6/7) * (1/6) = 1/7.
```

This is the only extra rational denominator forced by the current support
centering.

## The theorem-grade endpoint

### Smallest generator class

The smallest structurally admissible denominator generator class is therefore

```text
D_gen = {6, 7, sqrt(6), sqrt(7)}.
```

This is minimal because:

- `6` and `sqrt(6)` are genuinely present on the live endpoint;
- `7` and `sqrt(7)` are genuinely present on the live endpoint;
- every other live reciprocal denominator is a product of these generators;
- bridge ratios do not add new denominator generators because they keep a
  numerator component.

### Datum-inclusive realized class

The live endpoint also realizes two composite denominators:

```text
42 = 6 * 7
sqrt(42) = sqrt(6) * sqrt(7).
```

So the datum-inclusive realized admissible class is

```text
D_real = {6, 7, 42, sqrt(6), sqrt(7), sqrt(42)}.
```

This is the exact realized class on the current atoms. It is not an open
closure under arbitrary multiplication; it is the realized support-denominator
surface forced by the endpoint atoms already in play.

## `sqrt(7)` uniqueness / no-go

This gives the exact answer to the uniqueness question.

### On the full admissible class

`sqrt(7)` is **not** unique on the full realized admissible class. The
seven-bearing realized denominators are

```text
{7, 42, sqrt(7), sqrt(42)}.
```

So any claim that the current endpoint forces a unique seven-denominator would
be false.

### Even on the irrational seven-bearing subclass

`sqrt(7)` is still **not** unique if one restricts only to irrational
seven-bearing realized denominators:

```text
{sqrt(7), sqrt(42)}.
```

The mixed six-seven radical `sqrt(42)` remains admissible.

### Where `sqrt(7)` does become unique

`sqrt(7)` **is** unique on the pure seven-only irrational generator subclass:

```text
{sqrt(7)}.
```

That is the sharp theorem-grade statement:

- unique as the pure seven-only irrational generator;
- not unique on the full admissible class;
- not unique even on the irrational seven-bearing realized class.

## Why the two simplifications matter

Two denominator strings from the broader branch simplify the endpoint logic.

### `sqrt(42/5)`

The exact simplification

```text
sqrt(42/5) = sqrt(7) / sqrt(5/6)
```

shows that once the fixed projector prefactor is restored, this denominator
reduces to the `sqrt(7)` support slot. So it does **not** introduce a new
support denominator beyond the admissible class above.

### `2 + sqrt(5/6)`

The current best two-step denominator string simplifies to

```text
2 + sqrt(5/6).
```

This is additive projector dressing, not a multiplicative support denominator.
So it lies outside the admissibility grammar used here and does not enlarge the
exact denominator class.

## Interpretation

This sharply narrows the denominator lane.

The right conclusion is not:

- “try every nearby exact denominator.”

It is:

- the exact endpoint already lives on a four-generator support denominator
  grammar;
- the live realized denominator surface is only six elements wide;
- `sqrt(7)` is not globally forced;
- only the pure seven-only irrational generator slot is unique.

That is a theorem-grade restriction and a clean no-go against overclaiming
`sqrt(7)` as the unique admissible denominator on the current endpoint.

## Validation

Run:

```bash
python3 scripts/frontier_quark_endpoint_denominator_admissibility.py
```

Current expected result on this branch:

- `frontier_quark_endpoint_denominator_admissibility.py`: `PASS=11 FAIL=0`

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [quark_endpoint_readout_constraints_note_2026-04-19](QUARK_ENDPOINT_READOUT_CONSTRAINTS_NOTE_2026-04-19.md)
