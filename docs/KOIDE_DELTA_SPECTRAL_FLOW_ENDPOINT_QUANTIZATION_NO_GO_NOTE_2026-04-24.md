# Koide Delta Spectral-Flow Endpoint-Quantization No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative theorem. This rejects integer spectral-flow
endpoint quantization as a derivation of the physical selected-line Brannen
phase endpoint.
**Primary runner:** `scripts/frontier_koide_delta_spectral_flow_endpoint_quantization_no_go.py`

---

## 1. Question

The retained delta support stack has:

```text
eta_APS(Z_3; weights 1,2) = 2/9
```

and the selected-line Berry carrier has:

```text
delta = theta_end - theta0.
```

A possible physical bridge is:

```text
APS eta + spectral-flow endpoint quantization
-> theta_end - theta0 = eta_APS.
```

The executable answer is:

```text
No.
```

Spectral flow supplies integer crossing data. It does not select the
continuous open-path endpoint on the selected line.

---

## 2. Exact Support

The runner verifies:

```text
eta_APS = 2/9,
projective selected-line period = pi.
```

These are retained support facts.

---

## 3. Obstruction

Inside the first projective period, the selected-line endpoint is continuous.
The runner checks:

```text
delta = 0,
delta = 1/9,
delta = 2/9,
delta = 1/4.
```

All have the same first-period spectral-flow integer:

```text
SF = 0.
```

Thus the spectral-flow integer cannot distinguish the physical candidate
endpoint `2/9` from nearby endpoints.

---

## 4. APS Formula Still Needs The Endpoint Law

The exact residual remains:

```text
theta_end - theta0 - eta_APS.
```

Adding an integer spectral-flow period produces:

```text
delta_n = eta_APS + n pi.
```

But this expression already uses the fractional offset `eta_APS`. The integer
`n` shifts by periods; it does not derive the fractional selected-line
endpoint.

---

## 5. Falsifiers

This no-go would be falsified by a retained spectral-flow theorem proving
that the selected-line open-path endpoint is the APS fractional eta rather
than merely sharing an integer crossing sector.

It would also be falsified by a physical boundary condition that turns the
continuous selected-line endpoint into a discrete spectral-flow datum with
unique representative `2/9`.

No such theorem is present in the current retained package.

---

## 6. Executable Result

Run:

```bash
python3 scripts/frontier_koide_delta_spectral_flow_endpoint_quantization_no_go.py
```

Result:

```text
PASSED: 11/11
KOIDE_DELTA_SPECTRAL_FLOW_ENDPOINT_QUANTIZATION_NO_GO=TRUE
DELTA_SPECTRAL_FLOW_ENDPOINT_QUANTIZATION_CLOSES_DELTA=FALSE
RESIDUAL_SCALAR=theta_end-theta0-eta_APS
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
```

---

## 7. Boundary

This note does not demote APS or spectral flow as support. It rejects only the
claim that integer spectral-flow quantization by itself selects the physical
Brannen endpoint.

The delta residual remains:

```text
derive theta_end - theta0 = eta_APS.
```
