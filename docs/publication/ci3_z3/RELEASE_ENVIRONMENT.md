# Release Environment

This is the pinned execution environment for the current public validation
surface.

## Validated Runtime

- Python `3.13.5`
- `numpy==2.4.4`
- `scipy==1.17.1`

## Install

From the repo root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-release.txt
```

## Scope

This environment pin is for the active public validation path on `main`. The
repo-level [requirements.txt](../../../requirements.txt) remains a looser
developer convenience file; the public package should use the exact pin above.

## Release Rule

- use this environment for public reproduction checks
- record the exact commit under review in the release note, archive note, or
  submission freeze when preparing a formal submission snapshot
