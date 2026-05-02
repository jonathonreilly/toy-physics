# Signed Gravity Nonlocal Projector-Charge `chi_g` Probe Note

**Date:** 2026-04-25
**Status:** first concrete Candidate C probe; formal control only
**Script:** [`../scripts/signed_gravity_nonlocal_projector_charge_probe.py`](../scripts/signed_gravity_nonlocal_projector_charge_probe.py)

This note records a first matrix/projection pass on the nonlocal
projector-difference sector-charge candidate from
[`SIGNED_GRAVITY_NONLOCAL_BOUNDARY_CHI_TARGET_NOTE.md`](SIGNED_GRAVITY_NONLOCAL_BOUNDARY_CHI_TARGET_NOTE.md):

```text
Q_chi = P_+ - P_-
rho_active(x) = M_phys psi^dagger(x) Q_chi psi(x).
```

The language boundary is unchanged. This is not a negative-mass, shielding,
propulsion, or physical antigravity claim. The question here is only whether a
global projector-difference charge can evade the local neutral-label
obstruction enough to become a theorem target for `chi_g`.

## Probe Surface

The harness uses a finite local staggered chain tensored with an external
two-sector Hilbert space:

```text
H_total = H_position tensor C^2_sector
Q_chi = I_position tensor diag(+1, -1)
P_+ = (I + Q_chi)/2
P_- = (I - Q_chi)/2
H_retained = H_local tensor I_sector
```

This deliberately leaves the local taste-cell algebra audited in
[`SIGNED_GRAVITY_CHI_SELECTOR_THEOREM_OR_NOGO_NOTE.md`](SIGNED_GRAVITY_CHI_SELECTOR_THEOREM_OR_NOGO_NOTE.md).
It tests the best formal version of Candidate C: if the two global sectors are
already exact superselection sectors, does the projector charge pass the
consequence controls?

The probe also keeps the retained scalar source-action audit from
[`SIGNED_GRAVITY_SOURCE_ACTION_ESCAPE_HATCH_NOTE.md`](SIGNED_GRAVITY_SOURCE_ACTION_ESCAPE_HATCH_NOTE.md)
and
[`GRAVITY_SIGNED_SOURCE_DENSITY_BOUNDARY_NOTE.md`](GRAVITY_SIGNED_SOURCE_DENSITY_BOUNDARY_NOTE.md)
separate from an added projector-source action. That separation is the key
classification point.

## Result

Command:

```bash
python3 scripts/signed_gravity_nonlocal_projector_charge_probe.py
```

Summary output:

```text
Q Hermitian residual: 0.000e+00
Q^2-I residual:       0.000e+00
sector dimensions:    +8 / -8
[P_+/-, H_retained] residual: 0.000e+00  PASS
P_- U_retained P_+ leakage:   0.000e+00  PASS
sector-mixing perturbation residual: 1.000e-01  control should fail if allowed
epsilon spectrum in P_+ sector: [-1.0, +1.0]
epsilon spectrum in P_- sector: [-1.0, +1.0]
scalar pinning status: FAIL
inserted projector-source finite-difference residual: 0.000e+00
positive Born-source finite-difference residual:       0.000e+00
same-sector force prefactor:     +1
opposite-sector force prefactor: -1
action-reaction prefactor residual when source=response sign: 0.000e+00
pure + active charge:       +1.700000
equal +/- active charge:    -3.803094e-17
equal +/- inertial mass:    1.700000
q_bare pure +:              +21.362830
q_bare equal +/-:           -4.779109e-16
Born I3 residual:           +6.939e-17
unitary norm drift:         1.110e-16
weighted superposition <Q>:         +0.600000
same state under rotated Q=X:       +0.000000
equal +/- state as X-branch <X>:    +1.000000
FINAL_TAG: NONLOCAL_PROJECTOR_FORMAL_CONTROL_ONLY
```

## Gate Table

| gate | result | interpretation |
|---|---:|---|
| Hermitian involution | pass | `Q_chi = P_+ - P_-` is algebraically valid |
| nonempty sectors | pass | both sectors have equal finite dimension in the probe |
| conservation | pass on imposed surface | `H_retained = H_local tensor I_sector` commutes with both projectors |
| leakage | pass on imposed surface | exact unitary evolution has no `P_+` to `P_-` block |
| sector-mixing control | fail if allowed | adding `I tensor X` breaks the superselection surface |
| scalar-source pinning | fail | each `Q_chi` branch still contains both local parity signs |
| retained source derivation | fail | the retained scalar/Born source is not changed by naming `Q_chi` |
| inserted projector source | formal pass | a source action with `Q_chi` inserted varies to `psi^dagger Q_chi psi` |
| source/response locking | conditional pass | works only when the same sector sign is inserted on source and response |
| positive inertial mass | pass | inertial density remains `M_phys |psi|^2 >= 0` |
| null cancellation | pass | equal same-point `+/-` sector amplitudes cancel active charge |
| Born control | pass | the branch-preserving surface leaves the three-slit identity unchanged |
| norm control | pass | exact unitary evolution preserves norm |
| source-unit control | conditional pass | `q_bare = 4 pi chi_g M_phys` consumes an already supplied sign |
| mixed superpositions | obstruction | expectation-valued charge appears unless sectors are superselected |
| basis dependence | obstruction | rotating the sector basis changes the sign assignment without a native constraint |

## What This Evades

The local selector obstruction was:

```text
conserved local taste labels exist, but are scalar-source neutral
epsilon pins scalar sign, but is not conserved by kinetic hopping
```

The nonlocal projector construction evades the first half formally. A global
`Q_chi` can be made exactly conserved if the retained Hamiltonian is block
diagonal in the global sector:

```text
[P_+, H_retained] = [P_-, H_retained] = 0.
```

So Candidate C is not blocked by the local Pauli-string scan merely as an
operator-algebra construction.

## What It Does Not Evade

The probe does not derive a native signed active source. The projector source
works only if the source action is changed to include `Q_chi`:

```text
S_source,Q = M_phys psi^dagger Phi Q_chi psi.
```

Then:

```text
delta S_source,Q / delta Phi(x)
  = M_phys psi^dagger(x) Q_chi psi(x).
```

For a pure superselected sector this reduces to:

```text
rho_active(x) = chi_g M_phys |psi(x)|^2.
```

But that is an inserted projector-source action unless a separate boundary or
global-constraint theorem supplies the projectors and explains why the
gravitational source couples to `Q_chi` rather than to the retained Born or
parity scalar source.

The local scalar source is also not pinned inside the branches:

```text
epsilon spectrum in P_+ sector = {-1, +1}
epsilon spectrum in P_- sector = {-1, +1}.
```

Thus the construction does not repair the retained parity-scalar source
primitive. It only bypasses that primitive by proposing a new source action.

## Basis And Mixed-State Obstruction

Without a native boundary/global definition, `P_+` and `P_-` are basis labels.
The probe shows the ambiguity directly:

```text
same state under Q=Z_sector: +1
same state under rotated Q=X_sector: 0
equal Z-sector superposition under X_sector: +1
```

Mixed-sector states also have expectation-valued active charge:

```text
<Q_chi> = +0.6
```

for a weighted superposition. That is not a sharp `chi_g = +/-1` label unless
the theory supplies a superselection rule or a sector-preparation rule that
forbids coherent `P_+`/`P_-` mixtures on the retained surface.

## Verdict

The nonlocal projector-difference charge is a coherent formal control:

```text
FINAL_TAG: NONLOCAL_PROJECTOR_FORMAL_CONTROL_ONLY
```

It can avoid the local neutral-label obstruction only in the weak sense that an
externally supplied global sector label may commute with a block-diagonal
Hamiltonian and can be used in an inserted source/response-locked consequence
harness.

It does not yet promote `chi_g` to a native signed gravitational sector because
three proof obligations remain unmet:

1. `P_+` and `P_-` must be fixed by a basis-independent boundary or global
   constraint.
2. The retained or replacement source action must variationally expose
   `M_phys psi^dagger Q_chi psi` without hand insertion.
3. Mixed `P_+`/`P_-` superpositions must be forbidden, decohered, or classified
   as non-sector states on the theorem surface.

Until those obligations are met, Candidate C remains a no-claim algebraic
control rather than a derived `chi_g` selector.
