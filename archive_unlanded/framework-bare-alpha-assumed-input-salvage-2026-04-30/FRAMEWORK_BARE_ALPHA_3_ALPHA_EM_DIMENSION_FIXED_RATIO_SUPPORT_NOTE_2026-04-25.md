# Bare alpha_3 / alpha_em Dimension-Fixed Ratio Support Note

Date: 2026-04-25

**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/framework-bare-alpha-assumed-input-salvage-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- Date archived: 2026-04-30
- Archive directory: `archive_unlanded/framework-bare-alpha-assumed-input-salvage-2026-04-30/`
- Audit verdict (`verdict_rationale` from [audit_ledger.json](../../docs/audit/data/audit_ledger.json), claim_id `framework_bare_alpha_3_alpha_em_dimension_fixed_ratio_support_note_2026-04-25`, `audit_status: audited_failed`, `effective_status: retained_no_go`):

> "The claim fails as a candidate retained-grade support corollary because its own primary verifier rejects the authority boundary. The algebraic identity is trivial and correct once the inputs g3^2=1, g2^2=1/(d+1), gY^2=1/(d+2), and d=3 are assumed: the bare electromagnetic inverse sum is 2d+3=9 and therefore alpha_3/alpha_em=9. But the note's load-bearing scientific claim is stronger than arithmetic; it asserts this identity is a support corollary on the retained EW-normalization surface while not promoting the Cl(3)->SM support packet. The verifier's failed `EW normalization retained lane exists` check means that required package authority was not established under the note's own audit gate. To repair the claim, either update/register the retained EW-normalization authority so the verifier can find the intended status and bare-coupling bookkeeping, or narrow the note to a pure conditional algebra lemma with explicit assumptions and no candidate retained-grade package-surface authority. Also register the primary verifier in the audit queue and add one-hop dependencies for the EW normalization lane and Cl(3)->SM support packet. What can still be safely claimed is: if the bare bookkeeping inputs are assumed, then alpha_3(bare)/alpha_em(bare)=2d+3 and equals 9 at d=3, and the bare sin^2(theta_W)=4/9 differs from SU(5)'s 3/8 by 5/72. The audit does not support retained package authority, direct low-energy alpha_3/alpha_em phenomenology, or minimal-stack promotion."

Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

---

Primary verifier:

```bash
python3 scripts/frontier_framework_bare_alpha_3_alpha_em_dimension_fixed_ratio.py
```

## Claim

On the same bare-coupling bookkeeping used by the retained EW normalization
lane, and with spatial dimension `d = 3`, the color/electromagnetic bare
coupling ratio is the integer

```text
alpha_3(bare) / alpha_em(bare) = 9.
```

More generally, with

```text
g_3^2 = 1,
g_2^2 = 1/(d + 1),
g_Y^2 = 1/(d + 2),
```

the framework gives

```text
alpha_3(bare) / alpha_em(bare)
  = g_3^2 * (1/g_2^2 + 1/g_Y^2)
  = 2d + 3.
```

The `d = 3` specialization is therefore `2d + 3 = 9`.

## Authority Boundary

This support card uses two package facts already tracked on `main`.

1. The retained EW normalization lane carries the bare coupling bookkeeping
   used by the `YT_EW_COLOR_PROJECTION_THEOREM.md` pipeline.
2. The reviewed `Cl(3) -> SM` algebraic support packet records the
   dimension-count interpretation of the same factors, including the `d+1`
   and `d+2` carrier counts.

The second item remains support-only. It is explicitly not part of the
accepted minimal-input stack. Therefore this note is a support corollary and a
package-consistency card, not a new retained front-door theorem.

## Bare Electromagnetic Combination

At the bare lattice surface the electroweak mixing relation is

```text
1/g_em^2 = 1/g_2^2 + 1/g_Y^2.
```

Substituting the support-side dimension counts gives

```text
1/g_em^2 = (d + 1) + (d + 2) = 2d + 3.
```

Thus

```text
g_em^2(bare) = 1/(2d + 3).
```

For `d = 3`,

```text
g_em^2(bare) = 1/9.
```

## Closed-Form Identities

The support corollary packages the following exact identities.

```text
(D1) 1/g_2^2 + 1/g_Y^2 = 2d + 3 = 9.

(D2) g_em^2(bare) = 1/(2d + 3) = 1/9.

(D3) sin^2(theta_W)(bare)
     = g_Y^2 / (g_2^2 + g_Y^2)
     = (d + 1)/(2d + 3)
     = 4/9.

(D4) alpha_3(bare) / alpha_em(bare)
     = g_3^2 / g_em^2
     = g_3^2 * (2d + 3)
     = 9.

(D5) alpha_em(bare)
     = g_em^2/(4 pi)
     = 1/((2d + 3) 4 pi)
     = 1/(36 pi).

(D6) 1/alpha_3(bare) + 1/alpha_2(bare) + 1/alpha_Y(bare)
     = 4 pi * (1/g_3^2 + 1/g_2^2 + 1/g_Y^2)
     = 4 pi * (2d + 4)
     = 40 pi.
```

## Dimension Fingerprint

The color/electromagnetic bare ratio is an odd integer determined by the
spatial dimension:

```text
d = 2 -> 7
d = 3 -> 9
d = 4 -> 11
d = 5 -> 13
```

Within this support bookkeeping, the integer `9` is therefore the
dimension-`3` fingerprint.

## Distinction From SU(5)

This support card is not an SU(5) unification claim. The framework bare value
is

```text
sin^2(theta_W)(bare) = 4/9,
```

while the conventional SU(5) normalization gives

```text
sin^2(theta_W) = 3/8.
```

The exact difference is

```text
4/9 - 3/8 = 5/72.
```

So the support card also records a sharp negative statement: the bare
framework normalization is not the SU(5) bare normalization.

## Relation To The Retained EW Lane

The retained EW normalization lane remains the authoritative route for the
phenomenological electroweak readout. This note does not replace that lane and
does not promote the bare integer `9` as a directly observable low-energy
ratio.

The safe use is:

```text
bare algebraic support -> retained EW normalization pipeline -> low-energy EW
comparison.
```

The unsafe use is:

```text
bare ratio 9 -> direct low-energy alpha_3/alpha_em claim.
```

The latter is not claimed here.

## What This Does Not Claim

- It does not promote the `Cl(3) -> SM` support packet into the accepted
  minimal-input stack.
- It does not derive the retained EW normalization lane independently of its
  existing authority surface.
- It does not claim a direct physical observable at `M_Z` or at `v` without
  the retained running/projection pipeline.
- It does not claim SU(5) unification or SU(5)-style bare normalization.
- It does not alter the retained `alpha_s(M_Z)` or `alpha_s(v)` derivation.

## Program Impact

The useful scientific content is an exact support-side integer fingerprint:
the framework bare electroweak and color coupling normalizations imply
`alpha_3(bare) / alpha_em(bare) = 2d + 3`, hence `9` at `d = 3`. That gives a
compact way to reuse the retained EW bookkeeping and the reviewed
`Cl(3) -> SM` support counts without overstating either surface.
