# Provenance: Project HERCULES | HRC-JB-0924-O7
"""Q6 layout test on the stitched-window census (RULES.md DECL-P4-25-A13; table METRIC-HASH-42). Numbers only.

usage: q6_windows.py <census_summary.json> <key.json> <seg> <cand_r> <cand_c> <out.json>
TEXT window = census positive (rows Y and count >= threshold, as scored by score_p4.py, block variant).
A window's s = mean s_cm of its 4 tiles (logs/p4/regionO_S1_order.json; s increases inward).
Block = 8-connected cluster of TEXT windows containing any window that includes tile (cand_r, cand_c).
W = s-extent of the block's window centres + 4 cm; G_in = gap from the block's inner edge to the nearest TEXT
window inward (outside the block), else to the first confirmed text block (s 100.1 cm); G_out = gap outward to the
nearest TEXT window, else 'open'; P = G_in + W; line pitch = 40 mm / median 'lines' of the block's windows;
vertical extent = number of distinct window rows in the block.
Row scores (-1 fits (a) text column only, +1 fits (b) initial-title block only, 0 both/neither):
  W: (a) 5.5-7.0, (b) 2-5.5 cm.  G_in: (a) 1.3-2.2 or 8.8-10.8, (b) 9-26 cm.  P: (a) 7.0-8.8 or 14.0-17.7,
  (b) 11-19.5 cm.  G_out: +1 if open or >= 8 cm, -1 if <= 2.2 cm, else 0.
  Rows: +1 if vertical extent <= 2 window rows and line pitch in 6-9.5 mm; -1 if >= 3 window rows; else 0.
Sum >= +3 favours (b); <= -3 favours (a); else undecided.
"""
import json
import sys


def band(x, lo, hi):
    return x is not None and lo <= x <= hi


def main(summ_f, key_f, seg, cr, cc, out):
    cr, cc = int(cr), int(cc)
    S = json.load(open(summ_f)); K = json.load(open(key_f))
    order = json.load(open('logs/p4/regionO_S1_order.json'))['order']
    s_of = {(o['r'], o['c']): o['s_cm'] for o in order if o['seg'] == seg and 's_cm' in o}
    thr = S['threshold']
    win = {}
    for u, t in S['tiles'].items():
        k = K.get(u)
        if not k or k['rot'] != 0 or k['segment'] != seg:
            continue
        cnt = t.get('n_count', t['n_letters'])
        quad = [(k['r'], k['c']), (k['r'], k['c'] + 1), (k['r'] + 1, k['c']), (k['r'] + 1, k['c'] + 1)]
        ss = [s_of[q] for q in quad if q in s_of]
        win[(k['r'], k['c'])] = {'text': t['rows'] == 'Y' and cnt >= thr, 'lines': t.get('lines'), 'count': cnt,
                                 's': sum(ss) / len(ss) if ss else None}
    text = {w for w, v in win.items() if v['text']}
    seeds = [w for w in text if w[0] in (cr - 1, cr) and w[1] in (cc - 1, cc)]
    res = {'provenance': 'Project HERCULES | HRC-JB-0924-O7', 'serves': 'DECL-P4-25-A13, METRIC-HASH-42',
           'n_windows': len(win), 'n_text': len(text), 'threshold': thr,
           'windows_with_candidate': {f'{w}': win[w] for w in win if w[0] in (cr - 1, cr) and w[1] in (cc - 1, cc)}}
    if not seeds:
        res['verdict'] = 'undecided (no window support)'
    else:
        block, stack = set(seeds), list(seeds)
        while stack:
            r, c = stack.pop()
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    n = (r + dr, c + dc)
                    if n in text and n not in block:
                        block.add(n); stack.append(n)
        bs = [win[w]['s'] for w in block if win[w]['s'] is not None]
        lo, hi = min(bs), max(bs)
        W = hi - lo + 4.0
        others = [win[w]['s'] for w in text - block if win[w]['s'] is not None]
        inner = [s for s in others if s > hi]
        outer = [s for s in others if s < lo]
        G_in = (min(inner) - 2.0 - (hi + 2.0)) if inner else (100.1 - (hi + 2.0))
        G_out = ((lo - 2.0) - (max(outer) + 2.0)) if outer else None
        P = G_in + W
        lines = sorted(win[w]['lines'] for w in block if isinstance(win[w]['lines'], int) and win[w]['lines'] > 0)
        lp = (40.0 / lines[len(lines) // 2]) if lines else None
        vrows = len({w[0] for w in block})
        sc = {}
        sc['W'] = (1 if band(W, 2, 5.5) and not band(W, 5.5, 7.0) else -1 if band(W, 5.5, 7.0) and not band(W, 2, 5.5) else 0)
        a_g = band(G_in, 1.3, 2.2) or band(G_in, 8.8, 10.8); b_g = band(G_in, 9, 26)
        sc['G_in'] = 1 if b_g and not a_g else -1 if a_g and not b_g else 0
        a_p = band(P, 7.0, 8.8) or band(P, 14.0, 17.7); b_p = band(P, 11, 19.5)
        sc['P'] = 1 if b_p and not a_p else -1 if a_p and not b_p else 0
        sc['G_out'] = 1 if (G_out is None or G_out >= 8) else -1 if G_out <= 2.2 else 0
        sc['rows'] = 1 if (vrows <= 2 and band(lp, 6, 9.5)) else -1 if vrows >= 3 else 0
        tot = sum(sc.values())
        res.update(block=sorted(map(list, block)), s_range=[lo, hi], W_cm=W, G_in_cm=G_in, G_out_cm=G_out,
                   G_out_open=G_out is None, P_cm=P, line_pitch_mm=lp, vertical_window_rows=vrows, scores=sc, sum=tot,
                   verdict='favours (b) initial-title block' if tot >= 3 else 'favours (a) text column' if tot <= -3 else 'undecided')
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps({k: res[k] for k in res if k not in ('windows_with_candidate', 'block')}))


if __name__ == '__main__':
    main(*sys.argv[1:])
