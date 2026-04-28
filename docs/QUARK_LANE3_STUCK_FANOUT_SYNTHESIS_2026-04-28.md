# Quark Lane 3 Stuck Fan-Out Synthesis

**Date:** 2026-04-28

**Status:** exact current-bank synthesis / no-route-passes boundary for Lane 3.
This block-13 artifact is the required stuck fan-out after the deep 3B/3C
RPSR work. It does not claim retained `m_u`, `m_d`, `m_s`, `m_c`, or `m_b`,
and it does not claim that no future theorem can exist. It records that no
route currently passes without adding new theorem content.

**Primary runner:**
`scripts/frontier_quark_lane3_stuck_fanout_synthesis.py`

## 1. Question

After blocks 01 through 12, the loop has exact support and exact boundaries
for:

1. one-Higgs gauge selection;
2. CKM as mixing rather than mass singular values;
3. Route-2 endpoint/readout support;
4. down-type `5/6` scale selection;
5. `S_3` and oriented `C3[111]` generation Ward carriers;
6. `C3` circulant/A1/P1 readout support;
7. STRC/RPSR up-amplitude support;
8. RPSR single-scalar and RPSR+C3 joint readout rank boundaries.

This block asks:

```text
Does any current-bank route now reach retained non-top quark masses, or does
every orthogonal frame require new source/readout theorem content?
```

## 2. Fan-Out Frames

The synthesis checks six frames.

| Frame | Current-bank result | Reopen condition |
|---|---|---|
| Gauge/operator | one-Higgs selection gives the SM Dirac operator skeleton but leaves generation matrices free | species-differentiated Ward/source theorem |
| Ward-normalization | top Ward is top-channel scoped; species-uniform reuse fails | non-top Ward primitive or sector bridge |
| CKM/singular-value | CKM atlas supplies mixing, not quark Yukawa singular values | retained mass-basis bridge |
| Endpoint/source | Route-2 and `R_conn` support are exact, but the source-domain edge is missing | typed Route-2 source theorem |
| C3/RPSR readout | C3 represents the two-ratio surface and RPSR supplies one scalar, but no coefficient/readout law exists | C3 coefficient law, channel assignment, two-ratio readout |
| Down-type NP/scale | exact `5/6 = C_F - T_F` plus the strong threshold match is not a scale theorem | non-perturbative exponentiation plus scale-selection/RG transport |

## 3. Typed-Edge Synthesis

The current support graph has exact and retained nodes such as:

```text
one_Higgs_gauge_selection
CKM_atlas
top_Ward_anchor
Route2_endpoint_support
R_conn_8_9
C3_Fourier_carrier
RPSR_reduced_amplitude
five_sixths_Casimir
```

but it has no current typed path to:

```text
retained_non_top_quark_masses.
```

Adding one or more of the missing theorem edges would reopen the lane:

```text
C3_coefficient_source_law
physical_channel_assignment
two_ratio_readout
five_sixths_NP_scale_theorem
Route2_source_domain_bridge
species_differentiated_non_top_Ward
```

Those edges are not latent in the current support bank. They are exactly the
human-science theorem content that remains open.

## 4. Theorem

**Theorem (Lane 3 current-bank stuck fan-out).** Under the assumptions and
imports recorded in the Lane 3 loop pack after blocks 01 through 12, no
current typed route reaches retained non-top quark masses. Each orthogonal
fan-out frame terminates at a named missing theorem edge. Therefore the
best honest status is open, with retained closure withheld.

This is not a theorem that future Lane 3 closure is impossible. It is a
current-bank exhaustion result: the next retained movement requires a new
source/readout theorem, not another promotion of existing support.

## 5. Stop Implication

This synthesis justifies a supervisor stop for human science judgment if no
new theorem premise is being added in the current run:

```text
all viable current-bank routes are blocked after deep-work and fan-out;
the remaining progress requires choosing or deriving new theorem content.
```

## 6. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_lane3_stuck_fanout_synthesis.py
```

Expected result:

```text
TOTAL: PASS=68, FAIL=0
VERDICT: no current-bank Lane 3 route reaches retained non-top masses; new
source/readout theorem content is required.
```
