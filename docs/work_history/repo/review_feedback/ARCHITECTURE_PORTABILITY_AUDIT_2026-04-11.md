# Architecture Portability Audit

**Date:** 2026-04-11  
**Status:** proposed_retained bounded companion

## Verdict

Retainable to `main` as a bounded source-mass / attraction portability
companion.

## Exact Retained Wording

> This is a portability companion, not a standalone Newton closure. It demonstrates architecture portability of source-mass scaling and attraction sign across ordered 3D cubic, staggered 3D cubic, Wilson 3D cubic, and a 2D random geometric control row. The random geometric row is mass-scaling only and is not a distance-law comparison. The result does not establish architecture-independent full Newton closure.

## Why It Is Safe

- The architecture comparison is honest: the random geometric row is 2D and is
  used only for mass-scaling portability.
- The result stays bounded to source-mass scaling and attraction sign.
- The note does not claim full Newton closure, both-masses closure, or
  architecture-independent distance-law closure.
- Born-rule measurements are only used where the barrier implementation is
  supported, and the Wilson row remains `n/a` for that observable.

## What It Does Not Claim

- It does not claim architecture-independent full Newton closure.
- It does not claim a universal distance law on the 2D random geometric row.
- It does not claim both-masses closure.
- It does not claim a Wilson Born-rule measurement.
