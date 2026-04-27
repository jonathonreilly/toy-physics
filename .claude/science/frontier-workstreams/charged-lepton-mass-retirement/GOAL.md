# Charged-Lepton Mass Retirement Workstream

**Goal:** retire the charged-lepton mass observational pin and move toward
retained absolute `m_e`, `m_mu`, and `m_tau` from framework structure.

**User invocation:** `/frontier-workstream "go retire charged-lepton mass"
--mode run --literature --runtime 10h`

**Target status:** retained. Support-only work is acceptable only if it is the
strongest honest artifact toward retained closure, such as an exact support
theorem, a retained-objective no-go, or a narrowed blocker.

## Current Retained Objective

The branch should try to replace the bounded charged-lepton package's
three-real PDG observational pin with framework-derived structure.

The live open-lane note identifies the likely chain:

```text
Koide ratio closure + y_tau Ward identity + V_0 scale anchor
  -> absolute charged-lepton masses
```

This workstream prioritizes the absolute-scale side:

1. identify whether the tau-generation Ward route can produce a retained
   `y_tau` identity analogous to the retained top Ward identity;
2. identify whether the existing one-Higgs Yukawa/gauge-selection and hw=1
   triplet surfaces already force a charged-lepton Yukawa normalization;
3. if not, produce an exact no-go or narrowed theorem obligation rather than
   support-only prose.

## Delivery

Work is science-only on branch
`frontier/charged-lepton-mass-retirement-20260426`. Proposed repo weaving is
recorded in `HANDOFF.md` only.
