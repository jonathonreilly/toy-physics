# Neutrino Two-Amplitude Last-Mile Reduction

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-16  
**Script:** `scripts/frontier_neutrino_two_amplitude_last_mile.py`

## Question

After all current PMNS and Majorana reductions, what exact data are still
missing for full retained neutrino sole-axiom closure?

## Answer

Only two amplitudes remain:

- one complex PMNS amplitude `J_chi`
- one real Majorana amplitude `mu`

Here:

- `J_chi` is the native nontrivial `C3` character current on the retained
  `hw=1` PMNS response family
- `mu` is the rephasing-reduced charge-`2` source amplitude in the canonical
  doubled-`nu_R` normal form `mu J_2`

## Exact Content

The branch now proves:

1. the PMNS last mile is exactly one complex current `J_chi`
2. the current sole-axiom retained PMNS routes set `J_chi = 0`
3. the Majorana last mile is exactly one real amplitude `mu`
4. the current sole-axiom retained Majorana routes set `mu = 0`

So the full retained-neutrino last mile is not a diffuse matrix problem
anymore. It is exactly the pair

`(J_chi, mu)`.

## Consequence

This is the sharpest current endpoint on the science branch.

Full retained sole-axiom neutrino closure would now require:

- a sole-axiom law producing nonzero `J_chi`, and
- a sole-axiom law producing nonzero `mu`

If those two laws were derived, the rest of the closure stack is already in
place.

## Verification

```bash
python3 scripts/frontier_neutrino_two_amplitude_last_mile.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [pmns_c3_nontrivial_current_boundary_note](PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md)
- [pmns_sole_axiom_hw1_source_transfer_boundary_note](PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md)
- [pmns_uniform_scalar_deformation_boundary_note](PMNS_UNIFORM_SCALAR_DEFORMATION_BOUNDARY_NOTE.md)
- [neutrino_majorana_nur_character_boundary_note](NEUTRINO_MAJORANA_NUR_CHARACTER_BOUNDARY_NOTE.md)
- [neutrino_majorana_nur_charge2_primitive_reduction_note](NEUTRINO_MAJORANA_NUR_CHARGE2_PRIMITIVE_REDUCTION_NOTE.md)
