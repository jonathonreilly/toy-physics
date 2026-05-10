# Quark Route-2 R_conn Center-Ratio Bridge Obstruction

**Date:** 2026-04-28
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** (1) staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`); (2) g_bare = 1 derivation target (canonical parent: [`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md)).

**Status:** support / exact conditional bridge plus exact import-boundary obstruction for
Lane 3 target 3B. This note records a block-02 stretch attempt on the
Route-2 up-type amplitude scalar-law residual. It does not derive the
E-channel readout law `beta_E / alpha_E = 21/4`, and it does not claim
retained `m_u` or `m_c`.

**Primary runner:**
`scripts/frontier_quark_route2_rconn_center_ratio_bridge_obstruction.py`

## 1. Question

Block 01 reduced the Route-2 up-sector scalar-law residual to the E-center
ratio

```text
gamma_T(center) / gamma_E(center) = -8/9.
```

The strongest constructive-looking route is that `8/9` is already present in
the retained color-projection stack:

```text
R_conn = (N_c^2 - 1) / N_c^2 = 8/9  at  N_c = 3.
```

This note asks whether that retained color factor can supply the missing
Route-2 center readout ratio without importing observed quark masses, fitted
Yukawa values, CKM/J target minimization, or nearest-rational selection from
the live endpoint data.

## 2. Minimal Premise Set

Allowed premises:

1. the exact restricted Route-2 carrier columns;
2. the exact endpoint algebra
   `q_E = 1 + rho_E/6`, `q_T = 1 + rho_T/6`;
3. the conditional T-side candidates
   `rho_T = -1` and `alpha_T/alpha_E = -2`;
4. retained `N_c = 3` and retained color projection
   `R_conn = (N_c^2 - 1)/N_c^2 = 8/9`;
5. exact rational arithmetic.

Forbidden proof inputs:

1. observed quark masses;
2. fitted Yukawa entries;
3. CKM/J target minimization;
4. nearest-rational selection from the live endpoint data;
5. an untyped identification of a color projection with a Route-2 endpoint
   readout.

## 3. Conditional Bridge Algebra

With the T-side candidates granted, the exact endpoint algebra gives

```text
q_T = gamma_T(center)/gamma_T(shell) = 5/6,
s_TE = gamma_T(shell)/gamma_E(shell) = -2,
c_TE = gamma_T(center)/gamma_E(center).
```

Therefore

```text
q_E = gamma_E(center)/gamma_E(shell)
    = s_TE q_T / c_TE.
```

If the missing center ratio is identified with the negative retained color
projection,

```text
c_TE = -R_conn = -8/9,
```

then

```text
q_E = (-2)(5/6)/(-8/9) = 15/8,
rho_E = 6(q_E - 1) = 21/4.
```

So `-R_conn` is the sharpest currently visible conditional bridge to the
Route-2 E-channel law.

## 4. Why This Still Does Not Derive the Law

The exact restricted carrier/readout family after granting the T-side values
is

```text
P(rho_E) =
[[1, 0, rho_E, 0],
 [0, -2, 0, 2]].
```

The exact E endpoint columns are

```text
E-shell  = (1, 0, 0,   0),
E-center = (1, 0, 1/6, 0).
```

The exact T endpoint columns are

```text
T-shell  = (0, 1, 0,   0),
T-center = (0, 1, 0, 1/6).
```

Changing `rho_E` leaves the E-shell and both granted T-side readouts fixed.
It changes only the E-center lift. Thus `rho_E = 0` and `rho_E = 21/4` are
both exact maps on the same restricted carrier unless an additional E-center
source/readout primitive is supplied.

The retained `R_conn` surface lives on the SU(3) color-projection/color-trace
channel. The current Route-2 carrier surface lives on seven-site support
coordinates `A1`, `E`, and `T`. No current retained note supplies a typed
source-domain identification

```text
gamma_T(center) / gamma_E(center) = -R_conn.
```

Granting that equality is exactly the missing bridge; it is not a derivation
from the current Route-2 carrier.

## 5. Live Bounded Comparator

The live endpoint data remain suggestive:

```text
gamma_T(center)/gamma_E(center) = -0.890683778231...
-R_conn                         = -0.888888888889...
```

and

```text
beta_E/alpha_E live = 5.257476782081...
21/4                = 5.25.
```

Those are bounded comparator facts. They motivate the source-domain target,
but they cannot be used as theorem inputs.

## 6. Theorem

**Theorem (R_conn center-ratio bridge obstruction).** In the exact restricted
Route-2 carrier/readout class, after granting

```text
beta_T/alpha_T = -1,
alpha_T/alpha_E = -2,
```

the retained SU(3) color value

```text
R_conn = (N_c^2 - 1)/N_c^2 = 8/9
```

conditionally implies the target E-channel readout entry if and only if the
additional source-domain bridge

```text
gamma_T(center)/gamma_E(center) = -R_conn
```

is supplied. The existing carrier columns and endpoint algebra do not supply
that bridge. Therefore the R_conn observation is an exact conditional bridge
target and an import boundary, not a retained derivation of the up-type
scalar law.

## 7. What This Retires

This retires the direct promotion:

```text
R_conn = 8/9 numerically matches the missing endpoint ratio
=> Route-2 derives beta_E/alpha_E = 21/4.
```

The match is exact only after an extra source-domain identification is added.

## 8. What Remains Open

The next sharp 3B theorem target is now:

```text
derive gamma_T(center)/gamma_E(center) = -R_conn
```

from a typed bridge between the retained SU(3) color-projection surface and
the Route-2 support endpoint readout. If that bridge lands, the E-channel
`21/4` law follows immediately. Without it, Route-2 remains bounded support,
not retained `m_u`/`m_c` closure.

## 9. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_route2_rconn_center_ratio_bridge_obstruction.py
```

Expected result:

```text
TOTAL: PASS=26, FAIL=0
VERDICT: -R_conn is a sharp conditional bridge to rho_E=21/4,
but the source-domain identification is still missing.
```


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on **both** open gates:

1. **Staggered-Dirac realization derivation target** — canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`); in-flight supporting work: `PHYSICAL_LATTICE_NECESSITY_NOTE.md`, `THREE_GENERATION_STRUCTURE_NOTE.md`, `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`, `scripts/frontier_generation_rooting_undefined.py`, `GENERATION_AXIOM_BOUNDARY_NOTE.md`.
2. **`g_bare = 1` derivation target** — canonical parent: [`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md) (`claim_type: positive_theorem`, `audit_status: audited_conditional`); in-flight supporting work: `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`, `G_BARE_RIGIDITY_THEOREM_NOTE.md`, `G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`, `G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`, `G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`, `G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md`, `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`.

The note produces (or directly supports) a quantitative gauge prediction (Wilson plaquette content, `α_s`, `v`, `sin²θ_W`, `m_t`, `m_H`, `g_1`, `g_2`, `β = 6`, CKM/quark/hadron mass hierarchy, action-unit metrology, etc.) by fixing `g_bare = 1` without independently deriving it — therefore both gates must close for the lane to upgrade.

Therefore `claim_type: bounded_theorem` until both gates close. When both gates close, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.
