# Classical Number-Theory Characterization of the Retained CKM Structural Integers `(N_pair, N_color, N_quark) = (2, 3, 6)`

**Date:** 2026-04-25

**Status:** proposed_retained CKM-structure theorem on current `main`.

This note packages classical number-theoretic identities obeyed by the retained
CKM structural integers

```text
N_pair = 2,   N_color = 3,   N_quark = N_pair * N_color = 6.
```

The theorem is CKM-only. It does not promote any cross-sector identification
and does not claim any charged-lepton Koide closure.

**Primary runner:**
`scripts/frontier_ckm_classical_number_theory_integer_characterization.py`

## Statement

On the retained CKM structural-count surface,

```text
(P1)  Perfect-number identity:
      N_quark = 1 + N_pair + N_color = 6.

(P2)  Sigma-perfect condition:
      sigma(N_quark) = 2 N_quark = 12.

(P3)  Sum-product coincidence for the proper divisors of 6:
      1 + N_pair + N_color = 1 * N_pair * N_color = 6.

(P4)  Deficient/perfect classification:
      N_pair and N_color are deficient, while N_quark is perfect.

(T1)  Triangular ladder:
      N_color = T_{N_pair} = T_2 = 3,
      N_quark = T_{N_color} = T_3 = 6.

(L1)  Lie-dimensional identity:
      N_color = N_pair^2 - 1 = dim(adjoint SU(N_pair)) = 3.

(M1)  Mersenne-prime identity:
      N_color = 2^{N_pair} - 1 = 3.

(M2)  Euclid-Euler perfect-number identity:
      N_quark = 2^{N_pair-1} (2^{N_pair} - 1) = 6.

(U1)  Five independent three-constraint uniqueness routes:
      with common scaffold
        (a) N_pair = N_color - 1
        (b) N_quark = N_pair * N_color,
      each of
        (c) N_quark = 1 + N_pair + N_color,
        (d) N_quark = T_{N_color},
        (e) 1/N_pair + 1/N_color + 1/N_quark = 1,
        (f) N_color = N_pair^2 - 1,
        (g) N_color = 2^{N_pair} - 1
      independently forces the unique positive-integer solution
        (N_pair, N_color, N_quark) = (2, 3, 6).
```

The new content is not the retained counts themselves, but this exact
classical-number-theory packaging of those counts and the explicit uniqueness
routes `(a)+(b)+(x)` for `x in {c,d,e,f,g}`.

## Retained Inputs

All derivation inputs are retained on current `main`:

| Input | Authority on `main` |
| --- | --- |
| `N_pair = 2`, `N_color = 3`, `N_quark = N_pair * N_color = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) |

No PDG observable enters as a derivation input. No support-tier or open
cross-sector inputs are used.

## Derivation

### P1: Perfect-number identity

The proper divisors of `6` are `{1, 2, 3}` and they sum to `6`:

```text
1 + 2 + 3 = 6.
```

Substituting the retained CKM counts gives

```text
1 + N_pair + N_color = 1 + 2 + 3 = 6 = N_quark.
```

So `N_quark` is the smallest perfect number.

### P2: Sigma-perfect condition

The divisor-sum function satisfies

```text
sigma(6) = 1 + 2 + 3 + 6 = 12 = 2 * 6.
```

Hence `sigma(N_quark) = 2 N_quark`.

### P3: Sum-product coincidence

For the proper divisors of `6`,

```text
1 + 2 + 3 = 6,
1 * 2 * 3 = 6.
```

So on the retained CKM counts,

```text
1 + N_pair + N_color = 1 * N_pair * N_color = N_quark.
```

This is a classical arithmetic coincidence of the first perfect number and is
packaged here as a structural identity of the retained CKM counts.

### P4: Deficient/perfect classification

```text
sigma(2) - 2 = 1 < 2,   so N_pair is deficient
sigma(3) - 3 = 1 < 3,   so N_color is deficient
sigma(6) - 6 = 6 = 6,   so N_quark is perfect.
```

The retained CKM integer triple therefore splits as two deficient counts and
one perfect count.

### T1: Triangular ladder

The triangular numbers are `T_n = n(n+1)/2`. Hence

```text
T_2 = 3,   T_3 = 6.
```

Substituting the retained counts gives

```text
N_color = T_{N_pair} = T_2 = 3,
N_quark = T_{N_color} = T_3 = 6.
```

So `(2,3,6)` forms a triangular ladder.

### L1: Lie-dimensional identity

The adjoint representation of `SU(N)` has dimension `N^2 - 1`. For `N_pair=2`,

```text
dim(adjoint SU(2)) = 2^2 - 1 = 3 = N_color.
```

So the retained color count equals the adjoint dimension of `SU(N_pair)`.

### M1: Mersenne-prime identity

For `N_pair=2`,

```text
2^{N_pair} - 1 = 2^2 - 1 = 3 = N_color.
```

Thus the retained color count is the smallest Mersenne prime.

### M2: Euclid-Euler perfect-number identity

The Euclid-Euler form for even perfect numbers is

```text
2^{p-1}(2^p - 1).
```

At `p = N_pair = 2` this gives

```text
2^{N_pair-1}(2^{N_pair} - 1) = 2^1 (2^2 - 1) = 2 * 3 = 6 = N_quark.
```

So the retained quark count is the first Euclid-Euler perfect number.

### U1: Five independent three-constraint uniqueness routes

Use the common scaffold

```text
(a) N_pair = N_color - 1,
(b) N_quark = N_pair * N_color.
```

Then each additional classical constraint independently pins `N_color = 3`:

1. `(a)+(b)+(c)` with `N_quark = 1 + N_pair + N_color`:

   ```text
   (N_color - 1)N_color = 1 + (N_color - 1) + N_color
   N_color^2 - N_color = 2N_color
   N_color(N_color - 3) = 0
   => N_color = 3.
   ```

2. `(a)+(b)+(d)` with `N_quark = T_{N_color} = N_color(N_color+1)/2`:

   ```text
   (N_color - 1)N_color = N_color(N_color + 1)/2
   2(N_color - 1) = N_color + 1
   => N_color = 3.
   ```

3. `(a)+(b)+(e)` with `1/N_pair + 1/N_color + 1/N_quark = 1`:

   ```text
   1/(N_color-1) + 1/N_color + 1/[(N_color-1)N_color] = 1
   ```

   Multiplying by `N_color(N_color-1)` gives

   ```text
   N_color + (N_color - 1) + 1 = N_color(N_color - 1)
   2N_color = N_color^2 - N_color
   N_color(N_color - 3) = 0
   => N_color = 3.
   ```

4. `(a)+(b)+(f)` with `N_color = N_pair^2 - 1`:

   ```text
   N_color = (N_color - 1)^2 - 1 = N_color^2 - 2N_color
   N_color(N_color - 3) = 0
   => N_color = 3.
   ```

5. `(a)+(b)+(g)` with `N_color = 2^{N_pair} - 1`:

   ```text
   N_color = 2^{N_color - 1} - 1
   N_color + 1 = 2^{N_color - 1}.
   ```

   `N_color = 3` is a solution. It is unique over positive integers because
   the function `f(n)=2^{n-1}-n-1` has `f(3)=0`, `f(2)=-1`, and for `n>=4`

   ```text
   f(n+1)-f(n)=2^{n-1}-1 > 0,
   ```

   so `f` is strictly increasing past `n=3` and never returns to zero.

Therefore each of the five routes `(a)+(b)+(x)` with
`x in {c,d,e,f,g}` independently forces `(N_pair,N_color,N_quark)=(2,3,6)`.

## Numerical Verification

The runner checks the retained identities in exact integer/Fraction arithmetic
and performs exhaustive positive-integer searches confirming the five
three-constraint uniqueness routes on the audited count ranges.

## Science Value

This theorem pushes the retained CKM integer package forward in three ways:

1. It adds a classical number-theory characterization of the retained counts
   `(2,3,6)` via perfect-number, triangular, Lie-dimensional, and Mersenne
   identities.
2. It isolates five independent three-constraint routes that each recover the
   same retained integer triple.
3. It shows that the framework's primitive CKM counts are not merely stated on
   `main`, but can be re-read through several mutually reinforcing classical
   arithmetic structures.

That is a real structural sharpening of the retained CKM package even though it
does not promote any cross-sector bridge.

## What This Claims

- `(P1)`: `N_quark = 1 + N_pair + N_color`.
- `(P2)`: `sigma(N_quark) = 2 N_quark`.
- `(P3)`: the proper divisors of `N_quark = 6` satisfy both sum and product
  equalities.
- `(P4)`: `N_pair` and `N_color` are deficient while `N_quark` is perfect.
- `(T1)`: `N_color = T_{N_pair}` and `N_quark = T_{N_color}`.
- `(L1)`: `N_color = dim(adjoint SU(N_pair))`.
- `(M1)`: `N_color = 2^{N_pair} - 1`.
- `(M2)`: `N_quark = 2^{N_pair-1}(2^{N_pair} - 1)`.
- `(U1)`: each of the five routes `(a)+(b)+(x)` with `x in {c,d,e,f,g}`
  independently forces `(2,3,6)`.

## What This Does NOT Claim

- It does NOT close `A²` deeper than the retained structural-counts level.
- It does NOT close `Koide 2/9` or any specific Koide quantity.
- It does NOT promote any cross-sector identification to retained status.
- It does NOT use SUPPORT-tier inputs as derivation inputs.
- It does NOT explain WHY the framework's choice falls at the smallest
  Mersenne prime / perfect number — that would require deeper CL3 algebraic
  derivation.

## Exact-symbolic verification

The classical number-theory identities (`P1`)-(`P4`), (`T1`), (`L1`),
(`M1`), (`M2`), and the five three-constraint uniqueness routes
(`U1.c`)-(`U1.g`) are certified at exact-symbolic precision via `sympy`
in `scripts/audit_companion_ckm_classical_number_theory_integer_characterization_exact.py`.
The companion runner imports the retained CKM structural integers
`(N_pair, N_color, N_quark) = (2, 3, 6)` verbatim as exact
`sympy.Rational` values, treats the uniqueness-route count `c` as a
positive-integer symbol, and checks each identity by computing
`sympy.simplify(lhs - rhs)` and asserting the residual equals `0`
exactly. The cited count authority itself
(`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`) is
imported and not re-derived here.

| Identity | Symbolic form | Verification |
| --- | --- | --- |
| (`P1`) | `N_quark == 1 + N_pair + N_color` | `sympy.simplify` residual `= 0` |
| (`P1`) | proper divisors of 6 are `{1, N_pair, N_color}` | exact integer check |
| (`P2`) | `sigma(N_quark) == 2 N_quark` | `sympy.divisor_sigma(6) == 12` |
| (`P3`) | `1 + N_pair + N_color == 1 * N_pair * N_color` | `sympy.simplify` residual `= 0` |
| (`P4`) | `N_pair, N_color` deficient; `N_quark` perfect | `sympy.divisor_sigma` checks |
| (`T1`) | `N_color == T_{N_pair}`, `N_quark == T_{N_color}` | parametric `n(n+1)/2` substitution |
| (`L1`) | `N_color == N_pair^2 - 1` | `sympy.simplify` residual `= 0` |
| (`M1`) | `N_color == 2^{N_pair} - 1` | `sympy.simplify` residual `= 0` |
| (`M2`) | `N_quark == 2^{N_pair-1}(2^{N_pair} - 1)` | `sympy.simplify` residual `= 0` |
| (`U1.c`) | `(c-1)c - (1 + (c-1) + c)` factors as `c(c - 3)` | `sympy.factor` reduction |
| (`U1.d`) | `(c-1)c - c(c+1)/2` proportional to `c(c - 3)` | `sympy.factor` reduction |
| (`U1.e`) | `1/(c-1) + 1/c + 1/((c-1)c) - 1` cleared denominator equals `-c(c - 3)` | `sympy.simplify` |
| (`U1.f`) | `c - ((c-1)^2 - 1)` reduces to `-c(c - 3)` | `sympy.factor` |
| (`U1.g`) | `f(c) = 2^{c-1} - c - 1` has unique positive-integer zero `c = 3` | exact integer monotonicity |

For routes (`U1.c`)-(`U1.f`) the runner additionally calls
`sympy.solve` on each three-constraint system and verifies the
positive-integer solution set is exactly `[3]`. For route (`U1.g`)
the runner verifies `f(1) = -1`, `f(2) = -1`, `f(3) = 0`, and `f`
strictly increases for `c >= 3` over the audited range, ensuring no
other positive-integer root exists.

Counterfactual probes confirm the retained ordering is load-bearing:

- substituting `N_pair = 3` under scaffold `(a) + (b)` forces
  `N_color = 4` and `N_quark = 12`, which fails (`P2`) since
  `sigma(12) = 28 != 24`;
- substituting `N_pair = 4` under `(M1)` gives `N_color = 15`, not
  the retained `3`.

The structural relations are therefore exact-symbolic over the imported
retained counts and the parametric `c`-symbol. The companion runner
adds no new physical input and does not modify any retained authority.

## Reproduction

```bash
python3 scripts/frontier_ckm_classical_number_theory_integer_characterization.py
PYTHONPATH=scripts python3 scripts/audit_companion_ckm_classical_number_theory_integer_characterization_exact.py
```

Expected result:

```text
TOTAL: PASS=25, FAIL=0
```

The runner uses Python's `fractions.Fraction` and integer arithmetic exactly.

## Cross-References

- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  -- retained `N_pair = 2`, `N_color = 3`, and `N_quark = N_pair × N_color = 6`.
- [`CKM_MULTI_PROJECTION_BERNOULLI_FAMILY_THEOREM_NOTE_2026-04-25.md`](CKM_MULTI_PROJECTION_BERNOULLI_FAMILY_THEOREM_NOTE_2026-04-25.md)
  -- earlier retained CKM-only integer packaging over the same structural counts.
