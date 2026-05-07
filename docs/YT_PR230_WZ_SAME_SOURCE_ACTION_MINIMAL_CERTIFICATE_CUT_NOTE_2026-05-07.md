# PR230 W/Z Same-Source Accepted-Action Minimal Certificate Cut

Status: exact negative boundary / WZ accepted same-source action minimal certificate cut remains open.

This note packages the current W/Z fallback route as a dependency cut rather
than another route-completion summary.  The existing branch has useful
support-only pieces:

- an EW/Higgs same-source action ansatz;
- a Higgs mass-source bridge for a future centered `Phi^dagger Phi` source;
- a no-independent-top-source radial-spurion action contract;
- a conditional sector-overlap theorem for that radial spurion;
- a response-ratio identity showing how `dv/ds` would cancel.

Those pieces still do not validate the accepted same-source EW action
certificate.  The root non-shortcut certificate cut is:

- same-surface canonical Higgs operator certificate;
- current same-source sector-overlap identity or adopted radial-spurion action;
- production W/Z correlator mass-fit path certificate.

The accepted action candidate path is absent, and the builder cannot validate
without those three roots.  After the accepted action exists, the W/Z physical
readout still also needs matched top/W or top/Z covariance rows and strict
non-observed `g2` authority.

The artifact deliberately does not claim retained or proposed-retained closure.
It does not use `H_unit`, `yt_ward_identity`, observed top/W/Z/g2 values,
`alpha_LM`, plaquette/u0, reduced pilots, value recognition, or any
`kappa_s = 1`, `c2 = 1`, `Z_match = 1`, or `g2 = 1` convention.

Runner:

```bash
python3 scripts/frontier_yt_pr230_wz_same_source_action_minimal_certificate_cut.py
```

Certificate:

```text
outputs/yt_pr230_wz_same_source_action_minimal_certificate_cut_2026-05-07.json
```

The exact next action is to close one root vertex with a genuine artifact.
The cleanest route remains a same-surface canonical `O_H` certificate plus
`C_spH/C_HH` pole rows.  For the W/Z route specifically, close the accepted
action cut first, then add production W/Z response rows, matched covariance,
and strict non-observed `g2`.
