# Artifact Plan

- Add/freshen `logs/runner-cache/lattice_nn_deterministic_rescale.txt`.
- Update `docs/LATTICE_NN_DETERMINISTIC_RESCALE_NOTE.md` with relative runner
  links, cache metadata, source-to-schedule proof sketch, and cache-aligned
  rows.
- Register `scripts/lattice_nn_deterministic_rescale.py` as the audit ledger
  runner for `lattice_nn_deterministic_rescale_note`.
- Update the narrow canonical regression gate to accept machine-epsilon Born
  values for the h = 0.0625 row.
