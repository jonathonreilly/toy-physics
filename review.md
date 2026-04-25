Reject branch as a verbatim `main` landing, but approve the science for **selective** landing.

What improved on this pass:
- the force-pushed branch is materially more honest than the original theorem version
- it now separates:
  - retained CKM-only layer `(M1)-(M5)`
  - conditional dimension-reading layer `(M6)` under `(P1)`
- it no longer overstates the `d=3` conclusion as a retained empirical proof

Why I still did not land this branch verbatim:
- the branch front door is still a **mixed retained + conditional** note
- on `main`, the cleaner authority surface is to split those roles:
  - land the genuinely retained CKM theorem as a retained subtheorem
  - keep the conditional dimension-uniqueness template off the live retained surface for now
- `(M6)` still depends on the support-only bare-alpha premise
  `(\alpha_3/\alpha_em)(bare)=2d+3`, and the discrete integer-reading also leans on the same support-layer logic rather than the retained minimal stack

What I landed instead on `main`:
- `docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`
- `scripts/frontier_ckm_magnitudes_structural_counts.py`

That landing preserves the real retained science:
- `|V_us|_0^2 = alpha_s(v)/n_pair`
- `|V_cb|_0^2 = |V_ts|_0^2 = alpha_s(v)^2/(n_pair n_color)`
- `|V_ub|_0^2 = alpha_s(v)^3/(8 n_color^2)`
- `|V_td|_0^2 = (n_quark-1) alpha_s(v)^3/(8 n_color^2)`
- exact `n_pair` cancellation in `|V_ub|_0^2`

Why that is the right repo shape:
- those identities already follow from retained CKM authorities on `main`
- they are genuinely useful as a new package-level structural-counts theorem
- they do not depend on the open/support three-sector lane

Current recommendation for this branch:
- treat it as **source material successfully mined**
- do not try to land this mixed support note itself on top of the retained theorem
- if you still want the conditional dimension-reading on `main`, resubmit it later as a **separate, narrowly scoped support note** that explicitly cites the already-landed retained theorem and the bare-alpha support note, without re-packing the retained CKM layer again
