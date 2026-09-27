# Title Prize submission: ready to paste into the form

Form: https://forms.gle/4zeVPPBtNdSCAQa88 (owner signs in and submits; team leader = owner)
Attach: `outer_end_lead/20260701183148-w122-123.png` (named after its mesh) and `outer_end_lead/README.md`.

**Scroll / scan:** PHerc. Paris 4 (Scroll 1). Official segment `20260701183148-w122-123` (outer end, i.e. the beginning of the roll, about 105-109 cm along the spiral from the traced outer end). Ink predictions: the Vesuvius Challenge's published 2.4 um ink predictions for this segment.

**Mesh:** the official tifxyz segment `20260701183148-w122-123` with its published flattening. It is not redistributed by us (EduceLab licence); it is your own published segment.

**Image:** a programmatic 2 x 2 composite of the ink-prediction tiles c4-c5 x r3-r4 (2 cm tiles, 1068 px each, 53.40 px/mm), with a 1 cm scale bar (534 px). No manual annotation of characters. The sha256 of each tile matches our builder manifest.

**Letter dimensions (measured, not identified):** 5 continuous lines across the block; line pitch 6.48 mm (346 px); letter box height median 2.9-3.4 mm (155-182 px); lines about 37 mm long.

**Why we submit it:** it is blind-reader-confirmed text at the very beginning of the roll, where an initial title can stand (as on PHerc. 1497/1583). Our own ink model shows NO legible writing in the expected end-title slot (w010-027 c14-c17: 0 of 24 tiles), while it reads the adjacent known-text column (col. -1: 5 of 6 tiles, 7-11 letters each).

**Honest disclosure:** our pre-registered layout test favours ordinary body text here: about 19 lines at 6.3-6.5 mm in blocks of about 12.5 cm, with letter height equal to the body text. Our estimate of P(initial title) is about 0.07. We do not claim this is the title; we ask the papyrologists to judge.

**False-positive mitigation:**
- Blind readers saw only anonymous tiles in shuffled sessions; answers were sealed and machine-audited.
- Per-batch null: rotated copies of census tiles (N0; p99 threshold).
- Extended test: the upright tile (U) against the same tile rotated 90 degrees (R), plus 48 N0 tiles; exact permutation p = 2.06e-5 on 3 of 4 tiles (U letter counts 11/11/13, 8/8/8, 5/6/5 vs R 1-4).
- An independent re-derivation audit found every batch VALID.
- Every rule was declared in a hash-chained log before its data.
- Limitation: one 2 x 2 block, one model family.

**Training overlap:** tiles within 1.2 mm (3-D) of the 8 labelled segments are excluded from candidacy. These tiles passed; the outer strips are far from the labelled segments.

**Held-out validation:**
- Our own model P4-OWN, trained with the title zone plus 1.2 mm excluded, reaches pixel AUC 0.978 against your labels on col. -1, which it never trained on.
- A blind read of its col. -1 maps found text on 5 of 6 tiles.
- 3-fold held-out training is in progress.

**Methodology / reproduction:** repository abundantjoe/dominion (private; access on request). See RULES.md: DECL-P4-2, -3, -23, -25; P4-M-OUT2-P2/-EXT-RESULT; P4-OWN-S1X-RESULT; tools/p4/*.
**Confidentiality:** not to be made public before any official announcement (prize rule).
