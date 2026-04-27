# archive_unlanded — Science Archaeology Snapshot

**Generated:** 2026-04-27T12:12:59.879312+00:00  
**Source:** every remote branch with `last_commit_age_hours >= 24` whose `git diff origin/main...<branch>` adds files that do not exist on `origin/main`.

**Branches snapshotted:** 56  
**Unique files preserved:** 138

Each branch's novel content is preserved verbatim under `archive_unlanded/<branch_safe_name>/<original_path>`. The branches themselves are scheduled for archival (tag + delete) after this commit lands. Recovery of any individual branch remains possible via `git checkout archive/<branch>-<date>`.

## Reading guide

- `pair_classification: is_codex_review_or_land` — branch is   itself a Codex review/land branch; preserves the post-review   version of the science.
- `pair_classification: reviewed_unlanded` — Claude proposal   that has a Codex review partner; both versions preserved here   (look for the matching `codex/...` slug).
- `pair_classification: unreviewed_unlanded` — Claude proposal   with no Codex review partner; this is the highest-priority   bucket for the audit lane to triage.

## unreviewed_unlanded (9 branches)

| branch | files | age (h) | last commit subject |
|---|---:|---:|---|
| `ckm-a-squared-below-w2-y-quantum-closure` | 1 | 25 | ckm: CLOSE A^2 below W2 via Identification Source Theorem (S1) |
| `ckm-alpha-ew-lattice-adjoint-dim-closed-form` | 2 | 39 | ckm: land alpha_EW physical lattice-scale closed form via adjoint dim |
| `ckm-barred-nine-point-circle-protected-pencil` | 2 | 35 | ckm: land nine-point circle + protected coaxial pencil |
| `ckm-bernoulli-two-ninths-koide-bridge` | 1 | 43 | ckm: land Bernoulli-variance 2/9 identities supporting Koide bridge |
| `ckm-consecutive-primes-s3-koide-bridge` | 1 | 40 | ckm: land consecutive primes, S_3 group-theoretic Koide-bridge theorem |
| `ckm-perfect-number-triangular-koide-bridge` | 2 | 40 | ckm: land perfect-number, triangular, Lie-dimensional, Mersenne Koide-bridge the |
| `claude/flamboyant-hodgkin-e16786` | 3 | 42 | koide-a1: downgrade Brannen Plancherel note from claimed closure to support per  |
| `koide-q-closure-via-op-uniqueness` | 3 | 35 | Add Codex review for Koide Q OP closure |
| `koide-q-op-uniqueness-support-v4` | 2 | 35 | koide: V4 honest support, addressing all 3 Codex V3 review findings |

## reviewed_unlanded (19 branches)

| branch | files | age (h) | last commit subject |
|---|---:|---:|---|
| `ckm-a-rho-multiplicative-koide-bridge` | 2 | 43 | ckm: land multiplicative A^2-rho-eta^2 identities and 5th 2/9 path |
| `ckm-alpha-s-independent-structural-prophecy` | 2 | 25 | ckm: land alpha_s-independent structural-integer prophecy |
| `ckm-bare-ew-color-square-identity` | 2 | 39 | ckm: land bare EW gauge-coupling color-square identity theorem |
| `ckm-barred-brocard-angle-exact-closed-form` | 2 | 39 | ckm: land barred unitarity-triangle Brocard angle exact closed form |
| `ckm-barred-brocard-points-exact-closed-form` | 2 | 36 | ckm: land Brocard points exact closed form |
| `ckm-barred-orthic-triangle-exact-closed-form` | 2 | 35 | ckm: land orthic triangle exact closed form |
| `ckm-barred-steiner-inellipse-marden-closed-form` | 2 | 38 | ckm: land Steiner inellipse + Marden's theorem exact closed form |
| `ckm-barred-symmedian-brocard-circle-closed-form` | 2 | 38 | ckm: land Symmedian point + Brocard circle exact closed form |
| `ckm-bs-phi-s-nlo-jarlskog-bridge` | 2 | 40 | ckm: land B_s mixing phase phi_s NLO closed form and Jarlskog bridge theorem |
| `ckm-cubic-bernoulli-koide-bridge` | 1 | 42 | ckm: land cubic Bernoulli W(N) and triple-level factorization theorem |
| `ckm-egyptian-bernoulli-closures-koide-bridge` | 1 | 42 | ckm: land Egyptian fraction unitarity and Bernoulli sum closures Koide-bridge th |
| `ckm-magnitudes-vus-power-tower-bridge` | 2 | 34 | ckm: land \|V_us\|-power tower magnitude bridge |
| `ckm-multi-projection-bernoulli-koide-bridge` | 2 | 42 | ckm: land multi-projection Bernoulli family at three structural N-levels |
| `ckm-n9-structural-family-koide-bridge` | 1 | 43 | ckm: land complete n/N_color^2 structural family Koide-bridge theorem |
| `ckm-physical-ratios-circumradius-bridge` | 2 | 35 | ckm: land physical ratios circumradius bridge |
| `koide-closure-targets-AB` | 14 | 39 | koide: address review #3 documentation cleanups + record APPROVED verdict |
| `koide-closure-targets-AB-v2` | 2 | 38 | koide: close Q_l = 2/3 via OP local-source protocol + canonical descent (post-Co |
| `saturday-koide` | 2 | 35 | koide: V5 substantive proof advance via Frobenius reciprocity canonicality |
| `sunday-koide` | 2 | 24 | koide: V6 substantive proof advance via lepton-side analog of CKM A² closure |

## is_codex_review_or_land (28 branches)

| branch | files | age (h) | last commit subject |
|---|---:|---:|---|
| `codex/gauge-perron-variational-proof-2026-04-25` | 1 | 38 | gauge: prove Perron variational envelope |
| `codex/land-chronology-boundary-classifier-2026-04-25` | 23 | 39 | chronology: land boundary classifier packet |
| `codex/land-ckm-a-rho-multiplicative-2026-04-25` | 2 | 43 | ckm: land A-rho multiplicative identities |
| `codex/land-ckm-barred-brocard-points-2026-04-25` | 2 | 35 | ckm: land Brocard points exact closed form |
| `codex/land-ckm-brocard-closed-form-2026-04-25` | 2 | 38 | ckm: index barred Brocard corollary |
| `codex/land-ckm-ew-color-square-support-2026-04-25` | 2 | 39 | ckm: land bare EW color-square support |
| `codex/land-ckm-orthic-triangle-2026-04-25` | 2 | 35 | ckm: land orthic triangle closed forms |
| `codex/land-ckm-physical-ratios-circumradius-2026-04-25` | 2 | 34 | ckm: land physical-ratio circumradius bridge |
| `codex/land-ckm-steiner-marden-2026-04-25` | 2 | 37 | ckm: land barred Steiner Marden corollary |
| `codex/land-ckm-symmedian-brocard-circle-2026-04-25` | 2 | 38 | ckm: land barred symmedian Brocard circle corollary |
| `codex/land-ew-alpha-adjoint-support-2026-04-25` | 2 | 39 | ew: land alpha adjoint-dimension support |
| `codex/land-gauge-perron-variational-2026-04-25` | 2 | 38 | gauge: index Perron variational envelope |
| `codex/land-koide-closure-targets-ab-v2-2026-04-25` | 2 | 36 | koide: land OP local-descent boundary support |
| `codex/land-neutrino-seesaw-boundary-2026-04-25` | 2 | 35 | neutrino: land seesaw Schur boundary theorem |
| `codex/land-phase-valley-distance-law-2026-04-25` | 2 | 43 | gravity: land phase-valley distance-law universality |
| `codex/land-target3-coframe-derivation-2026-04-25` | 2 | 43 | planck: land target3 coframe support theorem |
| `codex/neutrino-seesaw-boundary-proof-2026-04-25` | 1 | 36 | neutrino: prove seesaw Schur boundary theorem |
| `codex/review-ckm-alpha-prophecy-2026-04-26` | 2 | 25 | ckm: land alpha-s independent structural ratios |
| `codex/review-ckm-vus-power-tower-2026-04-26` | 2 | 25 | ckm: land Cabibbo power-tower magnitude bridge |
| `codex/review-saturday-koide-2026-04-25` | 2 | 34 | koide: land Frobenius measure-selection support |
| `codex/review-sm-accidental-bl-proof-2026-04-26` | 2 | 25 | sm: land renormalizable accidental B/L conservation |
| `codex/review-sm-gim-neutral-current-proof-2026-04-26` | 2 | 24 | sm: prove GIM neutral-current projector theorem |
| `codex/review-sm-weinberg-operator-proof-2026-04-26` | 2 | 25 | sm: land active Weinberg operator uniqueness |
| `codex/sm-accidental-bl-proof-2026-04-26` | 2 | 25 | sm: prove renormalizable accidental B/L conservation |
| `codex/sm-gim-neutral-current-proof-2026-04-26` | 2 | 25 | sm: prove GIM neutral-current projector theorem |
| `codex/sm-quark-flavor-count-proof-2026-04-26` | 2 | 24 | docs: wire SM quark flavor count theorem |
| `codex/sm-weinberg-operator-proof-2026-04-26` | 1 | 25 | sm: prove active Weinberg operator uniqueness |
| `codex/target3-coframe-derivation` | 2 | 43 | planck: derive target3 coframe response |

