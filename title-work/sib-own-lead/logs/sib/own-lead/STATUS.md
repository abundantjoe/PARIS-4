# own-lead STATUS (DECL-P4-23, P4-OWN)
Updated: 2026-09-27 ~11:05Z (step 1 DONE; RECIPE draft; waiting on label shards)
State: step 1 complete. Tools: tools/sib/own-lead/{own_common,build_patches,train,infer,auc,timing,test_own}.py.
Synthetic unit tests: ALL OK (AUC exact vs brute force with ties; derangement no fixed point; 3 contiguous near-equal fold groups; straddling patches excluded from F arms; label shard overlapping X refused; patches never touch X or uncertified cells; shards byte-deterministic; resume after kill bit-identical (max weight diff 0.0); windowed inference = whole-image inference (diff 0.0) at HALO 160).
Fact: w028-037 2.4 um surface volume EXISTS (109 x 71600 x 174640) -> T includes w028-037.

## Timing test (DECL-P4-23 item 4; T only: w010-027 r4 c2, random labels; 4 vCPU fp32; logs/sib/own-lead/p4own/timing.json)
| cfg | params | RF radius | train s/step B16 P128 / P192 / P256 | infer min/tile (compute, halo 160) |
|---|---|---|---|---|
| A (8,16,32; head 32, dil 1-8) | 232,697 | 151 px | 0.50 / 1.41 / 2.70 | 1.7 |
| B (8,24,48; head 48) | 550,937 | 159 px | 0.96 / 2.84 / 5.28 | 3.4 |
S3 read 40.5 MB/s (132 chunks, 0 missing).
End-to-end tile (T tile w010-027 r4 c2, valid 1.0, random weights, output discarded, no map written): 4.89 min incl. S3 reads, peak RSS 3.75 GB, 0 missing chunks -> well under the 20 min bar.
(An earlier run was INVALID: two timing processes contended for the CPU; discarded.)
Pick (to be frozen in RECIPE.md): cfg A, input 256 px, loss core 192 px (margin 32), output stride 4, batch 16, 2500 steps
= ~2.1 h/arm incl. loading; tile inference ~5 min (WIN 1024, HALO 160). Cap 4000 stored patches (4.06 MB each).

p4-excl T certification landed (a4ea355, independent check all pass): 229 T tiles with certified px (w010-027: 40, c0-c4 mostly;
w028-037: 189). NOTE w028-037 tile size is 8301 px (not 8343): code made per-segment (tests ALL OK).
Geometry-only count (logs/sib/own-lead/p4own/geocount.json): fully certified 256-px windows (core 192) with core mesh-valid >= 50 %:
w010-027 2,485; w028-037 192,654 (217 tiles). Labels will restrict this; the 4000-patch cap (ink-first) will likely bind.
Labels: p4-excl label_shards.py written to our x4 interface (7584660); label shards not yet pushed.
RECIPE_DRAFT.md + recipe.json pushed (everything fixed except label-dependent counts/hashes/F tile lists). Fold groups frozen
from the 229 certified T tiles (77/76/76); train.py now reads them from recipe.json (tests ALL OK).
Labels landed (p4-excl 7ea9f34). FEASIBLE: 45,262 ink 64-px cells (bar 2000).
Build: 4000 patches, 17.04 GB, build_manifest sha256 c567393d... RECIPE.md FROZEN at 6b5bdc5, sha256 377784c2bd8dd8617f38ae0e054fbe37684004f6e0d105852e84e16c16a6dfb8 (pushed before any training step).

## Arms (started 13:05Z)
| arm | where | state | steps | ETA | held-out AUC | tiles pushed |
|---|---|---|---|---|---|---|
| S1 | own-lead | trained 16:20Z (loss 0.563); predicting X (col. -1 first; ~7.9 min/tile at 2 threads; 88 tiles ~12 h) | 2500/2500 | X done ~04:30Z | - | 2 @16:38Z |
| F1 NULL S2 F2 F3 S3 | own-lead (fallback, orchestrator 15:02Z: the six workers are blocked on owner permission for cross-branch checkout; ASKs on their branches) | F1 training since 16:21Z; others queued (run_arms.py) | F1 175/2500 @16:41Z | ~4.5 h train/arm at 2 threads (F1 ~20:50Z) | - | 0 |
Note: RECIPE-A1 (c23037b) = train.py lazy shard loader; the first S1 launch was OOM-killed at data loading (0 steps). Recipe unchanged.
Blockers: none.

Concurrency check (orchestrator 15:02Z): 2+2 threads, F1 train 6.42 s/step (4-thread alone 4.45 -> 0.69) + S1 infer ~7.9 min/tile (alone 4.9 -> 0.62): combined 1.31x sequential -> kept concurrent.

Reorder (orchestrator 20:39Z, DECL-P4-23-A1 scheduling; G1 is the critical path): run_arms.py edited only (sha256 07633449969a8f889898d447edc29b8d270278334749eba24f5aa1e084f19980).
- Predictor: per-tile priority F1 held-out -> F2/F3 held-out (once trained) -> rest of S1 X -> NULL -> S2 -> S3; AUC right after each F arm's 24 tiles.
- Trainer: F2, F3, NULL, S2, S3. F1 trained 20:37Z (loss 0.569).
- NULL had started at 20:37:11Z and was stopped at ~20:43Z before its first 15-min checkpoint (no checkpoint to keep); it restarts from step 0 after F3 (deterministic schedule).
- The S1 tile in progress at 20:40Z was allowed to finish; the new driver commits it.

Reschedule (orchestrator 21:11Z, wall-clock priority): run_arms.py only (sha256 2722d3ac53319d76d7f735ca84cf21d91fb5cdc04e0954cafe3357dc8be01a8c). Two 2-thread slots, one priority queue:
- F1 held-out 24 + AUC -> F2 train (running, adopted) -> F3 train concurrently (RAM rule: MemAvailable >= peak train RSS + 2 GB; at 21:15Z F2 VmHWM 7.4 GB (anon 1.85 GB, rest shared mmap), available 12.2 GB -> passes) -> F2/F3 held-out + AUCs -> S2 + NULL train concurrently -> S3 train
  -> S2/NULL title slot (col. -1 + c14-c17 r0-r5, 30 each) -> NULL 72 held-out + AUCs -> c11-c13 r2-r5 -> c18-c19 -> rest -> S3 maps -> remaining S1 X (idle slots).
- Status at 21:15Z: F1 held-out 4/24 pushed; F2 step ~300/2500; S1 X 32/88 pushed (paused).

FINAL SHOT (orchestrator 22:03Z, DECL-P4-25-A6): F2 paused at 22:06Z (checkpoint 21:57Z kept; resumes); predictor stopped after its current F1 tile.
S1 inference on 30 Region O tiles (regionO_S1_target2.json sha256 877d6ee0..., verified) with 4 threads, infer.py unchanged, outputs logs/sib/own-s1/maps_O/.
Both 2.4 um surface volumes and meshes exist and load (w122-123 zarr 109x79040x137360, w124-125 109x83920x143360; 0 missing chunks in a probe).
Config only: own_common.py SEGS/TILE_PX gained the two strips (T 8324 / 8349 from p4-inner mo2 grid.json); new sha256 f8850058e53e29ddab177d0a1aac85dece6391360e3b2679b7d98fc36ab0eb8e. Driver: tools/sib/own-lead/run_O.sh.
run_arms.py (00:58Z): deletes infer.py's band checkpoint after each committed tile (disk hit the 5 GB floor at 00:53Z; 73 stale checkpoints = 4.7 GB removed). sha256 1d8f83efc956ab4180924b8a4c13f4ebfc73dc5ba662fcad79dc355e3788d1f8.
FINAL SHOT DONE 00:55Z: 30/30 S1 Region O maps pushed in logs/sib/own-s1/maps_O/ (3 control w122-123 + 27 w124-125, declared order). Scheduler resumed (F2 from checkpoint).

## Progress 2026-09-28 13:50Z (after a container restart at ~13:48Z; scheduler relaunched, all steps resume)
| arm | trained | maps pushed | held-out pixel AUC (auc.py) |
|---|---|---|---|
| F1 | yes | 24/24 held-out | 0.9418 (ink px 22.7 M, bg 47.1 M) |
| F2 | yes | 24/24 held-out | 0.9415 (86.8 M / 264.3 M) |
| F3 | yes | 24/24 held-out | 0.9401 (23.8 M / 90.5 M) |
| S1 | yes | X 34/88 (+ Region O 30/30) | - |
| NULL | yes | 0 (next: title slot 30, then 72 held-out + AUCs) | pending |
| S2 | yes (13:47Z) | 0 (next: title slot 30) | - |
| S3 | training (restarted from step 0 at 13:48Z restart; no checkpoint yet) | 0 | - |
2026-09-30 03:40Z: all 7 models present in /work/own; run_arms.py (sha256 58de5abfe9a6f78a4d1bd7bdf75922a063998e87c6f0d100e5bc78f58dbfd874) queue = A7 seed check (S2/S3/NULL x 6 regionO_seed_check tiles -> maps_O) -> S3 c11-c17 r0-r5 (42) -> S2/S3/NULL x other 24 Region-O tiles -> previous queue; kept alive by detached watchdog.sh (no in-container mechanism survives a container restart: PID 1 is process_api, no cron/systemd; after a restart one turn must run: cd /home/user/dominion && setsid nohup tools/sib/own-lead/watchdog.sh >> /work/own/watchdog.log 2>&1 < /dev/null &).
2026-09-30 03:37Z (DECL-P4-23-A4): run_arms.py (sha256 9b42dba796de3206ffa5b6e6a392c8dc7877734d146e6b42057d1b76b2248c1d) queue = 18 seed-check maps -> S1 54 rest-of-X (X_rest_S1.json map_order, sha256 ba629969...) -> S3 42 -> S2/S3/NULL rest of Region O -> previous queue; watchdog unchanged.
2026-09-30 04:17Z liveness: container restarted (~04:15Z, uptime 0); last progress 03:39Z (S2/S3 w122-123 r4c5 at band 7/9, never finished); no unpushed commits, no uncommitted tiles; watchdog + scheduler relaunched 04:16Z from saved band checkpoints.
2026-09-30 04:22Z: harness-tracked background waiter started (exits when /work/own/ALL_DONE exists or the watchdog dies); scheduler unchanged since the 04:16Z relaunch.
2026-09-30 04:23Z: another container restart ~04:21Z (3 min after idle; S2+S3 w122-123 r4c5 pushed 04:18Z, 2/18 seed maps); watchdog relaunched (pid 483) with a harness-tracked background waiter on it (exits on ALL_DONE or watchdog death).
2026-09-30 15:28Z (DECL-P4-25-A8 item 2): scheduler paused (watchdog + run_arms stopped, resumable); run_O2.sh makes the 32 S1 ext-pool maps (regionO_S1_ext_pool.json sha256 49fde765...) at 4 threads into maps_O, then restarts the watchdog. run_arms.py unchanged.
2026-09-30 15:40Z (DECL-P4-25-A9): after the 32 A8 pool maps, run_O3.sh makes the 65 S1 maps of regionO_S1_rest.json (sha256 71283a59...) into maps_O, holding /work/own/PAUSE so the watchdog idles; then removes PAUSE and the queue resumes. watchdog.sh gained the PAUSE hold; run_arms.py unchanged.
2026-09-30 17:38Z (orchestrator 17:31Z, throughput only): run_O2/run_O3 replaced by run_Olanes.sh = remaining A8 pool then A9 rest maps, 2 lanes x 2 threads, file order by alternate tiles; per-lane staging, move + manifest rebuild (infer.py itself) + commit + push under git.lock; PAUSE held until both lanes finish, then watchdog resumes the queue. infer.py/run_arms.py unchanged.
2026-09-30 17:58Z (DECL-P4-25-A10, -A10-A1): S1 model published at logs/sib/own-s1/model/ (sha256 bfa9f7a6...; commit 65aa79f). run_Olanes.sh narrowed to own-lead's v2 assignment (s1map_assign.json sha256 4f77b04d...): pool idx 0-15 + rest idx 0-9 (26 tiles); helpers make the rest. Lanes restarted (2 x 2 threads); queue resumes after.
2026-09-30 17:57Z: correction - 65aa79f held only summary.json (*.pth is gitignored); model_final.pth force-added in 054ec4e, remote copy sha256 bfa9f7a6... verified.
2026-09-30 19:25Z (DECL-P4-25-A14): own_common.py gained w126-127 (a2a7ff6, sha256 9faed7ae...). run_Planes.sh makes own-lead's 10 Region-P S1 maps (s1map_assign_P.json sha256 f49852d0...) into maps_P, 2 lanes x 2 threads, ahead of the paused A8/A9 lanes (which resume after, then the queue).
2026-09-30 19:50Z (DECL-P4-25-A16): run_Qlanes.sh queued behind run_Planes.sh; after the 10 P maps are committed it adds ONLY w128-129 to own_common.py (commit msg 'w128-129 own_common' + sha256), then makes own-lead's 12 Region-Q S1 maps (s1map_assign_Q.json sha256 74e4042e...) into maps_Q; run_Olanes.sh waits on /work/own/HOLD_O until then.
2026-09-30 19:53Z (DECL-P4-25-A14-A2): w128-129 own_common entry committed now (058d5f7, own_common.py sha256 ddf90770...), during Region P (extra key only); run_Qlanes.sh skips its own_common step (entry present) and still runs after P.
2026-09-30 22:47Z: container restart (~22:41Z). Found an S3 read outage ~21:38Z: chunk reads failed for 6 Q, 4 A8/A9 and the S3+NULL seed maps (FAILED, nothing wrong pushed); the chain then fell through to the scheduler. S3 reachable again (206); relaunched run_Qlanes (failed Q tiles), run_Olanes (held on HOLD_O), run_seedP (S3, NULL r8c14) - all resumable; tracked wait re-armed.
2026-09-30 23:35Z (DECL-P4-26-A2): VERSO job first: run_verso.sh makes own-lead's 80 verso S1 maps (verso_assign.json sha256 f3364896..., wrapper infer_verso.py sha256 a1bd1f24..., infer.py ddf-era code unchanged, own_common sha256 ddf90770...) into logs/sib/own-s1/verso/tiles/, 2 lanes x 2 threads; Q lanes paused (resume after), seedP continues. CT chunks are not cached by the reader, so ~5 min/tile, not seconds.
2026-09-30 23:40Z: at the verso start, Region Q was already complete (12/12, 23:23Z), seedP complete (S2/S3/NULL r8c14 pushed), run_Olanes done 23:28Z with 1 FAILED (w124-125 r4c5, retried later). The scheduler (started 23:28Z) was paused under the lock for the verso job; after verso: run_Qlanes (no-op) -> run_Olanes (retries r4c5) -> PAUSE removed -> scheduler resumes.
