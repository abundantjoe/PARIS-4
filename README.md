# PHerc. Paris 4 (Scroll 1): Title Prize material

Provenance: Project HERCULES | HRC-JB-0924-O7
Status on 2026-09-27 21:45Z: **no title has been identified.** Full hash-chained record: `RULES.md` in abundantjoe/dominion, branch `claude/gifted-bell-gavnl5`.

## Latest result (P4-OWN-S1X-RESULT)
- Our own ink model, P4-OWN S1, is trained on Paris 4 with the title zone and a 1.2 mm margin excluded. We ran one blind read of its maps (`results/census_own_s1x_summary.json`, audit `results/own_s1x_audit.json`): 4 of 4 sessions valid; rotated null 0/0/0/0 letters.
- Control, col. -1 (the known text column beside the title slot, never trained on): 5 of 6 tiles show rows of writing with 7-11 letters. The model reads real text there.
- End-title slot (w010-027, columns c14-c17, rows r0-r5, 24 tiles): 0 of 24 show writing, and 0 letters were found.
- Conclusion: no carbon-ink title is legible in the end-title slot at this model. This was read before our held-out legibility gate G1 (DECL-P4-23-A3). It does not exclude:
  - non-carbon ink;
  - a flaked title, or its offset onto the facing winding;
  - the blank end c18-c19;
  - an initial title at the beginning of the roll.

## The only candidate: `outer_end_lead/`
- Blind-reader-confirmed text at the outer end (the beginning) of the roll: segment 20260701183148-w122-123, tiles c4-c5 x r3-r4. It passed the blind census, phase 2 and the extended test (p 2.06e-5), and an independent audit.
- **Its pre-registered layout test favours ordinary body text.** P(initial title) is about 0.07.
- It is offered only for papyrologists to judge, with that disclosure. It is NOT claimed as the title.

## Title Prize checklist (scrollprize.org)
| Item | Status |
|---|---|
| tifxyz mesh plus a low-distortion flattening | Official segments only (EduceLab-licensed): named here, never included |
| Programmatic image with a 1 cm scale bar and letter dimensions, named after the mesh | outer_end_lead only: line pitch 6.48 mm, letter height 2.9-3.4 mm |
| Methodology, false-positive mitigation, held-out validation | In dominion RULES.md: DECL-P4-2, -3, -23 (+A1-A3), -25; P4-M-OUT2-EXT-RESULT; P4-OWN-S1-COLM1-AUC (col. -1 AUC 0.978) |
| No overlap between ink-model training data and the region | M1: tiles >= 1.2 mm from the 8 labelled segments. P4-OWN: title zone plus 1.2 mm excluded |
| Submission | Needs the owner's own sign-in |

## Second lead (2026-10-03): verso of the end-title slot, census-positive, NOT extended-tested
P4-OFF (DECL-P4-26-A2, RULES.md P4-OFF-VW-RESULT): our own model's verso-offset maps of segment 20260701183124-w010-027 (the winding facing the end-title slot, where flaked ink would be mirrored) were read as 133 stitched 4 x 4 cm windows by the sealed local harness. Reader-sensitivity gate PASS on the known col. -1 text (counts 61 and 43). Null p99 threshold 8.52. Three windows are positive, all just above threshold: r3c1 (10 letters), r3c4 (9 + 1 mark), r4c5 (9), forming clusters {r3c4, r4c5} and {r3c1}. No phase-2 or extended test followed (the project was redirected). It is a census-level signal in the right place and nothing more; it is not a reading and not a title claim.
