#!/bin/bash
# Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7
# DECL-P4-25-A14: own-lead's 10 Region-P S1 maps (logs/p4/s1map_assign_P.json "own-lead", sha256 f49852d0...), in list
# order, 2 lanes x 2 threads, infer.py unchanged, S1 model, into logs/sib/own-s1/maps_P/ (same per-lane staging,
# locked move + manifest rebuild + commit + push as run_Olanes.sh). Resumable. Holds /work/own/PAUSE; when done it
# relaunches run_Olanes.sh (the paused A8/A9 lanes resume; that script releases PAUSE and restarts the queue).
cd /home/user/dominion
touch /work/own/PAUSE
OUT=logs/sib/own-s1/maps_P
MODEL="--model /work/own/arm_S1/model_final.pth --summary /work/own/arm_S1/summary.json"
LIST=/work/own/Planes_list.txt
git show origin/claude/gifted-bell-gavnl5:logs/p4/s1map_assign_P.json > /work/own/s1map_assign_P.json
echo "f49852d084cfcc58effd9f84d454eeda80a54563121b04f2a93dff59c857a68f  /work/own/s1map_assign_P.json" | sha256sum -c - || exit 3
/opt/ckb/bin/python -c "import json;d=json.load(open('/work/own/s1map_assign_P.json'));assert d['model_final_sha256']=='bfa9f7a62097374b93e87c7b406a9c3eba6b77dca3d9f79c10300fa0114daea5';[print(t, 'P') for t in d['own-lead']['tiles']]" > $LIST || exit 4

lane() {
  k=$1; i=0; STAGE=/work/own/stage_P_$k
  while read t decl; do
    if [ $((i % 2)) -eq $k ]; then
      seg=${t%%:*}; rc=${t#*:}; r=${rc%,*}; c=${rc#*,}; name=${seg}_r${r}_c${c}
      if [ ! -f $OUT/tiles/$name.png.json ]; then
        mkdir -p $STAGE
        OWN_WORK=/work/own /opt/ckb/bin/python tools/sib/own-lead/infer.py $MODEL --tiles "$t" --out $STAGE --threads 2 >> /work/own/infer_Plane$k.log 2>&1 || { echo "FAILED $t"; i=$((i+1)); continue; }
      fi
      flock /work/own/git.lock -c "
        set -e
        if [ -f $STAGE/tiles/$name.png.json ]; then mkdir -p $OUT/tiles; mv $STAGE/tiles/$name.png $STAGE/tiles/$name.png.json $OUT/tiles/; fi
        OWN_WORK=/work/own /opt/ckb/bin/python tools/sib/own-lead/infer.py $MODEL --tiles '$t' --out $OUT --threads 1 >> /work/own/infer_Plane$k.log 2>&1
        git add $OUT/tiles/$name.png $OUT/tiles/$name.png.json $OUT/manifest.json
        git diff --cached --quiet || { git commit -qm 'own-lead: S1 Region P map $name (DECL-P4-25-A14, lane $k)

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
echo "ALL_PLANES_DONE $(date -u +%FT%TZ)"
setsid nohup tools/sib/own-lead/run_Olanes.sh >> /work/own/run_Olanes.log 2>&1 < /dev/null &
echo "run_Olanes.sh relaunched $(date -u +%FT%TZ)"
