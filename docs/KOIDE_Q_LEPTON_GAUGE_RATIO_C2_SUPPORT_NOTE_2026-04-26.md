# Koide Q Lepton Gauge-Ratio c^2 Support Note

**Date:** 2026-04-26
**Status:** exact conditional support / target theorem for charged-lepton
Koide; **not retained native Koide closure**
**Primary runner:**
`scripts/frontier_koide_q_lepton_gauge_ratio_c2_support.py`

---

## 1. Purpose

The reviewed `sunday-koide` branch contained useful science, but it did not
close charged-lepton Koide. This note lands the useful part only.

The useful part is a sharp target statement:

```text
L_L : (2,1)_{-1}
    -> N_pair^ell  = dim_SU2(L_L) = 2
    -> N_color^ell = dim_SU3(L_L) = 1
    -> N_pair^ell / N_color^ell = 2.
```

If a future retained Brannen-W2 analog proves that the Brannen carrier
amplitude ratio is this lepton gauge-representation ratio,

```text
c_Brannen^2 = N_pair^ell / N_color^ell,
```

then the already-landed Brannen SO(2) support algebra gives

```text
Q = (c^2 + 2) / 6 = (2 + 2) / 6 = 2/3.
```

That is support and target-setting, not closure. The missing theorem is the
physical identification of `c^2` with the lepton-side gauge-representation
ratio.

---

## 2. Inputs and authority level

| Input | Status on main | Role here |
|---|---|---|
| `Q_L : (2,3)_{+1/3}` CKM source theorem | retained | Template: `A^2 = N_pair/N_color = 2/3` is closed for the CKM surface by a retained matter-source readout. |
| `L_L : (2,1)_{-1}` | retained corollary | Exact lepton-side representation readout: `N_pair^ell=2`, `N_color^ell=1`. |
| `Q=(c^2+2)/6` on the Brannen carrier | support theorem only | Exact algebra once the Brannen carrier and `c^2` are granted. |
| `c_Brannen^2 = N_pair^ell/N_color^ell` | open | The missing Brannen-W2 analog; not retained on main. |

The CKM theorem is a useful analogy because it derives `A^2=2/3` below W2
from the retained quark doublet source. The analogy does not itself prove the
Brannen observable map.

---

## 3. Exact lepton source readout

The retained left-handed charge-matching note gives

```text
L_L : (2,1)_{-1}.
```

Reading the gauge slots directly gives

```text
N_pair^ell  := dim_SU2(L_L) = 2,
N_color^ell := dim_SU3(L_L) = 1,
N_pair^ell / N_color^ell = 2.
```

This part is retained-source bookkeeping. It does not require charged-lepton
mass data.

---

## 4. Conditional Koide implication

The Brannen SO(2) support theorem proves, on the Brannen square-root mass
carrier,

```text
Q = (c^2 + 2) / 6.
```

Therefore the lepton gauge-ratio target would imply

```text
c^2 = 2  ->  Q = 2/3.
```

Conversely,

```text
Q = 2/3  ->  c^2 = 2.
```

So the residual can be stated exactly: prove a retained physical theorem
identifying the Brannen carrier value `c^2` with the lepton representation
ratio `2`.

---

## 5. Why this is not closure

The CKM side has two pieces:

```text
Q_L : (2,3)     retained source readout
A^2 = N_pair/N_color     retained CKM structural identity
```

The lepton side currently has only the first analogous piece:

```text
L_L : (2,1)     retained source readout
c^2 = N_pair^ell/N_color^ell     not retained
```

The missing second piece is load-bearing. Without it, the branch verifies the
consequences of assuming `c^2=2`; it does not derive that the physical
charged-lepton carrier has `c^2=2`.

---

## 6. Empirical signature

Using observed charged-lepton masses,

```text
Q_PDG = (m_e + m_mu + m_tau) / (sqrt(m_e)+sqrt(m_mu)+sqrt(m_tau))^2
      = 0.666660511...

c_PDG^2 = 6 Q_PDG - 2
        = 1.999963...
```

This is consistent with the target value `c^2=2`. It is not a proof of the
Brannen-W2 analog, because the mass data already encode the observed Koide
near-equality.

---

## 7. Closeout flags

```text
SUPPORT_NOT_CLOSURE=TRUE
LEPTON_SOURCE_READOUT_RETAINED=TRUE
LEPTON_GAUGE_REP_RATIO_EQ_2_FROM_L_L=TRUE
BRANNEN_C2_EQ_LEPTON_GAUGE_RATIO_CONDITIONAL_TARGET=TRUE
BRANNEN_W2_ANALOG_RETAINED=FALSE
KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE
DELTA_2_OVER_9_RAD_RETAINED_CLOSURE=FALSE
PDG_C2_APPROX_2_SIGNATURE_ONLY=TRUE
```

---

## 8. Validation

```bash
python3 scripts/frontier_koide_q_lepton_gauge_ratio_c2_support.py
```

The runner audits the retained/support authority boundary from disk, computes
the exact lepton gauge-ratio readout, verifies the conditional algebra
`c^2=2 <=> Q=2/3`, and checks that the closeout flags do not promote the open
Brannen-W2 analog.
