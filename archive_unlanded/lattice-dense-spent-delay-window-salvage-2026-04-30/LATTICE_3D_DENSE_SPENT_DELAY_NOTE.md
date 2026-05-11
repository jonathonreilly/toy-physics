# 3D Dense Spent-Delay Lattice Note

**Date:** 2026-04-04  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/lattice-dense-spent-delay-window-salvage-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- Date archived: 2026-04-30
- Archive directory: `archive_unlanded/lattice-dense-spent-delay-window-salvage-2026-04-30/`
- Audit verdict (`verdict_rationale` from [audit_ledger.json](../../docs/audit/data/audit_ledger.json), claim_id `lattice_3d_dense_spent_delay_note`, `audit_status: audited_failed`, `effective_status: retained_no_go`):

> "Issue: the source note's load-bearing attractive-window claim includes z=6, but the named live runner and checked log only test z=2,3,4,5 and report hierarchy-aligned support as 4/4 points. Why this blocks: a hostile auditor cannot ratify a retained z=2..6 window when the allowed runner output omits one endpoint; the exact retained wording is stale relative to the executable artifact even though the z=2..5 card is reproducible. Repair target: update the runner to include z=6 with assertions for centroid, P_near, bias, and hierarchy sign, or revise the note's retained window and table to z=2..5; register the runner path in the audit ledger if this card remains load-bearing. Claim boundary until fixed: it is safe to claim the current runner's finite 3D dense spent-delay card: Born 7.39e-16, d_TV=0.3785, k=0 controls zero, F~M alpha about 0.34, nonzero MI/decoherence, N=12/15 positive centroid response after N=10 away, and hierarchy-aligned attraction at z=2..5; it is not safe to claim the z=2..6 window or any broader/asymptotic attraction theorem."

Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

---

## Purpose

This note freezes the current 3D dense spent-delay reopening on the ordered
lattice family and keeps it separate from broader branch narrative.

The important correction is:

- the branch really does retain a strong same-family 3D dense card
- but the gravity sign should be read through the canonical observable
  hierarchy, not centroid alone

So this is a real retained branch, not a replacement for the mirror flagship.

## Fixed family and harness

- graph family: 3D ordered dense lattice
- forward span: `max_d = 3` (`49` edges per node)
- action: original spent-delay
- field strength: `5e-5`
- geometry: `L = 12`, `W = 6`, `h = 1.0`
- barrier card: upper/lower `y` half-space openings on one barrier layer
- Born audit: same-family companion audit on the same barrier layer using a
  three-opening partition

Primary artifact chain:

- [`scripts/lattice_3d_dense_10prop.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_dense_10prop.py)
- [`logs/2026-04-04-lattice-3d-dense-10prop.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-lattice-3d-dense-10prop.txt)

## Retained card

| property | value | read |
|---|---:|---|
| Born companion audit | `7.39e-16` | machine-clean |
| `d_TV` | `0.3785` | nontrivial |
| `k=0` gravity response | `0.000000` | exact on this harness |
| `F∝M` exponent | `0.34`, `R² = 0.97` | positive but sub-linear |
| gravity vs length | `N=10:-0.009546`, `N=12:+0.001941`, `N=15:+0.016972` | crosses to positive and grows on this tested window |
| decoherence | `13.5%` | nontrivial |
| MI | `0.1414` bits | nontrivial |
| purity scaling | `N^(-1.76)`, `R² = 0.952`, `N_half = 48` | real but steep/short-range |
| `k=0` hierarchy control | `0.000000` | exact on this harness |
| centroid distance law | `b^(-1.62)`, `R² = 0.976` | strong centroid-side decay |

## Gravity observable hierarchy

On this exact retained barrier card, the gravity sign is:

| `z_mass` | centroid | `P_near` | bias | read |
|---|---:|---:|---:|---|
| `2` | `+0.003101` | `+0.001469` | `+0.107097` | attractive |
| `3` | `+0.001941` | `+0.000374` | `+0.176381` | attractive |
| `4` | `+0.001157` | `+0.000626` | `+0.113676` | attractive |
| `5` | `+0.000693` | `+0.000715` | `+0.048601` | attractive |
| `6` | `+0.000572` | `+0.000536` | `+0.000112` | attractive |

So the retained 3D dense spent-delay read is:

- **genuine attraction on the retained tested window** (`z = 2, 3, 4, 5, 6`)

That is stronger than the older 3D ordered-lattice negative read, but it is
still not the same thing as an all-distances or asymptotic theorem.

## What is retained

- the original spent-delay action now has a real 3D dense ordered-lattice card
- Born stays machine-clean on the same family
- `k=0` stays at zero on the fixed barrier card
- MI, decoherence, and `d_TV` remain nonzero on the same family
- the branch keeps a positive sub-linear mass response
- the branch keeps a strong centroid-side distance decay
- the gravity hierarchy confirms a real attractive window on the retained
  tested `z = 2..6` range

## What is not retained

- not a replacement for the mirror flagship
- not a proof that all larger or asymptotic `z` values remain hierarchy-clean
  attraction
- not a continuum or RG theorem
- not a clean promoted `1/b^2` theorem on this 3D spent-delay branch
- not a broad architectural proof that ordered lattices solve the attraction /
  distance-law problem everywhere

## Program read

This result moves the ordered-lattice branch forward in an important way:

- 2D dense spent-delay keeps the clearest ultra-weak `1/b`-style reopening
- 3D dense spent-delay now adds a retained same-family dense card with
  nontrivial Born / MI / decoherence and a tested attractive window

But the project ranking does not change:

- **mirror remains the flagship**
- **ordered lattice remains the secondary branch**
- **NN refinement remains the continuum-side bridge**

## Next highest-value work

1. Improve the 3D dense spent-delay slit geometry so the attractive window
   extends beyond `z = 6` while preserving MI / decoherence.
2. Strengthen MI / decoherence on the same retained 3D dense family.
3. Keep the gravity-observable hierarchy attached to all future 3D dense
   gravity claims so centroid-only sign does not overstate the result.
