# PR230 Block68 Strict W/Z Or Neutral-Transfer Obstruction

**Status:** no-go / exact negative boundary for the current PR230 surface:
strict W/Z and neutral-transfer physical-response bypasses do not close without
an absolute normalization pin or a physical primitive neutral-transfer theorem

**Runner:** `scripts/frontier_yt_pr230_block68_strict_wz_neutral_transfer_obstruction.py`

**Certificate:**
`outputs/yt_pr230_block68_strict_wz_neutral_transfer_obstruction_2026-05-12.json`

```yaml
actual_current_surface_status: no-go / exact negative boundary for current PR230 Block68
conditional_surface_status: conditional-support if future work supplies accepted same-source EW/Higgs action, production W/Z/top rows, matched covariance, delta_perp, and one absolute pin among strict non-observed g2, explicit v, or canonical source-response normalization; or if future work supplies a same-surface primitive neutral-transfer operator/cone theorem plus source/canonical-Higgs coupling and pole/FVIR normalization authority
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

## Result

Block68 does not close PR230 on the current surface.

The strongest positive thing found is mathematical, not current-surface
physical closure: once the accepted W/Z action, production W/Z/top response
rows, additive-top subtraction, covariance, and `delta_perp` rows exist, one
absolute pin would remove the remaining W/Z scale kernel.  The runner verifies
that adding any one of strict non-observed `g2`, explicit `v`, or canonical
source-response normalization raises the top/W/Z mass-response Jacobian rank
from `5` to `6`.

The actual current surface has none of those pins and still lacks the W/Z
packet roots.  The neutral route also remains blocked: the current rows admit
an orthogonal-neutral counterfamily and the source-neutral off-diagonal
transfer coefficient `eta` is independent data.

## Assumptions Exercise

| Assumption | Why it is needed | If wrong |
|---|---|---|
| Accepted same-source EW/Higgs action | Gives physical meaning to W/Z response rows and the scalar source coordinate. | W/Z slopes are only schema/scout diagnostics; mass algebra cannot be used as physical response. |
| Sector overlap between top source and gauge-mass source | Lets the same `dv/ds` appear in top and W/Z slopes after additive-top subtraction. | The top/W ratio reads an arbitrary source-coordinate mismatch, not `y_t/g2`. |
| Additive-top subtraction row is measured in the same coordinate | Removes `O_top_additive` from `T_total = dE_top/ds`. | Setting `A_top = 0` by convention recreates a definition-as-derivation failure. |
| Top/WZ matched covariance or theorem | Needed for a strict readout and uncertainty on `g2 (T-A)/(sqrt(2) W)`. | Marginal rows can share labels while the joint law changes the response ratio and error. |
| Absolute `g2` or `v` normalization | Converts ratios into absolute `y_t`. | Top/W/Z mass-response rows determine only `y_t/g2`, `gY/g2`, and mass ratios. |
| `delta_perp` / orthogonal response control | Prevents unmeasured neutral directions from contaminating W/Z or source-Higgs response. | The readout can be rotated by an orthogonal scalar component without changing current rows. |
| Neutral-transfer primitive | Forces a unique full source-plus-neutral Perron direction. | Positivity or finite covariance rows preserve multiple completions; no rank-one source-Higgs bridge follows. |

## First-Principles Reduction

The W/Z route has only a few minimal physical drivers:

```text
m_t       = y_t v / sqrt(2)
M_W       = g2 v / 2
M_Z       = sqrt(g2^2 + gY^2) v / 2
T_total   = y_t (dv/ds) / sqrt(2) + A_top
W         = g2 (dv/ds) / 2
Z         = sqrt(g2^2 + gY^2) (dv/ds) / 2
```

With `A_top` measured and subtracted,

```text
y_t/g2 = (T_total - A_top) / (sqrt(2) W).
```

That is a ratio.  Absolute `y_t` still requires one of:

- strict non-observed `g2` in the same accepted EW normalization;
- explicit `v` authority with the dependency visible;
- canonical source-response normalization `a = dh/ds` from accepted `O_H`/LSZ
  or a physical neutral-transfer bridge.

The same-source rows that must be measured or derived are therefore:
`T_total`, strict `A_top`, production `W` or `Z`, matched covariance for
`T_total/A_top/W/Z` and the absolute pin, accepted action authority,
`delta_perp`, and a final readout certificate.

## Literature Search

These sources support route shape only.  None is used as PR230 proof authority.

| Surface | Stable source | Probe-D role |
|---|---|---|
| Gauge-invariant Higgs/W/Z spectroscopy | [Frohlich-Morchio-Strocchi IHES preprint](https://archives.ihes.fr/document/P_81_12.pdf), [Maas-Sondenheimer-Toerek arXiv:1709.07477](https://arxiv.org/abs/1709.07477) | Confirms the action-first composite-operator shape. It does not supply PR230 `O_H`, rows, or normalization. |
| Lattice transfer matrix / reflection positivity | [Luscher transfer matrix theorem](https://doi.org/10.1007/BF01614090) | Correct setting for future Euclidean pole rows; not a finite-row rank-one theorem. |
| Response / Feynman-Hellmann | [Feynman 1939, Caltech record](https://authors.library.caltech.edu/records/a5jtc-q3669/latest), [QFT/lattice FH usage](https://arxiv.org/abs/1612.06963) | Supports response-row methodology; does not identify the physical source coordinate. |
| Gauge coupling renormalization | [Schrodinger functional](https://arxiv.org/abs/hep-lat/9207009), [Wilson/gradient flow](https://arxiv.org/abs/1006.4518) | Gives possible non-observed `g2` certificate templates after an accepted EW action exists. |
| Ward identities | [Ward 1950 record](https://www.mindat.org/reference.php?id=7468273) | Context only. Ward identities are not load-bearing in this probe. |

## Math Search

| Math surface | Stable source | Probe-D verdict |
|---|---|---|
| Covariance and Schur complements | [Zhang, The Schur Complement and Its Applications](https://link.springer.com/book/10.1007/b105056) | Explains why matched covariance and Schur rows must be actual rows, not inferred labels. |
| Truncated moments / flat extension | [Curto-Fialkow truncated K-moment theorem](https://iro.uiowa.edu/esploro/outputs/journalArticle/Truncated-K-moment-problems-in-several-variables/9984240861702771) | Useful after full source-Higgs moment matrices exist; source-only finite rows do not force the missing entries. |
| Primitive cones / spectral rank one | [Rugh complex Perron-Frobenius theory](https://annals.math.princeton.edu/2010/171-3/p07) | Supplies the right theorem shape after a physical positivity-improving transfer kernel exists. |
| Response Jacobian identifiability | [observability-identifiability rank condition review](https://arxiv.org/abs/1812.04525) | The W/Z observable map has a rank-one normalization kernel until one absolute pin is added. |
| Dimensional / absolute normalization | [Buckingham pi theorem overview](https://www.britannica.com/science/pi-theorem) | Ratio data and dimensionless groups do not select an absolute coupling normalization by themselves. |

## Route Audit

| Route | Current result | Narrow obstruction |
|---|---|---|
| W/Z accepted-action root | `YT_PR230_WZ_ACCEPTED_ACTION_RESPONSE_ROOT_CHECKPOINT` remains exact negative boundary. | No accepted same-source EW/Higgs action, canonical-Higgs authority, sector-overlap, production W/Z mass-fit path, or response packet. |
| W/Z self-normalization | `YT_PR230_WZ_MASS_RESPONSE_SELF_NORMALIZATION_NO_GO` and the earlier response-only no-go pass. | A scale orbit changes `y_t`, `g2`, `gY`, and `v` while preserving top/W/Z masses and slopes. |
| W/Z absolute authority | `YT_PR230_WZ_ABSOLUTE_AUTHORITY_ROUTE_EXHAUSTION_AFTER_BLOCK41` passes. | Strict packet roots are absent: action, W/Z rows, top rows, covariance, strict `g2/v`, `delta_perp`, final readout. |
| Neutral rank-one bypass | `YT_PR230_NEUTRAL_RANK_ONE_BYPASS_POST_BLOCK37_AUDIT` passes. | An orthogonal neutral direction rotates the candidate Higgs readout while preserving current `C_ss/C_sx/C_xx` rows. |
| Top/WZ covariance | `YT_TOP_WZ_COVARIANCE_THEOREM_IMPORT_AUDIT` and factorization gate block imports. | Same-source labels do not imply joint covariance or factorization; matched rows or a theorem are required. |

## Proof Attempt

**Theorem 1: top/W/Z mass-response rows have an absolute-normalization kernel.**

Let the observable map be

```text
F(y_t,g2,gY,v,a,A_top)
  = (m_t, M_W, M_Z, T_total, W, Z, A_top),
```

with `a = dv/ds`.  Away from singular loci, the vector

```text
(-y_t, -g2, -gY, v, a, 0)
```

is in the Jacobian kernel.  The runner checks this numerically at a generic
point:

```text
base rank = 5
rank with strict g2 pin = 6
rank with explicit v pin = 6
rank with source-normalization a pin = 6
```

So W/Z rows can become identifiable only after a separate absolute pin exists.
The current surface has no such pin.

**Theorem 2: current neutral rows do not force a primitive rank-one bridge.**

The measured subblock fixes only `source_s` and taste-radial `x`.  The
completion

```text
H(theta) = cos(theta) x + sin(theta) n
```

with unmeasured orthogonal neutral `n` preserves current rows while changing
the candidate source-Higgs overlap.  The runner also checks a source-isolated
transfer with `eta = 0` is not primitive, while adding positive source-neutral
coupling `eta > 0` can make the matrix primitive.  Current PR230 does not
derive or measure `eta`.

## Exact New Row Or Theorem Required

For W/Z:

1. accepted same-source EW/Higgs action certificate;
2. production W/Z and same-source top response rows;
3. strict additive-top subtraction rows;
4. matched covariance for `T_total`, `A_top`, `W/Z`, and the absolute pin;
5. `delta_perp` / orthogonal-response correction authority;
6. one absolute normalization pin: strict non-observed `g2`, explicit `v`, or
   canonical source-response normalization.

For neutral transfer:

1. same-surface physical neutral transfer/off-diagonal generator fixing `eta`;
2. primitive-cone or irreducibility theorem on the full source-plus-neutral
   sector;
3. source/canonical-Higgs coupling theorem or strict `C_ss/C_sH/C_HH` pole
   rows;
4. pole residue, `K'(pole)`, threshold, contact, and FV/IR authority.

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.
It does not use `H_unit`, load-bearing Ward identities, `y_t_bare`, observed
targets, observed `g2/v`, `alpha_LM`, plaquette, `u0`, or unit settings for
`g2`, `v`, `kappa_s`, `c2`, or `Z_match`.  It does not assume top/WZ
covariance, promote W/Z smoke rows to production rows, treat positivity as a
primitive cone, or relabel `C_sx/C_xx` as `C_sH/C_HH`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block68_strict_wz_neutral_transfer_obstruction.py
python3 scripts/frontier_yt_pr230_block68_strict_wz_neutral_transfer_obstruction.py
# SUMMARY: PASS=18 FAIL=0
```
