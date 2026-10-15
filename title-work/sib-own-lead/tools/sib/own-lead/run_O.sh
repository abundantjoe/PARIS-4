#!/bin/bash
# Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7
# DECL-P4-25-A6: S1 maps of the 30 Region O tiles (logs/p4/regionO_S1_target2.json, sha256 877d6ee0...), in order,
# infer.py unchanged, 4 threads, one commit + push per tile into logs/sib/own-s1/maps_O/. Resumable (done tiles skipped).
cd /home/user/dominion
WAIT=$1; while [ -n "$WAIT" ] && kill -0 $WAIT 2>/dev/null; do sleep 15; done
git show origin/claude/gifted-bell-gavnl5:logs/p4/regionO_S1_target2.json > /work/own/regionO_target2.json
echo "877d6ee09bf9c5ba10c8a108738452f93f9c16a4433320cd21db81a79e77e0f6  /work/own/regionO_target2.json" | sha256sum -c - || exit 3
OUT=logs/sib/own-s1/maps_O
for t in $(/opt/ckb/bin/python -c "import json;[print(f\"{o['seg']}:{o['r']},{o['c']}\") for o in json.load(open('/work/own/regionO_target2.json'))['order']]"); do
  seg=${t%%:*}; rc=${t#*:}; r=${rc%,*}; c=${rc#*,}; name=${seg}_r${r}_c${c}
  if [ ! -f $OUT/tiles/$name.png.json ]; then
    OWN_WORK=/work/own /opt/ckb/bin/python tools/sib/own-lead/infer.py --model /work/own/arm_S1/model_final.pth --summary /work/own/arm_S1/summary.json --tiles "$t" --out $OUT --threads 4 >> /work/own/infer_O.log 2>&1 || { echo "FAILED $t"; exit 1; }
  fi
  flock /work/own/git.lock -c "git add $OUT/tiles/$name.png $OUT/tiles/$name.png.json $OUT/manifest.json && (git diff --cached --quiet || (git commit -qm 'own-lead: S1 Region O map $name (DECL-P4-25-A6)

Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_013RMBx9vJymzu55FFHNHGfd' && for i in 1 2 3 4; do git push -q origin HEAD && break; sleep \$((2**i)); done))"
  echo "done $name $(date -u +%H:%M)"
done
echo ALL_O_DONE
