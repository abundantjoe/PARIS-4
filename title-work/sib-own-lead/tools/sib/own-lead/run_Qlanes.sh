#!/bin/bash
# Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7
# DECL-P4-25-A16: after own-lead's 10 Region-P maps are pushed, (1) add ONLY the w128-129 entries to own_common.py
# (SEGS (89440, 142320), TILE_PX 8327; p4-inner mout/grid.json), commit + push; (2) own-lead's 12 Region-Q S1 maps
# (logs/p4/s1map_assign_Q.json "own-lead", sha256 74e4042e...), list order, 2 lanes x 2 threads, infer.py unchanged,
# S1 model, into logs/sib/own-s1/maps_Q/. Holds /work/own/HOLD_O (run_Olanes.sh waits on it) and /work/own/PAUSE.
cd /home/user/dominion
touch /work/own/PAUSE /work/own/HOLD_O
while pgrep -f "^/bin/bash tools/sib/own-lead/run_Planes.sh" > /dev/null; do sleep 20; done
NP=$(git ls-files logs/sib/own-s1/maps_P/tiles | grep -c 'png.json$')
if [ "$NP" -lt 10 ]; then echo "STOP: only $NP/10 Region-P maps committed; own_common not changed"; exit 5; fi
if ! grep -q "20260701183151-w128-129" tools/sib/own-lead/own_common.py; then
  /opt/ckb/bin/python - <<'PYEOF'
p='tools/sib/own-lead/own_common.py'; s=open(p).read()
a="    '20260701183150-w126-127': (94080, 154880),   # DECL-P4-25-A14 (p4-inner mo2/w126-127/grid.json canvas_shape)\n}"
b="           '20260701183150-w126-127': 8467}   # p4-inner logs/sib/p4-inner/mo2/w126-127/grid.json T_canvas_px"
assert a in s and b in s
s=s.replace(a,"    '20260701183150-w126-127': (94080, 154880),   # DECL-P4-25-A14 (p4-inner mo2/w126-127/grid.json canvas_shape)\n    '20260701183151-w128-129': (89440, 142320),   # DECL-P4-25-A16 (p4-inner mout/grid.json canvas_shape)\n}")
s=s.replace(b,"           '20260701183150-w126-127': 8467,   # p4-inner logs/sib/p4-inner/mo2/w126-127/grid.json T_canvas_px\n           '20260701183151-w128-129': 8327}   # p4-inner logs/sib/p4-inner/mout/grid.json T_canvas_px")
open(p,'w').write(s)
PYEOF
  H=$(sha256sum tools/sib/own-lead/own_common.py | cut -c1-64)
  flock /work/own/git.lock -c "git add tools/sib/own-lead/own_common.py && git commit -qm 'own-lead: w128-129 own_common entries (DECL-P4-25-A16): SEGS (89440, 142320), TILE_PX 8327; own_common.py sha256 $H

Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_013RMBx9vJymzu55FFHNHGfd' && for n in 1 2 3 4; do git push -q origin HEAD && break; sleep \$((2**n)); done"
  echo "own_common w128-129 committed sha256 $H $(date -u +%FT%TZ)"
fi
OUT=logs/sib/own-s1/maps_Q
MODEL="--model /work/own/arm_S1/model_final.pth --summary /work/own/arm_S1/summary.json"
LIST=/work/own/Qlanes_list.txt
git show origin/claude/gifted-bell-gavnl5:logs/p4/s1map_assign_Q.json > /work/own/s1map_assign_Q.json
echo "74e4042ef8f0d3bb8fb8fd9a5e338f9bf2272a67352f05ddc4e8024681307985  /work/own/s1map_assign_Q.json" | sha256sum -c - || exit 3
/opt/ckb/bin/python -c "import json;d=json.load(open('/work/own/s1map_assign_Q.json'));assert d['model_final_sha256']=='bfa9f7a62097374b93e87c7b406a9c3eba6b77dca3d9f79c10300fa0114daea5';[print(t, 'Q') for t in d['own-lead']['tiles']]" > $LIST || exit 4

lane() {
  k=$1; i=0; STAGE=/work/own/stage_Q_$k
  while read t decl; do
    if [ $((i % 2)) -eq $k ]; then
      seg=${t%%:*}; rc=${t#*:}; r=${rc%,*}; c=${rc#*,}; name=${seg}_r${r}_c${c}
      if [ ! -f $OUT/tiles/$name.png.json ]; then
        mkdir -p $STAGE
        OWN_WORK=/work/own /opt/ckb/bin/python tools/sib/own-lead/infer.py $MODEL --tiles "$t" --out $STAGE --threads 2 >> /work/own/infer_Qlane$k.log 2>&1 || { echo "FAILED $t"; i=$((i+1)); continue; }
      fi
      flock /work/own/git.lock -c "
        set -e
        if [ -f $STAGE/tiles/$name.png.json ]; then mkdir -p $OUT/tiles; mv $STAGE/tiles/$name.png $STAGE/tiles/$name.png.json $OUT/tiles/; fi
        OWN_WORK=/work/own /opt/ckb/bin/python tools/sib/own-lead/infer.py $MODEL --tiles '$t' --out $OUT --threads 1 >> /work/own/infer_Qlane$k.log 2>&1
        git add $OUT/tiles/$name.png $OUT/tiles/$name.png.json $OUT/manifest.json
        git diff --cached --quiet || { git commit -qm 'own-lead: S1 Region Q map $name (DECL-P4-25-A16, lane $k)

Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_013RMBx9vJymzu55FFHNHGfd'; for n in 1 2 3 4; do git push -q origin HEAD && break; sleep \$((2**n)); done; }
      "
      rm -rf /work/own/infer/S1/$name
      echo "lane $k done $name $decl $(date -u +%H:%M)"
    fi
    i=$((i+1))
  done < $LIST
}

lane 0 & L0=$!
lane 1 & L1=$!
wait $L0 $L1
echo "ALL_QLANES_DONE $(date -u +%FT%TZ)"
rm -f /work/own/HOLD_O
pgrep -f "^/bin/bash tools/sib/own-lead/run_Olanes.sh" > /dev/null || setsid nohup tools/sib/own-lead/run_Olanes.sh >> /work/own/run_Olanes.log 2>&1 < /dev/null &
echo "HOLD_O released $(date -u +%FT%TZ)"
