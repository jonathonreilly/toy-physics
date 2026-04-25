# Koide A1 radian-bridge irreducibility audit

**Date:** 2026-04-24
**Status:** retained support / no-go audit. This audit does **not** close the
charged-lepton Koide lane.
**Runner:** `scripts/frontier_koide_a1_radian_bridge_irreducibility_audit.py`

## Decision

The reviewed branch contains useful science, but its stronger closure language
is not retained.

What lands is narrower:

```text
retained periodic phase sources  ->  rational multiples of pi
Brannen selected-line target     ->  pure rational 2/9 used as a radian
therefore:
  a Type-B rational-to-radian observable law is still missing.
```

The branch's proposed postulate can be stated cleanly:

```text
P_A1:
  the charged-lepton Yukawa selected-line phase is a Type-A phase observable
  whose numerical value is the Type-B lattice ratio 2/N^2 at N=3.
```

`P_A1` is a sharp candidate primitive, not a retained theorem.

## Landed science

### 1. Type-A / Type-B split

The useful distinction is:

- **Type A:** periodic phase quanta. These come from finite lattice
  periodicity, APBC Matsubara phases, Brillouin-zone momenta, `Z_3`
  characters, finite Wilson monodromies, and closed-orbit Berry phases. On the
  retained lattice surfaces audited here, every such phase is of the form
  `q*pi` with `q in Q`.
- **Type B:** combinatorial or representation-counting quanta. These are pure
  rationals from dimension counts, Plancherel weights, Casimir ratios,
  charge products, and ABSS/APS fractional values.

The two numerical sets are disjoint away from zero:

```text
{q*pi : q in Q} cap Q = {0}.
```

So a nonzero pure rational such as `2/9` is not supplied as a literal radian
by a retained periodic phase source.

### 2. Retained periodic phase-source audit

The compact runner verifies the branch's main no-go content without landing
the generated probe forest:

- APBC phases are `(2n+1)pi/L_t`;
- Brillouin-zone momenta are `2pi n/L`;
- `Z_3` characters are `2pi k/3`;
- finite Wilson monodromies and cyclic extensions remain roots of unity;
- tensor, symmetric, exterior, and direct-product constructions preserve the
  root-of-unity / `q*pi` form;
- real Wilson/staggered sign phases are only `0` or `pi`.

Therefore the old "lattice propagator radian quantum" route does not provide
the literal `2/9` radian value on retained data.

### 3. Multiple `2/9` rational witnesses do not solve the unit step

The audit preserves the branch's useful inventory of exact `2/9` witnesses:

```text
2/N^2 at N=3                         = 2/9
dim_R(complex b) / dim_R(Herm_3)      = 2/9
2 * (1 - (1 - 1/N_c^2)) at N_c=3      = 2/9
C2(SU(3) fund) / C2(Sym^3 fund)       = (4/3)/6 = 2/9
Y_L^2 - Y_Q^2                         = 1/4 - 1/36 = 2/9
Q_up * |Q_down|                       = (2/3)(1/3) = 2/9
eta_APS(Z_3; 1,2)                     = 2/9
```

These are useful support coincidences on the retained arithmetic surface.
They do not derive that the selected-line phase observable must read that
dimensionless rational as radians. Stacking many rationals still leaves the
same Type-B-to-radian map as the remaining primitive.

### 4. The old remaining hopes collapse to the same obstruction

The audit keeps the branch's best route-pruning result:

- finite `Z_3` / `C_9` / tensor Wilson constructions can produce `d^2 = 9`
  arithmetic, but their phases are still roots of unity, hence `q*pi`;
- a proposed identity like `W^9 = exp(2i)` cannot be realized by a finite-order
  Wilson element, because finite order gives a root of unity and `exp(2i)` is
  not one;
- adding a `C_3` singlet or finite tensor/symmetric construction does not by
  itself introduce a new irrational-radian primitive.

Thus the finite-Wilson and extended-block escape routes reduce to the same
missing continuous/literal-radian source.

### 5. Two A1 mechanism no-gos are worth retaining

The branch also supplied two reusable A1-side negative results:

- **Equivariant-index no-go:** representation indices are insensitive to the
  continuous Hermitian modulus ratio `|b|^2/a^2`; they cannot force the A1
  condition `|b|^2/a^2 = 1/2` without an additional measure/readout primitive.
- **Minimal heat-kernel no-go:** a minimal single-trace heat-kernel expansion
  supplies single traces such as `Tr(Phi^2)` and `Tr(Phi^4)`, while the
  Koide-Nishiura quartic is multi-trace. Producing it requires a nonminimal
  multi-trace/source law.

Both are useful route eliminations. Neither is a positive derivation of A1.

## Boundary

This audit does **not** claim:

- that no future theorem can ever derive the Koide/Brannen phase;
- that `P_A1` is part of the retained framework axioms;
- that `delta = 2/9` is a direct PDG observable rather than the selected-line
  Brannen/Koide parameterization target;
- that the `Q` side is closed;
- that the selected-line local boundary-source law or based endpoint section
  is derived;
- that the overall charged-lepton scale `v_0` is derived.

The current safe closeout is:

```text
KOIDE_A1_RADIAN_BRIDGE_AUDIT_CLOSES_Q=FALSE
KOIDE_A1_RADIAN_BRIDGE_AUDIT_CLOSES_DELTA=FALSE
POSTULATE_P_A1_RETAINED_FRAMEWORK_AXIOM=FALSE
TYPE_B_TO_RADIAN_IDENTIFICATION_REMAINS_PRIMITIVE=TRUE
RESIDUAL_PRIMITIVE=type_b_rational_to_radian_observable_law
```

## Relationship to the April 24 Koide packet

This note sharpens the `delta` side of the April 24 native-dimensionless
packet. It does not replace that packet's residuals:

```text
Q remains:
  physical background-zero / Z-erasure.

delta remains:
  selected-line local boundary-source law
  plus based endpoint section
  plus Type-B rational-to-radian observable law.
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_a1_radian_bridge_irreducibility_audit.py
```

Expected final flags:

```text
KOIDE_A1_RADIAN_BRIDGE_AUDIT_CLOSES_Q=FALSE
KOIDE_A1_RADIAN_BRIDGE_AUDIT_CLOSES_DELTA=FALSE
POSTULATE_P_A1_RETAINED_FRAMEWORK_AXIOM=FALSE
TYPE_B_TO_RADIAN_IDENTIFICATION_REMAINS_PRIMITIVE=TRUE
```
