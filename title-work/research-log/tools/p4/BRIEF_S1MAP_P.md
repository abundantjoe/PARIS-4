# S1 map helper brief, Region P (RULES.md DECL-P4-25-A14)
Provenance: Project HERCULES | HRC-JB-0924-O7

Same job as tools/p4/BRIEF_S1MAP.md (read it), on new tiles further out along the roll. Numbers only: never open, display or describe any map, tile or CT image. Push only to your own branch.

1. Code: own-lead adds strip 20260701183150-w126-127 to tools/sib/own-lead/own_common.py (SEGS canvas (94080, 154880) and TILE_PX 8467, from p4-inner grid.json); nothing else changes.
   - Wait until origin/claude/gifted-bell-gavnl5-sib-own-lead has a commit whose message contains "w126-127 own_common".
   - Then run: git fetch origin claude/gifted-bell-gavnl5 claude/gifted-bell-gavnl5-sib-own-lead; git checkout origin/claude/gifted-bell-gavnl5-sib-own-lead -- tools/sib/own-lead/; git checkout origin/claude/gifted-bell-gavnl5 -- logs/p4/s1map_assign_P.json tools/p4/BRIEF_S1MAP_P.md
   - Record the sha256 of the new own_common.py in your STATUS.md.
2. Environment, model and options: as before (/opt/ckb with pillow; S1 model sha256 bfa9f7a6...; --threads 2 per lane; one staging dir per lane; commit per tile under the shared lock). If your container was reset, rebuild them per BRIEF_S1MAP.md steps 2-3.
3. Tiles: under helpers.<you> in logs/p4/s1map_assign_P.json.
   - FIRST, in lane A: re-make your `repro` tile (an existing w124-125 map) with the NEW own_common.py. Its png_sha256 must equal own-lead's map of that tile (logs/sib/own-s1/maps_O/tiles/<name>.png.json on own-lead's branch). This proves the code change changes nothing else. Record the result in STATUS.md.
   - Lane B meanwhile starts `tiles` in list order; lane A continues with them after the repro tile.
   - Push each map to logs/sib/<you>/s1maps_P/tiles/ (the .png and .png.json) as soon as it is written.
4. Liveness: keep a harness-tracked Bash run_in_background wait (timeout 7200000) on your lanes until the list is pushed.
5. Never change infer.py, the model, the options or the lists. The only code change allowed is own-lead's own_common.py entry above.
