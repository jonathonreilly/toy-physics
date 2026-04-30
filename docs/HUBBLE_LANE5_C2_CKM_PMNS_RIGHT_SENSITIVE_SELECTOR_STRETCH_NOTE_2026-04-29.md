# Hubble Lane 5 C2 CKM/PMNS Right-Sensitive Selector Stretch

**Date:** 2026-04-29
**Status:** no-go / conditional-support boundary for the current `(C2)`
selector route; no `eta`, `Omega_Lambda`, or `H_0` numerical claim.
**Loop:** `.claude/science/physics-loops/impact-campaign-20260429/`
**Runner:** `scripts/frontier_hubble_lane5_c2_ckm_pmns_right_sensitive_selector_stretch.py`

```yaml
actual_current_surface_status: no-go
conditional_surface_status: conditional-support
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "CKM CP orientation gives only a conditional PMNS A13 sign selector unless a typed CKM-to-PMNS right-sensitive coupling law is supplied"
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 1. Question

Lane 5 `(C2)` needs the eta-retirement gate:

```text
right-sensitive 2-real Z_3 doublet-block point-selection law
on dW_e^H = Schur_{E_e}(D_-)
```

The 2026-04-26 eta audit names the PMNS residual as a right-sensitive
selector and lists CKM atlas structure as a possible unexplored external
coupling source. This block tests that hard residual:

```text
Can CKM CP orientation select the PMNS A13 sheet?
```

## 2. Stretch Candidate

The CKM CP-phase identity gives a positive quark-sector orientation:

```text
rho_CKM = 1/6
eta_CKM = sqrt(5)/6
tan(delta_CKM) = sqrt(5)
```

The PMNS eta-retirement residual has been reduced to the one-bit selector:

```text
sign(A13_PMNS)
```

The tempting stretch law is:

```text
sign(A13_PMNS) = sign(eta_CKM)
```

This would select the constructive `A13 > 0` sheet.

## 3. Boundary Theorem

**Theorem.** On the current repo surface, CKM CP orientation does not
unconditionally select the PMNS `A13` sheet.

The candidate law is algebraically coherent, but it is conditional on a new
typed cross-sector coupling from the CKM CP orientation to the PMNS
`dW_e^H` doublet block.

## 4. Proof

The current PMNS even data are CP-sheet blind: the two PMNS witnesses related
by `delta -> -delta` have the same even response data but opposite `A13` sign.
The current CKM CP data are also unchanged between those two PMNS witnesses,
because no current theorem maps the quark-sector CKM orientation into the
charged-sector PMNS `dW_e^H` right-sensitive frame.

Thus there are two same-current-data witnesses:

```text
World +: CKM orientation positive, PMNS even data fixed, A13 > 0
World -: CKM orientation positive, PMNS even data fixed, A13 < 0
```

The proposed law `sign(A13_PMNS) = sign(eta_CKM)` chooses World +, but the
law itself is not present on the current authority surface. It would be a new
typed CKM-to-PMNS coupling premise, not a consequence of the existing CKM
phase identity plus the existing PMNS selector reductions.

Therefore the route does not close `(C2)` on the current surface.

## 5. Runner Witness

The runner checks:

- Lane 5 names the right-sensitive `Z_3` doublet-block selector as the
  eta-retirement gate;
- the PMNS minimal `A13` note reduces the residual to a one-bit sign;
- current PMNS selector banks are CP-sheet blind;
- the CKM CP identity supplies the positive `eta_CKM` orientation;
- the candidate cross-sector sign law would work if assumed;
- the typed cross-sector coupling is not present, so actual status remains
  no-go.

Checks:

```bash
set -o pipefail; python3 scripts/frontier_hubble_lane5_c2_ckm_pmns_right_sensitive_selector_stretch.py | tee outputs/frontier_hubble_lane5_c2_ckm_pmns_right_sensitive_selector_stretch_2026-04-29.txt
python3 -m py_compile scripts/frontier_hubble_lane5_c2_ckm_pmns_right_sensitive_selector_stretch.py
```

Expected runner result:

```text
SUMMARY: PASS=22 FAIL=0
```

## 6. What This Closes

This closes the narrow stretch:

```text
current CKM CP orientation
  => PMNS A13 sign selector
  => eta-retirement C2 closure
```

The implication fails without a typed CKM-to-PMNS right-sensitive coupling law.

## 7. What Remains Open

The exact missing object is now sharper:

- a canonical right-frame law for the PMNS `dW_e^H` block; or
- an equivalent right-sensitive observable principle; or
- a typed cross-sector coupling theorem that maps CKM CP orientation to the
  PMNS `A13` sign.

No numerical `H_0`, `Omega_Lambda`, or baryon-asymmetry value is derived here.
