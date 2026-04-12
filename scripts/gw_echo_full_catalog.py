#!/usr/bin/env python3
"""Full-catalog echo search: 75 events, Abedi reproduction + frozen-star prediction.

Two parallel analyses:
  A) ABEDI REPRODUCTION: Scan GW150914 at 50-200ms to reproduce the ~100ms, ~3 sigma claim
  B) FROZEN-STAR PREDICTION: For each event, predict t_echo from M_remnant and a_spin,
     then stack the matched-filter SNR across all events

Method: ringdown-template matched filter with proper PSD whitening.
"""

from __future__ import annotations
import math, time, sys, os, json
import numpy as np

try:
    import h5py
except ImportError:
    print("ERROR: h5py required."); sys.exit(1)

G_SI = 6.674e-11; C = 2.998e8; M_SUN = 1.989e30
L_PLANCK = 1.616e-35; M_NUCLEON = 1.673e-27


def predict_echo_time(M_sun_val, a_spin=0.0):
    M = M_sun_val * M_SUN
    R_S = 2 * G_SI * M / C**2
    N_p = M / M_NUCLEON
    R_min = max(N_p**(1/3) * L_PLANCK, L_PLANCK)
    eps = R_min / R_S
    t = 2 * R_S / C * abs(math.log(eps))
    if a_spin > 0:
        r_p = R_S/2 * (1 + math.sqrt(max(0, 1-a_spin**2)))
        r_m = R_S/2 * (1 - math.sqrt(max(0, 1-a_spin**2)))
        a_m = a_spin * G_SI * M / C**2
        if r_p > r_m:
            t = 2/C * (r_p**2 + a_m**2)/(r_p - r_m) * abs(math.log(eps))
    return t


def estimate_psd(data, sr, seg_len=0):
    if seg_len <= 0: seg_len = min(4*int(sr), len(data)//4)
    seg_len = max(256, seg_len)
    overlap = seg_len//2
    freqs = np.fft.rfftfreq(seg_len, 1/sr)
    psd = np.zeros(len(freqs))
    win = np.hanning(seg_len); wn = np.sum(win**2)
    c = 0
    for i in range((len(data)-overlap)//(seg_len-overlap)):
        s = i*(seg_len-overlap); e = s+seg_len
        if e > len(data): break
        psd += np.abs(np.fft.rfft(data[s:e]*win))**2; c += 1
    return freqs, np.maximum(psd/(max(c,1)*sr*wn), 1e-50)


def whiten(data, sr, pf, pv, flo=20, fhi=500):
    n = len(data); f = np.fft.rfftfreq(n, 1/sr)
    ft = np.fft.rfft(data)
    pi = np.maximum(np.interp(f, pf, pv), 1e-50)
    ft /= np.sqrt(pi)
    ft *= (f >= flo) & (f <= fhi)
    return np.fft.irfft(ft, n)


def matched_filter(data, template):
    n = len(data); tp = np.zeros(n); tp[:len(template)] = template
    cc = np.fft.irfft(np.fft.rfft(data) * np.conj(np.fft.rfft(tp)), n)
    tn = np.sqrt(np.sum(template**2))
    dn = np.sqrt(np.mean(data**2))
    if tn > 0 and dn > 0: cc /= (tn * dn)
    return cc


def analyze_one(h1_path, l1_path, gps_merger, M_rem, a_spin, sr_expect=4096):
    """Analyze one event. Returns dict with sweep results."""
    result = {}
    t_pred = predict_echo_time(M_rem, a_spin)
    t_pred_ns = predict_echo_time(M_rem, 0.0)
    result['t_pred_kerr'] = t_pred
    result['t_pred_nonspin'] = t_pred_ns

    for det, fpath in [('H1', h1_path), ('L1', l1_path)]:
        if not fpath or not os.path.exists(fpath): continue
        try:
            with h5py.File(fpath, 'r') as f:
                strain = f['strain/Strain'][:]
                gps0 = f['meta/GPSstart'][()]
                dur = f['meta/Duration'][()]
                sr = len(strain)/dur

            mi = int((gps_merger - gps0) * sr)
            if mi < int(2*sr) or mi >= len(strain)-int(2*sr): continue

            # PSD
            pe = mi - int(sr); ps = max(0, pe - int(10*sr))
            if pe-ps < int(sr): ps=0; pe=mi-int(0.5*sr)
            pf, pv = estimate_psd(strain[ps:pe], sr)

            # Whiten
            w = whiten(strain, sr, pf, pv)

            # Template: 80ms of ringdown
            tlen = int(0.08*sr)
            tmpl = w[mi:mi+tlen].copy()
            tf = 0.3; tl = int(len(tmpl)*tf/2)
            if tl > 0:
                tmpl[:tl] *= 0.5*(1-np.cos(np.pi*np.arange(tl)/tl))
                tmpl[-tl:] *= 0.5*(1+np.cos(np.pi*np.arange(tl)/tl))

            # Post-merger data
            po = 0.15  # offset in seconds
            post = w[mi+int(po*sr):mi+int(4*sr)]
            mf = matched_filter(post, tmpl)

            # Sweep
            n_sw = 500; t_sw = np.linspace(0.010, 0.300, n_sw)
            sw_snr = np.zeros(n_sw)
            for i, te in enumerate(t_sw):
                tot = 0; cnt = 0
                for k in range(1, 8):
                    s = int((k*te - po)*sr)
                    if 0 <= s < len(mf):
                        hw = int(0.002*sr)
                        tot += np.max(np.abs(mf[max(0,s-hw):min(len(mf),s+hw+1)]))
                        cnt += 1
                sw_snr[i] = tot/max(cnt,1)

            # At prediction
            pi_k = np.argmin(np.abs(t_sw - t_pred))
            pi_ns = np.argmin(np.abs(t_sw - t_pred_ns))

            # Background (200 shifts)
            bg = np.zeros(200)
            for i in range(200):
                sh = np.random.randint(int(0.5*sr), max(int(0.5*sr)+1, len(post)-int(0.5*sr)))
                mf_s = matched_filter(np.roll(post, sh), tmpl)
                tot = 0; cnt = 0
                for k in range(1, 8):
                    s = int((k*t_pred - po)*sr)
                    if 0 <= s < len(mf_s):
                        hw = int(0.002*sr)
                        tot += np.max(np.abs(mf_s[max(0,s-hw):min(len(mf_s),s+hw+1)]))
                        cnt += 1
                bg[i] = tot/max(cnt,1)

            bg_mu = np.mean(bg); bg_sd = np.std(bg)
            sig_k = (sw_snr[pi_k]-bg_mu)/bg_sd if bg_sd>0 else 0

            # Also background for Abedi ~100ms
            pi_100 = np.argmin(np.abs(t_sw - 0.100))
            bg100 = np.zeros(200)
            for i in range(200):
                sh = np.random.randint(int(0.5*sr), max(int(0.5*sr)+1, len(post)-int(0.5*sr)))
                mf_s = matched_filter(np.roll(post, sh), tmpl)
                tot = 0; cnt = 0
                for k in range(1, 8):
                    s = int((k*0.100 - po)*sr)
                    if 0 <= s < len(mf_s):
                        hw = int(0.002*sr)
                        tot += np.max(np.abs(mf_s[max(0,s-hw):min(len(mf_s),s+hw+1)]))
                        cnt += 1
                bg100[i] = tot/max(cnt,1)
            bg100_mu = np.mean(bg100); bg100_sd = np.std(bg100)
            sig_100 = (sw_snr[pi_100]-bg100_mu)/bg100_sd if bg100_sd>0 else 0

            result[det] = {
                'best_t': t_sw[np.argmax(sw_snr)],
                'best_snr': np.max(sw_snr),
                'pred_snr': sw_snr[pi_k],
                'pred_sigma': sig_k,
                'nonspin_snr': sw_snr[pi_ns],
                'abedi_snr': sw_snr[pi_100],
                'abedi_sigma': sig_100,
                'sweep_mean': np.mean(sw_snr),
                'sweep_std': np.std(sw_snr),
            }
        except Exception as e:
            result[det] = {'error': str(e)}

    return result


# Remnant parameters from PE (approximate)
EVENTS = {
    "GW150914": (63.1, 0.67, 1126259462.4),
    "GW151012": (35.6, 0.67, 1128678900.4),
    "GW151226": (20.5, 0.67, 1135136350.6),
    "GW170104": (48.9, 0.67, 1167559936.6),
    "GW170608": (17.8, 0.67, 1180922494.5),
    "GW170729": (79.5, 0.67, 1185389807.3),
    "GW170809": (56.3, 0.67, 1186302519.8),
    "GW170814": (53.2, 0.67, 1186741861.5),
    "GW170818": (59.4, 0.67, 1187058327.1),
    "GW170823": (65.4, 0.67, 1187529256.5),
    "GW190403_051519": (102.2, 0.67, 1238303737.2),
    "GW190408_181802": (41.1, 0.67, 1238782700.3),
    "GW190412_053044": (35.6, 0.67, 1239082262.1),
    "GW190413_052954": (56.0, 0.67, 1239168612.5),
    "GW190413_134308": (75.5, 0.67, 1239198206.7),
    "GW190421_213856": (69.7, 0.67, 1239917954.3),
    "GW190426_190642": (172.9, 0.67, 1240340820.6),
    "GW190503_185404": (68.6, 0.67, 1240944862.3),
    "GW190512_180714": (34.5, 0.67, 1241719652.4),
    "GW190513_205428": (51.6, 0.67, 1241816086.8),
    "GW190514_065416": (64.5, 0.67, 1241852074.8),
    "GW190517_055101": (59.3, 0.67, 1242107479.8),
    "GW190519_153544": (101.0, 0.67, 1242315362.4),
    "GW190521_074359": (71.0, 0.67, 1242459857.5),
    "GW190527_092055": (56.4, 0.67, 1242984073.8),
    "GW190602_175927": (110.9, 0.67, 1243533585.1),
    "GW190701_203306": (90.2, 0.67, 1246048404.6),
    "GW190706_222641": (99.0, 0.67, 1246487219.3),
    "GW190707_093326": (19.2, 0.67, 1246527224.2),
    "GW190719_215514": (54.9, 0.67, 1247608532.9),
    "GW190720_000836": (18.6, 0.67, 1247616534.7),
    "GW190727_060333": (71.7, 0.67, 1248242631.9),
    "GW190728_064510": (18.1, 0.67, 1248331528.5),
    "GW190731_140936": (55.3, 0.67, 1248530994.7),
    "GW190803_022701": (62.8, 0.67, 1248834439.9),
    "GW190805_211137": (52.2, 0.67, 1249073515.4),
    "GW190828_063405": (39.5, 0.67, 1251009263.8),
    "GW190828_065509": (29.5, 0.67, 1251010527.8),
    "GW190915_235702": (56.3, 0.67, 1252627040.7),
    "GW190916_200658": (16.4, 0.67, 1252698436.4),
    "GW190917_114630": (15.3, 0.67, 1252755008.4),
    "GW190924_021846": (13.7, 0.67, 1253326744.8),
    "GW190925_232845": (28.4, 0.67, 1253407743.7),
    "GW190926_050336": (54.3, 0.67, 1253422234.7),
    "GW190929_012149": (89.3, 0.67, 1253669327.5),
    "GW190930_133541": (18.6, 0.67, 1253885759.3),
    "GW191103_012549": (17.1, 0.67, 1256776967.3),
    "GW191105_143521": (17.7, 0.67, 1257015339.4),
    "GW191109_010717": (103.2, 0.67, 1257296855.2),
    "GW191113_071753": (41.8, 0.67, 1257660491.7),
    "GW191126_115259": (18.3, 0.67, 1258801997.8),
    "GW191127_050227": (38.2, 0.67, 1258862565.3),
    "GW191129_134029": (16.7, 0.67, 1259070447.1),
    "GW191204_110529": (29.2, 0.67, 1259492747.4),
    "GW191215_223052": (42.3, 0.67, 1260484270.3),
    "GW191216_213338": (18.6, 0.67, 1260567236.5),
    "GW191222_033537": (76.2, 0.67, 1261020955.1),
    "GW191230_180458": (56.3, 0.67, 1261680316.4),
    "GW200128_022011": (64.9, 0.67, 1264213229.9),
    "GW200129_065458": (55.7, 0.67, 1264316116.4),
    "GW200202_154313": (16.9, 0.67, 1264694611.6),
    "GW200208_130117": (54.7, 0.67, 1265201695.0),
    "GW200208_222617": (19.2, 0.67, 1265236795.6),
    "GW200209_085452": (44.5, 0.67, 1265273710.6),
    "GW200210_092254": (38.2, 0.67, 1265361792.3),
    "GW200216_220804": (89.1, 0.67, 1265930902.2),
    "GW200219_094415": (56.2, 0.67, 1266138273.5),
    "GW200220_061928": (122.7, 0.67, 1266213586.1),
    "GW200220_124850": (34.5, 0.67, 1266237948.7),
    "GW200224_222234": (57.7, 0.67, 1266618172.4),
    "GW200225_060421": (27.5, 0.67, 1266645879.3),
    "GW200308_173609": (42.7, 0.67, 1267725387.3),
    "GW200311_115853": (55.4, 0.67, 1267968951.3),
    "GW200316_215756": (21.2, 0.67, 1268437094.4),
    "GW200322_091133": (44.0, 0.67, 1268905511.4),
}

# For O2/O3 events without known PE remnant params, estimate from total mass
# M_remnant ~ 0.95 * M_total, a_spin ~ 0.67 (typical)
def estimate_remnant(event_name):
    """Rough remnant estimate for events without PE results."""
    # Try to get GPS from filename pattern
    return None  # We'll skip events without known parameters


def main():
    t0 = time.time()
    np.random.seed(42)

    print("=" * 85)
    print("FULL-CATALOG ECHO SEARCH: ABEDI REPRODUCTION + FROZEN-STAR PREDICTION")
    print("=" * 85)
    print()

    # Find all available events
    data_dir = "data"
    h1_files = sorted([f for f in os.listdir(data_dir)
                       if f.startswith('H1_GW') and f.endswith('.hdf5')
                       and '16k' not in f and '4096s' not in f])

    print(f"Available H1 event files: {len(h1_files)}")

    # ===================================================================
    # PART A: ABEDI REPRODUCTION (GW150914 only)
    # ===================================================================
    print()
    print("=" * 85)
    print("PART A: ABEDI REPRODUCTION — GW150914 at ~100ms")
    print("=" * 85)

    r150914 = analyze_one(
        'data/H1_GW150914.hdf5', 'data/L1_GW150914.hdf5',
        1126259462.423, 62.0, 0.67)

    for det in ['H1', 'L1']:
        if det in r150914 and 'error' not in r150914[det]:
            d = r150914[det]
            print(f"\n  {det}:")
            print(f"    Blind sweep best: {d['best_t']*1000:.1f}ms (SNR={d['best_snr']:.3f})")
            print(f"    At Abedi ~100ms: SNR={d['abedi_snr']:.3f}, sigma={d['abedi_sigma']:.2f}")
            print(f"    At prediction {r150914['t_pred_kerr']*1000:.1f}ms: "
                  f"SNR={d['pred_snr']:.3f}, sigma={d['pred_sigma']:.2f}")
            print(f"    Sweep mean={d['sweep_mean']:.3f}, std={d['sweep_std']:.3f}")

    # ===================================================================
    # PART B: MULTI-EVENT STACK (known PE events)
    # ===================================================================
    print()
    print("=" * 85)
    print("PART B: MULTI-EVENT STACK — EVENTS WITH KNOWN REMNANT PARAMS")
    print("=" * 85)

    pe_results = []
    for name, (M, a, gps) in sorted(EVENTS.items()):
        h1 = f'data/H1_{name}.hdf5'
        l1 = f'data/L1_{name}.hdf5'
        h1 = h1 if os.path.exists(h1) else None
        l1 = l1 if os.path.exists(l1) else None

        if not h1 and not l1:
            continue

        t_pred = predict_echo_time(M, a)
        print(f"\n  {name}: M={M:.1f}, a={a:.2f}, t_echo={t_pred*1000:.1f}ms")

        r = analyze_one(h1, l1, gps, M, a)
        sigmas = []
        for det in ['H1', 'L1']:
            if det in r and 'error' not in r[det]:
                d = r[det]
                print(f"    {det}: pred_sigma={d['pred_sigma']:.2f}, "
                      f"best={d['best_t']*1000:.1f}ms")
                sigmas.append(d['pred_sigma'])

        if sigmas:
            combined = sum(sigmas)/math.sqrt(len(sigmas))
            r['combined_sigma'] = combined
            r['name'] = name
            r['M'] = M
            pe_results.append(r)
            print(f"    Combined: {combined:.2f} sigma")

    # Stack
    print()
    print("-" * 85)
    print("STACKING (known PE events)")
    print("-" * 85)
    if pe_results:
        sigs = [r['combined_sigma'] for r in pe_results]
        print(f"\n  {'event':>12s} {'M':>6s} {'t_pred':>8s} {'sigma':>8s}")
        for r in pe_results:
            print(f"  {r['name']:>12s} {r['M']:>6.1f} "
                  f"{r['t_pred_kerr']*1000:>8.1f} {r['combined_sigma']:>8.2f}")

        n_pos = sum(1 for s in sigs if s > 0)
        stacked = sum(sigs)/math.sqrt(len(sigs))
        print(f"\n  Stacked: {stacked:.2f} sigma")
        print(f"  Positive: {n_pos}/{len(sigs)} ({n_pos/len(sigs)*100:.0f}%)")
        print(f"  Mean: {np.mean(sigs):.3f}")

    # ===================================================================
    # PART C: ALL AVAILABLE EVENTS (estimate remnant for unknowns)
    # ===================================================================
    print()
    print("=" * 85)
    print("PART C: ALL EVENTS (with estimated remnant params where needed)")
    print("=" * 85)

    all_sigmas = []
    all_abedi_sigmas = []

    for fname in h1_files:
        event_name = fname.replace('H1_', '').replace('.hdf5', '')
        h1 = os.path.join(data_dir, fname)
        l1 = os.path.join(data_dir, fname.replace('H1_', 'L1_'))
        l1 = l1 if os.path.exists(l1) else None

        # Get remnant params
        if event_name in EVENTS:
            M, a, gps = EVENTS[event_name]
        else:
            # Estimate: need GPS from file
            try:
                with h5py.File(h1, 'r') as f:
                    gps0 = f['meta/GPSstart'][()]
                    dur = f['meta/Duration'][()]
                gps = gps0 + dur/2  # rough merger time at center
                M = 50.0  # default remnant mass
                a = 0.67  # default spin
            except:
                continue

        t_pred = predict_echo_time(M, a)
        r = analyze_one(h1, l1, gps, M, a)

        sigmas = []
        abedi_sigmas = []
        for det in ['H1', 'L1']:
            if det in r and 'error' not in r[det]:
                sigmas.append(r[det]['pred_sigma'])
                abedi_sigmas.append(r[det]['abedi_sigma'])

        if sigmas:
            cs = sum(sigmas)/math.sqrt(len(sigmas))
            all_sigmas.append(cs)
            if abedi_sigmas:
                ca = sum(abedi_sigmas)/math.sqrt(len(abedi_sigmas))
                all_abedi_sigmas.append(ca)
            sys.stdout.write(f"  {event_name}: {cs:+.2f}σ (pred), t={t_pred*1000:.0f}ms")
            if abedi_sigmas:
                sys.stdout.write(f", Abedi: {ca:+.2f}σ")
            print()

    # ===================================================================
    # FINAL SUMMARY
    # ===================================================================
    print()
    print("=" * 85)
    print("FINAL SUMMARY")
    print("=" * 85)
    print()

    if all_sigmas:
        n = len(all_sigmas)
        n_pos = sum(1 for s in all_sigmas if s > 0)
        stacked = sum(all_sigmas)/math.sqrt(n)
        print(f"  FROZEN-STAR PREDICTION (all {n} events):")
        print(f"    Stacked sigma: {stacked:.2f}")
        print(f"    Mean sigma: {np.mean(all_sigmas):.3f}")
        print(f"    Positive: {n_pos}/{n} ({n_pos/n*100:.0f}%)")

        from math import comb as nchoose
        p_binom = sum(nchoose(n, k)*0.5**n for k in range(n_pos, n+1))
        print(f"    Binomial p: {p_binom:.4f}")

    if all_abedi_sigmas:
        n = len(all_abedi_sigmas)
        n_pos = sum(1 for s in all_abedi_sigmas if s > 0)
        stacked = sum(all_abedi_sigmas)/math.sqrt(n)
        print(f"\n  ABEDI ~100ms (all {n} events):")
        print(f"    Stacked sigma: {stacked:.2f}")
        print(f"    Mean sigma: {np.mean(all_abedi_sigmas):.3f}")
        print(f"    Positive: {n_pos}/{n} ({n_pos/n*100:.0f}%)")

    print()
    if all_sigmas:
        s = sum(all_sigmas)/math.sqrt(len(all_sigmas))
        if s > 3: print("  VERDICT: SIGNIFICANT echo signal across catalog!")
        elif s > 2: print("  VERDICT: MARGINAL — needs more events")
        elif s > 1: print("  VERDICT: WEAK HINT")
        else: print("  VERDICT: NULL RESULT — no echo detected")

    print(f"\n  Total events analyzed: {len(all_sigmas)}")
    print(f"  Runtime: {time.time()-t0:.0f}s ({(time.time()-t0)/60:.1f} min)")


if __name__ == "__main__":
    main()
