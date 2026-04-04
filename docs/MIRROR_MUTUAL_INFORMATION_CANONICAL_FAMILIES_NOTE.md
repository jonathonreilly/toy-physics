**Status:** broader mirror-family MI extension saved

This note complements the retained exact chokepoint MI artifact by extending
the same mutual-information measurement to the broader canonical 3D mirror
families used elsewhere in the repo.

Artifacts:
- [`scripts/mirror_mutual_information_canonical_families.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_mutual_information_canonical_families.py)
- [`logs/2026-04-03-mirror-mutual-information-canonical-families.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-mutual-information-canonical-families.txt)

Relationship to the retained exact harness:
- The review-safe exact result still lives in:
  [`scripts/mirror_mutual_information.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_mutual_information.py)
  and
  [`scripts/mirror_mutual_information_chokepoint.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_mutual_information_chokepoint.py)
- This extension is broader, not more canonical.
- Its job is to answer the multi-family “mirror DAGs” version of the MI
  question without overwriting the retained exact chokepoint chain.

What the extension measures:
- `I(slit_label ; detector_y_bin) = H(detector) - H(detector|slit)`
- strictly linear propagator
- same gravity-field construction as the mirror joint scripts
- matched random baselines where practical

Families included:
- original random
- original `Z2` mirror
- strict chokepoint random
- strict chokepoint mirror
- `S4` random hybrid baseline
- `S4` mirror hybrid

Main bounded read:
- `S4` mirror is the strongest scalable MI lane in this extension:
  - `N=25`: `0.7213±0.073` bits
  - `N=40`: `0.5956±0.067` bits
  - `N=60`: `0.5248±0.067` bits
  - `N=80`: `0.2559±0.047` bits
- The matched `S4` random baseline is lower at every retained row:
  - `N=25`: `0.5189±0.067` bits
  - `N=40`: `0.2852±0.051` bits
  - `N=60`: `0.1992±0.037` bits
  - `N=80`: `0.1147±0.029` bits
- The strict mirror chokepoint pocket has even stronger MI in its short
  window:
  - `N=15`: `0.9196±0.033` bits
  - `N=25`: `0.6578±0.091` bits
  - but it does not survive to larger `N` in this broader table
- The original mirror family is only mildly informative:
  - about `0.05` to `0.11` bits through `N=60`

Interpretation:
- The earlier branch claim of about `0.73` bits at `N=25` is consistent with
  the saved `S4` mirror row here.
- The earlier prose claim of about `0.48` bits at `N=80` was too optimistic
  for the canonical saved extension; the artifact-backed `S4` value is about
  `0.26` bits.

Bottom line:
- the exact chokepoint MI chain is the synthesis-grade retained result
- the broader canonical-family extension now makes the multi-family mirror MI
  story artifact-backed too
