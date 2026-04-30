# PR Backlog

**Updated:** 2026-04-30T10:43:36Z

## Recovery Status

The original backlog below records the unattended supervisor's failed delivery
attempts. Recovery completed on 2026-04-30 after removing the stale launchd
keepalive job, committing the aggregate campaign artifacts, pushing
`physics-loop/impact-campaign-20260429`, and opening PR #209.

PR: https://github.com/jonathonreilly/cl3-lattice-framework/pull/209

Blocks 01-05 ship together because the campaign ledgers, claim-status
certificate, review history, and global-stop marker are shared across all five
blocks.

Aggregate PR title:

```text
[physics-loop] impact campaign blocks 01-05: no-go boundaries
```

Aggregate verification:

```text
Block 01: SUMMARY: PASS=18 FAIL=0; py_compile PASS
Block 02: SUMMARY: PASS=21 FAIL=0; py_compile PASS
Block 03: SUMMARY: PASS=22 FAIL=0; py_compile PASS
Block 04: SUMMARY: PASS=18 FAIL=0; py_compile PASS
Block 05: SUMMARY: PASS=16 FAIL=0; py_compile PASS
```

Runtime supervisor artifacts are intentionally excluded from delivery:
`last_codex_message.md`, `supervisor.lock`, `supervisor.log`, and
`supervisor_status.json`.

## Block 01 PR Pending: Delivery Tooling Failure

**Block:** Lane 4D `(SR-2)` Pfaffian / scalar two-point boundary
**Honest status:** `no-go`
**Intended base:** `main`
**Intended head:** `physics-loop/impact-campaign-20260429`
**Intended title:** `[physics-loop] impact-campaign block01: no-go`

Delivery was attempted but failed before staging because the git index for
this worktree is stored outside the writable sandbox:

```text
fatal: Unable to create '/Users/jonBridger/Toy Physics/.git/worktrees/CI3Z2-physics-loop-impact-campaign-20260429/index.lock': Operation not permitted
```

Earlier, creating a dedicated block branch also failed for the same external
git reference-store reason:

```text
fatal: cannot lock ref 'refs/heads/physics-loop/impact-campaign-20260429-block01-20260429': Unable to create '/Users/jonBridger/Toy Physics/.git/refs/heads/physics-loop/impact-campaign-20260429-block01-20260429.lock': Operation not permitted
```

Run these commands from an environment with write access to the git directory:

```bash
git switch physics-loop/impact-campaign-20260429
git add .claude/science/physics-loops/impact-campaign-20260429/ARTIFACT_PLAN.md .claude/science/physics-loops/impact-campaign-20260429/ASSUMPTIONS_AND_IMPORTS.md .claude/science/physics-loops/impact-campaign-20260429/CLAIM_STATUS_CERTIFICATE.md .claude/science/physics-loops/impact-campaign-20260429/HANDOFF.md .claude/science/physics-loops/impact-campaign-20260429/LITERATURE_BRIDGES.md .claude/science/physics-loops/impact-campaign-20260429/NO_GO_LEDGER.md .claude/science/physics-loops/impact-campaign-20260429/OPPORTUNITY_QUEUE.md .claude/science/physics-loops/impact-campaign-20260429/PR_BACKLOG.md .claude/science/physics-loops/impact-campaign-20260429/REVIEW_HISTORY.md .claude/science/physics-loops/impact-campaign-20260429/ROUTE_PORTFOLIO.md .claude/science/physics-loops/impact-campaign-20260429/STATE.yaml docs/NEUTRINO_LANE4_SR2_PFAFFIAN_SCALAR_TWO_POINT_BOUNDARY_NOTE_2026-04-29.md outputs/frontier_neutrino_lane4_sr2_pfaffian_scalar_two_point_boundary_2026-04-29.txt scripts/frontier_neutrino_lane4_sr2_pfaffian_scalar_two_point_boundary.py
git commit -m "physics-loop block01 sr2 scalar boundary"
git push -u origin physics-loop/impact-campaign-20260429
gh pr create --base main --head physics-loop/impact-campaign-20260429 --title "[physics-loop] impact-campaign block01: no-go" --body-file .claude/science/physics-loops/impact-campaign-20260429/HANDOFF.md
gh pr view --web
```

Artifacts to review:

- `docs/NEUTRINO_LANE4_SR2_PFAFFIAN_SCALAR_TWO_POINT_BOUNDARY_NOTE_2026-04-29.md`
- `scripts/frontier_neutrino_lane4_sr2_pfaffian_scalar_two_point_boundary.py`
- `outputs/frontier_neutrino_lane4_sr2_pfaffian_scalar_two_point_boundary_2026-04-29.txt`
- `.claude/science/physics-loops/impact-campaign-20260429/CLAIM_STATUS_CERTIFICATE.md`
- `.claude/science/physics-loops/impact-campaign-20260429/REVIEW_HISTORY.md`

Verification already run:

```bash
set -o pipefail; python3 scripts/frontier_neutrino_lane4_sr2_pfaffian_scalar_two_point_boundary.py | tee outputs/frontier_neutrino_lane4_sr2_pfaffian_scalar_two_point_boundary_2026-04-29.txt
python3 -m py_compile scripts/frontier_neutrino_lane4_sr2_pfaffian_scalar_two_point_boundary.py
```

Result:

```text
SUMMARY: PASS=18 FAIL=0
```

## Block 05 PR Pending: Delivery Tooling Failure

**Block:** Lane 2 physical-unit Schrodinger/Coulomb scale boundary
**Honest status:** `no-go`
**Intended base:** `main`
**Intended head:** `physics-loop/impact-campaign-20260429`
**Intended title:** `[physics-loop] impact-campaign block05: no-go`

Delivery was attempted after Block 05 and failed before staging for the same
external git-index reason:

```text
fatal: Unable to create '/Users/jonBridger/Toy Physics/.git/worktrees/CI3Z2-physics-loop-impact-campaign-20260429/index.lock': Operation not permitted
```

Run these commands from an environment with write access to the git directory:

```bash
git switch physics-loop/impact-campaign-20260429
git add .claude/science/physics-loops/impact-campaign-20260429/ARTIFACT_PLAN.md .claude/science/physics-loops/impact-campaign-20260429/ASSUMPTIONS_AND_IMPORTS.md .claude/science/physics-loops/impact-campaign-20260429/CLAIM_STATUS_CERTIFICATE.md .claude/science/physics-loops/impact-campaign-20260429/HANDOFF.md .claude/science/physics-loops/impact-campaign-20260429/LITERATURE_BRIDGES.md .claude/science/physics-loops/impact-campaign-20260429/NO_GO_LEDGER.md .claude/science/physics-loops/impact-campaign-20260429/OPPORTUNITY_QUEUE.md .claude/science/physics-loops/impact-campaign-20260429/PR_BACKLOG.md .claude/science/physics-loops/impact-campaign-20260429/REVIEW_HISTORY.md .claude/science/physics-loops/impact-campaign-20260429/ROUTE_PORTFOLIO.md .claude/science/physics-loops/impact-campaign-20260429/STATE.yaml docs/ATOMIC_LANE2_PHYSICAL_UNIT_LIMIT_BOUNDARY_NOTE_2026-04-29.md outputs/frontier_atomic_lane2_physical_unit_limit_boundary_2026-04-29.txt scripts/frontier_atomic_lane2_physical_unit_limit_boundary.py
git commit -m "physics-loop block05 lane2 unit boundary"
git push -u origin physics-loop/impact-campaign-20260429
gh pr create --base main --head physics-loop/impact-campaign-20260429 --title "[physics-loop] impact-campaign block05: no-go" --body-file .claude/science/physics-loops/impact-campaign-20260429/HANDOFF.md
gh pr view --web
```

Artifacts to review:

- `docs/ATOMIC_LANE2_PHYSICAL_UNIT_LIMIT_BOUNDARY_NOTE_2026-04-29.md`
- `scripts/frontier_atomic_lane2_physical_unit_limit_boundary.py`
- `outputs/frontier_atomic_lane2_physical_unit_limit_boundary_2026-04-29.txt`
- `.claude/science/physics-loops/impact-campaign-20260429/CLAIM_STATUS_CERTIFICATE.md`
- `.claude/science/physics-loops/impact-campaign-20260429/REVIEW_HISTORY.md`

Verification already run:

```bash
set -o pipefail; python3 scripts/frontier_atomic_lane2_physical_unit_limit_boundary.py | tee outputs/frontier_atomic_lane2_physical_unit_limit_boundary_2026-04-29.txt
python3 -m py_compile scripts/frontier_atomic_lane2_physical_unit_limit_boundary.py
```

Result:

```text
SUMMARY: PASS=16 FAIL=0
```

## Block 02 PR Pending: Delivery Tooling Failure

**Block:** Lane 1 `(B2)` dynamical screening boundary
**Honest status:** `no-go`
**Intended base:** `main`
**Intended head:** `physics-loop/impact-campaign-20260429`
**Intended title:** `[physics-loop] impact-campaign block02: no-go`

Delivery was attempted after Block 02 and failed before staging for the same
external git-index reason:

```text
fatal: Unable to create '/Users/jonBridger/Toy Physics/.git/worktrees/CI3Z2-physics-loop-impact-campaign-20260429/index.lock': Operation not permitted
```

Run these commands from an environment with write access to the git directory:

```bash
git switch physics-loop/impact-campaign-20260429
git add .claude/science/physics-loops/impact-campaign-20260429/ARTIFACT_PLAN.md .claude/science/physics-loops/impact-campaign-20260429/ASSUMPTIONS_AND_IMPORTS.md .claude/science/physics-loops/impact-campaign-20260429/CLAIM_STATUS_CERTIFICATE.md .claude/science/physics-loops/impact-campaign-20260429/HANDOFF.md .claude/science/physics-loops/impact-campaign-20260429/LITERATURE_BRIDGES.md .claude/science/physics-loops/impact-campaign-20260429/NO_GO_LEDGER.md .claude/science/physics-loops/impact-campaign-20260429/OPPORTUNITY_QUEUE.md .claude/science/physics-loops/impact-campaign-20260429/PR_BACKLOG.md .claude/science/physics-loops/impact-campaign-20260429/REVIEW_HISTORY.md .claude/science/physics-loops/impact-campaign-20260429/ROUTE_PORTFOLIO.md .claude/science/physics-loops/impact-campaign-20260429/STATE.yaml docs/HADRON_LANE1_B2_DYNAMICAL_SCREENING_BOUNDARY_NOTE_2026-04-29.md outputs/frontier_hadron_lane1_b2_dynamical_screening_boundary_2026-04-29.txt scripts/frontier_hadron_lane1_b2_dynamical_screening_boundary.py
git commit -m "physics-loop block02 lane1 b2 boundary"
git push -u origin physics-loop/impact-campaign-20260429
gh pr create --base main --head physics-loop/impact-campaign-20260429 --title "[physics-loop] impact-campaign block02: no-go" --body-file .claude/science/physics-loops/impact-campaign-20260429/HANDOFF.md
gh pr view --web
```

Artifacts to review:

- `docs/HADRON_LANE1_B2_DYNAMICAL_SCREENING_BOUNDARY_NOTE_2026-04-29.md`
- `scripts/frontier_hadron_lane1_b2_dynamical_screening_boundary.py`
- `outputs/frontier_hadron_lane1_b2_dynamical_screening_boundary_2026-04-29.txt`
- `.claude/science/physics-loops/impact-campaign-20260429/CLAIM_STATUS_CERTIFICATE.md`
- `.claude/science/physics-loops/impact-campaign-20260429/REVIEW_HISTORY.md`

Verification already run:

```bash
set -o pipefail; python3 scripts/frontier_hadron_lane1_b2_dynamical_screening_boundary.py | tee outputs/frontier_hadron_lane1_b2_dynamical_screening_boundary_2026-04-29.txt
python3 -m py_compile scripts/frontier_hadron_lane1_b2_dynamical_screening_boundary.py
```

Result:

```text
SUMMARY: PASS=21 FAIL=0
```

## Block 03 PR Pending: Delivery Tooling Failure

**Block:** Lane 5 `(C2)` CKM/PMNS right-sensitive selector stretch
**Honest status:** `no-go`
**Intended base:** `main`
**Intended head:** `physics-loop/impact-campaign-20260429`
**Intended title:** `[physics-loop] impact-campaign block03: no-go`

Delivery was attempted after Block 03 and failed before staging for the same
external git-index reason:

```text
fatal: Unable to create '/Users/jonBridger/Toy Physics/.git/worktrees/CI3Z2-physics-loop-impact-campaign-20260429/index.lock': Operation not permitted
```

Run these commands from an environment with write access to the git directory:

```bash
git switch physics-loop/impact-campaign-20260429
git add .claude/science/physics-loops/impact-campaign-20260429/ARTIFACT_PLAN.md .claude/science/physics-loops/impact-campaign-20260429/ASSUMPTIONS_AND_IMPORTS.md .claude/science/physics-loops/impact-campaign-20260429/CLAIM_STATUS_CERTIFICATE.md .claude/science/physics-loops/impact-campaign-20260429/HANDOFF.md .claude/science/physics-loops/impact-campaign-20260429/LITERATURE_BRIDGES.md .claude/science/physics-loops/impact-campaign-20260429/NO_GO_LEDGER.md .claude/science/physics-loops/impact-campaign-20260429/OPPORTUNITY_QUEUE.md .claude/science/physics-loops/impact-campaign-20260429/PR_BACKLOG.md .claude/science/physics-loops/impact-campaign-20260429/REVIEW_HISTORY.md .claude/science/physics-loops/impact-campaign-20260429/ROUTE_PORTFOLIO.md .claude/science/physics-loops/impact-campaign-20260429/STATE.yaml docs/HUBBLE_LANE5_C2_CKM_PMNS_RIGHT_SENSITIVE_SELECTOR_STRETCH_NOTE_2026-04-29.md outputs/frontier_hubble_lane5_c2_ckm_pmns_right_sensitive_selector_stretch_2026-04-29.txt scripts/frontier_hubble_lane5_c2_ckm_pmns_right_sensitive_selector_stretch.py
git commit -m "physics-loop block03 lane5 c2 selector stretch"
git push -u origin physics-loop/impact-campaign-20260429
gh pr create --base main --head physics-loop/impact-campaign-20260429 --title "[physics-loop] impact-campaign block03: no-go" --body-file .claude/science/physics-loops/impact-campaign-20260429/HANDOFF.md
gh pr view --web
```

Artifacts to review:

- `docs/HUBBLE_LANE5_C2_CKM_PMNS_RIGHT_SENSITIVE_SELECTOR_STRETCH_NOTE_2026-04-29.md`
- `scripts/frontier_hubble_lane5_c2_ckm_pmns_right_sensitive_selector_stretch.py`
- `outputs/frontier_hubble_lane5_c2_ckm_pmns_right_sensitive_selector_stretch_2026-04-29.txt`
- `.claude/science/physics-loops/impact-campaign-20260429/CLAIM_STATUS_CERTIFICATE.md`
- `.claude/science/physics-loops/impact-campaign-20260429/REVIEW_HISTORY.md`

Verification already run:

```bash
set -o pipefail; python3 scripts/frontier_hubble_lane5_c2_ckm_pmns_right_sensitive_selector_stretch.py | tee outputs/frontier_hubble_lane5_c2_ckm_pmns_right_sensitive_selector_stretch_2026-04-29.txt
python3 -m py_compile scripts/frontier_hubble_lane5_c2_ckm_pmns_right_sensitive_selector_stretch.py
```

Result:

```text
SUMMARY: PASS=22 FAIL=0
```

## Block 04 PR Pending: Delivery Tooling Failure

**Block:** Lane 2 `alpha(0)` / QED-running bridge boundary
**Honest status:** `no-go`
**Intended base:** `main`
**Intended head:** `physics-loop/impact-campaign-20260429`
**Intended title:** `[physics-loop] impact-campaign block04: no-go`

Delivery was attempted after Block 04 and failed before staging for the same
external git-index reason:

```text
fatal: Unable to create '/Users/jonBridger/Toy Physics/.git/worktrees/CI3Z2-physics-loop-impact-campaign-20260429/index.lock': Operation not permitted
```

Run these commands from an environment with write access to the git directory:

```bash
git switch physics-loop/impact-campaign-20260429
git add .claude/science/physics-loops/impact-campaign-20260429/ARTIFACT_PLAN.md .claude/science/physics-loops/impact-campaign-20260429/ASSUMPTIONS_AND_IMPORTS.md .claude/science/physics-loops/impact-campaign-20260429/CLAIM_STATUS_CERTIFICATE.md .claude/science/physics-loops/impact-campaign-20260429/HANDOFF.md .claude/science/physics-loops/impact-campaign-20260429/LITERATURE_BRIDGES.md .claude/science/physics-loops/impact-campaign-20260429/NO_GO_LEDGER.md .claude/science/physics-loops/impact-campaign-20260429/OPPORTUNITY_QUEUE.md .claude/science/physics-loops/impact-campaign-20260429/PR_BACKLOG.md .claude/science/physics-loops/impact-campaign-20260429/REVIEW_HISTORY.md .claude/science/physics-loops/impact-campaign-20260429/ROUTE_PORTFOLIO.md .claude/science/physics-loops/impact-campaign-20260429/STATE.yaml docs/ATOMIC_LANE2_ALPHA0_RUNNING_BRIDGE_BOUNDARY_NOTE_2026-04-29.md outputs/frontier_atomic_lane2_alpha0_running_bridge_boundary_2026-04-29.txt scripts/frontier_atomic_lane2_alpha0_running_bridge_boundary.py
git commit -m "physics-loop block04 lane2 alpha0 boundary"
git push -u origin physics-loop/impact-campaign-20260429
gh pr create --base main --head physics-loop/impact-campaign-20260429 --title "[physics-loop] impact-campaign block04: no-go" --body-file .claude/science/physics-loops/impact-campaign-20260429/HANDOFF.md
gh pr view --web
```

Artifacts to review:

- `docs/ATOMIC_LANE2_ALPHA0_RUNNING_BRIDGE_BOUNDARY_NOTE_2026-04-29.md`
- `scripts/frontier_atomic_lane2_alpha0_running_bridge_boundary.py`
- `outputs/frontier_atomic_lane2_alpha0_running_bridge_boundary_2026-04-29.txt`
- `.claude/science/physics-loops/impact-campaign-20260429/CLAIM_STATUS_CERTIFICATE.md`
- `.claude/science/physics-loops/impact-campaign-20260429/REVIEW_HISTORY.md`

Verification already run:

```bash
set -o pipefail; python3 scripts/frontier_atomic_lane2_alpha0_running_bridge_boundary.py | tee outputs/frontier_atomic_lane2_alpha0_running_bridge_boundary_2026-04-29.txt
python3 -m py_compile scripts/frontier_atomic_lane2_alpha0_running_bridge_boundary.py
```

Result:

```text
SUMMARY: PASS=18 FAIL=0
```
