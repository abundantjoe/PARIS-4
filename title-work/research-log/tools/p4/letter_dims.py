# Provenance: Project HERCULES | HRC-JB-0924-O7
"""Letter dimensions for a package (numbers only; no letter identity, position list or image leaves this script).

usage: letter_dims.py <jobs.json> <key.json> <out.json>
For every VALID session (audited record), the sealed answer is opened through hercules.harness.collect.load_answer
(logged in logs/key_reads.tsv). For the items whose key role is U (the candidate, upright) and pc (known text), it
collects each named letter's box height and width (px) and centre y. Output per role: n letters, median and IQR of
height and width in px and mm (53.4 px/mm), and a line-pitch estimate: box centres sorted by y are split into lines
wherever consecutive centres differ by more than 0.6 x the median box height; line pitch = median distance between
consecutive line means. Only these aggregates are written.
"""
import json
import sys

import numpy as np

sys.path.insert(0, 'src')
PX_PER_MM = 53.4


def main(jobs_file, key_file, out):
    from hercules.harness.collect import load_answer
    key = json.load(open(key_file))
    role = {u: v['role'] for u, v in key.items()}
    acc = {'U': [], 'pc': []}
    for j in json.load(open(jobs_file))['jobs']:
        rec = json.load(open(f"/work/jobs/{j['job']}.json"))
        if not rec.get('valid'):
            continue
        ans = load_answer(rec['out'], 'letter-dims')
        for it in ans.get('items', []):
            r = role.get(it.get('id'))
            if r not in acc:
                continue
            boxes = [l['box'] for l in (it.get('left') or {}).get('letters') or []
                     if isinstance(l, dict) and isinstance(l.get('box'), list) and len(l['box']) == 4]
            acc[r].append([(b[3] - b[1], b[2] - b[0], (b[1] + b[3]) / 2) for b in boxes if b[3] > b[1] and b[2] > b[0]])
    res = {'provenance': 'Project HERCULES | HRC-JB-0924-O7', 'px_per_mm': PX_PER_MM, 'jobs': jobs_file}
    for r, reads in acc.items():
        hs = np.array([h for rd in reads for h, _, _ in rd], float)
        ws = np.array([w for rd in reads for _, w, _ in rd], float)
        pitches = []
        for rd in reads:
            if len(rd) < 3:
                continue
            ys = np.sort([y for _, _, y in rd])
            mh = np.median([h for h, _, _ in rd])
            lines, cur = [], [ys[0]]
            for y in ys[1:]:
                if y - cur[-1] > 0.6 * mh:
                    lines.append(np.mean(cur)); cur = [y]
                else:
                    cur.append(y)
            lines.append(np.mean(cur))
            if len(lines) >= 2:
                pitches += list(np.diff(lines))
        q = lambda a, p: float(np.percentile(a, p)) if len(a) else None
        res[r] = {'n_reads': len(reads), 'n_letters': int(len(hs)),
                  'height_px_median': q(hs, 50), 'height_px_iqr': [q(hs, 25), q(hs, 75)],
                  'height_mm_median': (q(hs, 50) / PX_PER_MM) if len(hs) else None,
                  'width_mm_median': (q(ws, 50) / PX_PER_MM) if len(ws) else None,
                  'line_pitch_mm_median': (float(np.median(pitches)) / PX_PER_MM) if pitches else None,
                  'n_line_gaps': len(pitches)}
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps({r: res[r] for r in acc}))


if __name__ == '__main__':
    main(*sys.argv[1:])
