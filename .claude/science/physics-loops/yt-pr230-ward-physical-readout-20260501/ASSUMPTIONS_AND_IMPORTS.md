# Assumptions And Imports

| Item | Role | Current status | Loop disposition |
|---|---|---|---|
| `g_bare = 1` canonical surface | substrate input | existing minimal-axiom surface | allowed as substrate input |
| `N_c = 3`, `N_iso = 2` | structural counts | retained/structural in repo | allowed for arithmetic |
| Old Ward `H_unit` matrix-element readout | forbidden shortcut | `audited_renaming` | may be cited only as the failure mode |
| Source / HS / Legendre normalization | physical readout bridge | `audited_renaming` via SSB matching note | open import |
| Chirality projection and right-handed selector | trilinear map | `audited_failed` via Class 5 ledger row | open import |
| Physical scalar carrier uniqueness | maps source scalar to Higgs fluctuation | `audited_failed` on current ledger row | open import |
| Scalar LSZ / `Z_phi` external leg | physical vertex normalization | `audited_conditional` | open import |
| Common tadpole/dressing | needed to compare gauge and scalar readouts | not clean after Ward audit | open import |
| Observed `m_t`, observed `y_t` | comparator only | external observation | forbidden as proof input |
| `alpha_LM` / plaquette normalization | prior quantitative bridge | audited non-clean in this lane | forbidden as load-bearing proof input |
| Production MC data | direct-measurement route evidence | not complete | unavailable for closure |
| Scalar-channel contact coupling `G` | HS/RPA pole condition | not in `A_min` | forbidden unless derived from Wilson gauge ladder |
| Scalar-channel Bethe-Salpeter kernel | interacting pole route | not yet retained | open import after ladder scout |
| IR / finite-volume kernel limit | needed for ladder eigenvalue crossing | not yet fixed | open import |

Minimal allowed premise set for the current stretch attempt:

```text
A_min = retained action/substrate + structural counts + standard functional
derivative definitions, but no H_unit matrix-element definition, no observed
top mass/Yukawa, no fitted selector, and no alpha_LM/plaquette bridge as proof.
```
