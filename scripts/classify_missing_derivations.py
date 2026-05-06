#!/usr/bin/env python3
"""One-shot difficulty classifier for the missing-derivation backlog.

Reads `docs/audit/MISSING_DERIVATION_PROMPTS.md` and asks Codex GPT-5.5
(at xhigh) to RATE each prompt as `easy` / `medium` / `hard` without
attempting the derivation. Persists the ratings to:

    docs/audit/data/missing_derivation_difficulty.json

The science-fix loop reads that file and prioritizes easy → medium →
hard, skipping hard by default. This means we get fast wins from the
easy bucket before burning 15-30 min budgets on rows that are
genuinely too hard for an autonomous AI loop.

Definitions
-----------
  easy    Mostly a notation / proof writeup of an algebraic identity
          already implied by cited authorities. Expect a small (~30
          LOC) change to the source note. Should close in <5 min of
          code-writing.
  medium  Requires modest new reasoning or small runner change.
          Tractable for an AI in <15 min.
  hard    Requires substantive new physics, a new theorem, deep
          symbolic computation, or a known-open subproblem. Likely
          beyond an autonomous AI loop; reserve for human review.

Usage
-----
    # Classify every prompt that doesn't already have a rating
    python3 scripts/classify_missing_derivations.py

    # Re-classify all (force overwrite)
    python3 scripts/classify_missing_derivations.py --force

    # Restrict to one category
    python3 scripts/classify_missing_derivations.py --category renaming

    # Dry-run: list rows that would be classified
    python3 scripts/classify_missing_derivations.py --dry-run

    # Higher concurrency (default 4)
    python3 scripts/classify_missing_derivations.py --concurrency 8

State file (`docs/audit/data/missing_derivation_difficulty.json`):

    {
      "ratings": {
        "<claim_id>": {
          "difficulty": "easy" | "medium" | "hard",
          "reason": "<one-sentence>",
          "category": "renaming" | "failed" | ...,
          "descendants": <int>,
          "elapsed_sec": <float>,
          "raw_tail": "<last 500 chars of classifier output>"
        }
      }
    }

No timestamps in the file (gate-clean). The file is committed to
`docs/audit/data/` so all workers share the same view.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Reuse parsing logic from the loop module
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import science_fix_loop as sfl  # noqa: E402

REPO_ROOT = sfl.REPO_ROOT
PROMPTS_FILE = sfl.PROMPTS_FILE
DIFFICULTY_FILE = REPO_ROOT / "docs" / "audit" / "data" / "missing_derivation_difficulty.json"
ISOLATED_BASE = Path("/tmp") / "science-fix-classify"

DEFAULT_MODEL = sfl.DEFAULT_MODEL
DEFAULT_REASONING = sfl.DEFAULT_REASONING
PER_ROW_TIMEOUT_SEC = 300         # 5 min hard cap per classification
PER_ROW_STALE_SEC = 90            # 90s of total silence = stuck

VALID_DIFFICULTIES = {"easy", "medium", "hard"}
DIFFICULTY_LINE_RE = re.compile(
    r"^\s*DIFFICULTY:\s*(easy|medium|hard)\s*$",
    re.IGNORECASE | re.MULTILINE,
)
REASON_LINE_RE = re.compile(
    r"^\s*REASON:\s*(.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


CLASSIFY_PROMPT = """CLASSIFY ONLY. Do NOT attempt the derivation. Do NOT edit any
files. Read the prompt block below and judge how hard the missing
derivation would be for an autonomous AI loop to close.

Output exactly two lines and nothing else:

    DIFFICULTY: <easy | medium | hard>
    REASON: <one short sentence>

Definitions:

  easy    Mostly a notation / proof writeup of an algebraic identity
          already implied by the cited authorities. Expect a small
          (~30 LOC) change. Should close in <5 min of code-writing.
  medium  Requires modest new reasoning or small runner change.
          Tractable for an AI in <15 min.
  hard    Requires substantive new physics, a new theorem, deep
          symbolic computation, or a known-open subproblem. Beyond
          autonomous-AI scope; reserve for human review.

The auditor's verdict_rationale embedded in the prompt below is the
strongest signal for difficulty — read it carefully. Indicators of
HARD: the rationale says no-go obstructions block, the chain requires
new physics, the runner is hard-coding a contested premise, the
load-bearing step demands a new theorem.

============================== PROMPT ==============================
"""


def load_difficulty() -> dict:
    if not DIFFICULTY_FILE.exists():
        return {"ratings": {}}
    try:
        return json.loads(DIFFICULTY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"ratings": {}}


def save_difficulty(state: dict) -> None:
    DIFFICULTY_FILE.parent.mkdir(parents=True, exist_ok=True)
    DIFFICULTY_FILE.write_text(
        json.dumps(state, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _terminate_tree(proc: subprocess.Popen, sig: int) -> None:
    try:
        os.killpg(proc.pid, sig)
    except ProcessLookupError:
        pass
    except Exception:
        try:
            proc.send_signal(sig)
        except Exception:
            pass


def classify_one(row: dict, model: str, reasoning: str,
                 isolated_dir: Path,
                 timeout_sec: int = PER_ROW_TIMEOUT_SEC,
                 stale_after_sec: int = PER_ROW_STALE_SEC) -> dict:
    """Run codex once on a classification-only prompt. Returns:
        {claim_id, difficulty, reason, elapsed_sec, raw_tail}
    Difficulty is "unknown" if the response can't be parsed.
    """
    cid = row["claim_id"]
    isolated_dir.mkdir(parents=True, exist_ok=True)
    full_prompt = CLASSIFY_PROMPT + row["prompt_body"]
    cmd = [
        "codex", "exec",
        "-C", str(isolated_dir),
        "--skip-git-repo-check",
        "-s", "read-only",
        "-m", model,
        "-c", f'model_reasoning_effort="{reasoning}"',
        full_prompt,
    ]
    t0 = time.time()
    try:
        stop_reason = "ok"
        last_stream_bytes = 0
        last_progress_time = t0
        with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as stdout_fh, \
             tempfile.TemporaryFile(mode="w+", encoding="utf-8") as stderr_fh:
            proc = subprocess.Popen(
                cmd,
                stdout=stdout_fh,
                stderr=stderr_fh,
                text=True,
                env=os.environ,
                start_new_session=True,
            )
            while True:
                try:
                    proc.wait(timeout=5)
                    break
                except subprocess.TimeoutExpired:
                    pass

                now = time.time()
                elapsed = now - t0
                try:
                    cur_stream_bytes = (
                        os.fstat(stdout_fh.fileno()).st_size
                        + os.fstat(stderr_fh.fileno()).st_size
                    )
                except Exception:
                    cur_stream_bytes = last_stream_bytes
                if cur_stream_bytes > last_stream_bytes:
                    last_progress_time = now
                    last_stream_bytes = cur_stream_bytes

                if stale_after_sec > 0 and now - last_progress_time >= stale_after_sec:
                    stop_reason = "stalled"
                    break
                if elapsed >= timeout_sec:
                    stop_reason = "timeout"
                    break

            if stop_reason != "ok":
                _terminate_tree(proc, signal.SIGTERM)
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    _terminate_tree(proc, signal.SIGKILL)
                    proc.wait(timeout=5)

            elapsed = time.time() - t0
            stdout_fh.seek(0)
            stderr_fh.seek(0)
            stdout = stdout_fh.read()
            stderr = stderr_fh.read()

        out = (stdout or "") + ("\n" + stderr if stderr else "")
        d_match = DIFFICULTY_LINE_RE.search(out)
        r_match = REASON_LINE_RE.search(out)
        difficulty = (d_match.group(1).lower() if d_match else "unknown")
        if r_match:
            reason = r_match.group(1).strip()
        elif stop_reason == "stalled":
            reason = f"(classifier had no output for {stale_after_sec}s)"
        elif stop_reason == "timeout":
            reason = f"(classifier timed out at {timeout_sec}s)"
        elif proc.returncode not in (0, None):
            reason = f"(classifier exited rc={proc.returncode})"
        else:
            reason = "(no reason parsed)"
        return {
            "claim_id": cid,
            "difficulty": difficulty if difficulty in VALID_DIFFICULTIES else "unknown",
            "reason": reason,
            "category": row["category"],
            "descendants": row["descendants"],
            "elapsed_sec": round(elapsed, 1),
            "raw_tail": out[-500:],
        }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        return {
            "claim_id": cid,
            "difficulty": "unknown",
            "reason": f"(classifier timed out at {timeout_sec}s)",
            "category": row["category"],
            "descendants": row["descendants"],
            "elapsed_sec": round(elapsed, 1),
            "raw_tail": "",
        }
    except Exception as e:
        elapsed = time.time() - t0
        return {
            "claim_id": cid,
            "difficulty": "unknown",
            "reason": f"(classifier error: {e!r})",
            "category": row["category"],
            "descendants": row["descendants"],
            "elapsed_sec": round(elapsed, 1),
            "raw_tail": "",
        }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=0,
                   help="Cap the number of rows to classify this run "
                        "(default: all unclassified)")
    p.add_argument("--category",
                   choices=sfl.CATEGORIES, default=None,
                   help="Restrict to one category")
    p.add_argument("--claim-id", default=None,
                   help="Classify only this claim_id")
    p.add_argument("--force", action="store_true",
                   help="Re-classify rows even if they already have a rating")
    p.add_argument("--concurrency", type=int, default=4,
                   help="Parallel codex calls (default 4)")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--reasoning", default=DEFAULT_REASONING)
    p.add_argument("--timeout-sec", type=int, default=PER_ROW_TIMEOUT_SEC)
    p.add_argument("--stale-after-sec", type=int, default=PER_ROW_STALE_SEC,
                   help="Classify as unknown and stop a row if codex emits "
                        "no stdout/stderr for this many seconds "
                        f"(default {PER_ROW_STALE_SEC}s; set 0 to disable)")
    p.add_argument("--dry-run", action="store_true",
                   help="List rows that would be classified, no codex calls")
    args = p.parse_args()
    if args.n < 0:
        p.error("--n must be non-negative")
    if args.concurrency <= 0:
        p.error("--concurrency must be positive")
    if args.timeout_sec <= 0:
        p.error("--timeout-sec must be positive")
    if args.stale_after_sec < 0:
        p.error("--stale-after-sec must be non-negative")

    rows = sfl.parse_prompts()
    if not rows:
        print(f"No prompts found in {PROMPTS_FILE}")
        return 1

    state = load_difficulty()
    ratings = state.setdefault("ratings", {})

    # Filter targets
    targets = rows
    if args.category:
        targets = [r for r in targets if r["category"] == args.category]
    if args.claim_id:
        targets = [r for r in targets if r["claim_id"] == args.claim_id]
    if not args.force:
        targets = [r for r in targets if r["claim_id"] not in ratings]
    if args.n > 0:
        targets = targets[: args.n]

    print(f"Total prompts: {len(rows)}; already rated: {len(ratings)}; to classify: {len(targets)}")
    if not targets:
        print("Nothing to do.")
        return 0

    if args.dry_run:
        print("\n[dry-run] Would classify:")
        for r in targets[:30]:
            print(f"  [{r['category']:<15s}] desc={r['descendants']:4d}  {r['claim_id']}")
        if len(targets) > 30:
            print(f"  ... and {len(targets) - 30} more")
        return 0

    run_id = uuid.uuid4().hex[:8]
    base_dir = ISOLATED_BASE / run_id
    base_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nClassifying {len(targets)} rows with concurrency={args.concurrency}...")
    counts = {"easy": 0, "medium": 0, "hard": 0, "unknown": 0}
    completed = 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futures = {}
        for i, r in enumerate(targets):
            iso = base_dir / f"row-{i:04d}"
            futures[ex.submit(
                classify_one, r, args.model, args.reasoning,
                iso, args.timeout_sec, args.stale_after_sec
            )] = r
        for fut in as_completed(futures):
            r = futures[fut]
            try:
                rating = fut.result()
            except Exception as e:
                rating = {
                    "claim_id": r["claim_id"],
                    "difficulty": "unknown",
                    "reason": f"(orchestrator error: {e!r})",
                    "category": r["category"],
                    "descendants": r["descendants"],
                    "elapsed_sec": 0.0,
                    "raw_tail": "",
                }
            cid = rating["claim_id"]
            difficulty = rating["difficulty"]
            counts[difficulty] = counts.get(difficulty, 0) + 1
            completed += 1
            print(f"  [{completed:3d}/{len(targets)}] "
                  f"{difficulty.upper():<7s} {rating['elapsed_sec']:5.1f}s  "
                  f"{cid[:60]}  — {rating['reason'][:70]}")
            ratings[cid] = rating
            # Persist after each result to survive interruption.
            state["ratings"] = ratings
            save_difficulty(state)

    total_elapsed = time.time() - t0
    print(f"\nDone in {total_elapsed:.1f}s.")
    for k in ("easy", "medium", "hard", "unknown"):
        print(f"  {k:8s} {counts.get(k, 0)}")
    print(f"\nDifficulty file: {DIFFICULTY_FILE.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
