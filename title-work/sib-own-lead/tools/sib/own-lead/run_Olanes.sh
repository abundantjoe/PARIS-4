#!/bin/bash
# Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7
# Orchestrator 2026-09-30 17:31Z (throughput only; DECL-P4-25-A8/A9 unchanged), narrowed by DECL-P4-25-A10-A1: S1 maps of
# regionO_S1_ext_pool.json (A8, 32) then regionO_S1_rest.json (A9, 65), in file order, as 2 lanes x 2 threads
# (lane k takes list positions k, k+2, ...). infer.py unchanged, S1 model, same outputs/records as run_O.sh.
# Each lane infers into its own staging dir; then, under /work/own/git.lock, moves the tile into maps_O/tiles/,
# rebuilds maps_O/manifest.json with infer.py itself (an already-done tile is skipped and only the manifest is
# rewritten from all records), commits and pushes. Resumable (band checkpoints; done tiles skipped).
# Holds /work/own/PAUSE; when both lanes finish, removes it and starts the watchdog (if none) so the queue resumes.
cd /home/user/dominion
touch /work/own/PAUSE
while [ -f /work/own/HOLD_O ]; do sleep 30; done   # run_Qlanes.sh (DECL-P4-25-A16) goes first
OUT=logs/sib/own-s1/maps_O
MODEL="--model /work/own/arm_S1/model_final.pth --summary /work/own/arm_S1/summary.json"
LIST=/work/own/Olanes_list.txt
: > $LIST
for spec in "regionO_S1_ext_pool.json 49fde7650855bdec74c8b2c1bbd02ecc3efe8cff4e133f6529bdda24087ca48d A8" \
            "regionO_S1_rest.json 71283a59fcd6d8258e23469850e1a7e83f2672eca57709d18e550ad04e1fda71 A9"; do
  set -- $spec
  git show origin/claude/gifted-bell-gavnl5:logs/p4/$1 > /work/own/$1
  echo "$2  /work/own/$1" | sha256sum -c - || exit 3
  # DECL-P4-25-A10-A1 (s1map_assign.json v2, sha256 4f77b04d...): own-lead makes pool idx 0-15 and rest idx 0-9 only
  case $3 in A8) MAXI=15;; A9) MAXI=9;; esac
  /opt/ckb/bin/python -c "import json;[print(f\"{o['seg']}:{o['r']},{o['c']} $3\") for i,o in enumerate(json.load(open('/work/own/$1'))['order']) if i <= $MAXI]" >> $LIST
done

lane() {
  k=$1; i=0; STAGE=/work/own/stage_O_$k
  while read t decl; do
    if [ $((i % 2)) -eq $k ]; then
      seg=${t%%:*}; rc=${t#*:}; r=${rc%,*}; c=${rc#*,}; name=${seg}_r${r}_c${c}
      if [ ! -f $OUT/tiles/$name.png.json ]; then
        mkdir -p $STAGE
        OWN_WORK=/work/own /opt/ckb/bin/python tools/sib/own-lead/infer.py $MODEL --tiles "$t" --out $STAGE --threads 2 >> /work/own/infer_Olane$k.log 2>&1 || { echo "FAILED $t"; i=$((i+1)); continue; }
      fi
      flock /work/own/git.lock -c "
        set -e
        if [ -f $STAGE/tiles/$name.png.json ]; then mkdir -p $OUT/tiles; mv $STAGE/tiles/$name.png $STAGE/tiles/$name.png.json $OUT/tiles/; fi
        OWN_WORK=/work/own /opt/ckb/bin/python tools/sib/own-lead/infer.py $MODEL --tiles '$t' --out $OUT --threads 1 >> /work/own/infer_Olane$k.log 2>&1
        git add $OUT/tiles/$name.png $OUT/tiles/$name.png.json $OUT/manifest.json
        git diff --cached --quiet || { git commit -qm 'own-lead: S1 Region O map $name ($decl, lane $k)

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
echo "ALL_OLANES_DONE $(date -u +%FT%TZ)"
rm -f /work/own/PAUSE
pgrep -f "^/bin/bash tools/sib/own-lead/watchdog.sh" > /dev/null || setsid nohup tools/sib/own-lead/watchdog.sh >> /work/own/watchdog.log 2>&1 < /dev/null &
echo "watchdog ensured $(date -u +%FT%TZ)"
