#!/bin/bash
# Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7
# DECL-P4-25-A8 item 2: S1 maps of the 32 extended-test pool tiles (logs/p4/regionO_S1_ext_pool.json, sha256 49fde765...),
# in file order, infer.py unchanged (as run_O.sh), 4 threads, one commit + push per tile into logs/sib/own-s1/maps_O/.
# Resumable. At the end it restarts the watchdog (queue continues).
cd /home/user/dominion
git show origin/claude/gifted-bell-gavnl5:logs/p4/regionO_S1_ext_pool.json > /work/own/regionO_S1_ext_pool.json
echo "49fde7650855bdec74c8b2c1bbd02ecc3efe8cff4e133f6529bdda24087ca48d  /work/own/regionO_S1_ext_pool.json" | sha256sum -c - || exit 3
OUT=logs/sib/own-s1/maps_O
for t in $(/opt/ckb/bin/python -c "import json;[print(f\"{o['seg']}:{o['r']},{o['c']}\") for o in json.load(open('/work/own/regionO_S1_ext_pool.json'))['order']]"); do
  seg=${t%%:*}; rc=${t#*:}; r=${rc%,*}; c=${rc#*,}; name=${seg}_r${r}_c${c}
  if [ ! -f $OUT/tiles/$name.png.json ]; then
    OWN_WORK=/work/own /opt/ckb/bin/python tools/sib/own-lead/infer.py --model /work/own/arm_S1/model_final.pth --summary /work/own/arm_S1/summary.json --tiles "$t" --out $OUT --threads 4 >> /work/own/infer_O2.log 2>&1 || { echo "FAILED $t"; continue; }
  fi
  flock /work/own/git.lock -c "git add $OUT/tiles/$name.png $OUT/tiles/$name.png.json $OUT/manifest.json && (git diff --cached --quiet || (git commit -qm 'own-lead: S1 Region O ext-pool map $name (DECL-P4-25-A8)

Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_013RMBx9vJymzu55FFHNHGfd' && for i in 1 2 3 4; do git push -q origin HEAD && break; sleep \$((2**i)); done))"
  rm -rf /work/own/infer/S1/$name
  echo "done $name $(date -u +%H:%M)"
done
echo ALL_O2_DONE
setsid nohup tools/sib/own-lead/watchdog.sh >> /work/own/watchdog.log 2>&1 < /dev/null &
echo "watchdog restarted $(date -u +%FT%TZ)"
