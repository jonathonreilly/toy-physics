## Block40 checkpoint: higher-shell chunks003-004 completed

Completed and checkpointed the remaining live higher-shell workers from the
previous wave:

- chunk003: seed `2026057003`, `created_utc=2026-05-12T06:29:14Z`,
  `runtime_seconds=7693.425`
- chunk004: seed `2026057004`, `created_utc=2026-05-12T06:29:28Z`,
  `runtime_seconds=7707.404`

What landed:

- row JSONs for chunks003-004 under
  `outputs/yt_pr230_schur_higher_shell_rows/`
- volume artifacts under
  `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/`
- completed chunk checkpoints:
  `outputs/yt_pr230_schur_higher_shell_chunk003_checkpoint_2026-05-12.json`
  and
  `outputs/yt_pr230_schur_higher_shell_chunk004_checkpoint_2026-05-12.json`
- note:
  `docs/YT_PR230_SCHUR_HIGHER_SHELL_CHUNKS003_004_COMPLETED_CHECKPOINT_NOTE_2026-05-12.md`
- campaign status runner updated from active-pending chunks003-004 to
  completed chunks003-004 support checks.

Validation:

- `python3 -m py_compile ...` passed for the higher-shell checkpoint,
  wave-launcher, and campaign status runners.
- chunk003 completed checkpoint: `PASS=15 FAIL=0`
- chunk004 completed checkpoint: `PASS=15 FAIL=0`
- wave launcher status: `PASS=11 FAIL=0`; no active higher-shell workers
- campaign status: `PASS=396 FAIL=0`
- assumption/import stress: `PASS=105 FAIL=0`
- full positive closure assembly: `PASS=187 FAIL=0`
- retained-route certificate: `PASS=319 FAIL=0`
- positive-closure completion audit: `PASS=73 FAIL=0`
- audit pipeline and strict audit lint: passed, with the five existing warnings

Claim boundary:

This is bounded support only.  The rows remain same-source `C_ss` plus
taste-radial `C_sx/C_xx` support under the unratified second-source
certificate.  They are not Schur A/B/C kernel rows, not strict scalar-LSZ
moment/FV/IR authority, not canonical `O_H`, not strict canonical
`C_sH/C_HH` pole rows, not W/Z response, not physical `kappa_s`, and not
retained or `proposed_retained` top-Yukawa closure.  PR #230 remains draft/open.
