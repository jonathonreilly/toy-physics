### Block43 checkpoint: higher-shell chunks007-008 complete; chunks009-010 launched

Packaged completed higher-shell chunks007-008 and launched the next
non-colliding support wave for chunks009-010.

Artifacts:

- `docs/YT_PR230_SCHUR_HIGHER_SHELL_CHUNKS007_008_COMPLETED_AND_009_010_LAUNCH_CHECKPOINT_NOTE_2026-05-12.md`
- `outputs/yt_pr230_schur_higher_shell_chunk007_checkpoint_2026-05-12.json`
- `outputs/yt_pr230_schur_higher_shell_chunk008_checkpoint_2026-05-12.json`
- `outputs/yt_pr230_schur_higher_shell_rows/yt_pr230_schur_higher_shell_rows_L12_T24_chunk007_2026-05-07.json`
- `outputs/yt_pr230_schur_higher_shell_rows/yt_pr230_schur_higher_shell_rows_L12_T24_chunk008_2026-05-07.json`
- `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/L12_T24_chunk007/L12xT24/ensemble_measurement.json`
- `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/L12_T24_chunk008/L12xT24/ensemble_measurement.json`
- `outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json`

Validation:

- chunk007 checkpoint: `PASS=15 FAIL=0`
- chunk008 checkpoint: `PASS=15 FAIL=0`
- wave launcher status before launch: `PASS=11 FAIL=0`,
  `completed_chunk_indices=[1,2,3,4,5,6,7,8]`,
  `planned_launch_chunk_indices=[9,10]`
- wave launcher launch: `PASS=11 FAIL=0`; launched chunk009 pid `39242`,
  chunk010 pid `39243`
- campaign status after launch: `PASS=403 FAIL=0`

Claim boundary: chunks007-008 are bounded higher-shell support only, and
chunks009-010 are run-control only until completed-mode checkpoints pass.
This block does not supply canonical `O_H`, strict `C_sH/C_HH` pole rows,
Schur A/B/C kernel rows, scalar-LSZ/FV/IR authority, W/Z response,
physical `kappa_s`, retained closure, or `proposed_retained` closure. PR #230
remains draft/open.
