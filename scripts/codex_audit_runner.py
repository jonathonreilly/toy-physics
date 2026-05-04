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
# AUDITOR_FAMILY is fixed: this runner always invokes Codex GPT-5.5.
# Independence is determined PER ROW (see determine_audit_role) because it
# depends on whether this is a first-pass (typically cross_family vs Claude
# autopilot authors) or a same-family second-pass (must be fresh_context).
AUDITOR_FAMILY = "codex-gpt-5.5"

# Statuses where this runner SHOULD NOT proceed automatically. Disagreements
# and three-way disagreements need a judicial third-auditor pass that the
# operator runs manually (per docs/audit/FRESH_LOOK_REQUIREMENTS.md and
# apply_audit.py's apply_judicial_review path).
SKIP_BLOCKERS = {
    "cross_confirmation_disagreement",
    "third_auditor_disagreement",
    "judicial_review_irresolvable",
}

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
# independence/audit_date. Independence is determined per-row by the role.
def add_auditor_metadata(verdict_blob: dict, auditor_name: str,
                         independence: str) -> dict:
    blob = dict(verdict_blob)
    blob.setdefault("auditor", auditor_name)
    blob.setdefault("auditor_family", AUDITOR_FAMILY)
    blob.setdefault("independence", independence)
    blob.setdefault("audit_date", datetime.now(timezone.utc).isoformat())
    # Some downstream callers want runner_check_breakdown even when missing.
    blob.setdefault("runner_check_breakdown", {"A": 0, "B": 0, "C": 0, "D": 0, "total_pass": 0})
    return blob


def determine_audit_role(led_row: dict) -> tuple[str, str | None]:
    """Decide what role this audit attempt plays for the given row.

    The runner only audits rows that genuinely need an audit. Re-auditing
    already-clean / already-conditional / already-failed / already-confirmed
    rows is a waste of subscription messages and produces churn — all
    existing audits in this repo were already done at xhigh, so re-doing
    them adds no quality. We skip them.

    Returns (role, reason_or_independence):
      - ("skip", "<reason>")              row should be skipped
      - ("first", "cross_family")         row is unaudited; Codex on a
                                          Claude/human-authored note is
                                          cross-family
      - ("second", "fresh_context")       row is awaiting cross-confirmation
                                          and the first auditor was Codex
                                          (same model family)
      - ("second", "cross_family")        row is awaiting cross-confirmation
                                          and the first auditor was a
                                          different family (Claude / human)

    apply_audit.py validates the independence rule; we precompute here so
    the metadata is always correct on the first try.
    """
    audit_status = led_row.get("audit_status") or "unknown"
    blocker = led_row.get("blocker") or ""
    cc = led_row.get("cross_confirmation") or {}
    if not isinstance(cc, dict):
        cc = {}
    cc_status = cc.get("status")

    # Skip rows that need judicial / human resolution.
    if blocker in SKIP_BLOCKERS:
        return "skip", f"blocker={blocker} (judicial review needed; manual)"
    if cc_status in {"disagreement", "three_way_disagreement", "disagreement_irresolvable"}:
        return "skip", f"cross_confirmation.status={cc_status} (judicial review needed; manual)"

    # First-pass: row has never been audited.
    if audit_status == "unaudited":
        return "first", "cross_family"

    # Second-pass on a critical-row first audit that is awaiting cross-confirmation.
    if audit_status == "audit_in_progress" and cc_status == "awaiting_second":
        first_audit = cc.get("first_audit") or {}
        first_family = first_audit.get("auditor_family") if isinstance(first_audit, dict) else None
        if first_family == AUDITOR_FAMILY:
            return "second", "fresh_context"
        return "second", "cross_family"

    # Anything else — already at a terminal verdict (audited_clean,
    # audited_conditional, audited_failed, audited_renaming,
    # audited_decoration, audited_numerical_match), or already in a
    # confirmed cross_confirmation state, or in some other in-progress
    # state we don't auto-handle — SKIP. Re-auditing settled rows wastes
    # subscription messages without adding quality (existing audits were
    # already done at xhigh).
    cc_note = f" cc.status={cc_status}" if cc_status else ""
    return "skip", f"already at audit_status={audit_status}{cc_note}; not re-auditing"


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


# Per-runner timeout overrides for known-heavy compute lanes. Anything not
# matched falls through to --runner-timeout-sec (default 120s). Patterns are
# substring matches against the runner basename. Long timeouts here trade
# wall-clock for verdict completeness on lanes that genuinely need it.
RUNNER_TIMEOUT_OVERRIDES: list[tuple[str, int]] = [
    ("frontier_alpha_s", 900),
    ("frontier_confinement", 900),
    ("frontier_gauge_vacuum_plaquette_perron", 900),
    ("frontier_gauge_vacuum_plaquette_reduction", 900),
    ("frontier_gauge_vacuum_plaquette_spectral", 900),
    ("frontier_gauge_vacuum_plaquette_susceptibility", 900),
    ("frontier_yt_uv_to_ir", 900),
    ("frontier_yt_p1_delta_r_master", 900),
    ("frontier_higgs_mass_full", 900),
    ("frontier_dm_neutrino_source_surface", 600),
    ("frontier_ckm_atlas", 600),
    ("frontier_self_consistent_field", 600),
    ("frontier_emergent_lorentz", 600),
]


def runner_timeout_for(runner_path: str, default_sec: int) -> int:
    """Return the timeout to use for a given runner."""
    bn = Path(runner_path).name
    for needle, override in RUNNER_TIMEOUT_OVERRIDES:
        if needle in bn:
            return override
    return default_sec


def find_cached_runner_output(runner_path: str) -> str | None:
    """Look for a recent log file from this runner. Returns its tail content
    if found, else None. Most runners in this repo emit logs/<name>-*.txt.
    """
    if not runner_path:
        return None
    bn = Path(runner_path).stem  # strip .py
    logs_dir = REPO_ROOT / "logs"
    if not logs_dir.is_dir():
        return None
    # Look for any file whose name contains the runner stem
    candidates = []
    try:
        for p in logs_dir.iterdir():
            if not p.is_file():
                continue
            if bn in p.name:
                candidates.append(p)
    except OSError:
        return None
    if not candidates:
        return None
    # Most recent by mtime
    latest = max(candidates, key=lambda p: p.stat().st_mtime)
    age_sec = time.time() - latest.stat().st_mtime
    try:
        body = latest.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    header = f"[cached runner output from {latest.name} (age {int(age_sec)}s)]\n"
    return header + body[-6000:]


def get_runner_stdout(runner_path: str | None, default_timeout_sec: int,
                      use_cache: bool = True) -> str:
    """Get runner output. Tries logs/<name>* cache first if use_cache=True;
    falls back to running the runner with a per-runner timeout (override
    map for known-heavy lanes; --runner-timeout-sec for everything else).
    """
    if not runner_path:
        return ""
    if use_cache:
        cached = find_cached_runner_output(runner_path)
        if cached:
            return cached
    p = REPO_ROOT / runner_path
    if not p.exists():
        return f"[runner missing on disk: {runner_path}]"
    timeout_sec = runner_timeout_for(runner_path, default_timeout_sec)
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
        return f"[runner timed out at {timeout_sec}s — likely needs compute-rerun]"
    except Exception as e:
        return f"[runner error: {e}]"


def render_prompt(row: dict, ledger_rows: dict[str, dict],
                  template: str, runner_timeout_sec: int,
                  use_cache: bool = True) -> str:
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

    runner_stdout = get_runner_stdout(runner_path, runner_timeout_sec, use_cache=use_cache)

    # Read the runner source code so the auditor can inspect what the runner
    # actually does, not just what it printed. Catches fake-pass runners
    # (hard-coded PASS lines, trivial assertions) and lets the auditor
    # validate class C/A/B/D against the actual code rather than trusting
    # the static heuristic in classify_runner_passes.py.
    runner_source = ""
    if runner_path:
        rp = REPO_ROOT / runner_path
        if rp.exists():
            try:
                src = rp.read_text(encoding="utf-8", errors="replace")
                MAX = 30_000
                if len(src) > MAX:
                    head = src[: MAX // 2]
                    tail = src[-MAX // 2 :]
                    runner_source = (
                        f"{head}\n\n"
                        f"... [truncated; runner is {len(src)} chars total] ...\n\n"
                        f"{tail}"
                    )
                else:
                    runner_source = src
            except OSError as e:
                runner_source = f"[could not read runner: {e}]"
        else:
            runner_source = f"[runner missing on disk: {runner_path}]"

    # Inline-substitute the {{...}} variables. We only replace the variables
    # actually appearing in the template; the FOREACH block uses cited_str.
    prompt = template
    prompt = prompt.replace("{{CLAIM_ID}}", cid)
    prompt = prompt.replace("{{NOTE_PATH}}", note_path)
    prompt = prompt.replace("{{CLAIM_TYPE_HINT}}", claim_type_hint or "(none)")
    prompt = prompt.replace("{{RUNNER_PATH}}", runner_path or "(none)")
    prompt = prompt.replace("{{NOTE_BODY}}", note_body)
    prompt = prompt.replace("{{RUNNER_STDOUT}}", runner_stdout or "(no stdout captured)")
    prompt = prompt.replace("{{RUNNER_SOURCE}}", runner_source or "(no source available)")

    # Replace the FOREACH ... ENDFOREACH block with the rendered cited authorities
    foreach_re = re.compile(
        r"\{\{FOREACH cited_authority IN CITED_AUTHORITIES\}\}.*?\{\{ENDFOREACH\}\}",
        re.DOTALL,
    )
    # Use a lambda so cited_str isn't interpreted as a re replacement template
    prompt = foreach_re.sub(lambda _m: cited_str, prompt)

    # Append a tightening footer so we get clean JSON back. We DELIBERATELY
    # do not suppress the COMPUTE_REQUIRED escape — the audit-lane policy
    # in AUDIT_AGENT_PROMPT_TEMPLATE.md says runner timeouts / missing
    # compute must NOT be converted to terminal verdicts. If codex returns
    # COMPUTE_REQUIRED, the wrapper detects it and skips the row (no
    # apply, no commit, logged for compute-rerun follow-up).
    prompt += (
        "\n\n---\n"
        "OUTPUT INSTRUCTIONS (binding):\n"
        "If the runner output is missing only because of timeout, missing\n"
        "stdout, or compute-budget exhaustion AND the load-bearing step\n"
        "cannot be judged without that completed run, return EXACTLY one\n"
        "line of the form:\n"
        "    COMPUTE_REQUIRED: <one sentence naming the missing run / cached\n"
        "    certificate / independent derivation needed>\n"
        "and nothing else. Do NOT fabricate a terminal verdict in that case.\n"
        "\n"
        "Otherwise, respond with EXACTLY one JSON object matching the schema\n"
        "in section 5. No markdown fences, no preamble, no explanation\n"
        "outside the JSON.\n"
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
    p.add_argument("--no-cache-runner", action="store_true",
                   help="Don't use logs/<runner-name>*.txt cache; always re-run "
                        "the runner. Slower but freshest output.")
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

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    run_id = uuid.uuid4().hex[:8]
    auditor_name_base = args.auditor_name or f"codex-cli-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{run_id}"
    run_log = LOG_DIR / f"run-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{run_id}.jsonl"
    print(f"Run log: {run_log}")
    print(f"Auditor (base): {auditor_name_base}  ({AUDITOR_FAMILY})")
    print("Per-row independence is determined from each row's existing cross_confirmation:")
    print("  first-pass with no prior audit                    -> cross_family")
    print("  second-pass after a prior audit by a different family -> cross_family")
    print("  second-pass after a prior audit by Codex            -> fresh_context")
    print("  rows in disagreement / awaiting-judicial-review     -> skipped (manual)")

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
            # Determine first-pass vs second-pass vs skip BEFORE invoking codex.
            # This avoids burning a codex call on a row apply_audit will reject,
            # and ensures the verdict's independence matches the row's history.
            full_led_row = ledger_rows.get(cid, {})
            role, role_info = determine_audit_role(full_led_row)
            if role == "skip":
                print(f"  SKIP: {role_info}")
                skipped += 1
                with run_log.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({
                        "claim_id": cid, "phase": "skip_role",
                        "reason": role_info,
                    }) + "\n")
                continue
            row_independence = role_info  # cross_family or fresh_context
            # Per-row auditor identity to guarantee uniqueness across passes.
            row_auditor = f"{auditor_name_base}-{cid[:24]}-{i:03d}"
            print(f"  role={role}  independence={row_independence}")

            use_cache = not args.no_cache_runner
            if args.no_runner:
                # Build the prompt manually with empty runner stdout
                ledger_rows_view = ledger_rows
                full_row = ledger_rows_view.get(cid, {})
                row_for_prompt = {**row, "note_path": full_row.get("note_path"),
                                  "runner_path": full_row.get("runner_path")}
                prompt = render_prompt(row_for_prompt, ledger_rows_view, template, 1,
                                       use_cache=False)
                # Wipe runner stdout block
                prompt = re.sub(r"### 3\. Runner output.*?### 4\.", "### 4.", prompt, count=1, flags=re.DOTALL)
            else:
                prompt = render_prompt(row, ledger_rows, template, args.runner_timeout_sec,
                                       use_cache=use_cache)

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

            # COMPUTE_REQUIRED escape per AUDIT_AGENT_PROMPT_TEMPLATE.md:
            # if codex says the load-bearing step needs a missing run, do
            # NOT apply a verdict. Skip the row and log it for compute-rerun.
            cr_match = re.search(r"COMPUTE_REQUIRED:\s*(.+?)(?:\n|$)", reply, re.IGNORECASE)
            if cr_match:
                reason = cr_match.group(1).strip()[:300]
                print(f"  COMPUTE_REQUIRED: {reason[:200]}")
                skipped += 1
                with run_log.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({
                        "claim_id": cid, "phase": "compute_required",
                        "elapsed_sec": elapsed, "reason": reason,
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

            full_blob = add_auditor_metadata(blob, row_auditor, row_independence)
            ok, msg = apply_one(full_blob, propagate=not args.no_propagate)
            if ok:
                print(f"  OK ({elapsed:.1f}s)  verdict={blob.get('verdict')}  "
                      f"class={blob.get('load_bearing_step_class')}  "
                      f"role={role}/{row_independence}")
                applied += 1
                with run_log.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({
                        "claim_id": cid, "phase": "applied",
                        "elapsed_sec": elapsed,
                        "verdict": blob.get("verdict"),
                        "claim_type": blob.get("claim_type"),
                        "lb_class": blob.get("load_bearing_step_class"),
                        "role": role,
                        "independence": row_independence,
                    }) + "\n")

                # Per-verdict push mode: commit + push immediately
                if args.push_mode == "per-verdict":
                    msg = (
                        f"audit: {cid} -> {blob.get('verdict')} "
                        f"(codex-cli, xhigh, {role}/{row_independence})"
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
            f"(xhigh, {auditor_name_base})"
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
