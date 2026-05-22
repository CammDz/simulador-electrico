import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np
import base64
from pathlib import Path

K = 8.99e9

st.set_page_config(
    page_title="Simulador de Fuerza Eléctrica",
    page_icon="⚡",
    layout="wide"
)

# ─── Logo ────────────────────────────────────────────────────────────────────
def get_logo_b64(path):
    try:
        return base64.b64encode(Path(path).read_bytes()).decode()
    except Exception:
        return ""

logo_b64 = get_logo_b64("logo.png")
logo_html = (
    f'<img src="data:image/png;base64,{logo_b64}" style="height:88px;width:88px;'
    'object-fit:contain;border-radius:14px;flex-shrink:0;'
    'filter:drop-shadow(0 0 16px rgba(250,204,21,0.55));" />'
    if logo_b64 else
    '<span style="font-size:70px;line-height:1;flex-shrink:0;">⚡</span>'
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background-color: #f0f2f8 !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"] { display:none !important; }
#MainMenu, footer { visibility:hidden !important; }

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #0a0820 0%, #1a1560 50%, #0f2460 100%);
    border-radius: 22px;
    padding: 32px 40px;
    margin-bottom: 32px;
    display: flex;
    align-items: center;
    gap: 28px;
    box-shadow: 0 16px 48px rgba(10,8,32,0.4);
    position: relative; overflow: hidden;
}
.hero::before {
    content:""; position:absolute; top:-100px; right:-100px;
    width:350px; height:350px;
    background: radial-gradient(circle, rgba(250,204,21,0.1) 0%, transparent 65%);
    border-radius:50%;
}
.hero::after {
    content:""; position:absolute; bottom:-60px; left:25%;
    width:400px; height:150px;
    background: radial-gradient(ellipse, rgba(96,165,250,0.08) 0%, transparent 70%);
}
.hero-title {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 2.1rem !important; font-weight: 700 !important;
    color: #facc15 !important; margin: 0 0 6px 0 !important;
    line-height: 1.1 !important;
    text-shadow: 0 0 40px rgba(250,204,21,0.35) !important;
}
.hero-sub {
    font-size: 0.85rem !important; font-weight: 300 !important;
    color: rgba(196,214,255,0.75) !important; margin: 0 !important;
}

/* ── Cards ── */
.card {
    background: #ffffff;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 4px 24px rgba(30,40,120,0.08);
    border: 1px solid rgba(200,210,255,0.5);
    margin-bottom: 20px;
}
.card-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.75rem; font-weight: 600;
    letter-spacing: 1.5px; text-transform: uppercase;
    color: #4f46e5; margin-bottom: 18px;
    display: flex; align-items: center; gap: 8px;
}
.card-title::after {
    content:""; flex:1; height:1.5px;
    background: linear-gradient(90deg, #c7d2fe, transparent);
    border-radius: 2px;
}

/* ── Charge badge ── */
.charge-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.95rem; font-weight: 700;
    letter-spacing: 0.5px;
    padding: 6px 14px;
    border-radius: 8px;
    display: inline-block;
    margin-bottom: 12px;
}

/* ── Botón PRINCIPAL ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    color: #ffffff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 16px 0 !important;
    width: 100% !important;
    box-shadow: 0 6px 24px rgba(79,70,229,0.4) !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%) !important;
    box-shadow: 0 10px 36px rgba(79,70,229,0.55) !important;
    transform: translateY(-3px) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(-1px) !important;
}

/* ── Result cards ── */
.res-grid { display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:14px; }
.res-card {
    border-radius: 14px; padding: 16px 20px;
    display: flex; align-items: center; gap: 14px;
}
.res-card.blue  { background:#eff6ff; border:1.5px solid #93c5fd; }
.res-card.green { background:#f0fdf4; border:1.5px solid #86efac; }
.res-card.red   { background:#fff7ed; border:1.5px solid #fca5a5; }
.res-card.purple{ background:#faf5ff; border:1.5px solid #d8b4fe; }
.res-icon { font-size:2rem; flex-shrink:0; }
.res-label { font-size:0.68rem; font-weight:600; text-transform:uppercase;
             letter-spacing:0.9px; color:#6b7280; margin-bottom:2px; }
.res-val { font-family:'Rajdhani',sans-serif; font-size:1.35rem;
           font-weight:700; color:#1e3a8a; line-height:1; }
.res-val.g { color:#166534; }
.res-val.r { color:#9a3412; }
.res-val.p { color:#6b21a8; }

/* ── Divider ── */
.div { height:1px; background:linear-gradient(90deg,transparent,#c7d2fe 40%,#c7d2fe 60%,transparent);
       border:none; margin:26px 0; }

/* ── Formula box ── */
.fbox {
    background:#f8f9ff; border:1.5px solid #e0e7ff;
    border-radius:12px; padding:14px 20px;
    font-family:'Inter',monospace; font-size:0.83rem;
    color:#374151; line-height:2;
}

/* inputs */
[data-testid="stNumberInput"] label p {
    font-weight:500 !important; font-size:0.85rem !important; color:#374151 !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important; font-size: 0.9rem !important;
    letter-spacing: 0.5px !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    {logo_html}
    <div>
        <div class="hero-title">Proyecto de Simulador de Fuerza Eléctrica</div>
        <p class="hero-sub">
            Ley de Coulomb en 2D &nbsp;·&nbsp; 4 cargas simultáneas &nbsp;·&nbsp;
            Componentes Fx, Fy &nbsp;·&nbsp; Ángulo θ &nbsp;·&nbsp; Fuerza neta vectorial
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Colores por carga ────────────────────────────────────────────────────────
CHARGE_COLORS = ["#ef4444", "#3b82f6", "#f59e0b", "#10b981"]
CHARGE_NAMES  = ["Q₁", "Q₂", "Q₃", "Q₄"]
CHARGE_BG     = ["#fff1f2", "#eff6ff", "#fffbeb", "#f0fdf4"]
CHARGE_BORDER = ["#fca5a5", "#93c5fd", "#fcd34d", "#86efac"]

# ─── Parámetros ──────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">⚙️ Configuración de las 4 Cargas — Posición (x, y) en metros</div>', unsafe_allow_html=True)

charges = []
cols_top = st.columns(4)
for i, col in enumerate(cols_top):
    with col:
        st.markdown(
            f'<div class="charge-header" style="background:{CHARGE_BG[i]};'
            f'border:1.5px solid {CHARGE_BORDER[i]};color:{CHARGE_COLORS[i]};">'
            f'{CHARGE_NAMES[i]}</div>',
            unsafe_allow_html=True
        )
        q_val = st.number_input(f"Carga (µC)", value=[5.0, -3.0, 4.0, -2.0][i],
                                 step=0.5, key=f"q{i}")
        cx = st.number_input(f"Posición X (m)", value=[0.0, 3.0, 3.0, 0.0][i],
                              step=0.5, key=f"x{i}")
        cy = st.number_input(f"Posición Y (m)", value=[0.0, 0.0, 2.0, 2.0][i],
                              step=0.5, key=f"y{i}")
        charges.append({"q": q_val * 1e-6, "q_uc": q_val, "x": cx, "y": cy})

st.markdown('</div>', unsafe_allow_html=True)

calcular = st.button("⚡  Calcular Fuerzas y Visualizar Sistema")

# ─── Cálculo ─────────────────────────────────────────────────────────────────
if calcular:

    n = len(charges)
    # Fuerza neta sobre cada carga: [Fx, Fy]
    net_forces = [[0.0, 0.0] for _ in range(n)]
    pair_data  = []  # info por par (i,j)

    for i in range(n):
        for j in range(n):
            if i >= j:
                continue
            q1, q2 = charges[i]["q"], charges[j]["q"]
            dx = charges[j]["x"] - charges[i]["x"]
            dy = charges[j]["y"] - charges[i]["y"]
            r  = np.sqrt(dx**2 + dy**2)
            if r < 1e-9:
                continue
            F_mag = K * abs(q1 * q2) / r**2
            theta = np.degrees(np.arctan2(dy, dx))       # ángulo en grados
            ux, uy = dx / r, dy / r                      # vector unitario i→j

            # Signo: mismas cargas → repulsión (se alejan), distintas → atracción
            sign = 1 if (q1 * q2) > 0 else -1            # +1 repulsión, -1 atracción

            # Fuerza sobre i por j: apunta LEJOS de j si repulsión
            # F sobre i = F_mag * (-sign) * (ux, uy)
            fix = F_mag * (-sign) * ux
            fiy = F_mag * (-sign) * uy
            # Fuerza sobre j por i: Newton 3ra ley
            fjx, fjy = -fix, -fiy

            net_forces[i][0] += fix
            net_forces[i][1] += fiy
            net_forces[j][0] += fjx
            net_forces[j][1] += fjy

            tipo = "Repulsión" if (q1 * q2) > 0 else "Atracción"
            pair_data.append({
                "i": i, "j": j, "r": r, "F": F_mag,
                "theta": theta, "tipo": tipo,
                "Fx_i": fix, "Fy_i": fiy,
                "Fx_j": fjx, "Fy_j": fjy,
            })

    # ── Tabs de resultados ──────────────────────────────────────────────────
    st.markdown('<hr class="div">', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊  Fuerzas por Par", "🔢  Fuerza Neta por Carga", "🎨  Visualización 2D"])

    # ── Tab 1: pares ──────────────────────────────────────────────────────
    with tab1:
        for p in pair_data:
            i, j = p["i"], p["j"]
            color_tipo = "#166534" if p["tipo"] == "Atracción" else "#9a3412"
            badge_bg   = "#dcfce7" if p["tipo"] == "Atracción" else "#fee2e2"
            st.markdown(f"""
            <div class="card">
              <div class="card-title">
                Par {CHARGE_NAMES[i]} ↔ {CHARGE_NAMES[j]}
                &nbsp;<span style="background:{badge_bg};color:{color_tipo};
                  padding:3px 12px;border-radius:100px;font-size:0.72rem;
                  font-weight:700;letter-spacing:0.5px;">{p['tipo']}</span>
              </div>
              <div class="res-grid">
                <div class="res-card blue">
                  <div class="res-icon">📏</div>
                  <div><div class="res-label">Distancia r</div>
                       <div class="res-val">{p['r']:.4f} m</div></div>
                </div>
                <div class="res-card purple">
                  <div class="res-icon">🧭</div>
                  <div><div class="res-label">Ángulo θ</div>
                       <div class="res-val p">{p['theta']:.2f}°</div></div>
                </div>
                <div class="res-card {'green' if p['tipo']=='Atracción' else 'red'}">
                  <div class="res-icon">⚡</div>
                  <div><div class="res-label">|F| Magnitud</div>
                       <div class="res-val {'g' if p['tipo']=='Atracción' else 'r'}">{p['F']:.4f} N</div></div>
                </div>
                <div class="res-card blue">
                  <div class="res-icon">📐</div>
                  <div><div class="res-label">Fx / Fy sobre {CHARGE_NAMES[i]}</div>
                       <div class="res-val">{p['Fx_i']:.3f} / {p['Fy_i']:.3f} N</div></div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 2: fuerza neta ────────────────────────────────────────────────
    with tab2:
        cols_r = st.columns(4)
        for i, col in enumerate(cols_r):
            fx, fy = net_forces[i]
            mag = np.sqrt(fx**2 + fy**2)
            ang = np.degrees(np.arctan2(fy, fx))
            with col:
                st.markdown(f"""
                <div class="card">
                  <div class="card-title">{CHARGE_NAMES[i]} — Fuerza Neta</div>
                  <div class="res-card blue" style="margin-bottom:10px">
                    <div class="res-icon">➡️</div>
                    <div><div class="res-label">Fx neto</div>
                         <div class="res-val">{fx:.4f} N</div></div>
                  </div>
                  <div class="res-card purple" style="margin-bottom:10px">
                    <div class="res-icon">⬆️</div>
                    <div><div class="res-label">Fy neto</div>
                         <div class="res-val p">{fy:.4f} N</div></div>
                  </div>
                  <div class="res-card green" style="margin-bottom:10px">
                    <div class="res-icon">⚡</div>
                    <div><div class="res-label">|F| neto</div>
                         <div class="res-val g">{mag:.4f} N</div></div>
                  </div>
                  <div class="res-card red">
                    <div class="res-icon">🧭</div>
                    <div><div class="res-label">Ángulo θ</div>
                         <div class="res-val r">{ang:.2f}°</div></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Tab 3: visualización 2D ───────────────────────────────────────────
    with tab3:
        fig, ax = plt.subplots(figsize=(8, 7))
        fig.patch.set_facecolor('#f8f9ff')
        ax.set_facecolor('#f8f9ff')

        xs = [c["x"] for c in charges]
        ys = [c["y"] for c in charges]
        margin = max(max(xs)-min(xs), max(ys)-min(ys)) * 0.55 + 1.2

        ax.set_xlim(min(xs)-margin, max(xs)+margin)
        ax.set_ylim(min(ys)-margin, max(ys)+margin)

        # Grid suave
        ax.grid(True, linestyle='--', alpha=0.3, color='#94a3b8', linewidth=0.8)
        ax.set_axisbelow(True)

        # Ejes
        ax.axhline(0, color='#cbd5e1', linewidth=0.8, alpha=0.6)
        ax.axvline(0, color='#cbd5e1', linewidth=0.8, alpha=0.6)
        ax.set_xlabel("x (m)", fontsize=10, color='#475569', labelpad=8)
        ax.set_ylabel("y (m)", fontsize=10, color='#475569', labelpad=8)
        ax.tick_params(colors='#64748b', labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor('#e2e8f0')

        # Líneas punteadas entre pares con ángulo
        for p in pair_data:
            i, j = p["i"], p["j"]
            xi, yi = charges[i]["x"], charges[i]["y"]
            xj, yj = charges[j]["x"], charges[j]["y"]
            ax.plot([xi, xj], [yi, yj], '--', color='#94a3b8',
                    linewidth=1.0, alpha=0.5, zorder=1)
            mx, my = (xi+xj)/2, (yi+yj)/2
            ax.text(mx, my, f"r={p['r']:.2f}m\nθ={p['theta']:.1f}°",
                    ha='center', va='center', fontsize=6.5,
                    color='#64748b', style='italic',
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#e2e8f0', alpha=0.85))

        # Vectores de fuerza neta sobre cada carga
        max_mag = max(np.sqrt(f[0]**2 + f[1]**2) for f in net_forces) or 1
        scale   = margin * 0.45 / max_mag

        for i, c in enumerate(charges):
            fx, fy = net_forces[i]
            mag = np.sqrt(fx**2 + fy**2)
            if mag > 1e-12:
                ax.annotate("",
                    xy=(c["x"] + fx*scale, c["y"] + fy*scale),
                    xytext=(c["x"], c["y"]),
                    arrowprops=dict(arrowstyle='->', color=CHARGE_COLORS[i],
                                    lw=2.2, mutation_scale=16),
                    zorder=4)
                ax.text(c["x"] + fx*scale*1.15, c["y"] + fy*scale*1.15,
                        f"F={mag:.2f}N\n{np.degrees(np.arctan2(fy,fx)):.1f}°",
                        ha='center', fontsize=7, color=CHARGE_COLORS[i], fontweight='bold')

        # Cargas (círculos)
        for i, c in enumerate(charges):
            circle = plt.Circle((c["x"], c["y"]), margin*0.06,
                                 color=CHARGE_COLORS[i], zorder=5,
                                 ec='white', linewidth=2.5)
            ax.add_patch(circle)
            sign = '+' if c["q"] > 0 else '−'
            ax.text(c["x"], c["y"], sign, ha='center', va='center',
                    fontsize=13, fontweight='bold', color='white', zorder=6)
            ax.text(c["x"], c["y"] - margin*0.12,
                    f"{CHARGE_NAMES[i]}\n{c['q_uc']:+.1f}µC\n({c['x']},{c['y']})",
                    ha='center', fontsize=7.5, color=CHARGE_COLORS[i],
                    fontweight='bold', zorder=6)

        # Leyenda
        legend_patches = [
            mpatches.Patch(color=CHARGE_COLORS[i],
                           label=f"{CHARGE_NAMES[i]} = {charges[i]['q_uc']:+.1f} µC")
            for i in range(n)
        ]
        ax.legend(handles=legend_patches, loc='upper left',
                  fontsize=8, framealpha=0.95,
                  edgecolor='#e0e7ff', fancybox=True)

        ax.set_title("Sistema de 4 Cargas — Vectores de Fuerza Neta",
                     fontsize=11, color='#1e3a8a', fontweight='bold', pad=14)

        st.pyplot(fig)

        # Fórmulas
        st.markdown('<hr class="div">', unsafe_allow_html=True)
        st.markdown('<div class="card"><div class="card-title">📐 Fórmulas Aplicadas</div>', unsafe_allow_html=True)

        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            st.markdown("**Ley de Coulomb**")
            st.latex(r"F = k_e \dfrac{|q_i \cdot q_j|}{r_{ij}^2}")
        with col_f2:
            st.markdown("**Componentes**")
            st.latex(r"F_x = F\cos\theta \quad F_y = F\sin\theta")
        with col_f3:
            st.markdown("**Ángulo y distancia**")
            st.latex(r"\theta = \arctan\!\left(\frac{\Delta y}{\Delta x}\right), \quad r=\sqrt{\Delta x^2+\Delta y^2}")

        st.markdown(f"""
        <div class="fbox">
            <b>kₑ</b> = 8.99 × 10⁹ N·m²/C² &nbsp;|&nbsp;
            Principio de superposición: <b>F_neta = Σ F_ij</b> &nbsp;|&nbsp;
            Vectores escalados visualmente para claridad
        </div></div>
        """, unsafe_allow_html=True)
