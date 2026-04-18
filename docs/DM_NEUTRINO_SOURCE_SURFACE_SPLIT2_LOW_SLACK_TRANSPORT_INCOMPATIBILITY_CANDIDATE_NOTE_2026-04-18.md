# DM Neutrino Source-Surface Split-2 Low-Slack Transport Incompatibility Candidate

**Date:** 2026-04-18  
**Status:** tested broad split-2 low-slack box stays transport-incompatible under the lower-repair constraint; not flagship closure

## Question

The split-2 broad-bundle pressure was already reduced to the low-slack interval

\[
0 \le s \le s_*^{\mathrm{edge}} \approx 0.195041737783
\]

on the tested broad bundle. Does the wider tested broad split-2 low-slack box

\[
m     \in [-0.19,-0.14],\qquad
\delta\in[-2.5,2.5],\qquad
s     \in[0,s_*^{\mathrm{edge}}],
\]

contain any point with

\[
\Lambda_+(m,\delta,s) \le \Lambda_+(x_*)
\]

that looks transport-compatible with the preferred recovered lane?

## Preferred reference lane

The preferred recovered point remains

\[
x_*=(1.021038842009,\;1.380791428982,\;0.215677476525),
\]

with

\[
\Lambda_+(x_*) = 1.586874714730,
\qquad
\eta_{\mathrm{best}}(x_*)/\eta_{\mathrm{obs}} = 1.052220313052,
\]

and preferred winning packet quotient

\[
Q_{\mathrm{pref}}
= (0.035644251472,\;0.035644362528,\;0.928711385999).
\]

## Coarse tested-box scan

On a coarse tested split-2 low-slack scan over

- \(m \in \{-0.19,-0.18,\dots,-0.14\}\),
- \(\delta \in [0.9,1.15]\),
- \(s \in [0,s_*^{\mathrm{edge}}]\),

no sampled point with

\[
\Lambda_+(m,\delta,s)\le\Lambda_+(x_*)
\]

reaches \(\eta/\eta_{\mathrm{obs}} \ge 1\).

The best coarse lower-repair transport point found is

\[
(m,\delta,s)=(-0.14,\;1.15,\;0.004876043445),
\]

with

\[
\Lambda_+ = 1.558622195198,\qquad
\eta_{\mathrm{best}}/\eta_{\mathrm{obs}} = 0.879221532368,
\]

still well below \(1\).

The closest coarse sampled winning transport column to the preferred quotient
still has distance

\[
\left\| \operatorname{sort}(P_{\mathrm{best}})-Q_{\mathrm{pref}} \right\|_2
= 0.250560685550.
\]

## Seeded global-search refinement on the full tested box

I then searched the full tested broad split-2 low-slack box

\[
m     \in [-0.19,-0.14],\qquad
\delta\in[-2.5,2.5],\qquad
s     \in [0,s_*^{\mathrm{edge}}],
\]

with a repair penalty enforcing the lower-repair condition
\(\Lambda_+ \le \Lambda_+(x_*)\).

Across seeded global searches:

- the strongest lower-repair transport rival found is near
  \[
  (m,\delta,s)\approx(-0.1400007,\;1.18838072,\;0.02114129),
  \]
  with
  \[
  \Lambda_+ \approx 1.586837712386,\qquad
  \eta_{\mathrm{best}}/\eta_{\mathrm{obs}} \approx 0.884523453538,
  \]
  and winning column
  \[
  \operatorname{sort}(P_{\mathrm{best}})
  \approx (0.04077956,\;0.20726092,\;0.75195952);
  \]

- the closest lower-repair winning packet lane found is near
  \[
  (m,\delta,s)\approx(-0.140104496,\;1.18883523,\;0.000069563584),
  \]
  with
  \[
  \Lambda_+ \approx 1.586842751739,\qquad
  \eta_{\mathrm{best}}/\eta_{\mathrm{obs}} \approx 0.883603974097,
  \]
  and distance
  \[
  \left\| \operatorname{sort}(P_{\mathrm{best}})-Q_{\mathrm{pref}} \right\|_2
  \approx 0.233468501596.
  \]

So even after widening from the tested edge to the tested broad split-2
low-slack box, the lower-repair region still does **not** look transport
compatible with the preferred recovered lane.

## Conclusion

On the tested broad split-2 low-slack box:

- no lower-repair sample reaches \(\eta/\eta_{\mathrm{obs}} \ge 1\),
- the strongest tested lower-repair transport rival stays below
  \(0.884523453538\),
- and the closest tested lower-repair packet lane still stays at distance at
  least \(0.233468501596\) from the preferred quotient.

That does **not** prove exact-carrier closure. But it sharpens the carrier-side
blocker again:

> a lower-repair, transport-compatible rival lane is not visible even on the
> tested broad split-2 low-slack box.

So the remaining carrier-side theorem target is narrower than “control the
whole split-2 box.” It is now:

> certify interval-style exclusion or dominance on the exact carrier inside the
> residual split-2 low-slack region.

## Boundary

This is still a numerical incompatibility candidate on the tested broad box,
not an interval-certified exclusion theorem on the exact carrier, and not
flagship closure.
