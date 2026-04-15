# Quantitative Summary Table

**Date:** 2026-04-14  
**Purpose:** reviewer-facing summary of the main prediction/observation rows in
the current package.

This table is broader than the retained theorem core. It includes retained and
bounded rows that a reviewer is likely to ask about.

Use with:

- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)
- [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)

| Quantity / lane | Predicted / framework result | Observed / comparator | Error / comparison | Status | Import class | Paper disposition | Primary authority | Primary runner |
|---|---|---|---|---|---|---|---|---|
| Electroweak scale `v` | `245.080424447914 GeV` | `246.22 GeV` | `-0.4628%` | retained | zero electroweak input | retained core | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) | [frontier_hierarchy_observable_principle_from_axiom.py](../../../scripts/frontier_hierarchy_observable_principle_from_axiom.py) |
| Dark matter ratio `R` | `5.48` | `5.47` | near-match | bounded | one-parameter + imported perturbative pieces | arXiv bounded companion | [DM_RELIC_PAPER_NOTE.md](../../DM_RELIC_PAPER_NOTE.md) | [frontier_dm_relic_paper.py](../../../scripts/frontier_dm_relic_paper.py) |
| `\Omega_\Lambda` conditional chain | `0.686` | `0.685` | near-match | bounded/conditional | observed `\eta` + flatness + bounded `R` | arXiv bounded companion | [OMEGA_LAMBDA_DERIVATION_NOTE.md](../../OMEGA_LAMBDA_DERIVATION_NOTE.md) | [frontier_omega_lambda_derivation.py](../../../scripts/frontier_omega_lambda_derivation.py) |
| `\alpha_s(M_Z)` zero-import route | `0.1181` | `0.1179` | `+0.2%` | bounded | zero-input chain, still bounded by review | review-only until closure | [YT_ZERO_IMPORT_CLOSURE_NOTE.md](../../YT_ZERO_IMPORT_CLOSURE_NOTE.md), [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md), [YT_VERTEX_POWER_DERIVATION.md](../../YT_VERTEX_POWER_DERIVATION.md) | [frontier_alpha_s_determination.py](../../../scripts/frontier_alpha_s_determination.py), [frontier_yt_2loop_chain.py](../../../scripts/frontier_yt_2loop_chain.py) |
| top mass `m_t` zero-import route | `169.4 GeV` | `172.69 GeV` | `-1.9%` | bounded | zero-input 2-loop chain, still bounded | review-only until closure | [YT_ZERO_IMPORT_CLOSURE_NOTE.md](../../YT_ZERO_IMPORT_CLOSURE_NOTE.md), [YT_BOUNDARY_THEOREM.md](../../YT_BOUNDARY_THEOREM.md), [YT_EFT_BRIDGE_THEOREM.md](../../YT_EFT_BRIDGE_THEOREM.md) | [frontier_yt_2loop_chain.py](../../../scripts/frontier_yt_2loop_chain.py), [frontier_yt_boundary_consistency.py](../../../scripts/frontier_yt_boundary_consistency.py), [frontier_yt_eft_bridge.py](../../../scripts/frontier_yt_eft_bridge.py) |
| top mass `m_t` import-allowed route | `171.0 GeV` | `173.0 +/- 0.6 GeV` | about `-1.1%` | bounded | imported matching coefficients | arXiv bounded appendix | [YT_GAUGE_CROSSOVER_THEOREM.md](../../YT_GAUGE_CROSSOVER_THEOREM.md) | [frontier_yt_gauge_crossover_theorem.py](../../../scripts/frontier_yt_gauge_crossover_theorem.py) |
| Cabibbo angle `|V_us|` | `0.2251` | `0.2243` | `+0.4%` | bounded | framework + bounded coefficient route | bounded companion only | [CABIBBO_BOUND_NOTE.md](../../CABIBBO_BOUND_NOTE.md) | [frontier_ckm_mass_basis_nni.py](../../../scripts/frontier_ckm_mass_basis_nni.py) |
| CKM magnitudes | `|V_us|=0.2251`, `|V_cb|=0.0420`, `|V_ub|=0.00435` | PDG `0.2243`, `0.0422`, `0.00382` | mixed but strong | bounded | framework + bounded coefficient route | arXiv bounded appendix | [CKM_MASS_BASIS_NNI_NOTE.md](../../CKM_MASS_BASIS_NNI_NOTE.md) | [frontier_ckm_mass_basis_nni.py](../../../scripts/frontier_ckm_mass_basis_nni.py) |
| Jarlskog invariant | `3.145 x 10^-5` | `3.08 x 10^-5` | near-match | bounded/partial | derived phase + observed angles | bounded companion only | [JARLSKOG_PHASE_BOUND_NOTE.md](../../JARLSKOG_PHASE_BOUND_NOTE.md) | [frontier_jarlskog_derived.py](../../../scripts/frontier_jarlskog_derived.py) |
| Spectral tilt `n_s` | `0.9667` | `0.9649 +/- 0.0042` | near-match | bounded/conditional | growth-model assumptions | arXiv companion only | [PRIMORDIAL_SPECTRUM_NOTE.md](../../PRIMORDIAL_SPECTRUM_NOTE.md) | [frontier_primordial_spectrum.py](../../../scripts/frontier_primordial_spectrum.py) |
| Dark energy EOS `w` | `-1` | observationally near `-1` | exact on chain / conditional overall | bounded/conditional | topology/cosmology dependent | arXiv companion only | [DARK_ENERGY_EOS_NOTE.md](../../DARK_ENERGY_EOS_NOTE.md) | [frontier_dark_energy_eos.py](../../../scripts/frontier_dark_energy_eos.py) |
| Cosmological constant `\Lambda` | `1.59 x 10^-52 m^-2` | `1.09 x 10^-52 m^-2` | same order, bounded | bounded/conditional | depends on `S^3` / Hubble-scale identification | arXiv companion only | [COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md](../../COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md) | [frontier_cosmological_constant.py](../../../scripts/frontier_cosmological_constant.py) |
| graviton mass `m_g` | `3.52 x 10^-33 eV` | strongest current bound `m_g < 1.76 x 10^-23 eV` | `10^10` below strongest bound | bounded/conditional | retained `S^3` + observed `H_0` | arXiv companion only | [GRAVITON_MASS_DERIVED_NOTE.md](../../GRAVITON_MASS_DERIVED_NOTE.md) | [frontier_graviton_mass_derived.py](../../../scripts/frontier_graviton_mass_derived.py) |
| Higgs mass `m_H` | mechanism derived; exact mass bounded | `125 GeV` | not closed | open/bounded | multiple remaining assumptions and route ambiguity | not for flagship promotion | [HIGGS_MASS_DERIVED_NOTE.md](../../HIGGS_MASS_DERIVED_NOTE.md), [HIGGS_MECHANISM_NOTE.md](../../HIGGS_MECHANISM_NOTE.md), [HIGGS_FROM_LATTICE_NOTE.md](../../HIGGS_FROM_LATTICE_NOTE.md) | [frontier_higgs_mass_derived.py](../../../scripts/frontier_higgs_mass_derived.py) |
| Bekenstein-Hawking entropy | `S/S_max = 0.2364` | `1/4` target | `5.4%` from area-law target | bounded | companion identification layer | companion only | [BH_ENTROPY_DERIVED_NOTE.md](../../BH_ENTROPY_DERIVED_NOTE.md) | [frontier_bh_entropy_derived.py](../../../scripts/frontier_bh_entropy_derived.py) |
| gravitational decoherence | `\gamma = 0.253 Hz`, `\Phi_{ent} = 12.4 rad` (BMV benchmark) | no direct observation; BMV coherence budget `\gamma_{tot} < 0.5 Hz` | benchmark-feasible / unmeasured | bounded | gravity derivation + benchmark geometry | companion only | [GRAV_DECOHERENCE_DERIVED_NOTE.md](../../GRAV_DECOHERENCE_DERIVED_NOTE.md) | [frontier_grav_decoherence_derived.py](../../../scripts/frontier_grav_decoherence_derived.py) |
| Proton lifetime | `~4 x 10^47 yr` | lower bounds only | sharp prediction | bounded | imported EFT decay-rate layer | companion only | [PROTON_LIFETIME_DERIVED_NOTE.md](../../PROTON_LIFETIME_DERIVED_NOTE.md) | [frontier_proton_lifetime_derived.py](../../../scripts/frontier_proton_lifetime_derived.py) |
| Lorentz-violation fingerprint | cubic `(E/E_Pl)^2` | bounds only | sharp prediction | bounded | companion phenomenology | companion only | [LORENTZ_VIOLATION_DERIVED_NOTE.md](../../LORENTZ_VIOLATION_DERIVED_NOTE.md) | [frontier_lorentz_violation.py](../../../scripts/frontier_lorentz_violation.py) |
| Magnetic monopole mass | `1.43 M_Pl` | lower bounds only | sharp prediction | bounded | companion phenomenology | companion only | [MONOPOLE_DERIVED_NOTE.md](../../MONOPOLE_DERIVED_NOTE.md) | [frontier_monopole_derived.py](../../../scripts/frontier_monopole_derived.py) |
| GW echo null result | no detectable echoes; the old `58-68 ms` timing family exists mathematically but observable amplitude is effectively zero | full-catalog stack null: `0.41 sigma` frozen-star, `1.29 sigma` Abedi-style | consistent null result | bounded/off-scope | frozen-star compact-object identification layer | later companion paper only | [GW_ECHO_NULL_RESULT_NOTE.md](../../GW_ECHO_NULL_RESULT_NOTE.md) | [frontier_echo_null_result.py](../../../scripts/frontier_echo_null_result.py) |

## Reading rule

- This table is not the retained claim surface by itself.
- Retained claims are defined by [CLAIMS_TABLE.md](./CLAIMS_TABLE.md).
- Bounded and frozen-out interpretation is defined by the matrix and ledger.
