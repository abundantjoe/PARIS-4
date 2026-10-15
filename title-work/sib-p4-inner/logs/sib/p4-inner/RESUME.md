# p4-inner RESUME (updated 2026-09-27T01:10Z)
- DECL-P4-15(a) P4-M-OUT build: DONE, pushed (logs/sib/p4-inner/mout/, tools/sib/p4-inner/). Nothing is running.
- To rebuild from scratch:
  1. `fetch_w128.sh <dl> <downloads.jsonl>`
  2. `tile_w128_129.py <dl> <out> [--skip-existing]` (resumable)
  3. `tile_geom_w128.py <out> <out>/tile_geom.json`
  4. `direction_w128.py <dl> <out>/direction.json`
  5. Assemble the manifest (inline script in commit 642393418d).
- The ink TIFF was deleted after tiling, as ordered. The mesh and metadata remain in scratch.
- Open item for the orchestrator: the outward-direction conflict (see STATUS.md).
- Earlier tasks are done: RECON, tile_winding_{m2a,a}, and DECL-P4-7 items 1-2 on 1.129 um (REPORT-P47.md).

## 2026-09-27T06:40Z: DECL-P4-25 (P4-M-OUT2) is running
- Driver: `nohup tools/sib/p4-inner/run_mo2.sh <scratch>/mo2`. It is resumable: each step skips if its output exists, the tiler uses `--skip-existing`, and a strip whose `mo2/<tag>/manifest.json` exists is skipped.
- Order: 20260701183150-w126-127, then 183149-w124-125, then 183148-w122-123 (the 20260701 set, as for w128-129).
- It pushes after each strip.
- After all 3: run `arclen.py mo2/locator_geometry.json` for w128-129, w126-127, w124-125 and w122-123 (outermost first), then update STATUS.

## 2026-09-27T07:50Z: DECL-P4-25 build and locator done; nothing is running.
