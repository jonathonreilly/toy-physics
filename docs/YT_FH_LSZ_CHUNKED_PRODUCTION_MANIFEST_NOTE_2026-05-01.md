# PR #230 FH/LSZ Chunked Production Manifest

**Status:** bounded-support / FH-LSZ chunked production manifest

## Question

The checkpoint-granularity gate blocks whole-volume foreground launch: the
smallest joint FH/LSZ shard is projected at `180.069` hours and current
`--resume` is whole-volume only.  This block asks whether any production
subroute can be scheduled inside a 12-hour foreground window without treating
partial output as evidence.

## Result

For `L12_T24`, yes as launch planning only.  Splitting the volume into
independent production-targeted chunks with `16` saved configurations per
chunk gives:

```text
conservative L12 chunk estimate: 11.3186 hours
chunks needed for 1000 saved configurations: 63
```

The commands still use production-targeted FH/LSZ observables:

```text
--scalar-source-shifts -0.01,0.0,0.01
--scalar-two-point-modes '0,0,0;1,0,0;0,1,0;0,0,1'
--scalar-two-point-noises 16
```

This does not solve the whole production route.  Even under a minimum
rethermalized chunk estimate, the larger volumes remain outside the foreground
window:

```text
L16 minimum estimate: 27.1003 hours
L24 minimum estimate: 137.195 hours
```

## Claim Boundary

This is a launch manifest only:

```text
proposal_allowed: false
```

No chunk is production evidence until it completes as `metadata.phase ==
"production"` and is combined by a separate multi-chain FH/LSZ postprocess
certificate.  The scalar pole derivative, FV/IR/zero-mode control, and retained
proposal gate remain required.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_chunked_production_manifest.py
python3 scripts/frontier_yt_fh_lsz_chunked_production_manifest.py
# SUMMARY: PASS=8 FAIL=0
```
