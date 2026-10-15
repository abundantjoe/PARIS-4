"""Per-tile geometry for P4-M-OUT (DECL-P4-15 item a): median z, median radius from the official umbilicus,
minimum distance to the 8 labelled Paris 4 segments (labelled-adjacent if < 1.2 mm), row-wise Spearman of
column vs radius. Numbers only; reads mesh vertex coordinates, never image pixels.
Provenance: Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7
usage: tile_geom_w128.py <out_dir with tile_points.npz> <result.json>
"""
import io, json, sys, urllib.request, hashlib
import numpy as np, tifffile
from scipy.spatial import cKDTree
from scipy.stats import spearmanr
B = "https://vesuvius-challenge-open-data.s3.amazonaws.com/PHercParis4/"
UMB = "representations/umbilicus/20260411134726-umbilicus-20260524235033.json"
LAB = ["20231016151002", "20230702185753", "20231031143852", "20231106155351",
       "20231012184424", "20231210121321", "20231007101619", "20230929220926"]
VOX_MM = 0.0024
out_dir, res_path = sys.argv[1:3]
ub = urllib.request.urlopen(B + UMB).read()
U = np.array(sorted([[p["z"], p["x"], p["y"]] for p in json.loads(ub)["control_points"]]), float)
prov = {"umbilicus": {"key": UMB, "sha256": hashlib.sha256(ub).hexdigest(), "n_points": len(U)}, "labelled_meshes": {}}
pts = []
for sid in LAB:
    base = f"{B}segments/{sid}/mesh/{sid}-on-20260411134726-2.4um.tifxyz/"
    X = {}
    for c in "xyz":
        b = urllib.request.urlopen(base + c + ".tif").read()
        prov["labelled_meshes"].setdefault(sid, {})[c + ".tif"] = {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
        X[c] = tifffile.imread(io.BytesIO(b)).astype(np.float32)
    ok = (X["x"] != -1) & (X["y"] != -1) & (X["z"] != -1) & np.isfinite(X["z"])
    pts.append(np.stack([X["x"][ok], X["y"][ok], X["z"][ok]], 1))
    prov["labelled_meshes"][sid]["n_valid"] = int(ok.sum())
tree = cKDTree(np.concatenate(pts))
d = np.load(f"{out_dir}/tile_points.npz")
tiles = {}
for k in d.files:
    P = d[k].astype(np.float64)
    r = np.hypot(P[:, 0] - np.interp(P[:, 2], U[:, 0], U[:, 1]), P[:, 1] - np.interp(P[:, 2], U[:, 0], U[:, 2])) * VOX_MM
    dist, _ = tree.query(P)
    rr, cc = (int(v) for v in k[1:].split("_c"))
    tiles[k] = {"r": rr, "c": cc, "n_points": int(len(P)), "median_z_mm": round(float(np.median(P[:, 2])) * VOX_MM, 3),
                "median_r_mm": round(float(np.median(r)), 3), "r_mm_p10_p90": [round(float(np.percentile(r, q)), 3) for q in (10, 90)],
                "min_dist_labelled_mm": round(float(dist.min()) * VOX_MM, 3),
                "labelled_adjacent": bool(dist.min() * VOX_MM < 1.2)}
rows = {}
for t in tiles.values():
    rows.setdefault(t["r"], []).append(t)
per_row = {}
for r, L in sorted(rows.items()):
    L.sort(key=lambda t: t["c"])
    per_row[r] = {"n": len(L), "spearman_col_vs_median_r": round(float(spearmanr([t["c"] for t in L], [t["median_r_mm"] for t in L])[0]), 3) if len(L) > 2 else None,
                  "median_r_first_last_mm": [L[0]["median_r_mm"], L[-1]["median_r_mm"]]}
allt = list(tiles.values())
pooled = float(spearmanr([t["c"] for t in allt], [t["median_r_mm"] for t in allt])[0])  # scipy ranks ties by average
json.dump({"provenance": "Project HERCULES | owner Joseph Balmaceda | HRC-JB-0924-O7", "sources": prov,
           "method": "radius = horizontal distance from the umbilicus polyline (linear in z) at each saved tile point; min distance = nearest valid vertex of the 8 labelled 2.4um meshes (vertex spacing ~48 um); labelled_adjacent iff < 1.2 mm",
           "pooled_spearman_col_vs_median_r_tie_averaged": round(pooled, 3),
           "outward_direction": "increasing column" if pooled > 0 else "decreasing column",
           "per_row": per_row, "tiles": dict(sorted(tiles.items(), key=lambda kv: (kv[1]["r"], kv[1]["c"])))}, open(res_path, "w"), indent=1)
print(round(pooled, 3), {r: v["spearman_col_vs_median_r"] for r, v in per_row.items()},
      "min_dist_mm", min(t["min_dist_labelled_mm"] for t in allt), "adjacent", sum(t["labelled_adjacent"] for t in allt))
