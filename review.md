# Review: `claude/cl3-minimality`

## Current Call

This branch now contains **two different CL3 stories**:

- the earlier `cl3-minimality-conditional-support-2026-04-17.md`, which is a
  coherent support / consistency note on the retained cubic surface
- the new `native-su2-tightness-forces-ds3-2026-04-17.md`, which tries to
  upgrade `d_s = 3` to retained closure

My current disposition is therefore:

- **No** as retained G16 / axiom-depth closure
- **Yes** as a support-note package, if the new retained-grade overclaim is
  removed or downgraded

So the branch is **not ready to land as a retained closure** in its current
state, but it still contains a scientifically useful support note.

## Replay Status

- `python3 -m py_compile scripts/frontier_cl3_minimality.py` passes
- `python3 scripts/frontier_cl3_minimality.py` ends with
  `THEOREM_PASS=50 SUPPORT_PASS=32 FAIL=0`
- `python3 -m py_compile scripts/frontier_native_su2_tightness.py` passes
- `python3 scripts/frontier_native_su2_tightness.py` ends with
  `THEOREM_PASS=19 SUPPORT_PASS=16 FAIL=0`

The issue is **not** arithmetic or syntax. The issue is that the new
`native-su2-tightness` theorem certifies a premise that is stronger than the
retained authority it cites.

## Main Blocker

### The new retained closure hinges on a stronger premise than the retained native-SU(2) authority actually proves

The new note says:

> the retained native-SU(2) theorem asserts that the Clifford bivectors close
> exactly into the weak SU(2) algebra ... the set of all bivectors is exactly
> the SU(2) weak-gauge Lie algebra, with no bivector left over and no selector
> required to pick them out

and then rewrites that as

> `spin(n) = su(2)` as Lie algebras

That is the load-bearing step of the new retained-grade derivation.

But the cited retained authority
`docs/NATIVE_GAUGE_CLOSURE_NOTE.md` does **not** currently prove that stronger
statement at comparison-family scope. What it actually says is:

- on the **cubic `Z^3` surface**
- `Cl(3)` in taste space
- **contains** an `su(2)` subalgebra

Specifically, the current retained authority says:

- `Cl(3) contains su(2) subalgebra -> SU(2) gauge symmetry`
- `Cl(3) on Z^3 produces exact SU(2)`

That is a theorem on the retained `Cl(3)` / `Z^3` surface. It is **not yet**
the general comparison-family theorem:

- for arbitrary `Cl(n)`,
- all bivectors are weak,
- with no selector,
- therefore `spin(n) = su(2)`

The new note itself more or less admits this in the non-circularity section:

> if a reviewer rejects the re-reading ... this note has only moved the
> circularity one step back

That is the right self-assessment. This is still an **interpretive upgrade** of
the retained theorem, not a retained theorem already on `main`.

So the branch has not yet proved retained closure of `d_s = 3`. It has proposed
a new stronger theorem that would *if separately retained* imply `d_s = 3`.

## Runner Weakness

### The new runner certifies the dimensional-matching theorem only after assuming the strengthened premise

The new runner is internally consistent, but it does not verify the actual
scientific gap.

It begins by taking as its theorem statement:

> `spin(n) = su(2)`

and then checks:

- the unique solution of `n(n-1)/2 = 3`
- explicit `spin(3) = su(2)`
- dimension mismatch for `n >= 4`
- a printed non-circularity audit

That is fine **if** `spin(n) = su(2)` were already an accepted retained input.
But the branch is using the runner to support the claim that the retained
native-gauge note already implies that input. The runner does **not** verify
that implication.

In particular:

- it does not parse or reconstruct the existing retained native gauge theorem
- it does not show that the current `Cl(3)` / `Z^3` proof separates its
  Lie-algebra content from its cubic-surface content
- it does not certify the "no selector / all bivectors" reading as a retained
  theorem on the `Cl(n)` comparison family
- its non-circularity section is largely a printed audit plus unconditional
  `True` checks, not an independent certification of the strengthened premise

So `19 THEOREM / 16 SUPPORT / 0 FAIL` is evidence for the algebra **after
assuming** the upgraded premise, not evidence that the current retained stack
already proves that premise.

## Best Outcome From Here

### Best immediate outcome

Do **not** land this as retained closure.

Instead:

1. keep the earlier `cl3-minimality-conditional-support-2026-04-17.md` as the
   canonical CL3 note if you want to land something now
2. downgrade `native-su2-tightness-forces-ds3-2026-04-17.md` to a
   speculative / support-grade route note
3. explicitly state that the new theorem depends on a stronger
   "canonical no-selector" reading that is **not yet separately retained**

That yields an honest support-note package with a promising future route, but no
false retained claim.

### What would actually get this to retained

You need a **separate retained theorem** establishing the upgraded native-gauge
premise itself.

Concretely, the branch would need to prove something like:

> The native weak-gauge closure is not merely that `Cl(3)` on `Z^3` contains an
> `su(2)` subalgebra, but that the framework's weak-gauge closure principle is
> canonically selector-free and identifies the full Clifford bivector Lie
> algebra with the weak algebra at comparison-family scope.

Only after that theorem is separately established can you legitimately run the
dimension-matching step

> `spin(n) = su(2)` -> `n(n-1)/2 = 3` -> `n = 3`

as a retained closure theorem.

And the runner would then need to verify **that** stronger theorem, not just the
downstream dimension count.

### Best possible retained-grade path

If you want to pursue retained closure, the clean decomposition is:

1. **Native-gauge scope theorem**
   prove that the retained native-SU(2) authority really has a
   comparison-family, selector-free reading
2. **Tightness theorem**
   once that is retained, the dimension match to `n = 3` is trivial
3. **Generation corollary**
   keep the old cubic / `hw` semantics chain as downstream support-level
   generation-count packaging unless you separately derive those semantics too

Without step 1, the current branch is still below retained bar.

## Bottom Line

My current call:

- **No** as retained G16 / `d_s = 3` closure
- **Yes** as a support-note package if the new overclaim is downgraded

The branch's real scientific value right now is:

- a solid conditional minimality / consistency note on the retained cubic
  surface
- plus a potentially interesting future route:
  "if canonical selector-free native SU(2) can be retained separately, then
  `d_s = 3` follows immediately by Lie-algebra dimensional matching"

That is useful. It is just not yet the same thing as a retained proof.
