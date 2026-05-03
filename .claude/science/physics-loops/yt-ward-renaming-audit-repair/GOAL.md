# Goal

Repair the current top audit-stack row `yt_ward_identity_derivation_theorem`
without promoting a support-only identification.

The highest-leverage defect on `origin/main` was that the row was queue rank
#1, ready, and critical while its audit ledger had `deps=[]`. The source note
imports a graph/gauge/Yukawa chain by prose labels, so the fresh-look audit
prompt could not see the load-bearing authorities.

This block turns the row into an explicit `open_gate` author hint, exposes the
load-bearing dependencies through markdown links, and updates the runner
narrative so the algebraic coefficient checks remain support evidence rather
than a theorem-grade advertisement.
