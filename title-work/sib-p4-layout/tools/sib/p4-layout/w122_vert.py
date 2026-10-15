"""Q6 section-3 discriminators 1-2 (METRIC-HASH-42) on 20260701183148-w122-123, numbers only.

Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7
Same material, s definition, mask and rows (r1-r6) as w122_profile.py. For named s-ranges (block B, the s >= 119
cluster N, and the baseline bins) it accumulates the M1 prediction over mesh-valid px in 0.5 mm canvas-row bins.
- d(row) = profile(range) - profile(baseline) for the same canvas row.
- Rows above baseline: d > 3 x noise, where noise = the median over rows of the per-row sd of the baseline's 1 mm
  s-bin means (so it is the s-bin-level noise of the same rows). Vertical extent = [first, last] such row, and
  the count of such 0.5 mm rows.
- Line pitch by autocorrelation (Q6 3.1): d over the extent, linearly detrended; the first local maximum of the
  normalised autocorrelation at lags 4-12 mm (0.5 mm steps). R = pitch(B) / pitch(N).
- Vertical-extent ratio (Q6 3.2): extent(B) / extent(N) and count(B) / count(N).
Usage: python w122_vert.py <dir> <locator.json> <out.json> B=<s0_mm>:<s1_mm> N=<s0_mm>:<s1_mm>
"""
import json, sys, time
import numpy as np, tifffile
sys.path.insert(0, __import__("os").path.dirname(__file__))
from w122_profile import s_grid

T = 8324
PX = 416.19747127139743
BASE = [(950, 1000), (1280, 1350)]
VB = 0.5  # mm


def main(d, loc, out, *ranges):
    t0 = time.time()
    R = {k: tuple(int(x) for x in v.split(":")) for k, v in (r.split("=") for r in ranges)}
    P = np.stack([tifffile.imread(f"{d}/mesh_{a}.tif").astype(np.float64) for a in "xyz"], -1)
    valid = (P != -1).all(-1) & np.isfinite(P).all(-1)
    Sg = s_grid(P, valid) * 10  # mm
    gh, gw = valid.shape
    tf = tifffile.TiffFile(f"{d}/m1_pred.tif")
    p = tf.pages[0]
    H, W = p.shape
    names = list(R) + ["BASE"]
    nvb = int(np.ceil(H / PX / VB))
    acc = {k: (np.zeros(nvb), np.zeros(nvb)) for k in names}
    bs_S = np.zeros((nvb, 1350 - 950)); bs_N = np.zeros((nvb, 1350 - 950))
    # canvas columns that can hold any wanted s
    want = np.zeros(gw, bool)
    allr = list(R.values()) + BASE
    for a, b in allr:
        want |= np.any((Sg >= a) & (Sg < b + 1), axis=0)
    th, tw = p.tilelength, p.tilewidth
    ntx, nty = -(-W // tw), -(-H // th)
    fh = tf.filehandle
    for ty in range(nty):
        y0 = ty * th
        if y0 >= 7 * T or y0 + th <= T:
            continue
        for tx in range(ntx):
            x0 = tx * tw
            if not want[x0 // 20: min((x0 + tw) // 20 + 1, gw)].any():
                continue
            idx = ty * ntx + tx
            y1, x1 = min(y0 + th, H), min(x0 + tw, W)
            ys, xs = np.arange(y0, y1), np.arange(x0, x1)
            gi, gj = ys // 20, xs // 20
            s = Sg[np.ix_(gi, gj)]
            m0 = valid[np.ix_(gi, gj)] & np.isfinite(s) & ((ys >= T) & (ys < 7 * T))[:, None]
            if not m0.any():
                continue
            if p.databytecounts[idx] == 0:
                seg = np.zeros((th, tw), np.uint8)
            else:
                fh.seek(p.dataoffsets[idx])
                seg, _, _ = p.decode(fh.read(p.databytecounts[idx]), idx)
                seg = np.asarray(seg).reshape(th, tw)
            seg = seg[: y1 - y0, : x1 - x0].astype(np.float64)
            vb = np.broadcast_to((ys / PX / VB).astype(int)[:, None], m0.shape)
            for k in names:
                rr = BASE if k == "BASE" else [R[k]]
                m = np.zeros_like(m0)
                for a, b in rr:
                    m |= (s >= a) & (s < b + 1)
                m &= m0
                if m.any():
                    np.add.at(acc[k][0], vb[m], seg[m]); np.add.at(acc[k][1], vb[m], 1)
                    if k == "BASE":
                        sb = np.floor(s[m]).astype(int) - 950
                        np.add.at(bs_S, (vb[m], sb), seg[m]); np.add.at(bs_N, (vb[m], sb), 1)
    prof = {k: np.where(acc[k][1] > 0, acc[k][0] / np.maximum(acc[k][1], 1), np.nan) for k in names}
    bm = np.where(bs_N > 200, bs_S / np.maximum(bs_N, 1), np.nan)
    rows = np.arange(nvb)
    inband = (rows * VB >= T / PX) & (rows * VB < 7 * T / PX)
    noise = float(np.nanmedian(np.nanstd(bm[inband], axis=1)))
    res = {"provenance": "Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7",
           "method": __doc__.split("\n\n", 1)[1].split("Usage")[0].strip(), "ranges_mm": R, "noise": round(noise, 3), "per_range": {}}
    for k in R:
        dd = prof[k] - prof["BASE"]
        ab = inband & np.isfinite(dd) & (dd > 3 * noise)
        idx = np.nonzero(ab)[0]
        r = {"n_rows_above_0p5mm": int(len(idx))}
        if len(idx):
            lo, hi = int(idx.min()), int(idx.max())
            r["extent_mm_from_canvas_top"] = [lo * VB, (hi + 1) * VB]
            r["extent_mm"] = (hi - lo + 1) * VB
            x = dd[lo:hi + 1].copy()
            ok = np.isfinite(x)
            ii = np.arange(len(x))
            x = np.where(ok, x, np.interp(ii, ii[ok], x[ok]))
            x = x - np.polyval(np.polyfit(ii, x, 1), ii)
            ac = np.array([np.corrcoef(x[:-L], x[L:])[0, 1] if len(x) - L > 4 else np.nan for L in range(1, len(x) // 2)])
            lags = np.arange(1, len(x) // 2) * VB
            pk = [i for i in range(1, len(ac) - 1) if 4 <= lags[i] <= 12 and ac[i] >= ac[i - 1] and ac[i] >= ac[i + 1]]
            if pk:
                i = pk[0]
                r.update({"autocorr_line_pitch_mm": float(lags[i]), "autocorr_at_pitch": round(float(ac[i]), 3),
                          "line_count_est": round(r["extent_mm"] / float(lags[i]), 1)})
            r["autocorr_lags_4_12"] = {str(float(l)): round(float(a), 3) for l, a in zip(lags, ac) if 4 <= l <= 12}
        res["per_range"][k] = r
    b, n = res["per_range"].get("B", {}), res["per_range"].get("N", {})
    if b.get("autocorr_line_pitch_mm") and n.get("autocorr_line_pitch_mm"):
        res["R_line_pitch_ratio"] = round(b["autocorr_line_pitch_mm"] / n["autocorr_line_pitch_mm"], 3)
    if b.get("extent_mm") and n.get("extent_mm"):
        res["vertical_extent_ratio"] = round(b["extent_mm"] / n["extent_mm"], 3)
        res["rows_above_count_ratio"] = round(b["n_rows_above_0p5mm"] / n["n_rows_above_0p5mm"], 3)
    res["seconds"] = round(time.time() - t0, 1)
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k not in ("method",)}, indent=0)[:3000])


if __name__ == "__main__":
    main(*sys.argv[1:])
