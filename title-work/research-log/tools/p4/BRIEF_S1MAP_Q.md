# S1 map helper brief, Region Q (RULES.md DECL-P4-25-A16)
Provenance: Project HERCULES | HRC-JB-0924-O7

Same job as tools/p4/BRIEF_S1MAP_P.md (read it), on the outermost tiles (s < 40 cm from the outer end). Numbers only: never open, display or describe any map, tile or CT image. Push only to your own branch.

0. Order of work: finish and push your whole Region-P list first. Region Q starts only after that.
1. Code: after its own Region-P maps, own-lead adds strip 20260701183151-w128-129 to tools/sib/own-lead/own_common.py: SEGS canvas (89440, 142320) and TILE_PX 8327, from p4-inner logs/sib/p4-inner/mout/grid.json. Nothing else changes.
   - Wait until origin/claude/gifted-bell-gavnl5-sib-own-lead has a commit whose message contains "w128-129 own_common".
   - Then run: git fetch origin claude/gifted-bell-gavnl5 claude/gifted-bell-gavnl5-sib-own-lead; git checkout origin/claude/gifted-bell-gavnl5-sib-own-lead -- tools/sib/own-lead/; git checkout origin/claude/gifted-bell-gavnl5 -- logs/p4/s1map_assign_Q.json tools/p4/BRIEF_S1MAP_Q.md
   - Record the sha256 of the new own_common.py in your STATUS.md.
2. Environment, model and options: as before (/opt/ckb with pillow; S1 model sha256 bfa9f7a6...; --threads 2 per lane; one staging dir per lane; commit per tile under the shared lock).
3. Tiles: under helpers.<you> in logs/p4/s1map_assign_Q.json.
   - FIRST, in lane A: re-make your `repro` tile (the same w124-125 tile as in Region P) with the NEW own_common.py. Push it to logs/sib/<you>/s1maps_Q/repro/ (.png and .png.json). Also record its png_sha256 and own-lead's in STATUS.md in one line containing "Region Q repro".
   - Lane B meanwhile starts `tiles` in list order; lane A continues with them after the repro tile.
   - Push each map to logs/sib/<you>/s1maps_Q/tiles/ (the .png and .png.json) as soon as it is written.
4. Liveness: keep a harness-tracked Bash run_in_background wait (timeout 7200000) on your lanes until the list is pushed.
5. Never change infer.py, the model, the options or the lists. The only code change allowed is own-lead's own_common.py entry above.
