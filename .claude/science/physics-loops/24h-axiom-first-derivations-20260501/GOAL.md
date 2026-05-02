# GOAL — 24h Axiom-First New Derivations Campaign

**Date:** 2026-05-01
**Slug:** `24h-axiom-first-derivations-20260501`
**Mode:** campaign (24h work budget, unattended)
**Target:** best-honest-status with priority on retained-positive new derivations

## Goal

Produce NEW first-principles derivations from the framework's `A_min`
(`docs/MINIMAL_AXIOMS_2026-04-11.md`) and the existing axiom-first retained
foundations (RP, spectrum cond, CPT, spin-statistics, cluster decomp,
Coleman-Mermin-Wagner, lattice Noether, BH 1/4 carrier).

Each block must:

- target a result that is **NOT yet in the repo** (verified by ls/grep);
- derive it rigorously from `A_min` plus retained corollaries;
- avoid hidden imports beyond the explicit admitted-context literature
  conventions allowed for the bridge in question;
- ship a runner that algebraically/numerically checks the derivation;
- carry honest claim-status under
  `docs/repo/CONTROLLED_VOCABULARY.md`;
- open one review PR per coherent science block.

## Out of scope

Do NOT redo or compete with work already on `main` or in active branches:

- Planck Pin (closed, sixth pass via Wald-Noether)
- Koide δ Brannen / Q closure (V1 + V2 + V7 attempts active)
- CKM mass-ratio routes (closed via taste-staircase)
- DM eta freezeout-bypass (bounded theorem)
- y_t mass-ratio routes (retained via Ward identity)
- Higgs mass derivation (m_H = 119.8 / 125.1 GeV already)

## Why these targets

The repo's Apr 29 axiom-first lineup proved RP, spectrum cond, CPT,
spin-statistics, cluster decomposition, lattice Noether,
Coleman-Mermin-Wagner, and the BH 1/4 carrier composition.
That foundation makes the following standard physics theorems
directly accessible from `A_min` plus retained results:

- **KMS condition** (thermal-state characterization) — directly from RP +
  spectrum cond
- **Hawking temperature** T_H = κ/(2π) — from KMS + framework GR Killing
  horizon
- **Bekenstein bound** S ≤ 2πRE — from area-law + spectrum cond
- **First law of BH mechanics** — from Wald-Noether + BH 1/4 + Hawking T_H
- **Microcausality** [O(x),O(y)]=0 spacelike — from lattice locality +
  cluster decomp + spectrum cond
- **Unruh temperature** T_U = a/(2π) — from KMS + Lorentz kernel
- **Stefan-Boltzmann** u = σT⁴ — from Planck distribution (KMS) + photon
  spectrum
- **Reeh-Schlieder cyclicity** — from spectrum cond + cluster decomp
- **Generalized Second Law** — from BH 1/4 + KMS monotonicity
- **Birkhoff theorem** (vacuum spherical → static) — from framework GR

These results would substantially complete the framework's axiom-first
foundational physics lineup and bring black-hole thermodynamics, thermal
QFT, and locality theorems into the retained / proposed-retained surface.

## Stop conditions

- runtime exhausted (24h budget; in-session this means context budget);
- max cycles exhausted (~10 blocks);
- queue exhausted (every viable target is blocked by human-judgment, missing
  retained dep, or tooling failure);
- worktree externally changes.

Per-block no-go, demotion, dirty PR, or missing GitHub auth is **not** a
campaign stop. Demote, checkpoint, pivot.
