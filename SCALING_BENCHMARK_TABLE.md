# Scaling Benchmark Table

| graph family | scaling variable | gravity metric | decoherence metric | expected good scaling | current failure mode |
|---|---|---|---|---|---|
| regular layered lattice | layer depth | packet-local near-mass action `Q`, `Δk_y` | detector-conditioned purity / mixedness | graded dependence should survive as depth grows | gravity trends toward plateau; finite env recoheres |
| branching tree | branching factor | `k * ΣΔS_local`, `Δk_y` | branch-distinguishability vs purity | response should remain graded as route count grows | route multiplicity may collapse gravity to threshold; shared labels destroy branch selectivity |
| layered random DAG with tunable path multiplicity | mean degree / path count at fixed local field geometry | packet-local action gap and `Q_local` | purity / decoherence strength at fixed local env density | gravity law should not reduce to sign-only; decoherence should not wash out | path averaging compresses gravity; env label reuse washes out decoherence |
| layered random DAG with tunable env-region depth or fraction | env depth or env fraction at fixed graph family | control only: verify gravity core survives env changes | detector-conditioned purity / mixedness | mixedness should stay bounded away from `1` or strengthen with size | tested finite/discrete env architectures wrong-scale as graph grows |

## Usage

Run these families before returning to the full random-DAG suite.

Rules:

- vary one scaling variable at a time
- keep the unitary core fixed
- report both the reduced variable and the observed response
- stop if a candidate architecture fails its minimal family before broadening
