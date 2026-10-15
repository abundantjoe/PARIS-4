"""DECL-P4-25-A2 item 2: layout profile of 20260701183148-w122-123 (M1 prediction), numbers only.

Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7
The P4-M item 1 method (col_profile.py / profile_analyze.py), applied along the spiral coordinate s.
Nothing is displayed; the TIFF is decoded tile by tile and reduced to bin sums.

- s(row, col): p4-inner locator_geometry.json (08292cbf) definition, recomputed from the official tifxyz: per grid
  row, cumulative 3-D length from the row's first valid column, gaps bridged by the straight 3-D chord between
  consecutive valid vertices; plus the strip offset 97.23 cm. Validated against every locator tile value.
- Canvas px (i, j) -> grid (i // 20, j // 20) (strip rule, scale exactly 20); mesh-valid = that vertex valid.
  s of a pixel = s of that vertex (48 um grid step; nearest).
- Bins: 1 mm in s over 95-135 cm, per tile row r1-r6 (canvas rows [rT, (r+1)T), T = 8324), and per 1 mm canvas
  row (for vertical profiles). Per bin: z-summed M1 value, mesh-valid px count, valid fraction
  = count / (px_per_mm x band height in px) (1 mm of s ~ px_per_mm canvas columns).
- Block statistic: the mean prediction over mesh-valid px (sum / count), as in P4-M item 1. Bins with valid
  fraction < 0.5 are not used (Q6 rule). Baseline = median + 3 MAD (raw MAD) of the used bins in s 95-100 and
  128-135 cm. Blocks = runs above the baseline, merged across gaps <= 2 mm (P4-M item 1 merge); raw runs listed.
- Per block: start, end, width W, gaps to neighbours (G_out outward = lower s, G_in inward), start-to-start pitch
  P; per-row (r1..r6) extents; a vertical profile (1 mm canvas-row bins over the block's s-range, vs the same rows
  over the baseline s bins) giving the vertical extent (rows above that row's baseline + 3 sd of r-noise) and the
  line pitch (periodogram peak of the detrended vertical profile over the extent, 4-8 mm) and line count.
Usage: python w122_profile.py <dir with mesh_[xyz].tif, m1_pred.tif> <locator_geometry.json> <census_mo2c.json> <out.json>
"""
import json, sys, time, hashlib
import numpy as np, tifffile

SEG = "20260701183148-w122-123"
OFFSET_CM = 97.23
S0, S1 = 950, 1350  # mm
BASE = [(950, 1000), (1280, 1350)]
ROWS = range(1, 7)


def s_grid(P, valid):
    gh, gw, _ = P.shape
    S = np.full((gh, gw), np.nan)
    for i in range(gh):
        j = np.nonzero(valid[i])[0]
        if len(j) == 0:
            continue
        d = np.linalg.norm(np.diff(P[i, j], axis=0), axis=1)
        S[i, j] = np.r_[0, np.cumsum(d)]
    return S * 0.0024 / 10 + OFFSET_CM  # cm


def main(d, loc, census, out):
    t0 = time.time()
    P = np.stack([tifffile.imread(f"{d}/mesh_{a}.tif").astype(np.float64) for a in "xyz"], -1)
    valid = (P != -1).all(-1) & np.isfinite(P).all(-1)
    Sg = s_grid(P, valid)
    gh, gw = valid.shape
    L = json.load(open(loc))["strips"]["w122-123"]
    tf = tifffile.TiffFile(f"{d}/m1_pred.tif")
    p = tf.pages[0]
    H, W = p.shape
    assert H == 20 * gh and W == 20 * gw
    T = 8324
    px = 416.19747127139743
    # validate s against the locator tiles (median over the tile's grid rows at its centre column)
    diffs = []
    for k, t in L["tiles"].items():
        r, c = t["r"], t["c"]
        gc = int((c * T + T / 2) // 20)
        rows = slice(-(-r * T // 20), min(-(-(r + 1) * T // 20), gh))
        v = Sg[rows, min(gc, gw - 1)]
        if np.isfinite(v).any():
            diffs.append(abs(float(np.nanmedian(v)) - t["s_from_outer_end_cm"]))
    val = {"n_tiles": len(diffs), "abs_diff_cm_max": round(max(diffs), 3), "abs_diff_cm_p50": round(float(np.median(diffs)), 4)}
    print("s validation", val, flush=True)
    nb = S1 - S0
    NR = int(np.ceil(H / px))
    Sr = np.zeros((7, nb)); Nr = np.zeros((7, nb))             # per tile row
    Sv = np.zeros((NR, nb)); Nv = np.zeros((NR, nb))           # per 1 mm canvas row
    th, tw = p.tilelength, p.tilewidth
    ntx, nty = -(-W // tw), -(-H // th)
    fh = tf.filehandle
    for ty in range(nty):
        y0 = ty * th
        if y0 >= 7 * T or y0 + th <= T:
            continue
        for tx in range(ntx):
            idx = ty * ntx + tx
            x0 = tx * tw
            y1, x1 = min(y0 + th, H), min(x0 + tw, W)
            ys, xs = np.arange(y0, y1), np.arange(x0, x1)
            gi, gj = ys // 20, xs // 20
            sb = np.floor(Sg[np.ix_(gi, gj)] * 10).astype(float) - S0  # mm bin index
            m = valid[np.ix_(gi, gj)] & np.isfinite(sb) & (sb >= 0) & (sb < nb) & ((ys >= T) & (ys < 7 * T))[:, None]
            if not m.any():
                continue
            if p.databytecounts[idx] == 0:
                seg = np.zeros((th, tw), np.uint8)
            else:
                fh.seek(p.dataoffsets[idx])
                seg, _, _ = p.decode(fh.read(p.databytecounts[idx]), idx)
                seg = np.asarray(seg).reshape(th, tw)
            seg = seg[: y1 - y0, : x1 - x0].astype(np.float64)
            sbi = np.where(m, sb, 0).astype(int)
            rr = np.broadcast_to((ys // T)[:, None], m.shape)
            vr = np.broadcast_to((ys / px).astype(int)[:, None], m.shape)
            np.add.at(Sr, (rr[m], sbi[m]), seg[m]); np.add.at(Nr, (rr[m], sbi[m]), 1)
            np.add.at(Sv, (vr[m], sbi[m]), seg[m]); np.add.at(Nv, (vr[m], sbi[m]), 1)
        print("tile row", ty, "/", nty, "%.0fs" % (time.time() - t0), flush=True)
    np.savez_compressed(out.replace(".json", "_bins.npz"), Sr=Sr, Nr=Nr, Sv=Sv, Nv=Nv)
    s_mm = np.arange(S0, S1)
    S16, N16 = Sr[1:7].sum(0), Nr[1:7].sum(0)
    vf = N16 / (px * 6 * T)
    mean = np.where(N16 > 0, S16 / np.maximum(N16, 1), np.nan)
    used = vf >= 0.5
    bmask = np.zeros(nb, bool)
    for a, b in BASE:
        bmask |= (s_mm >= a) & (s_mm < b)
    bvals = mean[bmask & used]
    med = float(np.median(bvals)); mad = float(np.median(np.abs(bvals - med)))
    thr = med + 3 * mad
    thr_scaled = med + 3 * 1.4826 * mad
    above = used & (np.nan_to_num(mean, nan=-1) > thr)

    def runs(mask):
        out, st = [], None
        for i, a in enumerate(mask):
            if a and st is None:
                st = i
            if not a and st is not None:
                out.append([st, i - 1]); st = None
        if st is not None:
            out.append([st, len(mask) - 1])
        return out
    raw = runs(above)
    merged = []
    for r in raw:
        if merged and r[0] - merged[-1][1] - 1 <= 2:
            merged[-1][1] = r[1]
        else:
            merged.append(list(r))
    # vertical noise per canvas row: sd over baseline bins
    vm = np.where(Nv > 0, Sv / np.maximum(Nv, 1), np.nan)

    def vprofile(a, b):
        sl = slice(a, b + 1)
        num, den = Sv[:, sl].sum(1), Nv[:, sl].sum(1)
        prof = np.where(den > 0, num / np.maximum(den, 1), np.nan)
        bnum, bden = Sv[:, bmask].sum(1), Nv[:, bmask].sum(1)
        bprof = np.where(bden > 0, bnum / np.maximum(bden, 1), np.nan)
        dd = prof - bprof
        rows = np.arange(len(dd))
        inband = (rows >= int(T / px)) & (rows < int(7 * T / px))
        noise = np.nanstd(vm[:, bmask][inband], axis=1)
        nz = float(np.nanmedian(noise))
        ab = inband & np.isfinite(dd) & (dd > 3 * nz)
        idx = np.nonzero(ab)[0]
        res = {"row_mm_above": idx.tolist(), "noise_sd_med": round(nz, 3)}
        if len(idx):
            lo, hi = int(idx.min()), int(idx.max())
            res["extent_row_mm"] = [lo, hi]
            res["extent_mm"] = hi - lo + 1
            x = dd[lo:hi + 1].copy()
            ok = np.isfinite(x)
            if ok.sum() >= 12:
                ii = np.arange(len(x))
                x = np.where(ok, x, np.interp(ii, ii[ok], x[ok]))
                x = x - np.polyval(np.polyfit(ii, x, 1), ii)
                Z = 32
                F = np.abs(np.fft.rfft(x * np.hanning(len(x)), n=Z * len(x))) ** 2
                f = np.fft.rfftfreq(Z * len(x))
                per = np.where(f > 0, 1 / np.maximum(f, 1e-12), np.inf)
                band = (per >= 4) & (per <= 8)
                k = np.nonzero(band)[0][np.argmax(F[band])]
                ref = (per >= 2) & (per <= 30) & ~band
                interior = bool(band[k - 1] and band[k + 1])
                res.update({"line_pitch_mm": round(float(per[k]), 2), "line_peak_snr": round(float(F[k] / np.median(F[ref])), 2),
                            "line_peak_interior": interior,
                            "line_count_est": round(float(len(x) / per[k]), 1),
                            "note": "extent %d mm -> native frequency resolution coarse; pitch valid only if interior and snr >= 3" % len(x)})
        return res
    blocks = []
    for n, (a, b) in enumerate(merged):
        per_row = {}
        for r in ROWS:
            mr = np.where(Nr[r] > 0, Sr[r] / np.maximum(Nr[r], 1), np.nan)
            vfr = Nr[r] / (px * T)
            sub = [i for i in range(a, b + 1) if vfr[i] >= 0.5 and mr[i] > thr]
            per_row[f"r{r}"] = {"extent_mm": [int(s_mm[min(sub)]), int(s_mm[max(sub)])] if sub else None,
                                "n_bins_above": len(sub), "valid_frac_mean": round(float(vfr[a:b + 1].mean()), 3)}
        blk = {"id": n, "start_mm": int(s_mm[a]), "end_mm": int(s_mm[b]), "width_mm": int(b - a + 1),
               "n_raw_runs": sum(1 for r in raw if r[0] >= a and r[1] <= b),
               "mean_value": round(float(np.nanmean(mean[a:b + 1])), 2), "per_row": per_row, "vertical": vprofile(a, b)}
        blocks.append(blk)
    for i, blk in enumerate(blocks):
        blk["gap_out_mm"] = blk["start_mm"] - blocks[i - 1]["end_mm"] - 1 if i > 0 else None
        blk["gap_in_mm"] = blocks[i + 1]["start_mm"] - blk["end_mm"] - 1 if i + 1 < len(blocks) else None
        blk["pitch_next_start_mm"] = blocks[i + 1]["start_mm"] - blk["start_mm"] if i + 1 < len(blocks) else None
    # census of tiles covering the baseline bins (rows r1-r6)
    cen = json.load(open(census))
    ct = {}
    for v in cen["tiles"].values():
        if v.get("strip") == SEG:
            ct[(v["r"], v["c"])] = v
    base_tiles = sorted({(t["r"], t["c"]) for t in L["tiles"].values()
                         if t["r"] in ROWS and any(a / 10 - 2 <= t["s_from_outer_end_cm"] <= b / 10 + 2 for a, b in BASE)})
    base_census = {f"r{r}_c{c}": (ct[(r, c)]["rows"], ct[(r, c)]["n_letters"]) if (r, c) in ct else None for r, c in base_tiles}
    res = {"provenance": "Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7",
           "declaration": "RULES.md DECL-P4-25-A2 item 2 (layout profile), after p4-titulus QA.md Q6 (78965ad)",
           "segment": SEG, "prediction_sha256": "bab5655721bc2a0271dc613d9f6778e0165e557cd50a23ef35bd1d4f5d07c530",
           "method": __doc__.split("\n\n", 1)[1].split("Usage")[0].strip(),
           "s_validation_vs_locator": val,
           "s_coverage_mm": {"strip_s_min_mm": round(float(np.nanmin(Sg)) * 10, 1), "strip_s_max_mm": round(float(np.nanmax(Sg)) * 10, 1),
                             "bins_with_valid_frac_ge_0p5": [int(s_mm[i]) for i in (np.nonzero(used)[0][[0, -1]] if used.any() else [])]},
           "baseline": {"bins_used": int((bmask & used).sum()), "bins_declared": int(bmask.sum()),
                        "median": round(med, 3), "mad": round(mad, 3), "threshold_med_plus_3mad": round(thr, 3),
                        "threshold_scaled_mad_sensitivity": round(thr_scaled, 3), "census_of_baseline_tiles": base_census},
           "profile": {"s_mm": s_mm.tolist(), "z_sum_r1_r6": [round(float(x), 1) for x in S16],
                       "mean_r1_r6": [None if not np.isfinite(x) else round(float(x), 3) for x in mean],
                       "valid_frac_r1_r6": [round(float(x), 3) for x in vf]},
           "raw_runs_mm": [[int(s_mm[a]), int(s_mm[b])] for a, b in raw],
           "blocks": blocks, "seconds": round(time.time() - t0, 1)}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: res[k] for k in ("s_coverage_mm", "baseline")}, indent=0))
    for b in blocks:
        print(b["start_mm"], b["end_mm"], "W", b["width_mm"], "Gout", b["gap_out_mm"], "Gin", b["gap_in_mm"], "P", b["pitch_next_start_mm"],
              "rows", {k: v["extent_mm"] for k, v in b["per_row"].items()}, "vert", {k: b["vertical"].get(k) for k in ("extent_row_mm", "line_pitch_mm", "line_peak_snr", "line_peak_interior", "line_count_est")})


if __name__ == "__main__":
    main(*sys.argv[1:])
