# Handoff

## Block

`teleportation-acceptance-suite-sync`, block 01.

## What Changed

- `docs/TELEPORTATION_ACCEPTANCE_SUITE_NOTE.md` now documents the full current
  `--strict-lane --list-probes` inventory.
- The runner's `--strict-lane` help text now names the later
  blocker-reduction/conclusion-boundary families rather than stopping at the
  microscopic-closure family.
- Cached outputs were added for default list-probes, strict-lane list-probes,
  and required-only execution.
- Mechanical audit metadata was refreshed so the edited source note hash is
  current and the old `audited_failed` row is archived under `previous_audits`;
  the live row is reset to `unaudited` pending independent re-audit.

## Checks

```text
python3 scripts/frontier_teleportation_acceptance_suite.py --list-probes
12 lines
```

```text
python3 scripts/frontier_teleportation_acceptance_suite.py --strict-lane --list-probes
24 lines
```

```text
python3 scripts/frontier_teleportation_acceptance_suite.py --required-only
required: {'PASS': 8}
```

```text
python3 -m py_compile scripts/frontier_teleportation_acceptance_suite.py
OK
```

```text
python3 docs/audit/scripts/audit_lint.py
OK: no errors
```

The lint command still reports pre-existing repo-wide warnings unrelated to
this row.

## Proposed Status

Branch-local author status: `bounded-support` / re-audit-ready harness
documentation. This branch does not propose retained physics closure.

## Next Exact Action

Open a PR against `main` and request independent audit of
`teleportation_acceptance_suite_note`.
