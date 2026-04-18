# DM Neutrino Source-Surface Split-2 Upper-m Slack-Floor Endpoint Candidate

**Date:** 2026-04-18  
**Status:** tested-line positive-path reduction on split-2; not flagship closure

## Question

After the tested split-2 low-slack search is already pushed toward the
upper-\(m\) ridge, does the remaining lower-repair pressure on that tested
ridge still occupy a whole interval, or does it collapse to one endpoint?

## Answer

On the tested upper-\(m\) slack-floor line, it collapses to one endpoint.

Restrict to

\[
m=-0.14,\qquad s=0,
\]

and define \(\delta_{\mathrm{edge}}\) by

\[
\Lambda_+(-0.14,\delta_{\mathrm{edge}},0)=\Lambda_+(x_*).
\]

Numerically this gives

\[
\delta_{\mathrm{edge}} \approx 1.188955544069.
\]

At that tested endpoint:

\[
\Lambda_+ = \Lambda_+(x_*),
\qquad
\eta_{\mathrm{best}}/\eta_{\mathrm{obs}} \approx 0.883631424817,
\]

with winning packet quotient

\[
\operatorname{sort}(P_{\mathrm{best}})
\approx (0.04461472,\;0.19592604,\;0.75945924),
\]

and packet distance to the preferred quotient

\[
\left\| \operatorname{sort}(P_{\mathrm{best}})-Q_{\mathrm{pref}} \right\|_2
\approx 0.233274467128.
\]

## Monotone reduction on the tested feasible interval

On the tested interval

\[
\delta \in [1.05,\delta_{\mathrm{edge}}],
\]

with \(m=-0.14\) and \(s=0\):

- repair is strictly increasing in `delta`,
- the winning transport column stays on the same label,
- the best lower-repair transport value is strictly increasing in `delta`,
- the packet distance to the preferred quotient is strictly decreasing in
  `delta`.

In particular:

\[
\eta_{\mathrm{best}}/\eta_{\mathrm{obs}}
\text{ rises from } 0.861112802893
\text{ to } 0.883631424817,
\]

while

\[
\left\| \operatorname{sort}(P_{\mathrm{best}})-Q_{\mathrm{pref}} \right\|_2
\text{ falls from } 0.437025762194
\text{ to } 0.233274467128.
\]

So on this tested feasible interval, both transport-facing objectives are
driven to the **same** endpoint \(\delta_{\mathrm{edge}}\).

## Interpretation

This is a real positive-path reduction.

The tested residual carrier pressure is no longer:

1. the whole split-2 low-slack box,
2. nor even the whole upper-\(m\) low-slack ridge,
3. but the single tested slack-floor endpoint on that ridge.

So the constructive target is now much smaller:

> the residual exact-carrier part near the tested endpoint
> \((m,s,\delta)=(-0.14,0,1.188955544069)\).

That still does not prove closure, because the exact carrier has not been
certified there. But it is the sharpest positive-path carrier localization yet
on this branch.

## Boundary

This is still a tested-line endpoint candidate, not exact-carrier closure, not
interval-certified exclusion, and not flagship closure.
