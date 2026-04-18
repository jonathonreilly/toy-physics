PF science review for `codex/pf-path-ground-2026-04-17`

Verdict

- Reject for `main`.
- Not approved for repo weaving.
- The branch is scientifically useful as a boundary/program packet, but it does not yet provide theorem-grade object-level certification of the missing PF selector route.

Branch reviewed

- Remote branch: `origin/codex/pf-path-ground-2026-04-17`
- Science tip reviewed: `5b749138` (`Sharpen Wilson PF route to local algebraic certificate`)

Replay

- `python3 scripts/frontier_perron_frobenius_selection_axiom_boundary.py`
  - `PASS = 110`, `FAIL = 0`, `SUPPORT = 47`
- `python3 scripts/frontier_perron_frobenius_step2_wilson_local_path_algebra_minimal_certificate_2026_04_18.py`
  - `THEOREM PASS = 5`, `SUPPORT = 1`, `FAIL = 0`
- `python3 scripts/frontier_perron_frobenius_step2_wilson_local_hermitian_minimal_certificate_2026_04_18.py`
  - `THEOREM PASS = 5`, `SUPPORT = 1`, `FAIL = 0`
- `python3 scripts/frontier_perron_frobenius_step2_wilson_physical_sharpest_certificate_target_2026_04_18.py`
  - `THEOREM PASS = 4`, `SUPPORT = 2`, `FAIL = 0`

Findings

1. [P0] The umbrella PF closure runner is still a note-audit script rather than an object-level theorem verifier.

The top-level runner at `scripts/frontier_perron_frobenius_selection_axiom_boundary.py` defines a `read()` helper at lines 56-57, then spends the theorem path reading note files and checking whether required phrases occur in those notes. Representative examples begin immediately at lines 76-116 and continue through the rest of the script. A replay of that runner is therefore evidence that the note stack is internally synchronized, not evidence that the branch has independently certified the underlying PF constructions or nonrealization claims on the framework objects themselves. For a retained-grade science landing, the master validator has to certify mathematical objects, reductions, or counterexamples, not mainly prose claims about those objects.

2. [P1] The new Wilson local certificate runners assume the missing constructive layer and then verify only the downstream generic finite identities.

The new path-algebra and local-Hermitian runners both start from the same structure: they read the relevant note files, then prove a toy downstream identity after the missing layer is granted. In `scripts/frontier_perron_frobenius_step2_wilson_local_path_algebra_minimal_certificate_2026_04_18.py`, the lead theorem check is explicitly conditional: “Once the local path-algebra layer exists...” (lines 62-66), and the rest of the theorem path is phrase-presence checks on the linked notes (lines 68-99). The Hermitian version does the same thing in `scripts/frontier_perron_frobenius_step2_wilson_local_hermitian_minimal_certificate_2026_04_18.py`: the main numerical check assumes the local Hermitian 4-source layer exists (lines 63-67), then the runner mostly verifies note text (lines 68-99). That is useful packaging, but it is not a certification that the current framework already realizes the missing Wilson local support object.

3. [P1] The “physical sharpest certificate” runner validates a generic embedded matrix-unit toy model, not the framework realization of the Wilson primitive it names.

In `scripts/frontier_perron_frobenius_step2_wilson_physical_sharpest_certificate_target_2026_04_18.py`, the support-side algebra is built by hand from generic matrix units `e(i,j)` and an `embedded()` map (lines 40-49, 71-97). The post-support layer is then checked on an arbitrary hand-written Hermitian block `h_e` embedded into a larger matrix `s_w` (lines 107-119). Those computations show that a local `2-edge + 3` certificate shape is algebraically coherent as an abstract finite certificate. They do not show that the current bank realizes the specific physical Wilson object, source packet, or support-side map that the notes identify as missing. The later theorem checks again reduce to note wording and packaging claims (lines 137-162).

What is good

- The top-level note `docs/PERRON_FROBENIUS_SELECTION_AXIOM_BOUNDARY_NOTE_2026-04-17.md` is materially more honest than an overclaimed closure note. Its actual message is a negative/boundary result: sector-local PF pieces exist, but the sole-axiom global selector is not yet derived.
- The newer Wilson notes are directionally better because they sharpen the missing Step-2 target to local finite certificates instead of vague “something PF-like.”
- The branch is useful as a research-program packet because it narrows the remaining Wilson bottleneck.

Why this still does not land

- A `PASS` on the current stack mostly means “the notes agree with each other and the proposed target shape is algebraically self-consistent.”
- It does not yet mean “the branch has derived or certified the missing local Wilson primitive on the actual framework surface.”
- That gap is exactly the difference between a good science-program boundary packet and a landable retained/bounded package result.

What would upgrade this

- Replace the umbrella runner with object-level validators for the load-bearing claims.
- For the Wilson route, certify one real framework-surface constructive or obstruction theorem instead of auditing note text about the target.
- In particular, the next accepted closure would need one of:
  - a positive realization theorem for the local Wilson primitive the notes now isolate, or
  - a genuine impossibility theorem showing that the current exact bank cannot realize that primitive.
- If the branch stays a boundary/program packet, keep the negative-scoping language but do not present the runner stack as theorem-grade certification of the unresolved step.

Landing note

- Independent of the science verdict, the branch is also not merge-ready as a branch diff because it sits on an old base and shows a very large unrelated diff against current `main`.
- If the science is ever approved later, it should land through a selective fresh landing branch, not by merging this branch directly.
