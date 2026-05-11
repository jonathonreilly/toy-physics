# Quark Route-2 Source-Domain Bridge No-Go

**Date:** 2026-04-28 (audit-status note added 2026-05-10)

**Status:** bounded current-bank typed-edge no-go on the configured Route-2
support / SU(3) connected-color bank, with the underlying typed-edge
inventory hard-coded by the runner rather than derived. This block-03
stretch attempt attacks the typed source-domain residual exposed by block
02. It does not derive the up-type scalar law
`beta_E / alpha_E = 21/4`, and it does not claim retained `m_u` or `m_c`.

**Primary runner:**
`scripts/frontier_quark_route2_source_domain_bridge_no_go.py`

## Audit-status note (2026-05-10)

The 2026-05-10 fresh audit verdict (`audited_conditional`,
`chain_closes=false`) supersedes the prior 2026-05-01 `audited_clean`
verdict and flagged a missing-dependency edge: the runner hard-codes the
typed-edge inventory `CURRENT_TYPED_EDGES` rather than deriving it from
the cited Route-2 / `R_conn` upstream authorities, and the audit packet
does not provide one-hop authorities for the named Route-2/readout/`R_conn`
inputs in a form the restricted packet can verify.

> "the source note relies on named Route-2/R_conn authorities and a
> complete current-bank typed-edge inventory, but the audit ledger
> supplies no one-hop authorities and the runner hard-codes
> CURRENT_TYPED_EDGES rather than deriving the inventory."

Admitted-context inputs (named upstream authorities, cited but not closed
inside this packet):

- `quark_route2_exact_readout_map_note_2026-04-19` (`audited_clean`) —
  exact bilinear carrier and restricted bright readout class
- `quark_route2_exact_time_coupling_note_2026-04-19` (`audited_clean`) —
  exact slice backbone `Lambda_R`
- `rconn_derived_note` (latest verdict `audited_conditional`,
  2026-05-10) — SU(3) connected color projection
  `R_conn = (N_c^2 - 1)/N_c^2`

Admitted-context inputs (configured runner constants, not derived):

- the typed-edge inventory `CURRENT_TYPED_EDGES` enumerated in
  `scripts/frontier_quark_route2_source_domain_bridge_no_go.py`
- the conditional T-side candidates
  `beta_T/alpha_T = -1`, `alpha_T/alpha_E = -2`
- exact rational arithmetic over the configured bank

Blocked-on: this row stays `audited_conditional` until either a retained
inventory-derivation authority is registered that produces
`CURRENT_TYPED_EDGES` from the named Route-2/`R_conn` authorities (so the
finite typed graph is not hard-coded), or the named one-hop authorities
are bundled into the audit packet at a grade that lets the restricted
packet verify the inventory. The bounded computational diagnostic — over
the configured typed-edge bank, no path exists from `R_conn = 8/9` to
`gamma_T(center)/gamma_E(center) = -8/9`, and adding exactly that bridge
forces `beta_E/alpha_E = 21/4` algebraically — is unaffected by this
status note.

## 1. Question

Block 02 proved the exact conditional statement:

```text
gamma_T(center) / gamma_E(center) = -R_conn = -8/9
    => gamma_E(center) / gamma_E(shell) = 15/8
    => beta_E / alpha_E = 21/4.
```

The remaining hard residual is not the arithmetic. It is the typed bridge
from the retained SU(3) connected color projection to the Route-2 endpoint
readout:

```text
R_conn = (N_c^2 - 1) / N_c^2
    ?=> gamma_T(center) / gamma_E(center) = -R_conn.
```

This note asks whether the current exact/retained support bank already
contains that source-domain bridge.

## 2. Minimal Premise Set

Allowed premises:

1. exact Route-2 support carrier
   `K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`;
2. exact restricted endpoint columns and endpoint algebra;
3. conditional T-side candidates
   `beta_T/alpha_T = -1` and `alpha_T/alpha_E = -2`;
4. retained SU(3) color-projection value
   `R_conn = (N_c^2 - 1)/N_c^2 = 8/9` at `N_c = 3`;
5. exact rational arithmetic and a finite typed-edge inventory over the
   current support bank.

Forbidden proof inputs:

1. observed quark masses;
2. fitted Yukawa entries;
3. CKM/`J` target-error minimization;
4. nearest-rational selection from the live endpoint data;
5. an untyped identification of a color projection with a Route-2 endpoint
   ratio.

## 3. Conditional Algebra Remains Exact

With the T-side candidates granted,

```text
q_T = gamma_T(center)/gamma_T(shell) = 5/6,
s_TE = gamma_T(shell)/gamma_E(shell) = -2.
```

For any proposed center ratio `c_TE`,

```text
q_E = gamma_E(center)/gamma_E(shell) = s_TE q_T / c_TE.
```

If an additional theorem supplies

```text
c_TE = gamma_T(center)/gamma_E(center) = -R_conn = -8/9,
```

then

```text
q_E = (-2)(5/6)/(-8/9) = 15/8,
rho_E = beta_E/alpha_E = 6(q_E - 1) = 21/4.
```

The arithmetic target is therefore sharp. The missing step is the typed
source-domain bridge theorem, not another endpoint-ratio manipulation.

## 4. Typed Source-Domain Inventory

The current bank supplies these typed edges:

| Source | Target | Authority | Role |
|---|---|---|---|
| `delta_A1`, `u_E`, `u_T` | `K_R` | `S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md` | support-side Route-2 carrier |
| `K_R` | restricted readout family | `QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md` | endpoint support |
| restricted readout family | endpoint algebra | `QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md` | algebra |
| T-side candidates | `q_T = 5/6`, `s_TE = -2` | block-01/block-02 stretch premises | conditional |
| SU(3) color trace | `R_conn = 8/9` | `RCONN_DERIVED_NOTE.md` | color projection |
| `c_TE = -8/9` | `q_E = 15/8` | endpoint algebra | algebra |
| `q_E = 15/8` | `rho_E = 21/4` | endpoint algebra | algebra |

There is no current typed edge

```text
R_conn = 8/9 -> c_TE = gamma_T(center)/gamma_E(center) = -8/9.
```

The Route-2 carrier lives on support-side `A1/E/T` endpoint coordinates. The
R_conn surface lives on the SU(3) color-trace singlet/adjoint decomposition.
The present repo has both objects, but no theorem that identifies the color
projection with the E/T center endpoint ratio.

## 5. Stretch Attempt And Fan-Out

The attempted bridge was checked across five orthogonal frames:

1. **Support-endpoint frame.** The exact restricted Route-2 carrier leaves
   `rho_E` free. `rho_E = 0` and `rho_E = 21/4` agree on E-shell and the
   granted T-side endpoints; they differ only at E-center.
2. **Color-trace frame.** `R_conn` is a positive SU(3) connected color
   fraction. The target bridge needs the signed endpoint ratio `-R_conn`.
   The sign and endpoint orientation are not supplied by the color projection
   itself.
3. **Representation-domain frame.** Route-2 uses support-side `A1/E/T`
   endpoint data. R_conn uses SU(3) singlet/adjoint color channels. These are
   different typed domains unless a cross-domain source theorem is added.
4. **Endpoint-functor frame.** The finite typed graph has no path from
   `R_conn` to `rho_E = 21/4`. Adding exactly the missing bridge creates the
   path immediately.
5. **Low-complexity scalar frame.** Many simple expressions in `R_conn`
   exist (`R_conn`, `-R_conn`, `1-R_conn`, `1/R_conn`, ...). Selecting
   `-R_conn` as the endpoint ratio is an extra source/readout rule, not a
   consequence of the color scalar alone.

All frames agree: the present support bank does not type the bridge.

## 6. Theorem

**Theorem (Route-2 source-domain bridge no-go).** In the current exact
Route-2 support bank plus the retained SU(3) color-projection bank, after
granting the conditional T-side candidates

```text
beta_T/alpha_T = -1,
alpha_T/alpha_E = -2,
```

there is no typed current-bank derivation of

```text
gamma_T(center)/gamma_E(center) = -R_conn.
```

If that source-domain bridge is added as a new premise, the endpoint algebra
forces

```text
beta_E/alpha_E = 21/4
```

exactly. Without it, `R_conn = 8/9` remains a conditional bridge target and
import boundary, not a retained derivation of the Route-2 up-type scalar law.

## 7. What This Retires

This retires the stronger overread left open after block 02:

```text
R_conn is retained, and Route-2 needs -8/9,
therefore the up-type E-channel readout is derived.
```

The current stack supports only:

```text
typed source-domain bridge theorem
    => beta_E/alpha_E = 21/4.
```

It does not supply the bridge theorem itself.

## 8. What Remains Open

The next sharp 3B target is unchanged but cleaner:

```text
derive a typed source-domain bridge theorem
R_conn -> gamma_T(center)/gamma_E(center) = -R_conn
```

or find an alternate Route-2/readout primitive outside the current endpoint
bank. Claim status remains open. There is still no retained derivation of
`m_u`, `m_c`, or the five non-top quark masses.

## 9. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_route2_source_domain_bridge_no_go.py
```

Expected result:

```text
TOTAL: PASS=33, FAIL=0
VERDICT: current Route-2 + SU(3) support has no typed R_conn
source-domain bridge. Adding that bridge would force rho_E=21/4,
but without it the up-type scalar law remains open.
```
