# Neutrino Majorana Lower-Level Pairing No-Go

**Status:** support - structural or confirmatory support note
**Claim type:** bounded_theorem
**Script:** [`scripts/frontier_neutrino_majorana_lower_level_pairing_nogo.py`](../scripts/frontier_neutrino_majorana_lower_level_pairing_nogo.py)
**Runner sha256:** `cb0094804621a83d7319565b1b875f8affdbf05fdbe6ababfd47868cd7a7e61f`

## Load-bearing statement (conditional, scope-narrowed)

**Conditional bounded no-go.** *If* the lower-level transport / Green /
source-response kernel acting on the `ΔL=2` Majorana channel is of the
charge-preserving normal block-diagonal class exhibited by the runner
(i.e. of the form `block_diag(N, conj(N))` for an invertible Hermitian
charge-preserving `N`), *then* the induced Nambu response has zero
anomalous block on that channel and the induced Majorana pairing
amplitude is identically zero.

This is the exact, runner-matched statement that this note now asserts.
The runner provides bounded numerical support (`PASS=5 FAIL=0` at
`n = 1, 3, 5` with fixed seeds) for the conditional consequence.

**What this note does *not* claim.** This note does **not** claim that
the framework's lower-level response layer is in fact restricted to the
charge-preserving normal class. That premise-side identification is a
separate bridge theorem (see *Repair path*, route 1) that this note
does not attempt and must not be read as carrying. Therefore, this note
must not be cited as evidence that the framework forbids Majorana
pairing on the `ΔL=2` channel; it only forbids it conditionally on the
runner's exhibited kernel class.

## Prior feedback perimeter (2026-05-05)

Prior independent feedback identified the missing bridge as the
load-bearing boundary for this row: the restricted packet did not derive
the relevant transport operator, Green/source-response construction,
Nambu block calculation, or uniqueness of the `ΔL=2` channel from the
framework. The requested repair was an explicit lower-level
transport / Green / source-response derivation proving that the
anomalous Nambu block vanishes on the unique `ΔL=2` Majorana channel.

This rigorization edit only sharpens that boundary. The runner-side
demonstration (`PASS=5 FAIL=0` on the inverted-block construction below)
is bounded support for the *induced* zero block on a generic
charge-preserving normal kernel, not the missing framework-to-bridge
derivation.

## What the runner demonstrates exactly

The companion script
[`scripts/frontier_neutrino_majorana_lower_level_pairing_nogo.py`](../scripts/frontier_neutrino_majorana_lower_level_pairing_nogo.py)
exhibits, for `n = 1, 3, 5`, an explicit Nambu kernel built from a generic
invertible charge-preserving Hermitian normal kernel `N` of size `n`:

`K_Nambu(N) = block_diag( (1 - N)^{-1}, (1 - conj(N))^{-1} )`

and verifies (deterministically with fixed `numpy.random.default_rng` seeds
1901, 2003, 2105) that:

1. the off-diagonal Nambu pairing block is identically zero, with measured
   norm below `1e-12`;
2. the induced Majorana amplitude vanishes (matches `mu = 0` in `mu J_2`
   for `n = 1` and `mu` times the size-`3` antisymmetric template for
   `n = 3`);
3. the same vanishing holds at `n = 5`, illustrating that the conclusion is
   not artifact-of-low-rank.

The runner thus demonstrates that *for any normal kernel of block-diagonal
charge-preserving form*, the algebraic Nambu-doubling formula produces a
diagonal block. It does **not** derive that the underlying
transport / Green / source-response layer of the framework is restricted
to such kernels; that is the missing bridge step flagged by prior
feedback.

## Dependency perimeter register

The table below separates load-bearing source references from sibling
context. Markdown links are reserved for intended graph dependencies;
plain code-formatted filenames are contextual and should not seed a
dependency edge.

| Source surface | Note | Role |
|---|---|---|
| Charge-preserving / number-zero normal grammar | [`NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md`](NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md) | candidate source for the charge-zero normal-kernel premise |
| Anomaly-fixed unique `nu_R` Majorana channel (`S_unique = nu_R^T C P_R nu_R`) | [`NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md`](NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md) | candidate source for uniqueness of the `ΔL=2` channel after one-generation matter closure |
| Local one-complex-coefficient reduction `mu J_2` | [`NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md`](NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md) | candidate source for the canonical antisymmetric Nambu-pairing form |
| Charge-two primitive reduction sibling | `NEUTRINO_MAJORANA_NUR_CHARGE2_PRIMITIVE_REDUCTION_NOTE.md` | contextual sibling; local `2 x 2` algebra |
| `nu_R` transfer-character boundary sibling | `NEUTRINO_MAJORANA_NUR_CHARACTER_BOUNDARY_NOTE.md` | contextual sibling; scalar-character family on the rank-`1` model line |
| Majorana lane packet | `NEUTRINO_MAJORANA_RETAINED_LANE_PACKET_2026-04-16.md` | aggregate context, not a theorem authority |

The open perimeter of this row is therefore the absence of a bridge theorem
deriving the *transport / Green / source-response operator class* from the
framework and proving that the framework class is contained in the
charge-preserving normal-kernel form the runner exhibits. The runner-side
calculation supports the *consequence* (zero anomalous block given a
charge-preserving normal kernel), but not the *premise* (the lower-level
layer is exactly that class).

## Repair path

This rigorization adopts the scope-narrowing route (route 2 below). The
load-bearing statement at the top of this note is now the conditional
implication that exactly matches the runner. The bridge theorem (route
1) remains a separately-targeted future row and is not asserted by this
note.

1. **Bridge theorem route (separate future row, not asserted here).**
   Provide a derivation that the lower-level transport / Green /
   source-response layer on the framework lane produces only kernels of
   the charge-preserving block-diagonal class exhibited in the runner;
   combine with this note's induced-zero demonstration to give the full
   bridge-then-block argument.
2. **Scope-narrowing route (adopted).** The load-bearing step is the
   conditional implication "*if* the lower-level response layer is
   contained in the charge-preserving normal-kernel class, *then* the
   induced Nambu pairing block vanishes," matching the runner's exact
   content. The bridge theorem is left as a separately-targeted future
   row rather than an asserted property of this note.

The runner calculation is unchanged. Independent audit owns any current
verdict or effective status after this source change.

## Verification

```bash
python3 scripts/frontier_neutrino_majorana_lower_level_pairing_nogo.py
```

Expected: `PASS=5 FAIL=0`. Runner sha256 `cb009480...7e61f`.
