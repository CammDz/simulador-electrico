from utils.validators import safe_max, safe_min, safe_mean


def precompute_stats(cargas, pares_info, fuerzas_netas):
    n = len(cargas)
    pos = sum(1 for c in cargas if c['q'] > 0)
    neg = n - pos
    total_pares = len(pares_info)
    atracciones = sum(1 for p in pares_info if p['atraccion'])
    repulsiones = total_pares - atracciones
    netas_mag = [fn['F'] for fn in fuerzas_netas]
    max_neta = safe_max(netas_mag)
    min_neta = safe_min(netas_mag)
    prom_neta = safe_mean(netas_mag)
    dists = [p['r'] for p in pares_info]
    dist_prom = safe_mean(dists)
    dist_min = safe_min(dists)
    f_mags = [p['F'] for p in pares_info]
    f_max = safe_max(f_mags)
    f_min = safe_min(f_mags)
    f_prom = safe_mean(f_mags)

    carga_max_idx = next(
        (fn['indice'] for fn in fuerzas_netas if abs(fn['F'] - max_neta) < 1e-10),
        None,
    )
    carga_min_idx = next(
        (fn['indice'] for fn in fuerzas_netas if abs(fn['F'] - min_neta) < 1e-10),
        None,
    )

    fx_all = [fn['Fx'] for fn in fuerzas_netas]
    fy_all = [fn['Fy'] for fn in fuerzas_netas]
    fx_pos = sum(1 for v in fx_all if v > 0)
    fx_neg = sum(1 for v in fx_all if v < 0)
    fy_pos = sum(1 for v in fy_all if v > 0)
    fy_neg = sum(1 for v in fy_all if v < 0)

    return {
        'n': n,
        'pos': pos,
        'neg': neg,
        'total_pares': total_pares,
        'atracciones': atracciones,
        'repulsiones': repulsiones,
        'netas_mag': netas_mag,
        'max_neta': max_neta,
        'min_neta': min_neta,
        'prom_neta': prom_neta,
        'dists': dists,
        'dist_prom': dist_prom,
        'dist_min': dist_min,
        'f_mags': f_mags,
        'f_max': f_max,
        'f_min': f_min,
        'f_prom': f_prom,
        'carga_max_idx': carga_max_idx,
        'carga_min_idx': carga_min_idx,
        'fx_all': fx_all,
        'fy_all': fy_all,
        'fx_pos': fx_pos,
        'fx_neg': fx_neg,
        'fy_pos': fy_pos,
        'fy_neg': fy_neg,
    }
