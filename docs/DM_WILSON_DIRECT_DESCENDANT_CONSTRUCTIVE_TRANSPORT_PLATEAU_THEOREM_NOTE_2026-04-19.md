# DM Wilson Direct-Descendant Constructive Transport Plateau Theorem

**Date:** 2026-04-19  
**Status:** exact current-branch nonuniqueness theorem for constructive-sign
transport extremality. On the fixed native `N_e` seed surface, maximizing the
favored constructive transport column inside the constructive sign chamber

```text
gamma > 0,  E1 > 0,  E2 > 0
```

does **not** uniquely pick the constructive endpoint. The branch carries at
least four pairwise distinct interior constructive witnesses with the same
extremal value

```text
eta_1 = 1.052220313052...
```

So transport extremality alone cannot canonicalize the endpoint of the new
canonical path law.

**Primary runner:**  
`scripts/frontier_dm_wilson_direct_descendant_constructive_transport_plateau_theorem_2026_04_19.py`
(`PASS=18 FAIL=0`).

## Question

The same-day canonical-path theorem gave a real selector-law candidate:

> choose the unique `eta_1 = 1` point on the aligned-seed ->
> constructive-witness affine path.

But that still left a natural next question:

Can the constructive endpoint itself be made canonical just by appealing to the
already-known transport result?

More sharply:

- the constructive projected-source theorem already proved that the
  constructive sign chamber reaches the current transport-extremal value;
- does maximizing `eta_1` inside that constructive sign chamber uniquely pick
  the constructive witness?

## Bottom line

No.

The current branch does not give a unique constructive-sign transport
extremizer. It gives a **plateau**.

In addition to the original constructive witness `W0`, deterministic local
refinement from three explicit constructive interior anchors recovers three
more pairwise distinct interior witnesses `W1`, `W2`, `W3` such that:

1. each lies strictly inside

   ```text
   gamma > 0, E1 > 0, E2 > 0;
   ```

2. each satisfies

   ```text
   eta_1 = 1.052220313052...
   ```

   to current-branch precision;
3. each is an interior stationary extremizer on the fixed seed surface;
4. the witnesses are pairwise distinct both in source coordinates and in
   observable data.

So the constructive extremal set is already nonunique before the path law is
even imposed.

## The four explicit constructive extremal witnesses

The branch now has at least the following four constructive interior
transport-extremal witnesses:

### `W0` (the original constructive witness)

```text
x = (1.17416156, 0.46254435, 0.05329409)
y = (0.75874142, 0.02690430, 0.13435428)
delta = 1.882595756164
eta = (0.92932093, 1.05222031, 0.80149003)
(gamma, E1, E2) = (0.15014724, 0.29656285, 1.98640744)
```

### `W1`

```text
x = (0.90533908, 0.34108481, 0.44357611)
y = (0.77562148, 0.00429993, 0.14007859)
delta = 2.248936000000
eta = (0.74569694, 1.05222031, 0.87957312)
(gamma, E1, E2) = (0.09875887, 0.12204367, 1.34544744)
```

### `W2`

```text
x = (1.10861499, 0.41991159, 0.16147342)
y = (0.83443268, 0.00372167, 0.08184565)
delta = 1.480589000000
eta = (0.82166028, 1.05222031, 0.69287680)
(gamma, E1, E2) = (0.09036640, 0.24289064, 1.99942908)
```

### `W3`

```text
x = (1.13210268, 0.52825826, 0.02963906)
y = (0.48423456, 0.18550120, 0.25026425)
delta = 2.930589000000
eta = (1.01405294, 1.05222031, 1.03502767)
(gamma, E1, E2) = (0.05933995, 0.39139937, 1.31153236)
```

All four sit on the same fixed native seed surface. All four are strictly
constructive. All four attain the same extremal `eta_1`.

## Why this matters

This closes the most obvious attempt to make the new path law less arbitrary.

One might have hoped that the path endpoint could be justified as:

> the unique constructive-sign transport extremizer.

That route is now closed negatively.

The branch instead shows:

- constructive-sign transport extremality is real;
- but it is already nonunique;
- so it does **not** uniquely determine the endpoint used by the canonical
  path law.

This is exactly the kind of obstruction the branch needed next, because it
sharpens the remaining selector problem:

- not “find any constructive transport extremizer”;
- but “find the finer law that picks one point on the constructive extremal
  plateau.”

## Relation to the canonical path theorem

The canonical path theorem remains valid:

- the aligned-seed -> constructive-witness path crosses exact closure once and
  transversely;
- so it gives a genuine path-selected law candidate.

But the present theorem shows that transport extremality does **not** derive
its endpoint uniquely.

So the path theorem’s honest scope becomes even sharper:

- **path-selected law:** yes;
- **endpoint canonicalized by transport extremality:** no.

## What this closes

- the attempt to make the path endpoint canonical by constructive-sign
  transport extremality alone;
- the idea that the constructive witness was already the unique extremal point
  of the constructive sign chamber;
- the possibility that transport extremality alone would remove the remaining
  arbitrariness in the new path law.

## What this does not close

- a finer law selecting one point on the constructive transport plateau;
- a reviewer-grade derivation of the constructive endpoint from retained
  physics;
- the microscopic value law on `L_e = Schur_{E_e}(D_-)`;
- the final DM flagship gate.

## Cross-references

- `docs/DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_PROJECTED_SOURCE_SELECTOR_THEOREM_NOTE_2026-04-16.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_PATH_SELECTOR_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md`

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_constructive_transport_plateau_theorem_2026_04_19.py
```

Expected:

- `PASS=18 FAIL=0`
