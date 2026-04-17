# Architecture Options

This file lists the current highest-value architecture moves. The goal is to
change asymptotics without breaking retained core behavior.

## Freeze first

Hold fixed unless theory forces a change:

- corrected `1/L^p` propagator
- Born-safe interference package
- `k=0 -> 0`
- retained unitary gravity sign

## Gravity-side architecture options

These are good candidates because they target path-sum asymptotics, not just
another microscopic parameter sweep.

### 1. Path-multiplicity-renormalized action

Idea:

- renormalize local action by nearby path multiplicity so many nearly identical
  microscopic routes do not all contribute as independent full-strength pushes

Why it helps:

- directly targets the saturation / threshold collapse

### 2. Packet-local coarse-grained action sampling

Idea:

- sample action over packet-local coarse-grained route bundles rather than raw
  edge-by-edge sums

Why it helps:

- matches the current empirical win of packet-local action spread

### 3. Multiscale propagator

Idea:

- define a coarse-grained propagation rule in which clusters of nearly
  equivalent microscopic paths contribute through one effective branch

Why it helps:

- turns the current “many routes average together” explanation into an explicit
  model choice

## Decoherence-side architecture options

These are good candidates because they scale environment capacity with branch
diversity instead of forcing all histories through one small global label space.

### 1. Many local environment ancillas

Idea:

- record branch information in many local environment degrees of freedom instead
  of one small shared register

### 2. Edge / angle-sector records

Idea:

- let the environment store local directional or sector-resolved traversal
  information

### 3. Path-history histogram records

Idea:

- let the environment accumulate coarse path-history counts rather than a single
  branch label

### 4. Continuous bath variable

Idea:

- replace finite bins with a continuous or effectively unbounded environment
  state

### 5. Irreversible regional coarse-graining

Idea:

- trace over a spatial region or persistent environment sheet, not one
  compressed global tag

## What not to prioritize next

Gravity:

- more raw `k` sweeps
- reopening the propagator without a scaling argument

Decoherence:

- another `8`-bin or `12`-bin finite-register variant
