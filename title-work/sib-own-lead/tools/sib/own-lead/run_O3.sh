#!/bin/bash
# Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7
# DECL-P4-25-A9: S1 maps of the 65 rest-of-Region-O tiles (logs/p4/regionO_S1_rest.json, sha256 71283a59...), after run_O2.sh;
# in file order, infer.py unchanged (as run_O.sh), 4 threads, one commit + push per tile into logs/sib/own-s1/maps_O/.
# Holds /work/own/PAUSE (watchdog idles) until done, then removes it and restarts the watchdog. Resumable.
cd /home/user/dominion
touch /work/own/PAUSE
while pgrep -f "^/bin/bash tools/sib/own-lead/run_O2.sh" > /dev/null; do sleep 30; done
git show origin/claude/gifted-bell-gavnl5:logs/p4/regionO_S1_rest.json > /work/own/regionO_S1_rest.json
echo "71283a59fcd6d8258e23469850e1a7e83f2672eca57709d18e550ad04e1fda71  /work/own/regionO_S1_rest.json" | sha256sum -c - || exit 3
OUT=logs/sib/own-s1/maps_O
for t in $(/opt/ckb/bin/python -c "import json;[print(f\"{o['seg']}:{o['r']},{o['c']}\") for o in json.load(open('/work/own/regionO_S1_rest.json'))['order']]"); do
  seg=${t%%:*}; rc=${t#*:}; r=${rc%,*}; c=${rc#*,}; name=${seg}_r${r}_c${c}
  if [ ! -f $OUT/tiles/$name.png.json ]; then
    OWN_WORK=/work/own /opt/ckb/bin/python tools/sib/own-lead/infer.py --model /work/own/arm_S1/model_final.pth --summary /work/own/arm_S1/summary.json --tiles "$t" --out $OUT --threads 4 >> /work/own/infer_O3.log 2>&1 || { echo "FAILED $t"; continue; }
  fi
  flock /work/own/git.lock -c "git add $OUT/tiles/$name.png $OUT/tiles/$name.png.json $OUT/manifest.json && (git diff --cached --quiet || (git commit -qm 'own-lead: S1 Region O rest map $name (DECL-P4-25-A9)

Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_013RMBx9vJymzu55FFHNHGfd' && for i in 1 2 3 4; do git push -q origin HEAD && break; sleep \$((2**i)); done))"
  rm -rf /work/own/infer/S1/$name
  echo "done $name $(date -u +%H:%M)"
done
echo ALL_O3_DONE; rm -f /work/own/PAUSE
pgrep -f "^/bin/bash tools/sib/own-lead/watchdog.sh" > /dev/null || setsid nohup tools/sib/own-lead/watchdog.sh >> /work/own/watchdog.log 2>&1 < /dev/null &
echo "watchdog restarted $(date -u +%FT%TZ)"
