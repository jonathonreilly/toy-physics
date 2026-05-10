# Scaling Failure Mechanisms

---

**This is a mechanism-inventory / diagnostic-narrative note. It does
not establish any retained claim.**
For retained claims on scaling-failure or saturation diagnostics, see
the per-claim notes referenced from the `## Audit scope` block below.

---

**Status:** support / mechanism-inventory record only — does not propagate retained-grade
**Claim type:** meta
**Claim scope:** support / mechanism-inventory record only — does not propagate retained-grade
**Audit authority:** independent audit ledger only; this source does not set an audit verdict.
**Propagates retained-grade:** no
**Proposes new claims:** no

## Audit scope (relabel 2026-05-10)

This file is a **mechanism-inventory / diagnostic-narrative note**
for scaling-failure diagnoses across the gravity / decoherence /
spectral lanes. It is **not** a single retained theorem and **must
not** be audited as one. The audit ledger row for
`scaling_failure_mechanisms` classified this source as
conditional/bounded_theorem with auditor's repair target:

> attach the scaling/decoherence logs or scripts that compute Q_sat,
> H, purity, and the reported correlations, and emit asserted
> runner checks.

The minimal-scope response in this PR is to **relabel** this document
as a mechanism-inventory diagnostic record rather than to attach the
scaling/decoherence logs, build asserted runner checks, or
materialize Q_sat / H / purity / correlation computations here.
Those steps belong in dedicated review-loop or per-mechanism audit
passes. Until that work is done:

- This file makes **no** retained-claim assertions of its own.
- The Q_sat saturation narrative, env-label-sharing mechanism,
  reduced-variable model framing, the `r=-0.89` vs `r=0.24`
  correlation comparison, and "fix candidates" inventory below are
  **historical mechanism-diagnostic memory only**.
- The retained-status surface for any saturation, decoherence, or
  correlation sub-claim is the audit ledger
  (`docs/audit/AUDIT_LEDGER.md`) plus the per-mechanism notes,
  **not** this diagnostic narrative.
- Retained-grade does **NOT** propagate from this mechanism-
  inventory note to any saturation reading, correlation value, or
  successor scaling diagnosis.

For any retained claim about scaling-failure mechanisms, audit the
corresponding dedicated note and its runner as a separate scoped
claim — not this mechanism-inventory record.

---

## Gravity: Phase-Valley Saturation

**Reduced variable:** `Q_sat = k × ΣΔS` (total phase deficit across the beam)

**Mechanism:**
1. The spent-delay action DECREASES near mass: ΔS ≈ -L√(2f)
2. Paths through high-field regions accumulate less phase → constructive interference toward mass
3. At small Q_sat (< 1): shift ∝ k² × field gradient (perturbative, could scale)
4. At Q_sat > π: the beam probability flips entirely to one side (saturated)
5. In saturated regime: shift = ±height, independent of b and M

**Why it doesn't scale:**
- The total ΔS across the beam depends on ∫√(f(r)) dx, which converges
- On a 2D lattice: f ~ log(R/r), so ∫√(log) dx is finite and weakly b-dependent
- On a 3D DAG: f ~ 1/r, same convergence
- Path-sum averaging over many near-equivalent routes further compresses the response
- Result: tanh-like saturation curve, not power law

**Codex's reduced model:** `Δky ≈ Δk_sat × tanh(C × Q_sat(b))` where Q_sat = valley-mean action gap / pooled valley action spread.

**Fix candidates:**
- Action renormalized by local path multiplicity (more paths → less action per effective path)
- Coarse-grained propagator where near-identical microscopic paths don't all add equally
- Multiscale path-sum with scale-dependent k

## Decoherence: Env-Label Sharing

**Reduced variable:** env sector entropy H = -Σ p_env × log(p_env)

**Mechanism:**
1. Two-register env labels paths by last mass node
2. On small graphs (N < 200): few paths → slits exit through different mass nodes → H high → low purity
3. On large graphs (N > 400): many paths → both slits reach all mass nodes via many routes → env labels shared → H drops → purity rises
4. Depth-scaled env partially fixes this (purity plateaus at 0.79 instead of climbing to 0.89)

**Why it doesn't scale:**
- Path multiplicity grows exponentially with graph depth (~degree^depth)
- Env label diversity grows linearly (one label per mass node)
- At large N: exponential paths through linear labels → both slits converge to same env distribution
- Central limit theorem: ensemble of many paths through same labels → converges

**Env sector entropy predicts purity at r=-0.89** (much better than structural predictors at r=0.24)

**Fix candidates:**
- Multi-local tensor env: each mass-region cell gets its own register, connected via tensor product
- Edge-sector records: coarse histogram of incoming/outgoing directions per cell
- Continuous bath variable (infinite-dim env)
- Irreversible coarse-graining over spatial region, not single label

## Key Insight: The Two Failures Are Different

| | Gravity | Decoherence |
|---|---|---|
| What fails | Magnitude scaling | Size scaling |
| Root cause | Phase deficit saturates | Env labels get shared |
| Reduced variable | Q_sat = k×ΣΔS | H = env sector entropy |
| Fix domain | Propagator architecture | Environment architecture |
| Can fix independently | Yes | Yes |
