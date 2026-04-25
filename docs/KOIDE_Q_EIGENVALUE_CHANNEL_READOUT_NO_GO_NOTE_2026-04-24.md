# Koide Q Eigenvalue-Channel Readout No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative audit. This sharpens the positive-parent /
set-equality route but does not close charged-lepton `Q = 2/3`.
**Primary runner:** `scripts/frontier_koide_q_eigenvalue_channel_readout_no_go.py`

---

## 1. Theorem Attempt

After the positive-parent audit, the strongest remaining escape hatch is:

> a positive `C_3`-covariant parent has a mathematically exact spectrum, and
> the charged-lepton comparison can be made at unordered set level, so perhaps
> the eigenvalue channel is already the physical charged-lepton readout.

The executable result is negative.

The eigenvalue channel is exact support. It is not forced by the retained
axis-local charged-lepton readout or by set-equality comparison language.

---

## 2. Exact Parent Algebra

For arbitrary positive amplitudes

```text
(a0, a1, a2),
```

define the positive parent

```text
M = F^dag diag(a0^2, a1^2, a2^2) F,
```

where `F` is the retained `C_3` Fourier transform. The runner verifies exactly:

- `M` is Hermitian;
- `M` commutes with the retained three-cycle;
- the eigenvalue channel contains the unordered mass set
  `{a0^2, a1^2, a2^2}`.

This keeps the positive-parent / square-root dictionary as valid support.

---

## 3. Axis-Local Blindness

The strict axis-local diagonal readout gives

```text
diag_axis(M)
  = ((a0^2+a1^2+a2^2)/3,
     (a0^2+a1^2+a2^2)/3,
     (a0^2+a1^2+a2^2)/3).
```

The runner checks the stronger functional statement too:

```text
diag_axis(F^dag diag(g0,g1,g2) F)
  = ((g0+g1+g2)/3,
     (g0+g1+g2)/3,
     (g0+g1+g2)/3)
```

for arbitrary spectral values `g_i`.

Thus every retained `C_3`-equivariant functional of the parent remains
axis-diagonal-blind. The current strict axis readout erases the two traceless
spectral degrees of freedom.

---

## 4. What The Eigenvalue Channel Adds

The eigenvalue channel is recovered by the Fourier spectral projectors

```text
P_k = F^dag E_kk F.
```

They satisfy

```text
tr(P_k M) = a_k^2,
```

but they are not axis-local diagonal readouts. For example `P_1` has flat
diagonal entries `1/3` and nonzero off-diagonal Fourier entries.

So the eigenvalue channel is a different observable channel, not a consequence
of applying the existing axis-basis diagonal readout more carefully.

---

## 5. Value Freedom Remains

With eigenvalue-channel amplitudes, the Koide scalar is

```text
Q_spec(a0,a1,a2)
  = (a0^2+a1^2+a2^2)/(a0+a1+a2)^2.
```

The runner checks exact samples:

```text
(1,1,1) -> Q_spec = 1/3
(1,2,3) -> Q_spec = 7/18
(1,1,2) -> Q_spec = 3/8
```

So even after adopting the eigenvalue channel, the projective amplitude ratios
remain free. The channel does not by itself supply the value law.

---

## 6. Set-Equality Boundary

Set-equality comparison is a useful way to avoid importing charged-lepton
naming or ordering conventions. But it starts only after the physical observable
has been chosen.

The same exact parent with amplitudes `(1,2,3)` gives:

```text
axis readout     = {14/3, 14/3, 14/3}
spectral readout = {1, 4, 9}.
```

Both are mathematically defined from the same `C_3` parent. The retained
set-equality language does not decide which one is the charged-lepton mass
observable.

---

## 7. Review Consequence

The positive-parent route now has two distinct residuals:

```text
eigenvalue_channel_readout_or_spectral_value_law
```

More explicitly, a closure still needs one of:

- a retained theorem deriving the Fourier spectral projectors as physical;
- a non-axis-local charged-sector reduction;
- a controlled charged-lepton-specific breaking of strict `C_3` axis readout;
- an independent spectral value law forcing the projective amplitudes.

Absent such a theorem, promoting `eig(M)` to the charged-lepton mass observable
renames a missing readout primitive as a theorem.

---

## 8. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_eigenvalue_channel_readout_no_go.py
```

Result:

```text
PASSED: 11/11
KOIDE_Q_EIGENVALUE_CHANNEL_READOUT_NO_GO=TRUE
Q_EIGENVALUE_READOUT_CLOSES_Q=FALSE
RESIDUAL_PRIMITIVE=eigenvalue_channel_readout_or_spectral_value_law
```

No PDG masses, `K_TL = 0`, `K = 0`, `P_Q = 1/2`, `Q = 2/3`,
`delta = 2/9`, or `H_*` observational pin is used.

---

## 9. Boundary

This note does not demote:

- the positive-parent construction;
- the square-root amplitude dictionary;
- unordered set-equality comparison as a comparison protocol.

It rejects only the stronger closure claim that these support statements already
derive the physical eigenvalue-channel readout or the Koide value law.

Package status is unchanged:

- `Q = 2/3` still needs the normalized traceless-source law `K_TL = 0` or an
  equivalent retained physical observable theorem;
- `delta = 2/9` still needs the physical selected-line Berry/APS bridge;
- `v0` remains a separate support lane.
