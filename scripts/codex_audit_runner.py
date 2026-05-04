#!/usr/bin/env python3
"""Drive Codex CLI as the audit-lane independent auditor.

Pulls the top-N rows from `docs/audit/data/audit_queue.json`, constructs
the prompt from `docs/audit/AUDIT_AGENT_PROMPT_TEMPLATE.md` for each, runs
`codex exec` (which uses the local ChatGPT subscription, no per-call API
billing), captures the JSON verdict, validates it, adds auditor metadata,
and pipes it through `docs/audit/scripts/apply_audit.py`. Each successful
verdict triggers `apply_audit.py`'s built-in propagation slice so the
pipeline stays consistent.

Usage:
  python3 scripts/codex_audit_runner.py [--n 10] [--dry-run] [--criticality critical]
                                        [--auditor-name codex-batch-2026-05-04]
                                        [--timeout-sec 300]

Cross-family rule: the audit lane requires Codex GPT-5.5 as the auditor
because most ledger notes were authored by Claude. This wrapper records
auditor_family='codex-gpt-5.5' and independence='cross_family' on every
verdict it lands. Do NOT change those fields without re-reading
`docs/audit/FRESH_LOOK_REQUIREMENTS.md`.

Restricted-inputs rule: each codex exec runs with --skip-git-repo-check
in an empty workdir under /tmp/codex-audit-isolated/<run-id>/, so the
auditor sees ONLY the prompt content (claim note + cited authorities +
runner stdout) and not the broader repo. This satisfies the audit lane's
fresh-look requirement.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AUDIT_DIR = REPO_ROOT / "docs" / "audit"
LEDGER_PATH = AUDIT_DIR / "data" / "audit_ledger.json"
QUEUE_PATH = AUDIT_DIR / "data" / "audit_queue.json"
PROMPT_TEMPLATE_PATH = AUDIT_DIR / "AUDIT_AGENT_PROMPT_TEMPLATE.md"
APPLY_AUDIT_SCRIPT = AUDIT_DIR / "scripts" / "apply_audit.py"
ISOLATED_BASE = Path("/tmp/codex-audit-isolated")
LOG_DIR = REPO_ROOT / "logs" / "codex-audit-runs"

# These fields are NOT controlled by the LLM; we set them on the runner side.
AUDITOR_FAMILY = "codex-gpt-5.5"
AUDITOR_INDEPENDENCE = "cross_family"

REQUIRED_VERDICT_FIELDS = {
    "claim_id",
    "load_bearing_step",
    "load_bearing_step_class",
    "claim_type",
    "claim_scope",
    "chain_closes",
    "chain_closure_explanation",
    "verdict",
    "verdict_rationale",
}

# Map JSON-extracted-from-stdout to apply_audit.py's input schema. apply_audit
# expects `verdict` etc. plus the runner-side fields auditor/auditor_family/
# independence/audit_date.
def add_auditor_metadata(verdict_blob: dict, auditor_name: str) -> dict:
    blob = dict(verdict_blob)
    blob.setdefault("auditor", auditor_name)
    blob.setdefault("auditor_family", AUDITOR_FAMILY)
    blob.setdefault("independence", AUDITOR_INDEPENDENCE)
    blob.setdefault("audit_date", datetime.now(timezone.utc).isoformat())
    # Some downstream callers want runner_check_breakdown even when missing.
    blob.setdefault("runner_check_breakdown", {"A": 0, "B": 0, "C": 0, "D": 0, "total_pass": 0})
    return blob


def load_queue(criticality_filter: str | None = None) -> list[dict]:
    q = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    rows = q.get("queue", [])
    if criticality_filter:
        rows = [r for r in rows if (r.get("criticality") or "") == criticality_filter]
    # rows are already pre-sorted by descending score in audit_queue.json
    return rows


def load_ledger_rows() -> dict[str, dict]:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))["rows"]


def read_note_body(note_path: str) -> str | None:
    p = REPO_ROOT / note_path
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8", errors="replace")


def get_runner_stdout(runner_path: str | None, timeout_sec: int) -> str:
    """Run the row's primary runner with a timeout; return stdout or empty."""
    if not runner_path:
        return ""
    p = REPO_ROOT / runner_path
    if not p.exists():
        return f"[runner missing on disk: {runner_path}]"
    try:
        res = subprocess.run(
            [sys.executable, str(p)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            env={**os.environ, "PYTHONPATH": str(REPO_ROOT / "scripts")},
        )
        if res.returncode != 0:
            return f"[runner exit={res.returncode}]\n{res.stdout[-3000:]}\n--- stderr ---\n{res.stderr[-1500:]}"
        return res.stdout[-6000:]   # cap to keep prompt size sane
    except subprocess.TimeoutExpired:
        return f"[runner timed out at {timeout_sec}s]"
    except Exception as e:
        return f"[runner error: {e}]"


def render_prompt(row: dict, ledger_rows: dict[str, dict],
                  template: str, runner_timeout_sec: int) -> str:
    """Substitute the prompt template's variables for one queue row."""
    cid = row["claim_id"]
    note_path = row.get("note_path") or ledger_rows.get(cid, {}).get("note_path") or ""
    runner_path = row.get("runner_path") or ledger_rows.get(cid, {}).get("runner_path") or ""
    claim_type_hint = (
        row.get("claim_type")
        or ledger_rows.get(cid, {}).get("claim_type")
        or ""
    )

    note_body = read_note_body(note_path) or f"[note missing on disk: {note_path}]"

    # Cited authorities: one-hop deps from the ledger row
    led_row = ledger_rows.get(cid, {})
    deps = led_row.get("deps", [])
    cited_blocks = []
    for dep_cid in deps:
        dep_row = ledger_rows.get(dep_cid, {})
        dep_path = dep_row.get("note_path") or ""
        dep_body = read_note_body(dep_path) or f"[dep note missing: {dep_path}]"
        eff = dep_row.get("effective_status") or "unaudited"
        ct = dep_row.get("claim_type") or "?"
        cited_blocks.append(
            f"=== BEGIN CITED AUTHORITY: {dep_path} ===\n"
            f"=== Cited authority effective_status: {eff} ===\n"
            f"=== Cited authority claim_type: {ct} ===\n"
            f"{dep_body}\n"
            f"=== END CITED AUTHORITY: {dep_path} ==="
        )
    cited_str = "\n\n".join(cited_blocks) if cited_blocks else "(no cited authorities — load-bearing step must derive from axiom)"

    runner_stdout = get_runner_stdout(runner_path, runner_timeout_sec)

    # Inline-substitute the {{...}} variables. We only replace the variables
    # actually appearing in the template; the FOREACH block uses cited_str.
    prompt = template
    prompt = prompt.replace("{{CLAIM_ID}}", cid)
    prompt = prompt.replace("{{NOTE_PATH}}", note_path)
    prompt = prompt.replace("{{CLAIM_TYPE_HINT}}", claim_type_hint or "(none)")
    prompt = prompt.replace("{{RUNNER_PATH}}", runner_path or "(none)")
    prompt = prompt.replace("{{NOTE_BODY}}", note_body)
    prompt = prompt.replace("{{RUNNER_STDOUT}}", runner_stdout or "(no stdout captured)")

    # Replace the FOREACH ... ENDFOREACH block with the rendered cited authorities
    foreach_re = re.compile(
        r"\{\{FOREACH cited_authority IN CITED_AUTHORITIES\}\}.*?\{\{ENDFOREACH\}\}",
        re.DOTALL,
    )
    # Use a lambda so cited_str isn't interpreted as a re replacement template
    prompt = foreach_re.sub(lambda _m: cited_str, prompt)

    # Append a tightening footer so we get clean JSON back
    prompt += (
        "\n\n---\n"
        "OUTPUT INSTRUCTIONS (binding):\n"
        "Respond with EXACTLY one JSON object matching the schema in section 5. "
        "No markdown fences, no preamble, no explanation outside the JSON. "
        "If you must signal compute is required (per the COMPUTE_REQUIRED rule), "
        "set verdict to one of the audited_* values that best reflects what you can "
        "actually decide; do not return the literal COMPUTE_REQUIRED string in this "
        "automated mode — instead set chain_closes=false and explain the missing "
        "compute in chain_closure_explanation.\n"
    )
    return prompt


def run_codex(prompt: str, isolated_dir: Path, timeout_sec: int,
              reasoning_effort: str | None = None,
              model: str | None = None) -> tuple[bool, str, str]:
    """Run `codex exec` in an isolated workdir. Returns (ok, stdout, stderr).

    reasoning_effort: low | medium | high | xhigh. Controls Codex internal
    reasoning depth. Lower = cheaper rate-limit cost per call. Default of
    None falls back to ~/.codex/config.toml (typically xhigh).
    """
    isolated_dir.mkdir(parents=True, exist_ok=True)
    cmd = ["codex", "exec", "--skip-git-repo-check"]
    if reasoning_effort:
        cmd += ["-c", f"model_reasoning_effort={reasoning_effort!r}"]
    if model:
        cmd += ["-c", f"model={model!r}"]
    cmd.append(prompt)
    try:
        # --skip-git-repo-check lets us run outside a repo.
        # We deliberately do NOT pass --cd because in our smoke test that
        # combination hung; running from the isolated dir as cwd is enough
        # to keep codex from reading the surrounding repo.
        proc = subprocess.run(
            cmd,
            cwd=isolated_dir,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        if proc.returncode != 0:
            return False, proc.stdout, proc.stderr
        return True, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return False, "", f"[codex timed out at {timeout_sec}s]"
    except FileNotFoundError:
        return False, "", "[codex CLI not on PATH; install or `codex login`]"


# Files that the audit pipeline regenerates and that should be committed
# alongside any verdict-write to keep main internally consistent.
AUDIT_DATA_FILES = [
    "docs/audit/AUDIT_LEDGER.md",
    "docs/audit/AUDIT_QUEUE.md",
    "docs/audit/data",
    "docs/publication/ci3_z3/CLAIMS_TABLE_EFFECTIVE_STATUS.md",
    "docs/publication/ci3_z3/DERIVATION_ATLAS_EFFECTIVE_STATUS.md",
    "docs/publication/ci3_z3/PUBLICATION_MATRIX_EFFECTIVE_STATUS.md",
    "docs/publication/ci3_z3/FULL_CLAIM_LEDGER_EFFECTIVE_STATUS.md",
    "docs/publication/ci3_z3/USABLE_DERIVED_VALUES_INDEX_EFFECTIVE_STATUS.md",
    "docs/publication/ci3_z3/RESULTS_INDEX_EFFECTIVE_STATUS.md",
    "docs/publication/ci3_z3/QUANTITATIVE_SUMMARY_TABLE_EFFECTIVE_STATUS.md",
    "docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP_EFFECTIVE_STATUS.md",
    "docs/publication/ci3_z3/PUBLICATION_AUDIT_DIVERGENCE.md",
]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT, capture_output=True, text=True, check=check,
    )


def assert_main_and_clean() -> str | None:
    """Return None if we're on main with a clean tree; else a reason string."""
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if branch != "main":
        return f"not on main (currently on {branch!r})"
    # Allow audit-data files to be dirty (we'll commit them); fail on
    # other dirty paths.
    porcelain = git("status", "--porcelain").stdout
    other_dirty = []
    for line in porcelain.splitlines():
        path = line[3:]
        if not any(path == f or path.startswith(f + "/") or path.startswith(f) for f in AUDIT_DATA_FILES):
            other_dirty.append(path)
    if other_dirty:
        return f"working tree dirty outside audit-data files: {other_dirty[:5]}"
    return None


def commit_and_push_to_main(message: str, max_attempts: int = 3) -> tuple[bool, str]:
    """Stage audit-data files, commit, push to main with rebase-on-conflict retry."""
    # Stage every audit-data path that exists
    paths = [p for p in AUDIT_DATA_FILES if (REPO_ROOT / p).exists()]
    add = git("add", *paths, check=False)
    if add.returncode != 0:
        return False, f"git add failed: {add.stderr.strip()[:200]}"
    diff = git("diff", "--cached", "--quiet", check=False)
    if diff.returncode == 0:
        return True, "no audit-data changes to commit"
    commit = git("commit", "-m", message, check=False)
    if commit.returncode != 0:
        return False, f"git commit failed: {(commit.stderr or commit.stdout).strip()[:200]}"
    for attempt in range(1, max_attempts + 1):
        push = git("push", "origin", "main", check=False)
        if push.returncode == 0:
            return True, f"pushed (attempt {attempt})"
        # Try fetch + rebase
        git("fetch", "origin", "main", check=False)
        rebase = git("rebase", "origin/main", check=False)
        if rebase.returncode != 0:
            git("rebase", "--abort", check=False)
            return False, f"push attempt {attempt} failed and rebase conflicted: {(push.stderr or push.stdout).strip()[:200]}"
    return False, f"push failed after {max_attempts} attempts"


CODEX_RESPONSE_RE = re.compile(
    r"(?:^|\n)codex\n(.*?)(?:\ntokens used\b|\Z)", re.DOTALL
)


def extract_response(stdout: str) -> str | None:
    """Pull the model's actual reply out of `codex exec` stdout.

    Output format:
      <metadata block>
      --------
      user
      <prompt>
      codex
      <reply>
      tokens used
      <count>

    Falls back to returning the whole stdout so JSON-extract can still try.
    """
    m = CODEX_RESPONSE_RE.search(stdout)
    if m:
        return m.group(1).strip()
    # Fallback: return the whole stdout; parse_verdict_json will regex-find
    # the JSON object inside.
    return stdout if stdout.strip() else None


def parse_verdict_json(reply: str) -> dict | None:
    """Best-effort extract a JSON object from the codex reply.

    Codex output may include a leading metadata block, the prompt echo, a
    "codex" header, the actual reply, and a "tokens used" trailer. The
    audit verdict is always the LAST JSON object in the reply, so we
    search backward from the last `}` and try progressively earlier `{`
    starts until something parses.
    """
    reply = reply.strip()
    # Drop any tokens-used trailer
    if "\ntokens used" in reply:
        reply = reply.split("\ntokens used", 1)[0].rstrip()
    # Try direct parse first
    try:
        return json.loads(reply)
    except json.JSONDecodeError:
        pass
    # Strip markdown fences if present
    if reply.startswith("```"):
        stripped = reply.strip("`").lstrip("json").strip()
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            pass

    # Find the last `}` in the reply and try every `{` start before it
    last_close = reply.rfind("}")
    if last_close == -1:
        return None
    cursor = 0
    while True:
        first_open = reply.find("{", cursor)
        if first_open == -1 or first_open > last_close:
            return None
        candidate = reply[first_open : last_close + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            cursor = first_open + 1


def validate_verdict(blob: dict, expected_cid: str) -> str | None:
    """Return an error string if the verdict is unusable, else None."""
    missing = REQUIRED_VERDICT_FIELDS - set(blob)
    if missing:
        return f"missing fields: {sorted(missing)}"
    if blob.get("claim_id") != expected_cid:
        return f"claim_id mismatch: expected {expected_cid!r}, got {blob.get('claim_id')!r}"
    return None


def apply_one(verdict_blob: dict, propagate: bool) -> tuple[bool, str]:
    """Pipe a verdict blob through apply_audit.py via stdin."""
    cmd = [sys.executable, str(APPLY_AUDIT_SCRIPT)]
    if not propagate:
        cmd.append("--no-propagate")
    proc = subprocess.run(
        cmd,
        input=json.dumps(verdict_blob),
        text=True,
        capture_output=True,
        cwd=REPO_ROOT,
    )
    return proc.returncode == 0, (proc.stdout + proc.stderr).strip()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=5,
                   help="How many top-of-queue rows to audit this run (default 5).")
    p.add_argument("--criticality",
                   choices=["critical", "high", "medium", "leaf"],
                   help="Restrict to one criticality tier.")
    p.add_argument("--dry-run", action="store_true",
                   help="Build prompts but do NOT call codex or apply_audit.")
    p.add_argument("--auditor-name", default=None,
                   help=f"Auditor identity recorded in the ledger. "
                        f"Default: codex-cli-batch-<utc-yyyymmdd-hhmm>")
    p.add_argument("--codex-timeout-sec", type=int, default=600,
                   help="Per-row codex exec timeout (default 600).")
    p.add_argument("--runner-timeout-sec", type=int, default=120,
                   help="Per-row primary-runner timeout (default 120).")
    p.add_argument("--no-propagate", action="store_true",
                   help="Pass --no-propagate to apply_audit; run the pipeline once at end.")
    p.add_argument("--no-runner", action="store_true",
                   help="Skip running each row's primary runner (faster; uses empty stdout).")
    p.add_argument("--push-mode",
                   choices=["per-verdict", "batch", "none"],
                   default="batch",
                   help="When to commit and push audit-data to main: "
                        "'per-verdict' (commit+push after each apply), "
                        "'batch' (one commit covering the whole run; default), "
                        "'none' (no auto-commit; for testing).")
    p.add_argument("--allow-non-main", action="store_true",
                   help="Permit running from a branch other than main. "
                        "Default refuses unless the runner can push to main "
                        "directly. Use only for testing.")
    args = p.parse_args()

    # Reasoning-effort policy: per repo audit-lane decision (2026-05-04),
    # ALL audits run at xhigh. We do not expose a knob to lower it.
    REASONING_EFFORT = "xhigh"

    auditor_name = args.auditor_name or f"codex-cli-batch-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M')}"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    run_id = uuid.uuid4().hex[:8]
    run_log = LOG_DIR / f"run-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{run_id}.jsonl"
    print(f"Run log: {run_log}")
    print(f"Auditor: {auditor_name}  ({AUDITOR_FAMILY}, {AUDITOR_INDEPENDENCE})")

    # Verify branch + cleanliness before any push-capable operation.
    if args.push_mode != "none" and not args.dry_run:
        reason = assert_main_and_clean()
        if reason and not args.allow_non_main:
            print(f"REFUSING to run with --push-mode={args.push_mode}: {reason}")
            print("Either checkout main and clean the worktree, or pass --allow-non-main "
                  "(local-only; verdicts will be applied but NOT pushed to main).")
            return 2
        if reason and args.allow_non_main:
            print(f"WARNING: {reason}; --allow-non-main forces push-mode=none for safety.")
            args.push_mode = "none"
        else:
            # Pull in any remote audit-bot commits before we start.
            git("fetch", "origin", "main", check=False)
            git("rebase", "origin/main", check=False)

    ledger_rows = load_ledger_rows()
    queue = load_queue(args.criticality)
    targets = queue[: args.n]
    if not targets:
        print("Queue empty for this filter; nothing to do.")
        return 0

    print(f"Selected {len(targets)} rows from the queue.")
    print(f"Push mode: {args.push_mode}  Reasoning: {REASONING_EFFORT}")
    print(f"Top of selection:")
    for r in targets[:5]:
        print(f"  - {r['claim_id']}  [{r.get('criticality')}, "
              f"score={r.get('score','?')}, audit_status={r.get('audit_status','?')}]")

    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")

    applied = 0
    failed = 0
    skipped = 0
    for i, row in enumerate(targets, 1):
        cid = row["claim_id"]
        print(f"\n[{i}/{len(targets)}] {cid}")
        try:
            # Honor --no-runner by passing 0 timeout (subprocess.run skips)
            timeout = 0 if args.no_runner else args.runner_timeout_sec
            if args.no_runner:
                # Build the prompt manually with empty runner stdout
                ledger_rows_view = ledger_rows
                full_row = ledger_rows_view.get(cid, {})
                row_for_prompt = {**row, "note_path": full_row.get("note_path"),
                                  "runner_path": full_row.get("runner_path")}
                prompt = render_prompt(row_for_prompt, ledger_rows_view, template, 1)
                # Wipe runner stdout block
                prompt = re.sub(r"### 3\. Runner output.*?### 4\.", "### 4.", prompt, count=1, flags=re.DOTALL)
            else:
                prompt = render_prompt(row, ledger_rows, template, args.runner_timeout_sec)

            if args.dry_run:
                print(f"  [dry-run] prompt size: {len(prompt)} chars")
                with run_log.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({
                        "claim_id": cid, "phase": "dry-run", "prompt_size": len(prompt)
                    }) + "\n")
                continue

            isolated = ISOLATED_BASE / f"{run_id}-{i:03d}"
            t0 = time.time()
            ok, stdout, stderr = run_codex(
                prompt, isolated, args.codex_timeout_sec,
                reasoning_effort=REASONING_EFFORT,
            )
            elapsed = time.time() - t0

            if not ok:
                print(f"  FAIL codex exec: {stderr.strip()[:300]}")
                with run_log.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({
                        "claim_id": cid, "phase": "codex_failed",
                        "elapsed_sec": elapsed, "stderr": stderr[:500]
                    }) + "\n")
                failed += 1
                continue

            reply = extract_response(stdout)
            if not reply:
                print("  FAIL: could not extract codex reply from stdout")
                failed += 1
                with run_log.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({
                        "claim_id": cid, "phase": "extract_failed",
                        "elapsed_sec": elapsed, "stdout_tail": stdout[-2000:]
                    }) + "\n")
                continue

            blob = parse_verdict_json(reply)
            if blob is None:
                print(f"  FAIL: codex reply not valid JSON")
                failed += 1
                with run_log.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({
                        "claim_id": cid, "phase": "json_parse_failed",
                        "reply": reply[:2000]
                    }) + "\n")
                continue

            err = validate_verdict(blob, cid)
            if err:
                print(f"  FAIL validate: {err}")
                failed += 1
                with run_log.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({
                        "claim_id": cid, "phase": "validate_failed",
                        "error": err, "blob": blob
                    }) + "\n")
                continue

            full_blob = add_auditor_metadata(blob, auditor_name)
            ok, msg = apply_one(full_blob, propagate=not args.no_propagate)
            if ok:
                print(f"  OK ({elapsed:.1f}s)  verdict={blob.get('verdict')}  "
                      f"class={blob.get('load_bearing_step_class')}")
                applied += 1
                with run_log.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({
                        "claim_id": cid, "phase": "applied",
                        "elapsed_sec": elapsed,
                        "verdict": blob.get("verdict"),
                        "claim_type": blob.get("claim_type"),
                        "lb_class": blob.get("load_bearing_step_class"),
                    }) + "\n")

                # Per-verdict push mode: commit + push immediately
                if args.push_mode == "per-verdict":
                    msg = (
                        f"audit: {cid} -> {blob.get('verdict')} "
                        f"(codex-cli, xhigh, {auditor_name})"
                    )
                    pushed, push_msg = commit_and_push_to_main(msg)
                    if pushed:
                        print(f"    pushed to main: {push_msg}")
                    else:
                        print(f"    FAIL push: {push_msg}")
                        with run_log.open("a", encoding="utf-8") as f:
                            f.write(json.dumps({
                                "claim_id": cid, "phase": "push_failed",
                                "msg": push_msg
                            }) + "\n")
            else:
                print(f"  FAIL apply_audit: {msg[:300]}")
                failed += 1
                with run_log.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({
                        "claim_id": cid, "phase": "apply_failed",
                        "msg": msg[:500], "blob": full_blob
                    }) + "\n")

        finally:
            iso = ISOLATED_BASE / f"{run_id}-{i:03d}"
            if iso.exists():
                shutil.rmtree(iso, ignore_errors=True)

    # Batch push mode: one commit covering the whole run
    if args.push_mode == "batch" and applied > 0 and not args.dry_run:
        crit = f" {args.criticality}" if args.criticality else ""
        msg = (
            f"audit: codex-cli batch {applied} verdict(s){crit} "
            f"(xhigh, {auditor_name})"
        )
        pushed, push_msg = commit_and_push_to_main(msg)
        if pushed:
            print(f"\nBatch pushed to main: {push_msg}")
        else:
            print(f"\nBatch push FAILED: {push_msg}")
            print("Local state has the verdicts; run `git push origin main` manually after resolving.")

    print(f"\nDone. applied={applied} failed={failed} skipped={skipped}  "
          f"(of {len(targets)} attempted)")
    print(f"Run log: {run_log}")
    if args.no_propagate and applied > 0:
        print("\nNote: --no-propagate was set; run "
              "`bash docs/audit/scripts/run_pipeline.sh` to refresh effective_status.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
