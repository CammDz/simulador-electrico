import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import streamlit as st
from ui.components import render_vector_panel


def plot_sistema_cargas(cargas_coulombs, pares_info, fuerzas_netas, cargas):
    fig1, ax1 = plt.subplots(figsize=(7, 7))
    fig1.patch.set_facecolor('#ffffff')
    ax1.set_facecolor('#f8fafc')

    xs = [c['x'] for c in cargas_coulombs]
    ys = [c['y'] for c in cargas_coulombs]
    margin = 2.5
    xc = (min(xs) + max(xs)) / 2
    yc = (min(ys) + max(ys)) / 2
    half = max(max(xs) - min(xs), max(ys) - min(ys)) / 2 + margin

    ax1.set_xlim(xc - half, xc + half)
    ax1.set_ylim(yc - half, yc + half)
    ax1.set_aspect('equal')

    ax1.grid(True, color='#e2e8f0', linewidth=0.5, alpha=0.7)
    ax1.axhline(0, color='#cbd5e1', linewidth=0.8, alpha=0.5)
    ax1.axvline(0, color='#cbd5e1', linewidth=0.8, alpha=0.5)

    for p in pares_info:
        ci = cargas_coulombs[p['i'] - 1]
        cj = cargas_coulombs[p['j'] - 1]
        ls = '--' if p['atraccion'] else ':'
        ax1.plot(
            [ci['x'], cj['x']], [ci['y'], cj['y']],
            color='#cbd5e1', linewidth=0.7, linestyle=ls, alpha=0.5, zorder=1
        )

    n_charges = len(cargas_coulombs)
    label_offsets = []
    for idx, c in enumerate(cargas_coulombs):
        near = False
        for other in cargas_coulombs:
            if other['indice'] == c['indice']:
                continue
            dist = math.hypot(c['x'] - other['x'], c['y'] - other['y'])
            if dist < half * 0.5:
                near = True
                break
        if near:
            offset_y = half * 0.16 if idx % 2 == 0 else -half * 0.16
        else:
            offset_y = half * 0.11 if idx % 2 == 0 else -half * 0.11
        label_offsets.append(offset_y)

    for idx, (c, fn) in enumerate(zip(cargas_coulombs, fuerzas_netas)):
        col = fn['color']
        ax1.scatter(c['x'], c['y'], s=190, color=col, zorder=4,
                    edgecolors='white', linewidths=2, alpha=0.9)
        signo = '+' if c['q'] > 0 else '−'
        ax1.text(c['x'], c['y'], signo, ha='center', va='center',
                 color='white', fontsize=10, fontweight='bold', zorder=5)
        off = label_offsets[idx]
        va = 'top' if off > 0 else 'bottom'
        ax1.text(
            c['x'], c['y'] + off,
            f"Q{c['indice']}  {cargas[c['indice'] - 1]['q']:.1f}µC",
            ha='center', va=va, fontsize=7.5, color='#64748b',
            fontfamily='monospace',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff',
                      edgecolor=col + '66', linewidth=0.8), zorder=5
        )
        if fn['F'] > 1e-6:
            scale = half * 0.28
            fx_v = (fn['Fx'] / fn['F']) * scale
            fy_v = (fn['Fy'] / fn['F']) * scale
            ax1.annotate('', xy=(c['x'] + fx_v, c['y'] + fy_v),
                         xytext=(c['x'], c['y']),
                         arrowprops=dict(arrowstyle='->', color=col, lw=2.2, mutation_scale=13),
                         zorder=3)

    ax1.set_xlabel('X (m)', fontsize=8.5, color='#64748b', fontfamily='monospace')
    ax1.set_ylabel('Y (m)', fontsize=8.5, color='#64748b', fontfamily='monospace')
    ax1.tick_params(colors='#94a3b8', labelsize=7.5)
    ax1.spines[:].set_color('#e2e8f0')
    plt.tight_layout(pad=1.2)
    st.pyplot(fig1, use_container_width=True)
    plt.close(fig1)


def plot_descomposicion_vectorial(par):
    fig2, ax2 = plt.subplots(figsize=(7, 7))
    fig2.patch.set_facecolor('#ffffff')
    ax2.set_facecolor('#f8fafc')

    F, Fx, Fy = par['F'], par['Fx'], par['Fy']
    theta_rad = math.radians(par['theta'])
    theta_deg = par['theta']
    max_c = max(abs(Fx), abs(Fy), F, 0.01)
    norm = 3.5 / max_c
    fx_n = Fx * norm
    fy_n = Fy * norm
    f_nx = F * norm * math.cos(theta_rad)
    f_ny = F * norm * math.sin(theta_rad)

    ax2.set_xlim(-0.8, 5.8)
    ax2.set_ylim(-0.8, 5.8)
    ax2.set_aspect('equal')
    ax2.grid(True, color='#e2e8f0', linewidth=0.4, alpha=0.4)

    ax2.axhline(0, color='#e2e8f0', linewidth=0.5, zorder=0)
    ax2.axvline(0, color='#e2e8f0', linewidth=0.5, zorder=0)
    ax2.annotate('', xy=(5.2, 0), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='#cbd5e1', lw=0.7))
    ax2.annotate('', xy=(0, 5.2), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='#cbd5e1', lw=0.7))
    ax2.text(5.25, -0.15, 'x', fontsize=7.5, color='#94a3b8', fontfamily='monospace')
    ax2.text(-0.18, 5.25, 'y', fontsize=7.5, color='#94a3b8', fontfamily='monospace')

    ax2.plot([fx_n, fx_n], [0, fy_n], color='#cbd5e1', linewidth=0.5, linestyle='--', alpha=0.35)
    ax2.plot([0, fx_n], [fy_n, fy_n], color='#cbd5e1', linewidth=0.5, linestyle='--', alpha=0.35)

    ax2.annotate('', xy=(fx_n, 0), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='#0284c7', lw=3, mutation_scale=18))
    ax2.annotate('', xy=(fx_n, fy_n), xytext=(fx_n, 0),
                 arrowprops=dict(arrowstyle='->', color='#ea580c', lw=3, mutation_scale=18))
    ax2.annotate('', xy=(f_nx, f_ny), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='#7c3aed', lw=3.8, mutation_scale=22))

    # Fx label
    fx_lab_x = max(fx_n / 2, 0.6)
    fx_lab_y = 0.6 if abs(theta_deg) < 35 else 0.4
    ax2.text(fx_lab_x, fx_lab_y, f'Fx = {Fx:+.3f} N', ha='center', va='bottom',
             fontsize=8, color='#0284c7', fontfamily='monospace', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.15', facecolor='#ffffff',
                       edgecolor='#0284c720', linewidth=0.5), zorder=10)

    # Fy label
    fy_ha = 'left'
    fy_lab_x = fx_n + 0.45
    if fy_lab_x > 5.2:
        fy_lab_x = fx_n - 0.45
        fy_ha = 'right'
    ax2.text(fy_lab_x, fy_n / 2, f'Fy = {Fy:+.3f} N', ha=fy_ha, va='center',
             fontsize=8, color='#ea580c', fontfamily='monospace', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.15', facecolor='#ffffff',
                       edgecolor='#ea580c20', linewidth=0.5), zorder=10)

    # F (resultant) label
    perp = 0.75
    if f_ny >= 0:
        ang_p = theta_rad + math.pi / 2
    else:
        ang_p = theta_rad - math.pi / 2
    lx = f_nx * 0.5 + perp * math.cos(ang_p)
    ly = f_ny * 0.5 + perp * math.sin(ang_p)
    lx = max(-0.5, min(5.5, lx))
    ly = max(-0.5, min(5.5, ly))
    ax2.text(lx, ly, f'F = {F:.3f} N', ha='center', va='center',
             fontsize=9, color='#7c3aed', fontfamily='monospace', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff',
                       edgecolor='#7c3aed20', linewidth=0.5), zorder=10)

    # Angle arc
    if abs(theta_rad) > 0.01:
        arc_r = 0.7
        arc = np.linspace(0, theta_rad, 60)
        ax2.plot(arc_r * np.cos(arc), arc_r * np.sin(arc), color='#dc2626', linewidth=1.5, alpha=0.5)
        mid = theta_rad / 2
        ang_lab_r = 0.95
        ax2.text(ang_lab_r * math.cos(mid), ang_lab_r * math.sin(mid),
                 f'{theta_deg:.1f}°', fontsize=7.5, color='#dc2626',
                 fontfamily='monospace', ha='center', va='center', zorder=10)

    # Legend
    legend_items = [
        mpatches.Patch(color='#7c3aed', label=f'F  |F| = {F:.4f} N'),
        mpatches.Patch(color='#0284c7', label=f'Fx  Fx = {Fx:+.4f} N'),
        mpatches.Patch(color='#ea580c', label=f'Fy  Fy = {Fy:+.4f} N'),
    ]
    leg = ax2.legend(handles=legend_items, loc='upper left', fontsize=6.5,
                     framealpha=0.85, facecolor='#ffffff', edgecolor='#e2e8f0',
                     labelcolor='#475569')
    leg.get_frame().set_linewidth(0.5)

    ax2.tick_params(colors='#cbd5e1', labelsize=6)
    ax2.spines[:].set_color('#e2e8f0')
    plt.tight_layout(pad=0.8)
    st.pyplot(fig2, use_container_width=True)
    plt.close(fig2)


def render_system_vector_summary(neta_sum):
    if not neta_sum:
        return
    fx_s, fy_s, fm_s, th_s = neta_sum['Fx'], neta_sum['Fy'], neta_sum['F'], neta_sum['theta']
    if fx_s > 0 and fy_s > 0:
        cuad_s = "Primer cuadrante (noreste)"
    elif fx_s < 0 and fy_s > 0:
        cuad_s = "Segundo cuadrante (noroeste)"
    elif fx_s < 0 and fy_s < 0:
        cuad_s = "Tercer cuadrante (suroeste)"
    elif fx_s > 0 and fy_s < 0:
        cuad_s = "Cuarto cuadrante (sureste)"
    else:
        cuad_s = "Eje"
    max_comp = max(abs(fx_s), abs(fy_s))
    dom_s = "Horizontal (Fx)" if abs(fx_s) == max_comp else "Vertical (Fy)"

    items = [
        ("Fx total", f"{fx_s:+.4f} N", "color:#0284c7;"),
        ("Fy total", f"{fy_s:+.4f} N", "color:#ea580c;"),
        ("|F| resultante", f"{fm_s:.4f} N", "color:#7c3aed;"),
        ("Ángulo θ", f"{th_s:.2f}°", ""),
        ("Dirección", cuad_s.split(" (")[0], ""),
        ("Componente dom.", dom_s, ""),
    ]
    st.markdown(
        render_vector_panel(
            "📊 Resumen vectorial del sistema",
            items,
            "Datos correspondientes a la carga con mayor fuerza neta del sistema"
        ),
        unsafe_allow_html=True,
    )


def render_decomposition_panel(par, F, Fx, Fy, theta_deg):
    dir_label = "derecha" if Fx > 0 else "izquierda"
    if Fy > 0:
        dir_label += "/arriba"
    elif Fy < 0:
        dir_label += "/abajo"

    items = [
        ("Fuerza resultante (F)", f"{F:.4f} N", "color:#7c3aed;"),
        ("Componente horizontal (Fx)", f"{Fx:+.4f} N", "color:#0284c7;"),
        ("Componente vertical (Fy)", f"{Fy:+.4f} N", "color:#ea580c;"),
        ("Ángulo θ", f"{theta_deg:.2f}°", ""),
    ]
    fx_dom = "domina" if abs(Fx) > abs(Fy) else "secundaria"
    fy_dom = "domina" if abs(Fy) > abs(Fx) else "secundaria"
    st.markdown(
        render_vector_panel(
            f"📐 Descomposición del par Q{par['i']}–Q{par['j']}",
            items,
            f"F inclinada {theta_deg:.1f}° · Fx {fx_dom} · Fy {fy_dom}"
        ),
        unsafe_allow_html=True,
    )
