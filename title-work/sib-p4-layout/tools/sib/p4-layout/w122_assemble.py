"""Assemble logs/sib/p4-layout/w122_profile.json: DECL-P4-25-A2 item 2 profile, Q6 section-3 discriminators 1-2,
and the Q6 section-2 decision table applied mechanically (METRIC-HASH-42). Numbers only.

Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7
B = the declared block (w122_profile.py) that contains the P4 candidate tiles r3-r4 c4-c5 (s ~105-109 cm).
Usage: python w122_assemble.py <w122_profile.json> <w122_vert.json> <out.json>
"""
import json, sys
import numpy as np


def score_table(B, blocks, i, vf_out_bins):
    """Q6 section 2, row by row, exactly as pre-registered. Widths in cm."""
    W = B["width_mm"] / 10
    rows = {}
    rows["W"] = -1 if W >= 5.6 else (1 if W <= 4.8 else 0)
    gin = B["gap_in_mm"] / 10 if B["gap_in_mm"] is not None else None
    if gin is None:
        rows["G_in"] = 0; gin_flag = "no inward block"
    elif 1.0 <= gin <= 2.5:
        rows["G_in"] = -1; gin_flag = ""
    elif 8.8 <= gin <= 10.8:
        rows["G_in"] = 0; gin_flag = ""
    elif 10.9 <= gin <= 14.5:
        rows["G_in"] = 1; gin_flag = ""
    elif 14.6 <= gin <= 26:
        rows["G_in"] = 0.5; gin_flag = ""
    else:
        rows["G_in"] = 0; gin_flag = "FLAG: G_in fits neither (a) nor (b) (2.6-8.7 cm or out of range)"
    P = B["pitch_next_start_mm"] / 10 if B["pitch_next_start_mm"] is not None else None
    if P is None:
        rows["P"] = 0
    elif 7.0 <= P <= 8.8 or (14.0 <= P <= 17.7 and W >= 4.9):
        rows["P"] = -1
    elif 14.0 <= P <= 17.7 and W <= 4.8:
        rows["P"] = 0
    elif 8.9 <= P <= 13.9 or 17.8 <= P <= 31:
        rows["P"] = 1
    else:
        rows["P"] = 0
    gout = B["gap_out_mm"] / 10 if B["gap_out_mm"] is not None else None
    if gout is not None and (1.0 <= gout <= 2.5 or 8.8 <= gout <= 10.8):
        rows["G_out"] = -1; gout_note = "ink block outward at %.1f cm" % gout
    elif gout is None and vf_out_bins["n_valid_ge_0p5"] * 0.1 >= 8.0 and vf_out_bins["all_below_baseline"]:
        rows["G_out"] = 1; gout_note = "blank >= 8 cm outward"
    else:
        rows["G_out"] = 0
        gout_note = ("no block outward on this strip; only %.1f cm of valid (>= 0.5) bins outward of B (s %s-%s mm), "
                     "then the strip ends (s < 97.2 cm lies on w124-125, not profiled): 'no baseline available outward'"
                     % (vf_out_bins["n_valid_ge_0p5"] * 0.1, vf_out_bins["s_first"], vf_out_bins["s_last"]))
    ext = [v["extent_mm"] for v in B["per_row"].values() if v["extent_mm"] and v["valid_frac_mean"] >= 0.5]
    eq = 0
    for a in range(len(ext)):
        for b in range(a + 1, len(ext)):
            if abs(ext[a][0] - ext[b][0]) <= 3 and abs(ext[a][1] - ext[b][1]) <= 3:
                eq = max(eq, 2)
    widths = [e[1] - e[0] + 1 for e in ext]
    mids = [(e[0] + e[1]) / 2 for e in ext]
    if eq >= 2:
        rows["row_consistency"] = -1
    elif len(ext) <= 1:
        rows["row_consistency"] = 0
    elif max(widths) / min(widths) >= 1.3 and max(mids) - min(mids) <= 3:
        rows["row_consistency"] = 1
    else:
        rows["row_consistency"] = 0
    total = sum(rows.values())
    verdict = "layout favours (b) initial-title block" if total >= 3 else ("layout favours (a) text column" if total <= -3 else "undecided")
    return {"row_scores": rows, "sum": total, "verdict": verdict,
            "inputs": {"W_cm": W, "G_in_cm": gin, "G_in_flag": gin_flag, "P_cm": P, "G_out_cm": gout, "G_out_note": gout_note,
                       "row_extents_mm": ext, "row_widths_mm": widths, "row_mids_mm": mids}}


def main(prof, vert, out):
    d = json.load(open(prof))
    v = json.load(open(vert))
    blocks = d["blocks"]
    i = [k for k, b in enumerate(blocks) if b["start_mm"] <= 1070 <= b["end_mm"]][0]
    B = blocks[i]
    s = np.array(d["profile"]["s_mm"])
    vf = np.array(d["profile"]["valid_frac_r1_r6"])
    mean = np.array([np.nan if x is None else x for x in d["profile"]["mean_r1_r6"]])
    outb = (s < B["start_mm"]) & (vf >= 0.5)
    vo = {"n_valid_ge_0p5": int(outb.sum()), "s_first": int(s[outb].min()) if outb.any() else None,
          "s_last": int(s[outb].max()) if outb.any() else None,
          "all_below_baseline": bool(np.all(mean[outb] <= d["baseline"]["threshold_med_plus_3mad"])) if outb.any() else None}
    table = score_table(B, blocks, i, vo)
    res = {"provenance": "Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7",
           "declaration": "RULES.md DECL-P4-25-A2 item 2; decision table and discriminators per METRIC-HASH-42 (Q6)",
           "waited_for": "32ba93c8 (p4-titulus QA.md Q6; pre-registered at 78965ad 07:43:02Z; Q6 section sha256 de2f0335.. = METRIC-HASH-42, verified)",
           "numbers_only": "no image, tile or pixel was viewed; the TIFF was decoded to arrays and reduced to bin sums",
           "segment": d["segment"], "prediction_sha256": d["prediction_sha256"],
           "s_validation_vs_locator": d["s_validation_vs_locator"], "s_coverage_mm": d["s_coverage_mm"],
           "baseline": d["baseline"],
           "blocks": [{k: b[k] for k in ("start_mm", "end_mm", "width_mm", "gap_out_mm", "gap_in_mm", "pitch_next_start_mm", "mean_value", "n_raw_runs", "per_row", "vertical")} for b in blocks],
           "B_block_index": i,
           "discriminators_q6_s3": {k: v[k] for k in v if k not in ("method", "provenance")},
           "decision_table_q6_s2": table,
           "profile": d["profile"], "raw_runs_mm": d["raw_runs_mm"], "method": d["method"]}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(table, indent=0))


if __name__ == "__main__":
    main(*sys.argv[1:])
