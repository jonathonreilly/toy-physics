# yt_ew M-Residual Stretch Attempt: Sharpened Obstruction Note

**Date:** 2026-05-02
**Type:** stretch_attempt_outcome (negative; sharpened obstruction)
**Claim scope:** The naive interpretation of the M residual — "CMT mean-field
factorization absorbs the singlet channel S and leaves only the adjoint
channel C" — is **NOT** supported by an explicit channel-level bookkeeping.
The runner verifies that under U → u_0 V factorization, **both S and C inherit
the same u_0² factor uniformly**. The physical channel selection (singlet vs
adjoint) must therefore come from elsewhere — specifically the framework's
explicit EW current Wilson-line construction, which is currently implicit
on the retained surface.
**Status:** stretch attempt outcome (negative); sharpens the named obstruction
for future closure work.
**Loop:** `audit-backlog-campaign-20260502`
**Cycle:** 5 (planned per HANDOFF.md)
**Branch:** `physics-loop/yt-ew-m-residual-stretch-attempt-20260502`
**Runner:** `scripts/yt_ew_m_residual_channel_check.py`
**Log:** `outputs/yt_ew_m_residual_channel_check_2026-05-02.txt`

## Background

The framework's package-level "9/8 EW coupling correction" decomposes via
[`EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01`](EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md)
into:
- **(F)** an exact group-theory ratio `(N_c² − 1)/N_c² = 8/9` at N_c = 3
  (retained, derived inline via Fierz identity);
- **(M)** a matching rule: "the physical EW vacuum polarization, after CMT
  mean-field factorization U → u_0 V, projects onto the adjoint channel
  C(x, y), not onto the total Tr_color[G(x, y) G(y, x)]" — currently a
  structural input, not derived.

The audit-backlog campaign queued cycle 5 as a stretch attempt to derive
(M) from retained primitives. This note records the outcome.

## Stretch attempt setup

The Fierz channel decomposition (from the cited note) is:

```text
Tr_color[G(x, y) G(y, x)] = (1/N_c) |Tr G(x, y)|²  +  2 Σ_A |Tr[G(x, y) t^A]|²
                          ≡ S(G)             +  C(G)                       (1)
```

The naive (M) reading: under CMT factorization U → u_0 V, the singlet
S is absorbed by u_0 powers (mean-field improvement), and only the
adjoint C remains in the physical correlator.

The runner tests this naive reading explicitly.

## Key finding: CMT does NOT distinguish singlet from adjoint

The runner verifies (Test 5):

```text
G_full = u_0 · G_V    ⇒    S(G_full) = u_0² · S(G_V),    C(G_full) = u_0² · C(G_V)    (2)
```

**Both channels inherit the same u_0² scaling.** The CMT factorization
acts uniformly on the propagator and does not distinguish singlet from
adjoint at the channel level.

This contradicts the naive M reading. The physical channel selection
(if any) is NOT at the CMT factorization level.

## Where the actual selection must come from

Given that CMT alone is channel-blind, the physical (M) selection must
come from one of:

(A) **The definition of the physical EW current.** If the framework's
    lattice EW current is constructed as an *explicitly adjoint-projected*
    bilinear at the lattice level (rather than a color-singlet bilinear),
    then ⟨J^EW J^EW⟩ would automatically be C, not S+C. This is a
    *construction choice* in the framework's lattice-current primitive,
    not a derivation.

(B) **Renormalization convention.** If the bare singlet S is "absorbed"
    by the renormalization of the link u_0 in a specific RG-improved
    sense (e.g., the link improvement u_0^n_link extracts the singlet
    content additively rather than multiplicatively), then the
    improved physical correlator would equal C alone. This requires a
    careful renormalization-convention argument that is not visible in
    the channel-level bookkeeping.

(C) **Disconnected-vs-connected interpretation.** If "physical EW vacuum
    polarization" is defined as the *connected* two-point function (with
    disconnected vacuum bubbles subtracted), and S happens to be the
    disconnected piece while C is the connected piece, then the
    interpretation of (M) reduces to a connected-correlator definition.
    However, the Fierz decomposition (1) shows BOTH S and C come from
    the SAME single color trace Tr[G G] — they are both connected at
    the gauge-trace level. So (C) is not a clean resolution.

## Sharpened obstruction

Before this stretch attempt, (M) was named as: "physical EW vacuum
polarization projects onto adjoint after CMT factorization."

After this stretch attempt, (M) sharpens to:

> **Sharpened (M):** The framework's lattice EW current `J^EW_μ(x)` is
> defined such that the contraction `⟨J^EW_μ(x) J^EW_ν(y)⟩` mechanically
> selects the adjoint channel `C(x, y) = 2 Σ_A |Tr[G(x, y) t^A]|²`
> rather than the total `Tr_color[G(x, y) G(y, x)]`. CMT factorization
> alone is channel-blind (it scales both S and C by u_0² uniformly);
> the channel selection is a property of the EW current's Wilson-line
> construction at the lattice level, not of CMT improvement.

The remaining work for full closure of (M):

1. **Identify the framework's lattice EW current Wilson-line construction.**
   Currently implicit on the retained surface; needs to be a named
   primitive note (probably citing
   [NATIVE_GAUGE_CLOSURE_NOTE](NATIVE_GAUGE_CLOSURE_NOTE.md) or
   [GRAPH_FIRST_SU3_INTEGRATION_NOTE](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
   — both retained_bounded).

2. **Prove the channel selection from that construction.** Show that the
   bilinear `J^EW_μ J^EW_ν` reduces to the adjoint contraction by
   construction. This may follow from:
   - Color-blindness of the EW current (no SU(3) index)
   - Wick contraction structure
   - Wilson-line orientation in the framework's lattice action

3. **Distinguish bare from improved correlator.** If the singlet is
   absorbed by RG improvement (as in standard tadpole-improvement
   schemes), the precise renormalization convention needs to be
   stated as part of (M).

## What this stretch attempt closes

It closes the *naive* M interpretation as DISPROVEN: CMT factorization is
channel-blind. This rules out an entire class of would-be closures and
focuses the remaining work on the EW current construction (point 1 above).

This is a NEGATIVE stretch attempt outcome with structurally useful
content. The runner's 7/7 PASS verifies the channel bookkeeping is
internally consistent and that the disproof of the naive M reading is
exact at machine precision.

## Cited authorities (one hop)

- [`EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md`](EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md)
  — `effective_status: retained_bounded`. Provides:
  - The exact Fierz channel decomposition (equation 3.1)
  - The named matching rule (M) as a structural input

This is the only one-hop dependency.

## Hypothesis set used

- `ew_current_fierz_channel_decomposition_note_2026-05-01` (retained_bounded):
  provides (F) and the (M) structural-input statement.

No fitted parameters. No observed values. No physics conventions admitted
beyond the cited Fierz channel decomposition.

## Honest scope

Stretch attempt outcome: NEGATIVE (CMT alone insufficient for M closure).
Sharpened obstruction: the EW current construction is the missing primitive.

This note is a **stretch_attempt_outcome** classification — it is NOT a
positive theorem nor a no-go. It documents:
1. That the naive M interpretation has been ruled out by explicit
   channel-level bookkeeping.
2. The sharpened obstruction (now reduced to a single named question
   about the EW current construction).
3. The path forward for future closure work.

```yaml
claim_type_author_hint: stretch_attempt_outcome
claim_scope: "Naive M (CMT absorbs singlet, only adjoint survives) is disproven by channel-level bookkeeping; sharpened obstruction reduces to: which channel does framework EW current construction project on?"
upstream_dependencies:
  - ew_current_fierz_channel_decomposition_note_2026-05-01 (retained_bounded)
admitted_context_inputs:
  - none beyond the cited Fierz channel decomposition note
resolution_status: open (closure requires explicit framework EW current Wilson-line primitive)
```
