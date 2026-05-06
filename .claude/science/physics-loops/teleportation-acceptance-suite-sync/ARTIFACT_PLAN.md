# Artifact Plan

## Source Note

- Update `docs/TELEPORTATION_ACCEPTANCE_SUITE_NOTE.md` so its strict-lane
  profile mirrors `--strict-lane --list-probes`.
- Add validation snapshot links.

## Runner

- Update the `--strict-lane` help text so it no longer truncates the current
  strict-lane family after microscopic closure checks.

## Outputs

- Add default and strict list-probe snapshots.
- Add a required-only run snapshot showing `required: {'PASS': 8}`.

## Audit Metadata

- Refresh mechanical audit data so the edited note hash is current and the old
  failed verdict is archived for independent re-audit.
