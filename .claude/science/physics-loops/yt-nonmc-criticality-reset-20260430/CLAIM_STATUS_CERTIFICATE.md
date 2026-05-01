# Claim Status Certificate

**Block:** `yt-nonmc-criticality-reset-20260430`  
**Artifact:** `docs/YT_PLANCK_DOUBLE_CRITICALITY_SELECTOR_NOTE_2026-04-30.md`  
**Runner:** `scripts/frontier_yt_planck_double_criticality_selector.py`

```yaml
actual_current_surface_status: conditional-support / open selector route
conditional_surface_status: "Candidate y_t selector if beta_lambda(M_Pl)=0 is derived from the substrate."
hypothetical_axiom_status: "Planck double-criticality if beta_lambda(M_Pl)=0 is adopted rather than derived."
admitted_observation_status: "y_t(v), m_H, m_t, and 1/sqrt(6) are comparators only."
proposal_allowed: false
proposal_allowed_reason: "The decisive beta_lambda(M_Pl)=0 premise is open."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

Allowed wording:

- conditional-support / open selector route;
- route reset;
- non-MC candidate;
- isolated hard premise.

Forbidden wording:

- audit-clean `y_t` derivation;
- direct top mass measurement;
- closure of PR #230 strict mode;
- any claim that `beta_lambda(M_Pl)=0` has been derived here.

Verification:

```bash
PYTHONPATH=scripts python3 scripts/frontier_yt_planck_double_criticality_selector.py
# SUMMARY: PASS=19 FAIL=0
```

