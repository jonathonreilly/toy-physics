# Koide Higgs-Dressed Resolvent Root Theorem

**Date:** 2026-04-20
**Lane:** charged-lepton Koide, constructive transport avenue
**Status:** exact scalar reduction of the proposed_retained Higgs-dressed intermediate-propagator route, **conditional on the imported upstream H3/readout package**, including the observational PMNS chamber pins `(M_STAR, DELTA_STAR, Q_PLUS_STAR)` that fix the missing-axis affine Hermitian `H_*` and the chart/readout constants used by `H3`. This does **not** finish a proposed_retained Koide derivation, but it turns the old broad transport ambiguity into one scalar root law on the most natural missing-axis lift, contingent on that upstream package.
**Runner:** `scripts/frontier_koide_higgs_dressed_resolvent_root_theorem.py`

## Observational pins (audit-explicit)

The theorem below is conditional on three observational inputs imported via
`scripts/frontier_higgs_dressed_propagator_v1.py`:

| Constant | Value | Source | Status |
|---|---|---|---|
| `M_STAR` | `0.657061342210` | G1 observational chamber pin (PMNS-pinned to NuFit 5.3 normal-ordering 1-sigma band; not framework-derived) | Observational |
| `DELTA_STAR` | `0.933806343759` | Same G1 chamber pin | Observational |
| `Q_PLUS_STAR` | `0.715042329587` | Same G1 chamber pin | Observational |

These are the same pins flagged in
[`KOIDE_CLOSURE_ATLAS_ISSUES_FLAGGED.md`](KOIDE_CLOSURE_ATLAS_ISSUES_FLAGGED.md)
(Issue 4) and labeled as `# G1 observational chamber pin (PMNS-pinned; not
framework-derived)` directly in the runner module. They appear here only via
`H_* = H3(M_STAR, DELTA_STAR, Q_PLUS_STAR)` on the missing-axis lift; no other
import from the chamber pin enters the theorem statement.

The remaining numerical inputs (`E1 = sqrt(8/3)`, `E2 = sqrt(8)/3`, `gamma = 1/2`,
the cyclic generators `T_M, T_Delta, T_Q`, and the affine Hermitian `H_base`)
are imported from the same upstream `H3`/readout module. They are not
observational PMNS pins, but this note does not re-derive them; the audit
dependency remains on a retained authority or source packet for the upstream
H3/readout package.

A candidate retained-derivation surface for the three pins exists as an
`audited_conditional` support route in
[`PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md`](PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md),
which numerically recovers `(m, delta, q_+) ~= (0.667, 0.933, 0.715)` from the
proposed three-equation system `Tr(H) = Q_Koide`, `delta * q_+ = Q_Koide`,
`det(H) = E2`. That note's last two equations are explicitly **proposed**, not
retained, so it does not yet discharge the observational dependency in this
theorem. Promotion of that support route would lift this theorem from
"conditional on observational pins" to "conditional on retained selector laws".

## Question

The existing Higgs-dressed intermediate-propagator avenue already showed one
numerically strong near-hit:

- missing-axis lift of the retained `H(m, delta, q_+)` operator,
- resolvent weight `(lambda I - W_4)^(-1)`,
- `Q ~ 2/3`,
- direction cosine to PDG `sqrt(m)` near `0.996`.

But the old avenue note was still too broad. It mixed:

- the lift choice,
- the `O_0` scalar weight,
- the resolvent scalar `lambda`,
- and several different functional classes.

What remains after stripping that down to the sharpest retained candidate?

## Bottom line

One scalar.

Fix the most natural missing-axis lift

```text
W_4(h_0) = diag(h_0, H_*)
```

on `(O_0, T_2[011], T_2[101], T_2[110])`, where `H_*` is the retained
`3 x 3` G1-pinned affine Hermitian on the missing-axis ordering. Then the
resolvent family

```text
R_lambda(h_0) = (lambda I_4 - W_4(h_0))^(-1)
```

induces the species block

```text
Sigma_lambda(h_0)
  = P_{T_1} Gamma_1 R_lambda(h_0) Gamma_1 P_{T_1}.
```

On the baseline `h_0 = 0`, the Koide condition on the absolute eigenvalues of
`Sigma_lambda(0)` has exactly eight isolated roots on the tested real line.
Among them there is exactly one small positive root:

```text
lambda_* = 0.015808703285395...
```

At that root:

```text
Q = 2/3
cos(dir(lambda_*), dir_PDG) = 0.996266551503...
```

So the retained Higgs-dressed transport avenue is no longer a loose search over
many functional classes. Once the baseline lift is fixed, it reduces to one
scalar `lambda` law.

## 1. Setup

The starting point is the existing avenue-G construction in
`frontier_higgs_dressed_propagator_v1.py`.

### 1.1 Missing-axis lift

Use the missing-axis ordering of the three `T_2` states:

```text
(011, 101, 110).
```

Then the retained `3 x 3` affine Hermitian `H_*` embeds directly on the `T_2`
block, while `O_0` carries a separate scalar weight `h_0`.

At `h_0 = 0` the four poles of the resolvent are exactly:

```text
lambda in {
  -1.309094..., -0.320434..., 0, 2.286589...
}.
```

These are one `O_0` pole plus the three lifted `H_*` eigenvalues.

### 1.2 Chamber-slack comparison scalar

The most natural old scalar candidate in the avenue was the retained chamber
slack

```text
lambda_slack = q_+* + delta_* - sqrt(8/3)
             = 0.015855511490548...
```

This is branch-internal and small positive, so it is the obvious comparison
point for any transport-root law.

## 2. The theorem

> **Theorem.** On the missing-axis Higgs-dressed resolvent family:
>
> 1. for `h_0 = 0`, the scalar equation
>    ```text
>    Q(abs eig Sigma_lambda(0)) = 2/3
>    ```
>    has exactly eight isolated real roots on the tested window `[-5, 5]`;
> 2. there is exactly one small positive root below `0.1`,
>    ```text
>    lambda_* = 0.015808703285395...;
>    ```
> 3. at `lambda_*`, the induced spectrum lands exactly on Koide and matches the
>    PDG charged-lepton direction with cosine `> 0.996`;
> 4. `lambda_*` is close to but not equal to the old chamber slack:
>    ```text
>    lambda_* - lambda_slack = -4.6808205... x 10^(-5);
>    ```
> 5. if one insists on fixing `lambda = lambda_slack` instead, exact Koide is
>    restored by a tiny positive `O_0` correction
>    ```text
>    h_0,small = 4.4898983... x 10^(-5).
>    ```

## 3. What this means

This is not yet a retained derivation of charged-lepton Koide. The open object
is still real. But it is now much smaller and more concrete than before.

The transport avenue no longer reads:

```text
find some H-lift / propagator dressing / chamber functional that works.
```

It now reads:

```text
derive one scalar lambda-law on the missing-axis resolvent family,
or equivalently the near-surface two-scalar relation on (lambda, h_0).
```

That is a real reduction.

## 4. Honest scope boundary

This theorem does **not** claim any of the following:

- that the chamber pins `(M_STAR, DELTA_STAR, Q_PLUS_STAR)` are derived from
  framework axioms; they are observational PMNS pins on the canonical surface
  (see "Observational pins" above);
- that the upstream H3/readout constants (`E1`, `E2`, `gamma`, `T_M`,
  `T_Delta`, `T_Q`, `H_base`) are re-derived inside this note;
- that the missing-axis lift is already the unique retained lift;
- that `lambda_*` is already derivable from Cl(3)/Z^3 alone;
- that `lambda_slack` itself is the answer;
- that the Koide lane is now retained-closed.

What it does claim is sharper and correct, **conditional on that upstream
package**:

- the strongest surviving transport route, once the three observational pins
  fix `H_*`, has been reduced to isolated scalar roots;
- the best-supported one is a unique small positive root near chamber slack;
- the old avenue-G ambiguity is now one-scalar, not broad.

## 5. Consequence for the frontier

This creates a new explicit candidate closure object for the Koide `Q = 2/3`
import, **stacked behind the upstream H3/readout package**:

```text
(a) provide retained authority or source-packet derivation for the upstream
    H3/readout package, including the observational-pin discharge if desired,
    then
(b) derive lambda_* on the missing-axis Higgs-dressed resolvent lane.
```

If both retained theorems land, this avenue closes without going back through
the older broad H-lift search.

So even though the full derivation is still open, the constructive frontier is
cleaner than it was:

- not a generic H-lift ambiguity,
- not a generic intermediate-weight ambiguity,
- one scalar resolvent root law, conditional on the upstream H3/readout
  package.

## 6. Cited authorities (one hop)

The theorem statement at section 2 imports the following from these on-repo
surfaces. Each is listed with its ledger-side authority status to keep the
audit dependency transparent.

- [KOIDE_CLOSURE_ATLAS_ISSUES_FLAGGED.md](KOIDE_CLOSURE_ATLAS_ISSUES_FLAGGED.md)
  -- Issue 4 explicitly flags `(M_STAR, DELTA_STAR, Q_PLUS_STAR)` as
  observational PMNS pins, not framework-derived constants.
- [PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md](PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md)
  -- candidate retained-derivation surface for `(m_*, delta_*, q_+*)` via
  the proposed three-equation system; **`audited_conditional` support, not
  retained**. Promotion would discharge the observational dependency.
- `KOIDE_QUBIT_LATTICE_DIM_ALGEBRAIC_CLOSURE_NOTE_2026-04-20.md` (plain-text
  reference to avoid citation back-edge; transitive cycle exists through
  `koide_berry_phase_theorem_note_2026-04-19`) -- companion note that
  explicitly lists these chamber pins as separately-pinned observational
  inputs (section 5.3).
- [SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md](SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md)
  -- the open-imports register listing this theorem as one of four candidate
  routes to the Koide cone, all currently conditional on the chamber pins
  (Priority 1 entry 3).
- [KOIDE_CL3_SELECTOR_GAP_NOTE_2026-04-19.md](KOIDE_CL3_SELECTOR_GAP_NOTE_2026-04-19.md)
  -- prior gap statement classifying the same three pins as G1 observational
  chamber pins not derived from `Cl(3)`.

The chart/readout constants `E1 = sqrt(8/3)`, `E2 = sqrt(8)/3`, `gamma = 1/2`,
and the cyclic generators `T_M, T_Delta, T_Q, H_base` enter via
`H3(m, delta, q_+)` from `scripts/frontier_higgs_dressed_propagator_v1.py`.
They are not observational PMNS pins, but they remain imported upstream
constants rather than derivations supplied by this note.
