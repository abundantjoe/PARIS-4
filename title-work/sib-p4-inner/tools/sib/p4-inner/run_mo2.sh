#!/bin/bash
# Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7
# DECL-P4-25 builder driver: detached, resumable (steps skip when outputs exist). usage: run_mo2.sh <scratch_root>
set -uo pipefail
R="$1"; REPO=/home/user/dominion; T=$REPO/tools/sib/p4-inner
cd $REPO
for SEG in 20260701183150-w126-127 20260701183149-w124-125 20260701183148-w122-123; do
  TAG=${SEG#*-}; W=$R/$TAG; D=$REPO/logs/sib/p4-inner/mo2/$TAG; mkdir -p $W/dl $W/out
  [ -f $D/manifest.json ] && { echo "$TAG already pushed"; continue; }
  avail=$(df --output=avail -BG / | tail -1 | tr -dc 0-9); [ "$avail" -lt 6 ] && { echo "LOW DISK ${avail}G"; exit 3; }
  [ -s $W/downloads.jsonl ] && [ $(wc -l < $W/downloads.jsonl) -eq 7 ] || bash $T/fetch_strip.sh $W/dl $W/downloads.jsonl $SEG || exit 4
  grep -q ALL_DONE $W/tile.log 2>/dev/null || P4_SEG=$SEG python3 $T/tile_strip.py $W/dl $W/out --skip-existing > $W/tile.log 2>&1 || exit 5
  [ -f $W/out/tile_geom.json ] || python3 $T/tile_geom_w128.py $W/out $W/out/tile_geom.json > $W/geom.log 2>&1 || exit 6
  [ -f $W/out/direction.json ] || python3 $T/direction_strip.py $W/dl $W/out/direction.json $TAG > $W/dir.log 2>&1 || exit 7
  python3 $T/build_manifest.py $W $D "RULES.md DECL-P4-25 item 1 (P4-M-OUT2), tiling and display as DECL-P4-2 item 2, same code as P4-M-OUT" || exit 8
  rm -f $W/dl/*new_canon*.tif
  git add logs/sib/p4-inner/mo2/$TAG tools/sib/p4-inner && git commit -q -m "p4-inner: DECL-P4-25 $SEG M1 tiles + manifest

Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01AXfmasnYmkW3pgGvTRpDwK"
  for i in 1 2 3 4; do git push -q origin claude/gifted-bell-gavnl5-sib-p4-inner && break; sleep $((2**i)); done
  echo "PUSHED $TAG $(git rev-parse --short HEAD)"
done
echo ALL_STRIPS_DONE
