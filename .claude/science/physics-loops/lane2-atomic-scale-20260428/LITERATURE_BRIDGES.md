# Lane 2 Literature Bridges

**Updated:** 2026-05-01T10:53:48Z

No new external literature was imported at loop start.

The selected QED-threshold route may use the standard one-loop gauge-running
form and decoupling logic as an admitted standard QFT bridge. This is already
the style used by `docs/SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md`.

Any numerical value used only to compare against the current scaffold, such as
`1/alpha(0) = 137.035999084` or the Rydberg energy, remains a comparator and
must not be treated as a framework-derived input.

## Block 01 Usage

The QED threshold firewall uses the standard one-loop inverse-coupling running
form as an admitted standard QFT bridge:

```text
1/alpha(Q_low) = 1/alpha(Q_high) + (b_active / 2 pi) log(Q_high / Q_low)
```

This bridge is used only to prove threshold sensitivity and underdetermination.
It does not derive `alpha(0)`. `M_Z`, `m_e`, and `1/alpha(0)` appear only in
the physical-scale comparator section of the note/runner.
