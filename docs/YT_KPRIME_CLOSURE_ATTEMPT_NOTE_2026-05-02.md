# K'(Pole) Closure Attempt

Status: open / K-prime closure attempt blocked

Claim firewall:

```yaml
actual_current_surface_status: open / K-prime closure attempt blocked
proposal_allowed: false
bare_retained_allowed: false
```

This block checks whether the current scalar determinant, ladder derivative,
Ward/Feshbach, carrier/projector, and threshold artifacts close the
interacting scalar-kernel derivative required by the same-source FH/LSZ
readout.

Available support:

- the determinant gate identifies `D'(pole)` and the load-bearing `K'(pole)`;
- the matrix eigen-derivative gate identifies `d lambda_max / d p^2`;
- the finite total-momentum derivative scout computes a finite derivative
  proxy.

Remaining blockers:

- no retained zero-mode / IR / volume limiting order for the derivative;
- residue proxy remains dependent on zero-mode, projector, and volume choices;
- Ward/Feshbach surfaces do not fix `K'(pole)` or common dressing;
- no retained scalar-kernel enhancement authority is present;
- fitting a kernel multiplier imports the missing normalization;
- physical scalar carrier/projector remains open;
- the denominator / threshold stack remains open.

Verification:

```bash
python3 scripts/frontier_yt_kprime_closure_attempt.py
# SUMMARY: PASS=9 FAIL=0
```

Boundary:

This does not close PR #230 and does not authorize `retained` or
`proposed_retained`.  `K'(pole)` is named and finite proxies exist, but the
retained theorem or direct same-source production measurement remains missing.
