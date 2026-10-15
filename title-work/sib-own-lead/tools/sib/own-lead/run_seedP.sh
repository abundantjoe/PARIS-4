#!/bin/bash
# Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7
# DECL-P4-25-A14-A4 item 2: S2, S3 and NULL maps of w126-127 r8c14 (6(d) seed check), infer.py unchanged, 1 thread,
# alongside the Region-Q lanes; into logs/sib/own-<arm>/maps_P/, one commit + push per map under git.lock.
cd /home/user/dominion
T=20260701183150-w126-127:8,14; N=20260701183150-w126-127_r8_c14
for a in S2 S3 NULL; do
  l=$(echo $a | tr A-Z a-z); OUT=logs/sib/own-$l/maps_P
  if [ ! -f $OUT/tiles/$N.png.json ]; then
    OWN_WORK=/work/own /opt/ckb/bin/python tools/sib/own-lead/infer.py --model /work/own/arm_$a/model_final.pth --summary /work/own/arm_$a/summary.json --tiles "$T" --out $OUT --threads 1 >> /work/own/infer_seedP.log 2>&1 || { echo "FAILED $a"; continue; }
  fi
  flock /work/own/git.lock -c "git add $OUT/tiles/$N.png $OUT/tiles/$N.png.json $OUT/manifest.json && (git diff --cached --quiet || (git commit -qm 'own-lead: $a map $N (6(d) seed check, DECL-P4-25-A14-A4)

Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_013RMBx9vJymzu55FFHNHGfd' && for n in 1 2 3 4; do git push -q origin HEAD && break; sleep \$((2**n)); done))"
  rm -rf /work/own/infer/$a/$N
  echo "done $a $N $(date -u +%H:%M)"
done
echo SEEDP_DONE
