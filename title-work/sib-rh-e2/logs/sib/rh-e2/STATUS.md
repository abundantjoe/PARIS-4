Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7

# rh-e2 STATUS (DECL-REMOTE-HARNESS-1, P4-E material E2)

State: DONE. COMMIT A f2502c2 (pre-read, pushed before any reader); COMMIT B (this commit) holds the reads.

- Code: tools/p4/*.py sha256 == METRIC-HASH-27 (norm_manifest b549026e, p4_jobs 1ebc3e74, score_p4 581bc41e, p4_phase2 b99335e8, p4_ext cd240108); audit.py e36cb995 == METRIC-HASH-5. Base commit 0e30894.
- Builder: claude/gifted-bell-gavnl5-sib-pairs0814b @ cc81a67748f62b46b23678d9eb7a0e738bf85fac, logs/sib/pairs0814b/e2/.
- norm_manifest (no --coverage): eligible 160, skipped mesh_valid 0, coverage 0, unique png 160.
- import e2: 160 tiles, key sha256 76c3c62f...797794.
- null ne2: n 20 (= ceil(160/8)), seed 20297847, key sha256 351f64b7...ef6519.
- jobs census_e2 (sigma2): 20 sessions of 8 census + 1 N0, key sheet v2 first; 180 tile images.
- Recipient: orchestrator age key age1vp0t...rstvvcq5 (public key only in this container).
- Sub-siblings: none (briefs reference local uuid files, incl. 20 derived N0 PNGs; a split would need a byte-exact rebuild in another container for little time saved).

- Reads: 20 fresh general-purpose agents, model opus, <= 4 concurrent, prompt = brief text. Each made 12 tool calls (10 Reads, 1 sealed write, hand-back).
- Audit (tools/sib/rh-e2/audit_e2.py -> hercules.harness.audit.audit, sealed-output, orchestrator recipient): 20/20 VALID; prompt == brief 20/20; hand-back == DONE 20/20; 10/10 listed images read in every job, 0 unread; 0 violations; image bytes unchanged since commit A 20/20; .age sha256 == audit answer_sha256 20/20.
- Re-runs: 0. Integrity events: none. No answer was read, decrypted or quoted by this sibling.
- Commit B: B/age/<job>.age (20), B/audit.json, B/harness_jobs.tsv, B/transcripts/<job>.jsonl.gz (20, ~80 MB), B/SHA256SUMS.
Next (orchestrator, DECL-REMOTE-HARNESS-1 item 7): verify key sha256 vs commit A, independent re-audit of the pushed transcripts, then decrypt/score locally with score_p4.py.
Blockers: none.

## P4-L (DECL-P4-12) harness, from 2026-09-26 18:17Z
State: WAITING for builder p4-l2 (origin/claude/gifted-bell-gavnl5-sib-p4-l2, logs/sib/p4-l2/l2/manifest.json). Branch did not exist at 18:20Z.
- Merged orchestrator head 3cf5756; norm_manifest.py sha256 d2faee66 (METRIC-HASH-29), p4_jobs.py 1ebc3e74, audit.py e36cb995.
- Polling git ls-remote every 5 min. Full manifest -> batches l2 / nl2 / census_l2. A partial r0-r1 manifest -> early batch l2a / nl2a / census_l2a, rest later as l2b.
- Layout: logs/sib/rh-e2/L2/A (pre-read, pushed before any reader), logs/sib/rh-e2/L2/B.
- 18:28Z DECL-P4-12-A1: merged orchestrator head d401ecd (contains 696c893). Verified vs METRIC-HASH-35: p4_jobs.py 7966d6b1, p4_phase2.py df93f9bf, p4_ext.py b58d555d, k_d2_task_sigma2t.txt f07fbdff, ref_brief_sigma2.txt 82c7008e, ref_brief_sigma2t.txt 627ebb0f (all equal). P4-L jobs will use variant sigma2t; builder_ref.json will record the new p4_jobs.py hash and k_d2_task_sigma2t.txt.
Blockers: none (waiting on builder).
- 18:40Z L2 batch l2a (early, partial manifest): builder p4-l2 @ d0b8360e (partial=true, 24 tiles: r0 c0-c19, r1 c0-c3). norm_manifest: 24 eligible, 0 skipped. import l2a 24 (key 7d2af1d0...), null nl2a 3 (seed 20328375, key c05250c8...), jobs census_l2a sigma2t: 3 sessions (8 + 1 N0). Briefs match logs/p4/ref_brief_sigma2t.txt template. COMMIT A = logs/sib/rh-e2/L2/A/l2a, pushed before any l2a reader. Remainder later as l2b (tiles not in l2a only).
- 18:47Z l2a reads: 3 fresh general-purpose opus readers (prompt = brief), each 12 tool calls. Audit 3/3 VALID; prompt == brief 3/3; hand-back DONE 3/3; 10/10 images read each, 0 unread; 0 violations; images unchanged since commit A; .age sha256 == audit answer_sha256 3/3. Re-runs 0. COMMIT B = logs/sib/rh-e2/L2/B/l2a.
- Builder p4-l2 manifest still partial (36 tiles at 18:47Z). Waiting for the non-partial manifest; the remainder (tiles not in l2a) runs as l2b / nl2b / census_l2b.
- 21:20Z L2 batch l2b: builder p4-l2 @ 152c0bb9 (partial=false, 160 tiles; checks all true). norm_manifest: 160 eligible, 0 skipped; the 24 l2a (r,c) are byte-identical to l2a. l2b = 136 tiles (final minus l2a). import l2b 136 (key f5045eb8...), null nl2b 17 (seed 20274254, key c6b6bef4...), jobs census_l2b sigma2t: 17 sessions (8 + 1 N0). No key/uuid/(r,c) overlap with l2a. Briefs match ref_brief_sigma2t template. COMMIT A = logs/sib/rh-e2/L2/A/l2b, pushed before any l2b reader.
- 21:35Z l2b reads: 17 fresh general-purpose opus readers (prompt = brief), <= 4 concurrent, each 12 tool calls. Audit 17/17 VALID; prompt == brief 17/17; hand-back DONE 17/17; 10/10 images read each, 0 unread; 0 violations; images unchanged since commit A 17/17; .age sha256 == audit answer_sha256 17/17. Re-runs 0. COMMIT B = logs/sib/rh-e2/L2/B/l2b.
State: P4-L L2 COMPLETE (l2a 24 + l2b 136 = 160 tiles; 20 sessions; 20/20 VALID). Next (orchestrator): verify + score l2b. No blockers.

## P4-L3 (DECL-P4-12-A3) harness, from 2026-09-26 21:31Z
State: WAITING for builder p4-depth (origin/claude/gifted-bell-gavnl5-sib-p4-depth). At 21:40Z it has calib_params.json frozen; no calib.json (PASS/STOP) and no l3/manifest.json yet.
- Merged orchestrator head 36dcbc6; norm_manifest d2faee66, p4_jobs 7966d6b1, k_d2_task_sigma2t f07fbdff, audit e36cb995 (unchanged).
- Watcher every 5 min: calib.json STOP -> stand by; l3 manifest -> l3a (r0-r1 partial) then l3b remainder, or l3 on a full manifest; sigma2t; layout logs/sib/rh-e2/L3/A/<batch>, L3/B/<batch>.
Blockers: none (waiting on builder).

## P4-M-OUT (DECL-P4-15 item a) harness, from 2026-09-26 21:56Z
State: WAITING for builder p4-inner manifest (20260701183151-w128-129; none under logs/sib/p4-inner at 22:00Z).
- Plan: norm_manifest (METRIC-HASH-29) without --coverage; keys mo / nmo (N0 from mo only, ceil(n/8)); jobs census_mo sigma2t, 8+1; layout logs/sib/rh-e2/MO/{A,B}; COMMIT A before any reader.
- Priority: if L3 and MO are ready together, L3 first. Commit shas will be listed here.
Blockers: none (waiting on builders p4-depth and p4-inner).
- 01:00Z L3: p4-depth calib.json verdict STOP (d* -31.2 um, z 1.94 < 3; commit 5e32424c). Standing by for L3 per orders.
- 01:02Z MO batch: builder p4-inner @ 64239341 (mout/manifest.json, partial false). norm_manifest (d2faee66, no --coverage): 138 eligible, 0 skipped, 128 unique PNGs (11 tiles have prediction mean 0.0 and identical bytes; kept as declared; disclosed in MO/A/builder_ref.json; 2 of the 18 N0 are drawn from them). Code at merge 835462b: p4_jobs e9f99ce4 (METRIC-HASH-38; sigma2t path unchanged from METRIC-HASH-35), score_p4 9a5b4761. import mo 138 (key 6a136acb...), null nmo 18 (seed 20266678, key 0fd21097...), jobs census_mo sigma2t: 18 sessions (17 x 8+1, 1 x 2+1). Briefs match ref_brief_sigma2t template. COMMIT A = logs/sib/rh-e2/MO/A, pushed before any mo reader.
- 01:20Z MO reads: 18 fresh general-purpose opus readers (prompt = brief), <= 4 concurrent. Audit 18/18 VALID; prompt == brief 18/18; hand-back DONE 18/18; all listed images read (10 per 8+1 session, 4 in the 2+1 session), 0 unread; 0 violations; images unchanged since commit A 18/18; .age sha256 == audit answer_sha256 18/18. Re-runs 0. COMMIT B = logs/sib/rh-e2/MO/B.
- MO commits: A 0e7b616 (pre-read), B d83f4b41dae308a5deaa4d47206e4a8ad0dcbdac.

## P4-M-OUT2 (DECL-P4-25) harness, from 2026-09-27 06:19Z
State: WAITING for p4-inner mo2 manifests (none under logs/sib/p4-inner/mo2 at 06:20Z). Code at merge ef63cec unchanged (norm_manifest d2faee66, p4_jobs e9f99ce4, sigma2t f07fbdff, audit e36cb995).
- Batch naming: the order names mo2 / nmo2 / census_mo2; the three strips land separately and p4_jobs import takes one strip per manifest, so each strip is its own self-contained batch, suffixed per strip as with l2a/l2b: w126-127 -> mo2a / nmo2a / census_mo2a; w124-125 -> mo2b ...; w122-123 -> mo2c .... N0 per strip from that strip's own tiles (within "this material"). Layout logs/sib/rh-e2/MO2/{A,B}/<batch>.
- Watcher polls every 10 min (economy). Commit A before any reader of each batch.
- 06:45Z mo2a (w126-127): builder p4-inner @ 0f0c47d4 (mo2/w126-127/manifest.json, partial false). norm_manifest: 147 eligible, 0 skipped, 134 unique PNGs (14 all-zero identical tiles, kept as declared, disclosed in builder_ref note). import mo2a 147 (key 4efec575...), null nmo2a 19 (seed 20349461, key 3641570a...), jobs census_mo2a sigma2t: 19 sessions (18 x 8+1, 1 x 3+1). COMMIT A = logs/sib/rh-e2/MO2/A/mo2a, pushed before any mo2a reader.
- 07:15Z mo2a reads: 19 fresh general-purpose opus readers (prompt = brief), <= 4 concurrent. Audit 19/19 VALID; prompt == brief 19/19; hand-back DONE 19/19; all listed images read (10 per 8+1 session, 5 in the 3+1 session), 0 unread; 0 violations; images unchanged 19/19; .age sha256 == audit 19/19. Re-runs 0. COMMIT B = logs/sib/rh-e2/MO2/B/mo2a. mo2a commits: A cb49495, B (this commit; see RESUME.md).
- w124-125 and w122-123 manifests: not yet pushed by p4-inner (watcher running, 10-min polling).
- Correction: the "07:15Z" stamp on the mo2a reads line above was an estimate; the mo2a reads finished before 07:01Z (clock checked 07:01Z). Nothing else changes.
- 07:05Z mo2b (w124-125): builder p4-inner @ 19fc1dde (partial false). norm_manifest: 138 eligible, 0 skipped, 127 unique PNGs (12 all-zero identical tiles, kept, disclosed; 1 of 18 N0 drawn from them). import mo2b 138 (key 24a9b5c6...), null nmo2b 18 (seed 20305126, key 1dbe1b4e...), jobs census_mo2b sigma2t: 18 sessions (17 x 8+1, 1 x 2+1). COMMIT A = logs/sib/rh-e2/MO2/A/mo2b, pushed before any mo2b reader.
- 07:06Z mo2b reads: 18 fresh general-purpose opus readers (prompt = brief), <= 4 concurrent. Audit 18/18 VALID; prompt == brief 18/18; hand-back DONE 18/18; all listed images read (10 per 8+1 session, 4 in the 2+1 session), 0 unread; 0 violations; images unchanged 18/18; .age sha256 == audit 18/18. Re-runs 0. COMMIT B = logs/sib/rh-e2/MO2/B/mo2b. mo2b commits: A 370abcd, B see RESUME.md.
- w122-123 manifest: not yet pushed (watcher running, 10-min polling).
- 07:14Z mo2c (w122-123): builder p4-inner @ f7dfd1e2 (partial false). norm_manifest: 132 eligible, 0 skipped, 123 unique PNGs (10 all-zero identical tiles, kept, disclosed). import mo2c 132 (key 1b5f7270...), null nmo2c 17 (seed 20339233, key b916daac...), jobs census_mo2c sigma2t: 17 sessions (16 x 8+1, 1 x 4+1). COMMIT A = logs/sib/rh-e2/MO2/A/mo2c, pushed before any mo2c reader.
- 07:17Z mo2c reads: 17 fresh general-purpose opus readers (prompt = brief), <= 4 concurrent. Audit 17/17 VALID; prompt == brief 17/17; hand-back DONE 17/17; all listed images read (10 per 8+1 session, 6 in the 4+1 session), 0 unread; 0 violations; images unchanged 17/17; .age sha256 == audit 17/17. Re-runs 0. COMMIT B = logs/sib/rh-e2/MO2/B/mo2c. mo2c commits: A 460df3e, B see RESUME.md.
State: DECL-P4-25 harness COMPLETE (mo2a 147 + mo2b 138 + mo2c 132 = 417 tiles; 54 sessions; 54/54 VALID; 0 re-runs). Standing by. No detached processes.

## P4-M-OUT2 phase 2 p2mo2 (DECL-P4-25-A1), from 2026-09-27 07:26Z
- Inputs at orchestrator 13e9c363: logs/p4/p2_select_mo2.json (20 candidates from mo2a/b/c; sha 8efa3da3...) and logs/p4/pc_pool_m1 (15 PC PNGs; all sha256 = manifest; pool = p2_select_1.json pc_pool).
- Format adaptation (disclosed): p2_select_mo2.json holds pc_pool as a dict {source, uuids, files}; p4_phase2.py build (999cb553, unchanged) reads pc_pool as a list of uuids. Used select_p2mo2.json = identical except pc_pool = that uuids list (sha 642ec3af...; both recorded in P2MO2/A/builder_ref.json).
- build p2mo2 (sigma2t; N0 pool mo,mo2a,mo2b,mo2c): 15 sessions of 4 cand + 4 N0 + 1 PC; 20 cand, 20 N0 (mo 7, mo2a 5, mo2b 5, mo2c 3; 5 of them all-zero tiles; 0 overlap with candidates), 15 PC; N0 seed 20273453; key sha256 6b824552... Every candidate and N0 in exactly 3 sessions; copies byte-identical to sources; briefs match ref_brief_sigma2t template. COMMIT A = logs/sib/rh-e2/P2MO2/A, pushed before any reader.
- 07:31Z p2mo2 reads: 15 fresh general-purpose opus readers (prompt = brief), <= 4 concurrent. Audit 15/15 VALID; prompt == brief 15/15; hand-back DONE 15/15; 10/10 images read each, 0 unread; 0 violations; images unchanged 15/15; .age sha256 == audit 15/15. Re-runs 0 (a re-run is possible only for a void session, i.e. PC read rows N, which only the orchestrator's scoring can tell; send the session number and I run p4_phase2.py rerun). COMMIT B = logs/sib/rh-e2/P2MO2/B. p2mo2 commits: A 2335c73, B see RESUME.md.
State: p2mo2 complete; standing by for void-session re-runs or new orders.

## Extended test extmo2_1..4 (DECL-P4-25-A2 item 1; DECL-P4-3 unchanged), from 2026-09-27 07:42Z
- Candidates (p2mo2 cand files, w122-123): extmo2_1 r4 c5 0a917b2f, extmo2_2 r4 c4 e14aa2b8, extmo2_3 r3 c5 5bad9413, extmo2_4 r3 c4 63383f16.
- Build: python3 tools/p4/p4_ext.py build extmo2_<k> p2mo2 <cand> mo,mo2a,mo2b,mo2c (p4_ext 843a2664, METRIC-HASH-38; sigma2t taken from p2mo2 jobs; PC pool from select_p2mo2.json = pc_pool_m1). Each: 18 sessions (9 U / 9 R), 48 N0 (seeds 20323752 / 20334409 / 20327838 / 20273006; key sha 15ebc0a0 / 52cfc422 / e1eecde0 / 33a45e14), 18 PC copies.
- Checks per batch (tools/sib/rh-e2/commit_a_ext.py): R == rot90(U) bytes; every N0 == rot90(src); PC copies identical; N0 only from mo/mo2a/mo2b/mo2c and none excluded (cand source, PC pool, p2mo2 N0 sources); each session 8 N0 + 1 PC + U or R, no duplicate; each N0 in exactly 3 sessions; briefs match sigma2t template. All true.
- COMMIT A: extmo2_1 3cd7745, extmo2_2 6949d14, extmo2_3 e082d0c, extmo2_4 0534d2a (all pushed before any extmo2 reader).
- extmo2_1 COMMIT B e088edb: 18/18 VALID, 0 re-runs, .age sha256 == audit for all 18 (logs/sib/rh-e2/EXTMO2/B/extmo2_1). Next: verify + score (orchestrator).
- extmo2_2 COMMIT B 590bed3: 18/18 VALID, 0 re-runs, .age sha256 == audit for all 18.
- extmo2_3 COMMIT B 469bbdc: 18/18 VALID, 0 re-runs, .age sha256 == audit for all 18.
- extmo2_4 COMMIT B ba77aec: 18/18 VALID; 19 transcripts. 91e5351d attempt 1 void (API 429 before any tool call), attempt 2 valid (.r2). 2c57b4d6, 693acd80, 797b3be1 valid attempt 1 with handback_is_DONE=False (API 429 after the sealed write; kept per orchestrator 10:54Z rule: transcripts and sealed answers intact). audit_e2.py fixed so a void attempt is never credited with a later attempt's .age. .age sha256 == audit for all 18.
- EXTMO2 COMPLETE: 72/72 sessions VALID over 4 batches (73 reader runs, 1 re-run). Next: verify + score extmo2_4 (orchestrator). ASK-2 RESOLVED (orchestrator 11:07Z): the .r2 re-run of 91e5351d is accepted as the one DECL-P4-3 re-run; extmo2_4r1 form withdrawn; no further re-run. extmo2_4 verified (v2, METRIC-HASH-44) and scored by orchestrator. State: STANDBY, no harness work pending.
- 2026-09-30T04:01Z FL PHerc0826 (DECL-FL-1): BLOCKED at step 1 — detached env setup/dockerd launch denied by session permission classifier; no organizer segments in bucket (grow needed; surface pred 1.1 TB, stream only). See ASK.md ASK-3.
