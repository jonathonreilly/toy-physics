# Assumptions And Imports

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| Same-surface positive scalar-source Stieltjes measure | Makes pole residue an atom mass | support-only | Block58 plus Stieltjes gate | yes | yes | derive contact-subtracted scalar measure and rerun monotonicity/Hankel checks | open |
| Finite rows are actual moments | Allows truncated moment theory | unsupported import on current surface | current finite-shell/source rows | yes | yes | future moment certificate with source coordinate, zero-source limit, contact subtraction, covariance | open |
| Pole coordinate and support shift `lambda=s-m_pole^2>=0` | Makes localizing rank drop physically meaningful | unsupported import | no current pole/gap certificate | yes | yes | scalar pole/gap theorem or direct pole rows | open |
| Exact or interval moments to flat order | Enables PSD/rank/flat-extension checks | unsupported import | current prefix only | yes | yes | exact algebraic or interval-certified moment production | open |
| Flat extension or extremal consistency | Fixes finite atomic representing measure | literature theorem | Curto-Fialkow / Curto-Fialkow-Moeller | yes | yes | same-surface certificate using these theorems | bridge only |
| Localizing rank drop at `lambda=0` | Counts the pole atom | literature theorem plus same-surface data | Curto-Fialkow localizing theorem | yes | yes | future rank certificate | open |
| Threshold/FVIR/contact authority | Prevents soft-continuum/contact ambiguity | unsupported import | Block59/Carleman gates keep this open | yes | yes | FVIR/contact theorem or direct rows | open |
| Canonical `O_H` or physical-response bridge | Converts source atom into physical scalar residue authority | unsupported import | PR230 source-Higgs/WZ bridge remains open | yes | yes | `C_sH/C_HH`, Gram purity, or W/Z response rows | open |
| Forbidden-input firewall | Prevents hidden normalization/target imports | exact support | this runner and parent firewalls | yes | yes | keep explicit in future certificate | satisfied |
