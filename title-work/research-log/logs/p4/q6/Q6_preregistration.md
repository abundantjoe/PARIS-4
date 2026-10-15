## Q6: PRE-REGISTRATION (asked 07:41Z; written before any w122-123 layout-profile number exists, and before this sibling has seen any such number)
Title block vs text column on w122-123, candidate block c4-c5 × r3-r4, s about 105-109 cm. Numbers only; no letter content was seen or used.

Definitions:
- s increases inward, i.e. forward in the text.
- Let the candidate block be B = [s1, s2] with width W = s2 − s1.
- G_out is the blank gap outward of B, to the nearest block at lower s.
- G_in is the blank gap inward, to the next block N at s3.
- P = s3 − s1, start to start.
- All measured on the p4-layout profile (1 mm bins, z-summed M1, rows r1-r6, block = a run above median + 3 MAD of the declared baseline bins).
- The tolerance for scan and carbonisation shrinkage is ±12 %. CERC54 measured the same crumpled roll, so the reference values are already "as scanned".

### 1. Predictions

| quantity | (a) text column | (b) initial-title block | sources |
|---|---|---|---|
| block width W | **5.5-7.0 cm** (6.2 ± 12 %). A column fills its width edge to edge; a short or damaged column can only be *narrower* if the loss is lateral | **2-5.5 cm**: the width of the longest centred line. Titles are 2-4 centred lines, 3-6 cm wide; the author line is short | CERC54 (6.2 cm); organizers 2025 ("each center justified"); D 1.2, TITLE_PRIOR (d) |
| G_in (to the next block) | **1.3-2.2 cm** if the next column is visible. **8.8-10.8 cm** if exactly one column is invisible to M1 (6.2 + 2 × 1.7, ± 12 %) | **9-14 cm** typical, up to 26 cm. PHerc. 222: 12-13 cm from the right edge of the title to the left edge of col. 1 (Capasso, Titoli IV, FIRM); PHerc. 1457: about 12 cm (Titoli II, LIKELY); Phanias: about 25 cm | as cited |
| G_out (outward) | 1.3-2.2 cm (the previous column), or 8.8-10.8 cm (one invisible column), or open-ended blank if B is col. 1 | open-ended blank (the initial agraphon or protokollon). There is **no** ink block within 8 cm outward | Capasso IV (the title stands in the initial agraphon) |
| pitch P = s3 − s1 | **7.0-8.8 cm or 14.0-17.7 cm** (1 or 2 × 7.9 ± 12 %) | W + G_in: **11-19.5 cm** typical, up to 31 cm. It is not tied to multiples of 7.9 | derived |
| vertical extent | as tall as the text at s ≥ 119 on the same strip, i.e. the same preserved rows | shorter than the column text on the same strip: 1.5-4 cm | D 1.2 |
| line pitch within B | **6.0-6.3 mm** (CERC54: 18-19 lines in at most 11.37 cm, and 8-9 lines in 5.38 cm) | 1.0-1.5 × the text pitch, i.e. **6-9.5 mm**, with larger letters possible (a calligraphic hand) | CERC54; D 1.2 |
| line count within B | fills the preserved height at the text pitch | **2-6** | organizers 2024; D 1.2 |
| line edges | left edges aligned (std ≤ 2 mm); line widths similar | centred: line mid-points aligned (std ≤ 3 mm); line widths differ (max/min ≥ 1.3); left-edge std > 3 mm | layout convention |

### 2. Decision table for the p4-layout profile
Score each row: +1 favours (b), −1 favours (a), 0 undecided.

| measure | favours (a) (−1) | undecided (0) | favours (b) (+1) |
|---|---|---|---|
| W | ≥ 5.6 cm | 4.9-5.5 cm | ≤ 4.8 cm |
| G_in | 1.0-2.5 cm | 8.8-10.8 cm, or 2.6-8.7 cm (fits neither: flag it) | 10.9-14.5 cm; also 14.6-26 cm, but score that +0.5 |
| P | 7.0-8.8 cm, or 14.0-17.7 cm **and** W ≥ 4.9 cm | 14.0-17.7 cm with W ≤ 4.8 cm | 8.9-13.9 cm, or 17.8-31 cm |
| G_out | an ink block within 1.0-2.5 cm or 8.8-10.8 cm outward | no baseline available outward (s < 95 not profiled) | blank ≥ 8 cm outward over valid-fraction ≥ 0.5 bins |
| row consistency (the per-row r1-r6 s-extents of B) | extents equal within 3 mm on ≥ 2 rows | only 1 row carries signal | the widths differ by ≥ 30 % between rows, with the mid-points aligned within 3 mm |

Verdict:
- Sum ≥ +3 means **layout favours (b)**; ≤ −3 means **favours (a)**; otherwise undecided.
- A row is skipped (0) if the valid fraction is < 0.5 over the bins concerned.
- The verdict is descriptive only (DECL-P4-25-A2 item 2).
- Note, fixed now: the geometry already reported gives s1 ≈ 105 and s3 ≈ 119, i.e. P ≈ 14 cm. That sits at the (a) two-pitch lower bound (14.0) and inside the (b) range. **P alone therefore cannot decide**; W and G_in carry the weight.

### 3. Other numbers-only discriminators (to run in addition, if declared)
1. **The line-pitch ratio R.** Take the 0.5 mm z-profile over B's s-range, and the same over N's s-range (the text cluster at s ≥ 119, same strip, same rows); estimate each pitch by autocorrelation. R = pitch(B)/pitch(N): **R ≥ 1.2 favours (b)**, 0.9-1.1 favours (a).
2. **The vertical-extent ratio** of B's rows to N's rows on the same strip (rows with signal above baseline): ≤ 0.6 favours (b); ≥ 0.9 favours (a). This is confounded by damage, so compare within the same strip only.
3. **The surface integrity of s 60-101 cm** (REDTEAM N7), measured on raw CT at d* (deposit fraction and two-layer fibre structure):
   - (b) needs this region to be *blank papyrus* (agraphon or protokollon);
   - if it is intact **and** carries deposits at a text-like fraction, then col. 1 lies further out, and B is a column: favours (a).
   - Control: the text cells at s ≥ 119; null: the blank end of the inner strip.
4. **A kollesis or protokollon join outward of B** (REDTEAM N5): a double-thickness band 1-2 cm wide in s < 105. A protokollon with vertical recto fibres directly outward of B favours (b). It is weak and optional.

### 4. L6 re-weight given P4-M-OUT2-P2-RESULT (UNCERTAIN)
- **Baseline shift, independent of the candidate.** Text-like signal at s ≥ 105-119 cm on w122-123 shows that the outer part of the roll is at least partly preserved. So P(beginning preserved) rises from 0.3 to 0.45, and baseline L6 = 0.25 × 0.45 × 0.6 ≈ **0.07**.
- **The candidate before the extended test and the layout.**
  - P(pattern | a) ≈ 0.3: M1 on this strip is spotty (text-like only in r3-r4), so invisible neighbour columns are plausible.
  - P(pattern | b) ≈ 0.6.
  - The block's apparent width of at most about 4-5 cm (c3 and c6 are empty) gives an LR of about 2 for (b).
  - Prior P(b) ≈ 0.075, from an initial title existing (0.25) × being preserved here (0.3).
  - **P(b) ≈ 0.25 (range 0.1-0.4).**
- Conditional on the outcomes:

| extended test | layout verdict | P(B is an initial-title block) | L6 (a readable initial title in hand or recoverable) |
|---|---|---|---|
| EXT-CONFIRMED | favours (b) | about 0.65 | about 0.6 |
| EXT-CONFIRMED | undecided | about 0.30 | about 0.3 |
| EXT-CONFIRMED | favours (a) | about 0.07 | about 0.08 (the baseline, plus a small chance of a title further out) |
| not confirmed | favours (b) | about 0.45 (the block is real ink, but M1 is not legible enough) | about 0.15; go to raw-CT L3 and P4-W on B |
| not confirmed | undecided or (a) | about 0.15 or 0.05 | about 0.07 (the baseline) |

Red-team caveat, fixed in advance:
- Under (b), the traced sheet outward of B (s < 101 cm, about 1 m, w124-w129) must be blank or unreadable.
- A blank of about 1 m is longer than any attested initial agraphon (12-25 cm). So (b) implies that most of that metre is **damaged or unreadable** outer layers, not blank. If it is damaged, text columns could lie there invisibly, and then "col. 1 at s = 119" is unproven.
- Discriminator 3 (surface integrity of s 60-101) is therefore the most important supporting number.

Integrity: no issues. This was written before any layout-profile number existed. No image or letter content was seen. No title word was written.
