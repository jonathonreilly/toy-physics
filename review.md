# Review: `frontier/cl3-sm-embedding`

## Verdict

Reject for `main` at the current science tip (`1cbb91c8`).

The branch is scoped cleanly and the main verifier replays at `PASS=94 FAIL=0`,
but the replay is not certifying the science the notes claim. The current packet
contains several real algebra checks on a hand-built `8x8` toy realization, but
the load-bearing Standard Model claims are still being inserted rather than
derived from the retained framework surface.

If the science were clean, I would land and weave it myself. The blockers below
are scientific blockers.

## Replay

- `python3 scripts/verify_cl3_sm_embedding.py`
  → `PASS=94 FAIL=0`

The issue is not arithmetic or syntax. The issue is that key theorem steps are
currently asserted by construction.

## Main Blockers

### 1. The branch does not derive the physical hypercharge operator from the central Clifford `U(1)` direction

The notes say the pseudoscalar `omega = Gamma_1 Gamma_2 Gamma_3` generates the
native `U(1)_Y` direction, and then present the Standard Model hypercharge
spectrum as retained.

But the verifier does two different things:

- it proves `Omega` is central and linearly independent from `Cl^+(3)`;
- then, separately, it defines
  `Y = (+1/3) P_symm + (-1) P_antisymm`
  from the `b1 <-> b2` swap projector and checks the spectrum of that chosen
  operator.

No theorem step identifies the physical hypercharge operator with `Omega`, or
derives the coefficients `+1/3` and `-1` from the Clifford center. So the
branch currently proves:

> there exists a central `U(1)` direction in the Clifford algebra, and there
> also exists a separately chosen projector-valued operator with SM-like left
> hypercharge eigenvalues.

That is not the same as:

> the retained Clifford center itself forces the physical `U(1)_Y` assignment.

This is a load-bearing blocker because the theorem note and master note both
advertise the latter, not merely the former.

## 2. The `g_2^2 = 1/(d+1)` and `g_Y^2 = 1/(d+2)` claims are asserted, not derived

The note says the bare couplings are fixed by the dimensions of `Cl^+(3)` and
`Cl^+(3) + {omega}`. But Section D of the verifier literally sets:

- `g2_sq = 1.0 / 4`
- `g_Y_sq = 1.0 / 5`

and then checks those numbers against themselves.

What is missing is the actual normalization argument: an action-level or
kinetic-term derivation showing why the inverse number of basis elements is the
coupling. Dimension counting by itself does not fix gauge coupling normalization.

So the branch currently has:

- a real dimension count,
- plus a stated normalization rule,
- but not a verification that the retained framework forces that normalization
  rule.

That means the new packet does not actually close the old coupling blocker at
retained bar.

## 3. The claimed `SU(3)_c` emergence is a manual Gell-Mann embedding, not a derived automorphism theorem

The color note claims the automorphism structure of the taste cube contains the
physical color algebra and thereby forces:

- `SU(3)_c`,
- `T_F = 1/2`,
- `R_conn = 8/9`,
- the `sqrt(9/8)` electroweak-color correction.

But the verifier implements this by:

1. choosing a `3D_sym + 1D_antisym` base split,
2. writing down the standard `3x3` Gell-Mann matrices by hand,
3. embedding them as `diag(T^a, 0) ⊗ I_2`,
4. then verifying the standard `SU(3)` relations for that inserted copy.

That proves the manually embedded matrices form an `SU(3)` representation. It
does **not** prove that the `Z^3` automorphism / commutant structure itself
uniquely forces that exact `SU(3)_c` as the physical color algebra.

So the branch has a valid consistency embedding, but not yet the native
derivation it claims in the theorem prose.

## 4. The taste-to-generation theorem overclaims equal gauge quantum numbers

The taste theorem claims the `hw=1` triplet gives three generation candidates
with identical `SU(2) x U(1)` quantum numbers.

What the verifier actually checks in Section G is:

- the `S_3` / `Z_3` permutation action,
- the character decomposition `C^8 = 4A_1 + 2E`,
- the cyclic permutation of the three `hw=1` basis states.

It does **not** verify the load-bearing gauge-content statement for those three
states. There is no direct check that the three `hw=1` basis states have equal
`Y` eigenvalues or identical weak representation content under the chosen gauge
operators.

And the note's justification for equality is itself not closed: it says `Y` is
defined independently of which axis is active, but the actual `Y` operator is
defined from the specific `b1 <-> b2` swap projector, so the branch has not
yet shown the needed `Z_3`-compatibility at theorem level.

So the branch currently proves:

> the `hw=1` triplet is a `Z_3` orbit,

not yet:

> that orbit already carries three identical SM generation sectors.

## 5. The A-BCC positivity upgrade is narrower than the theorem text claims

The notes say Kramers degeneracy turns the determinant positivity of the
bilinear condensate operator into a theorem.

But the verifier only checks the much narrower statement that random operators
of the form

`H_L = a I + b J1_L + c J2_L + d J3_L`

have doubly degenerate eigenvalues and nonnegative determinant. That is a
special `4`-parameter family inside the space of `4x4` Hermitian operators, and
the script does not show that the actual condensate operator is restricted to
that family.

More importantly, Kramers degeneracy applies to Hermitian operators that obey
the relevant anti-unitary symmetry. The current packet does not prove that the
full A-BCC operator class inherits exactly that symmetry constraint.

So the branch has a useful local model calculation, not yet the general
condensate-positivity theorem the master note advertises.

## Hygiene

The branch is also stale relative to `origin/main`:

- `origin/main...origin/frontier/cl3-sm-embedding` = `22 behind / 1 ahead`

That is not the reason for rejection here, but it would need cleanup before any
landing discussion after the science is fixed.

## What Would Upgrade This

To reach retained bar, the worker needs to close the actual missing derivation
layers, not just add more consistency checks on the same hand-built model:

1. Derive the physical hypercharge operator from the native Clifford center, or
   explicitly prove the map from `Omega` to the projector-valued `Y`.
2. Derive the coupling-normalization rule from the retained gauge kinetic
   structure instead of asserting inverse-dimension normalization.
3. Derive the `SU(3)_c` copy from the native automorphism / commutant structure,
   rather than embedding Gell-Mann matrices by hand and checking them.
4. Prove that the `hw=1` triplet carries identical gauge content under the
   actual derived gauge operators.
5. Prove that the full A-BCC operator class has the Kramers symmetry being used,
   rather than testing random operators in the `I + su(2)` span.

## Bottom Line

The branch contains a coherent algebraic toy realization of several desired SM
structures. But the current theorem notes repeatedly present those inserted
structures as if they were framework-forced derivations.

So the current call is:

- **do not land on `main`**
- **do not weave through claim surfaces**
- **resubmit only after the load-bearing derivation layers above are actually
  closed**
