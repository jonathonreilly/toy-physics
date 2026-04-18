# DM Neutrino Source-Surface Split-2 Low-Slack Upper-m Ridge Candidate

**Date:** 2026-04-18  
**Status:** coarse tested-grid positive-path reduction on split-2 low-slack; not flagship closure

## Question

After the tested broad split-2 low-slack box already failed to show a
lower-repair transport-compatible rival lane, is the remaining tested pressure
still spread across the whole box, or is it already collapsing onto a smaller
ridge?

## Answer

On the tested coarse split-2 low-slack slices, it is already collapsing toward
the upper-\(m\) boundary.

Consider the coarse tested family

\[
m \in \{-0.19,-0.18,-0.17,-0.16,-0.15,-0.14\},
\qquad
\delta \in [1.05,1.25],
\qquad
s \in [0,0.06],
\]

under the lower-repair constraint

\[
\Lambda_+(m,\delta,s) \le \Lambda_+(x_*).
\]

Then the slice-wise best lower-repair transport value increases monotonically
toward the upper-\(m\) boundary:

\[
0.872467928964,\;
0.874920988524,\;
0.876750875663,\;
0.879535247852,\;
0.881619288207,\;
0.883821045613.
\]

At the same time, the slice-wise minimum packet distance to the preferred
winning quotient decreases monotonically:

\[
0.301833484766,\;
0.290041037451,\;
0.270486034097,\;
0.259702724344,\;
0.249261594067,\;
0.239159397681.
\]

So both transport-facing objectives point in the same direction:

- the strongest lower-repair transport rival on the tested slices sits at
  \(m=-0.14\);
- the closest lower-repair packet lane on the tested slices also sits at
  \(m=-0.14\).

## More structure

The best-eta point on each tested \(m\)-slice occurs at small slack:

\[
(\delta,s)=
(1.136666666667,0.032),
(1.150000000000,0.032),
(1.163333333333,0.012),
(1.170000000000,0.028),
(1.176666666667,0.024),
(1.183333333333,0.020).
\]

The closest-lane point on each tested \(m\)-slice occurs exactly at the slack
floor:

\[
(\delta,s)=
(1.143333333333,0),
(1.150000000000,0),
(1.163333333333,0),
(1.170000000000,0),
(1.176666666667,0),
(1.183333333333,0).
\]

So the tested residual pressure is no longer a generic 3-real box effect.
It is already being pushed toward an upper-\(m\), low-slack ridge, with the
closest-lane points even concentrating on the slack floor \(s=0\).

## Interpretation

This is a **positive-path** reduction, not just another obstruction note.

It says the constructive carrier target is smaller than:

> the whole tested split-2 low-slack box.

On the current science branch it is already more like:

> the upper-\(m\) low-slack ridge near \(m=-0.14\), especially its
> smallest-slack part.

That is the right direction for a final carrier theorem, because it compresses
the residual positive-path threat from a 3-real box toward a much thinner
boundary object.

## Boundary

This is still a coarse tested-grid ridge candidate, not interval-certified
exact-carrier closure, and not flagship closure.
