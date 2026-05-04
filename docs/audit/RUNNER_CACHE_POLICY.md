# Runner Cache Policy

**Status:** binding for all PRs that modify runners under `scripts/`.

## What this is

Every primary runner referenced from a ledger row has a SHA-pinned cache
file at:

```
logs/runner-cache/<runner-stem>.txt
```

The cache header pins the file to the runner's content SHA-256. The
audit prompt's Section 3 (runner output) is sourced from this cache.

The cache is **version-controlled**: cache files live in git on every
branch and are landed alongside the runner change that produced them.

## Why the cache exists

The audit lane's auditor uses the strongest configured full Codex GPT
model at maximum reasoning by default. It judges each claim from a
restricted packet that includes the runner's source code and the runner's
stdout. If the runner changes but the cached stdout doesn't, the auditor
sees a stale picture and may issue a verdict that doesn't match the
current code. The cache must therefore stay synchronized with its runner.

A naive "always run live" approach has two costs we explicitly do not
want to pay: long compute jobs (`frontier_alpha_s`, lattice plaquette
sweeps, etc.) would block every audit, and the same expensive run would
happen many times across audits that share a runner.

## Cache file format

```
===== runner cache v1 =====
runner: scripts/<name>.py
runner_sha256: <hex>
timeout_sec: 120
exit_code: 0
elapsed_sec: 12.34
status: ok          # ok | nonzero_exit | timeout | error
----- stdout -----
<stdout, capped at 200 KB tail>
----- stderr -----
<stderr, capped at 50 KB tail>
```

No timestamps anywhere. The file is purely a function of the runner SHA
and the execution result, so re-running `precompute_audit_runners.py` on
an already-fresh cache is a byte-level no-op (gate-clean).

## Freshness rule

A cache file is **fresh** iff its header `runner_sha256` equals the
SHA-256 of the runner file on disk. Anything else is **stale**:

| Status         | Meaning                                                         |
| -------------- | --------------------------------------------------------------- |
| `fresh`        | `runner_sha256` matches current SHA — auditor uses this cache   |
| `missing`      | No cache file exists for this runner                            |
| `corrupt`      | Cache file exists but the header is malformed                   |
| `sha_mismatch` | Header SHA differs from current runner SHA — runner was edited  |

`missing`, `corrupt`, and `sha_mismatch` all require refresh.

## Policy

Three gates enforce that no runner change lands without a fresh cache:

1. **Pre-commit hook** (`docs/audit/scripts/pre_commit_audit_check.sh`)
   When a developer stages a Python file under `scripts/`, the hook
   runs `precompute_audit_runners.py --staged-only --check-only` and
   blocks the commit if any staged runner has a stale cache. The
   developer's fix is to run `precompute_audit_runners.py --staged-only`
   and stage the resulting `logs/runner-cache/` files.

2. **CI gate** (`.github/workflows/audit.yml`)
   Every PR runs `precompute_audit_runners.py --all --check-only` on
   the head commit and fails if any cache (across the full ledger,
   not just staged files) is stale.

3. **Audit-runner consumption** (`scripts/codex_audit_runner.py`)
   The audit runner reads cache files only when their SHA matches.
   A stale cache is treated as if absent, and the audit runner falls
   back to live execution. Live execution writes back to the cache,
   so the first audit after a missed refresh is slow but
   self-healing.

## Refresh commands

```bash
# Refresh all stale caches in the audit queue (default — fastest path)
python3 scripts/precompute_audit_runners.py

# Cover the full ledger, not just queue
python3 scripts/precompute_audit_runners.py --all

# Refresh only currently-staged runners (pre-commit fix)
python3 scripts/precompute_audit_runners.py --staged-only

# Specific runners by path
python3 scripts/precompute_audit_runners.py \
    --runners scripts/foo.py,scripts/bar.py

# Dry verification (CI gate behavior; exit 1 if any stale)
python3 scripts/precompute_audit_runners.py --all --check-only

# Re-run even fresh caches
python3 scripts/precompute_audit_runners.py --force

# Delete cache files for runners that no longer exist
python3 scripts/precompute_audit_runners.py --cleanup-orphans
```

## Implementation files

| File                                          | Role                                          |
| --------------------------------------------- | --------------------------------------------- |
| `scripts/runner_cache.py`                     | Shared module: SHA, paths, format, execution |
| `scripts/precompute_audit_runners.py`         | Refresh tool with all the modes above         |
| `scripts/codex_audit_runner.py`               | Reads cache via `runner_cache.cache_excerpt_for_audit` |
| `docs/audit/scripts/pre_commit_audit_check.sh`| Pre-commit gate                               |
| `.github/workflows/audit.yml`                 | CI gate                                       |
| `docs/audit/templates/audit_workflow.yml`     | Template for the workflow file                |

## Bypass

`git commit --no-verify` skips the pre-commit hook. Do this only when
you understand the audit-evidence cost: any subsequent audit reading the
stale cache will be misled. The CI gate cannot be bypassed; PRs with
stale caches cannot be merged.
