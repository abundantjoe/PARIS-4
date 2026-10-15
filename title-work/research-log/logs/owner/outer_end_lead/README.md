# PHerc. Paris 4: confirmed text at the outer end of the roll (hand-off under DECL-P4-3 item 4)

Provenance: Project HERCULES | HRC-JB-0924-O7
Prepared 2026-09-27 ~22:00Z at the owner's request. Every number below comes from RULES.md (hash-chained): P4-M-OUT2-P2-RESULT, P4-M-OUT2-EXT-RESULT, METRIC-HASH-42 (Q6).

## What this is
- A blind-reader-confirmed region of text-like ink at the outer end of PHerc. Paris 4, which is the beginning of the roll.
- Segment `20260701183148-w122-123`, tiles c4-c5 x r3-r4. It lies about 105-109 cm along the spiral from the traced outer end.
- Image: `w122-123_M1_c4-c5_r3-r4_scalebar.png`, built in code from the four census tiles. The sha256 of each tile matches the builder manifest. Scale 53.40 px/mm; the scale bar is 1 cm (534 px).

**We do not claim that this is the title.** Our own pre-registered layout test favours ordinary body text. It is offered as the one region of this scroll that passed every check we set, at the place where an initial title would stand (as on PHerc. 1497 and 1583). Whether it is a title is for papyrologists to judge.

## Ink model and training overlap
- Ink model: M1, the Vesuvius Challenge organizers' 2.4 um ink predictions.
- Their training labels come from 8 labelled segments. Every census tile carries its minimum 3-D distance to those segments' meshes, and a tile closer than 1.2 mm can never become a candidate (RULES.md DECL-P4-2). These tiles passed that rule.
- The outer strips lie far from the labelled segments.

## Validation and false-positive control (all declared before the data)
1. Blind census: sealed answers from independent readers who saw only the images named in their brief. N0 null = a per-batch rotated copy of census tiles, thresholded at p99.
2. Phase 2: 4 candidates in this 2 x 2 block (P4-M-OUT2-P2-RESULT).
3. Extended test (DECL-P4-3, DECL-P4-25-A2): the upright tile (U) against the same tile rotated 90 degrees (R), plus 48 N0 tiles; exact permutation p over 48,620 labelings.
   | Tile | U letter counts | R letter counts | Result |
   |---|---|---|---|
   | r4 c5 | 11, 11, 13 | 1-2 | p 2.06e-5, EXT-CONFIRMED |
   | r4 c4 | 8, 8, 8 | 3-4 | p 2.06e-5, EXT-CONFIRMED |
   | r3 c5 | 5, 6, 5 | 2-3 | p 2.06e-5, EXT-CONFIRMED, exactly at the bar |
   | r3 c4 | 3, 4, 3 | - | NOT confirmed |
4. Independent audit: all four batches VALID. All runner numbers re-derived and matched; the timelines hold (declaration, then commit A, then readers, then commit B).
5. Disclosures:
   - The three confirmations are ONE 2 x 2 lead read by one model family, not three independent finds.
   - One void session was re-run under a pinned rule.
   - Three sessions lost their DONE hand-back but sealed valid answers.

## Geometry (auditor; numbers only)
- 5 continuous lines across the block, common line pitch 6.48 mm (RMS 0.04). Lines are about 37 mm long as M1 shows them.
- Letter box height: median 2.9-3.4 mm. The known body-text reference is 3.46 mm.

## Layout test (pre-registered, METRIC-HASH-42): favours body text
- Block 1 (s 100.1-112.5 cm) holds about 19 lines at 6.26 mm over 120 mm. Block 2 (s 116.2-129.1 cm) holds about 17.5 lines at 6.51 mm.
- The mechanical Q6 score is -3, "layout favours a text column", exactly at the boundary.
- Estimated P(initial title) is about 0.07.

## What a Title Prize submission would still need
- The tifxyz mesh (the official w122-123 segment; EduceLab-licensed, so it is named here and not included) and a flattening-distortion figure.
- The letter dimensions above.
- This methodology.
- The owner's own sign-in on the submission form.
