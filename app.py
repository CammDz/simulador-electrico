import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Arc
import numpy as np
import base64
from pathlib import Path

K = 8.99e9

st.set_page_config(
    page_title="Simulador de Fuerza Eléctrica 2D",
    page_icon="⚡",
    layout="wide"
)

# ─── Logo ────────────────────────────────────────────────────────────────────
def get_logo_b64(path):
    try:
        return base64.b64encode(Path(path).read_bytes()).decode()
    except:
        return ""

logo_b64 = get_logo_b64("logo.png")
logo_html = (
    f'<img src="data:image/png;base64,{logo_b64}" '
    'style="height:85px;width:85px;object-fit:contain;border-radius:14px;'
    'filter:drop-shadow(0 0 18px rgba(79,70,229,0.45));" />'
    if logo_b64 else
    '<span style="font-size:68px;line-height:1;">⚡</span>'
)

# ─── CSS COMPLETO ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background: linear-gradient(135deg, #f0f2f8 0%, #e8ecf8 100%) !important;
}
[data-testid="stHeader"] { background:none !important; }
[data-testid="stToolbar"] { display:none !important; }
#MainMenu, footer { visibility:hidden !important; }

* { font-family: 'Inter', sans-serif; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #0a0820 0%, #1a1560 50%, #0f2460 100%);
    border-radius: 24px; padding: 32px 40px; margin-bottom: 32px;
    display: flex; align-items: center; gap: 28px;
    box-shadow: 0 20px 60px rgba(10,8,32,0.5), 0 0 40px rgba(79,70,229,0.15);
    position: relative; overflow: hidden;
}
.hero::before {
    content:""; position:absolute; top:-120px; right:-120px;
    width:400px; height:400px;
    background: radial-gradient(circle, rgba(79,70,229,0.15) 0%, transparent 65%);
    border-radius:50%;
}
.hero::after {
    content:""; position:absolute; bottom:-80px; left:20%;
    width:450px; height:180px;
    background: radial-gradient(ellipse, rgba(96,165,250,0.1) 0%, transparent 70%);
}
.hero-title {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 2.2rem !important; font-weight: 700 !important;
    color: #facc15 !important; margin: 0 0 8px 0 !important;
    line-height: 1.1 !important;
    text-shadow: 0 0 40px rgba(250,204,21,0.4) !important;
}
.hero-sub {
    font-size: 0.88rem !important; font-weight: 300 !important;
    color: rgba(196,214,255,0.8) !important; margin: 0 !important;
}

/* ── Card ── */
.card {
    background: #ffffff; border-radius: 20px; padding: 28px;
    box-shadow: 0 4px 24px rgba(30,40,120,0.08);
    border: 1px solid rgba(200,210,255,0.6);
    margin-bottom: 20px;
}
.card-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.78rem; font-weight: 700;
    letter-spacing: 1.8px; text-transform: uppercase;
    color: #4f46e5; margin-bottom: 20px;
    display: flex; align-items: center; gap: 10px;
}
.card-title::after {
    content:""; flex:1; height:1.5px;
    background: linear-gradient(90deg, #c7d2fe, transparent);
}

/* ── Charge box ── */
.charge-box {
    background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
    border: 2px solid; border-radius: 16px; padding: 20px;
    margin-bottom: 14px;
}
.charge-label {
    font-family: 'Rajdhani', sans-serif; font-weight: 700;
    font-size: 1.05rem; margin-bottom: 14px;
    display: flex; align-items: center; gap: 8px;
}

/* ── BOTÓN PRINCIPAL MEJORADO ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #6d28d9 100%) !important;
    color: #ffffff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.15rem !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    border: 3px solid transparent !important;
    border-radius: 18px !important;
    padding: 22px 0 !important;
    width: 100% !important;
    min-height: 60px !important;
    box-shadow: 
        0 0 40px rgba(79,70,229,0.5),
        0 8px 32px rgba(79,70,229,0.45),
        inset 0 1px 0 rgba(255,255,255,0.3) !important;
    transition: all 0.35s cubic-bezier(0.34,1.56,0.64,1) !important;
    cursor: pointer !important;
    position: relative !important;
}

[data-testid="stButton"] > button::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    background: radial-gradient(circle at 50% 0%, rgba(255,255,255,0.3), transparent) !important;
    border-radius: 18px !important;
    pointer-events: none !important;
}

[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #4338ca 0%, #6d28d9 50%, #581c87 100%) !important;
    box-shadow: 
        0 0 60px rgba(79,70,229,0.7),
        0 16px 48px rgba(79,70,229,0.65),
        inset 0 1px 0 rgba(255,255,255,0.4) !important;
    transform: translateY(-6px) !important;
}

[data-testid="stButton"] > button:active {
    transform: translateY(-2px) !important;
    box-shadow: 
        0 0 30px rgba(79,70,229,0.5),
        0 6px 20px rgba(79,70,229,0.4) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.98rem !important;
    letter-spacing: 0.8px !important;
    padding: 14px 22px !important;
    border-radius: 12px !important;
}

/* ── Result cards ── */
.res-grid { 
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px;
    margin-bottom: 14px;
}
.res-card {
    border-radius: 14px;
    padding: 18px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    transition: transform 0.2s, box-shadow 0.2s;
}
.res-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}
.res-card.blue  { background: linear-gradient(135deg, #eff6ff, #dbeafe);
                  border: 1.5px solid #93c5fd; }
.res-card.green { background: linear-gradient(135deg, #f0fdf4, #dcfce7);
                  border: 1.5px solid #86efac; }
.res-card.red   { background: linear-gradient(135deg, #fff7ed, #fee2e2);
                  border: 1.5px solid #fca5a5; }
.res-card.purple{ background: linear-gradient(135deg, #faf5ff, #f3e8ff);
                  border: 1.5px solid #d8b4fe; }
.res-icon { font-size: 2.4rem; flex-shrink: 0; }
.res-label {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #6b7280;
    margin-bottom: 3px;
}
.res-val {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.45rem;
    font-weight: 700;
    color: #1e3a8a;
    line-height: 1;
}
.res-val.g { color: #166534; }
.res-val.r { color: #9a3412; }
.res-val.p { color: #6b21a8; }

/* ── Divider ── */
.div {
    height: 2px;
    background: linear-gradient(90deg, transparent, #c7d2fe 35%, #c7d2fe 65%, transparent);
    border: none;
    margin: 28px 0;
}

/* ── Formula ── */
.fbox {
    background: linear-gradient(135deg, #f8f9ff, #f0f4ff);
    border: 1.5px solid #e0e7ff;
    border-radius: 14px;
    padding: 18px 24px;
    font-family: 'Inter', monospace;
    font-size: 0.87rem;
    color: #374151;
    line-height: 2.2;
}

[data-testid="stNumberInput"] label p {
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    color: #1e293b !important;
}

[data-testid="stSelectbox"] label p {
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    color: #1e293b !important;
}

/* ── Matplotlib container ── */
.stPyplotChart {
    padding: 20px !important;
    background: #ffffff !important;
    border-radius: 20px !important;
    margin-top: 20px !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    {logo_html}
    <div>
        <div class="hero-title">Simulador de Fuerza Eléctrica 2D</div>
        <p class="hero-sub">
            Ley de Coulomb · Ángulo θ Visualizado · Componentes Fx, Fy · 2-6 cargas
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Selector ────────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">🔧 Configuración del Sistema</div>',
            unsafe_allow_html=True)

num_cargas = st.selectbox(
    "¿Cuántas cargas?",
    [2, 3, 4, 5, 6],
    index=2,
    help="Selecciona el número total de cargas"
)

st.markdown('</div>', unsafe_allow_html=True)

# ─── Colores ─────────────────────────────────────────────────────────────────
COLORS = ["#ef4444", "#3b82f6", "#f59e0b", "#10b981", "#8b5cf6", "#ec4899"]
NAMES  = ["Q₁", "Q₂", "Q₃", "Q₄", "Q₅", "Q₆"]
BG     = ["#fff1f2", "#eff6ff", "#fffbeb", "#f0fdf4", "#f5f3ff", "#fce7f3"]
BORDER = ["#fca5a5", "#93c5fd", "#fcd34d", "#86efac", "#ddd6fe", "#fbcfe8"]

# ─── Entrada de parámetros ───────────────────────────────────────────────────
st.markdown(
    f'<div class="card"><div class="card-title">⚙️ Parámetros de las {num_cargas} Cargas</div>',
    unsafe_allow_html=True
)

default_charges = [
    {"q": 5.0, "x": 0.0, "y": 0.0},
    {"q": -3.0, "x": 3.0, "y": 0.0},
    {"q": 4.0, "x": 3.0, "y": 2.0},
    {"q": -2.0, "x": 0.0, "y": 2.0},
    {"q": 3.0, "x": 1.5, "y": -1.5},
    {"q": -1.5, "x": -1.5, "y": 1.5},
]

charges = []

for i in range(0, num_cargas, 2):
    cols = st.columns(2)
    for j, col in enumerate(cols):
        idx = i + j
        if idx >= num_cargas:
            break
        with col:
            st.markdown(
                f'<div class="charge-box" style="border-color:{BORDER[idx]};">'
                f'<div class="charge-label" style="color:{COLORS[idx]};">'
                f'{NAMES[idx]}</div>',
                unsafe_allow_html=True
            )

            default = default_charges[idx] if idx < len(default_charges) else {"q": 2.0, "x": float(idx), "y": 0.0}

            q_val = st.number_input("Carga (µC)", value=default["q"], step=0.5, key=f"q_{idx}")
            col1, col2 = st.columns(2)
            with col1:
                x_val = st.number_input("X (metros)", value=default["x"], step=0.5, key=f"x_{idx}")
            with col2:
                y_val = st.number_input("Y (metros)", value=default["y"], step=0.5, key=f"y_{idx}")

            charges.append({"q": q_val * 1e-6, "q_uc": q_val, "x": x_val, "y": y_val})
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── BOTÓN GRANDE Y DESTACADO ────────────────────────────────────────────────
st.markdown('<div style="margin: 30px 0;"></div>', unsafe_allow_html=True)
calcular = st.button("⚡ CALCULAR FUERZAS", use_container_width=True)
st.markdown('<div style="margin: 30px 0;"></div>', unsafe_allow_html=True)

# ─── CÁLCULOS ────────────────────────────────────────────────────────────────
if calcular:
    n = len(charges)

    # Validación
    valid = True
    for i in range(n):
        for j in range(i+1, n):
            dx = charges[j]["x"] - charges[i]["x"]
            dy = charges[j]["y"] - charges[i]["y"]
            if np.sqrt(dx**2 + dy**2) < 0.01:
                st.error(f"⚠️ {NAMES[i]} y {NAMES[j]} están demasiado cerca.")
                valid = False
    if not valid:
        st.stop()

    # Cálculo
    net_forces = [[0.0, 0.0] for _ in range(n)]
    pair_data = []

    for i in range(n):
        for j in range(i+1, n):
            q1, q2 = charges[i]["q"], charges[j]["q"]
            dx = charges[j]["x"] - charges[i]["x"]
            dy = charges[j]["y"] - charges[i]["y"]
            r  = np.sqrt(dx**2 + dy**2)

            F_mag = K * abs(q1 * q2) / r**2
            theta = np.degrees(np.arctan2(dy, dx))
            ux, uy = dx / r, dy / r

            sign = 1 if (q1 * q2) > 0 else -1

            fix = F_mag * (-sign) * ux
            fiy = F_mag * (-sign) * uy
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

    st.markdown('<hr class="div">', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "📊 Fuerzas Entre Pares",
        "🔢 Fuerza Neta por Carga",
        "🎨 Visualización 2D + Ángulos"
    ])

    # ── TAB 1 ──────────────────────────────────────────────────────────────
    with tab1:
        if not pair_data:
            st.info("No hay pares de cargas.")
        else:
            for p in pair_data:
                i, j = p["i"], p["j"]
                color_tipo = "#166534" if p["tipo"] == "Atracción" else "#9a3412"
                badge_bg = "#dcfce7" if p["tipo"] == "Atracción" else "#fee2e2"

                st.markdown(f"""
                <div class="card">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                    <span style="font-family:'Rajdhani',sans-serif;font-size:1.15rem;
                      font-weight:700;color:#1e293b;">{NAMES[i]} ↔ {NAMES[j]}</span>
                    <span style="background:{badge_bg};color:{color_tipo};padding:5px 16px;
                      border-radius:100px;font-size:0.8rem;font-weight:700;
                      letter-spacing:0.8px;">{p['tipo']}</span>
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
                  </div>
                  <div style="background:#f8f9ff;border-radius:12px;padding:16px;margin-top:16px;
                    font-family:'Rajdhani',monospace;font-size:0.82rem;color:#475569;line-height:2;">
                    <b style="color:#4f46e5;">Descomposición (θ = {p['theta']:.2f}°):</b><br>
                    <b>Sobre {NAMES[i]}:</b> Fx = {p['Fx_i']:+.4f} N,  Fy = {p['Fy_i']:+.4f} N<br>
                    <b>Sobre {NAMES[j]}:</b> Fx = {p['Fx_j']:+.4f} N,  Fy = {p['Fy_j']:+.4f} N
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 2 ──────────────────────────────────────────────────────────────
    with tab2:
        grid_cols = st.columns(min(3, n))
        for i in range(n):
            fx, fy = net_forces[i]
            mag = np.sqrt(fx**2 + fy**2)
            ang = np.degrees(np.arctan2(fy, fx))

            with grid_cols[i % len(grid_cols)]:
                st.markdown(f"""
                <div class="card">
                  <div style="font-family:'Rajdhani',sans-serif;font-size:1.18rem;
                    font-weight:700;color:{COLORS[i]};margin-bottom:18px;">{NAMES[i]} — Fuerza Neta</div>
                  <div class="res-grid">
                    <div class="res-card blue">
                      <div class="res-icon">→</div>
                      <div><div class="res-label">Fx</div>
                           <div class="res-val">{fx:+.4f} N</div></div>
                    </div>
                    <div class="res-card purple">
                      <div class="res-icon">↑</div>
                      <div><div class="res-label">Fy</div>
                           <div class="res-val p">{fy:+.4f} N</div></div>
                    </div>
                    <div class="res-card green">
                      <div class="res-icon">⚡</div>
                      <div><div class="res-label">|F| Neto</div>
                           <div class="res-val g">{mag:.4f} N</div></div>
                    </div>
                    <div class="res-card red">
                      <div class="res-icon">🧭</div>
                      <div><div class="res-label">θ</div>
                           <div class="res-val r">{ang:.2f}°</div></div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 3: GRÁFICA MEJORADA ───────────────────────────────────────────
    with tab3:
        st.markdown('<div class="card"><div class="card-title">🎨 Sistema Completo con Ángulos θ</div>',
                    unsafe_allow_html=True)

        fig = plt.figure(figsize=(16, 7))
        fig.patch.set_facecolor('#ffffff')

        # Subplot 1: Sistema
        ax1 = plt.subplot(1, 2, 1)
        ax1.set_facecolor('#fafbff')

        xs = [c["x"] for c in charges]
        ys = [c["y"] for c in charges]

        if len(xs) > 1:
            margin = max(max(xs)-min(xs), max(ys)-min(ys)) * 0.7 + 2.0
        else:
            margin = 2.5

        ax1.set_xlim(min(xs)-margin, max(xs)+margin)
        ax1.set_ylim(min(ys)-margin, max(ys)+margin)
        ax1.set_aspect('equal')

        ax1.grid(True, linestyle='--', alpha=0.2, color='#cbd5e1', linewidth=1.0)
        ax1.set_axisbelow(True)
        ax1.axhline(0, color='#94a3b8', linewidth=1.8, alpha=0.8, linestyle='-')        
        ax1.axvline(0, color='#94a3b8', linewidth=1.5, alpha=0.8, linestyle='-', linewidth=1.8)
        ax1.set_xlabel("x (metros)", fontsize=12, color='#1e293b', fontweight='700')
        ax1.set_ylabel("y (metros)", fontsize=12, color='#1e293b', fontweight='700')
        ax1.tick_params(colors='#64748b', labelsize=10, width=2, length=6)
        for spine in ax1.spines.values():
            spine.set_edgecolor('#cbd5e1')
            spine.set_linewidth(1.5)

        # Líneas y ángulos
        for p in pair_data:
            i, j = p["i"], p["j"]
            xi, yi = charges[i]["x"], charges[i]["y"]
            xj, yj = charges[j]["x"], charges[j]["y"]
            
            ax1.plot([xi, xj], [yi, yj], '--', color='#cbd5e1',
                    linewidth=1.5, alpha=0.5, zorder=1)
            
            # Arco del ángulo
            theta_rad = np.radians(p["theta"])
            arc_radius = 0.6
            arc = Arc((xi, yi), 2*arc_radius, 2*arc_radius,
                     angle=0, theta1=0, theta2=p['theta'],
                     color=COLORS[i], linewidth=3, linestyle='-', zorder=3)
            ax1.add_patch(arc)
            
            # Etiqueta ángulo
            angle_label_r = arc_radius * 1.5
            angle_x = xi + angle_label_r * np.cos(theta_rad/2)
            angle_y = yi + angle_label_r * np.sin(theta_rad/2)
            ax1.text(angle_x, angle_y, f"θ={p['theta']:.1f}°",
                    ha='center', va='center', fontsize=9, color='#1e293b',
                    fontweight='700', style='italic',
                    bbox=dict(boxstyle='round,pad=0.4', fc='#fef3c7',
                              ec='#f59e0b', alpha=0.97, linewidth=1.5))

            # Etiqueta distancia
            mx, my = (xi+xj)/2, (yi+yj)/2
            ax1.text(mx, my-0.35, f"r={p['r']:.2f}m",
                    ha='center', va='top', fontsize=8.5, color='#475569',
                    style='italic', fontweight='600',
                    bbox=dict(boxstyle='round,pad=0.35', fc='#ffffff',
                              ec='#cbd5e1', alpha=0.95, linewidth=1.2))

        # Vectores de fuerza
        max_mag = max(np.sqrt(f[0]**2 + f[1]**2) for f in net_forces) or 1
        scale = margin * 0.35 / max_mag

        for i, c in enumerate(charges):
            fx, fy = net_forces[i]
            mag = np.sqrt(fx**2 + fy**2)
            if mag > 1e-12:
                # Vector principal
                ax1.annotate("",
                    xy=(c["x"] + fx*scale, c["y"] + fy*scale),
                    xytext=(c["x"], c["y"]),
                    arrowprops=dict(arrowstyle='->', color=COLORS[i],
                                    lw=3.5, mutation_scale=22),
                    zorder=4)
                
                # Líneas punteadas de proyección
                ax1.plot([c["x"] + fx*scale, c["x"] + fx*scale],
                        [c["y"], c["y"] + fy*scale],
                        ':', color=COLORS[i], linewidth=2, alpha=0.4, zorder=2)
                ax1.plot([c["x"], c["x"] + fx*scale],
                        [c["y"] + fy*scale, c["y"] + fy*scale],
                        ':', color=COLORS[i], linewidth=2, alpha=0.4, zorder=2)
                
                theta_f = np.degrees(np.arctan2(fy, fx))
                ax1.text(c["x"] + fx*scale*1.3, c["y"] + fy*scale*1.3,
                        f"F={mag:.2f}N\nθ={theta_f:.1f}°",
                        ha='center', fontsize=8.5, color='#ffffff',
                        fontweight='700', zorder=5,
                        bbox=dict(boxstyle='round,pad=0.5', fc=COLORS[i],
                                  ec='#ffffff', alpha=0.95, linewidth=2))

        # Cargas
        for i, c in enumerate(charges):
            circle = plt.Circle((c["x"], c["y"]), margin*0.07,
                                 color=COLORS[i], zorder=5,
                                 ec='white', linewidth=4)
            ax1.add_patch(circle)
            sign = '+' if c["q"] > 0 else '−'
            ax1.text(c["x"], c["y"], sign, ha='center', va='center',
                    fontsize=16, fontweight='900', color='white', zorder=6)
            ax1.text(c["x"], c["y"] - margin*0.16,
                    f"{NAMES[i]}\n{c['q_uc']:+.1f}µC\n({c['x']:.1f},{c['y']:.1f})",
                    ha='center', fontsize=8.5, color=COLORS[i],
                    fontweight='700', zorder=6)

        # Leyenda
        legend_patches = [
            mpatches.Patch(color=COLORS[i], label=f"{NAMES[i]} = {charges[i]['q_uc']:+.1f} µC")
            for i in range(n)
        ]
        ax1.legend(handles=legend_patches, loc='upper left',
                  fontsize=10, framealpha=0.98, edgecolor='#cbd5e1',
                  fancybox=True, shadow=True)

        ax1.set_title(f"Sistema de {n} Cargas — Vectores y Ángulos θ",
                     fontsize=13, color='#1e3a8a', fontweight='700', pad=16)

        # Subplot 2: Descomposición
        if pair_data:
            ax2 = plt.subplot(1, 2, 2)
            ax2.set_facecolor('#fafbff')
            
            p = pair_data[0]
            F = p['F']
            theta = np.radians(p['theta'])
            Fx = F * np.cos(theta)
            Fy = F * np.sin(theta)

            ax2.axhline(0, color='#cbd5e1', linewidth=2, alpha=0.8)
            ax2.axvline(0, color='#cbd5e1', linewidth=2, alpha=0.8)
            ax2.set_xlim(-F*1.4, F*1.4)
            ax2.set_ylim(-F*1.4, F*1.4)
            ax2.set_aspect('equal')
            ax2.grid(True, linestyle='--', alpha=0.2, color='#cbd5e1', linewidth=1)
            ax2.set_axisbelow(True)

            # Vector principal
            ax2.arrow(0, 0, Fx, Fy, head_width=F*0.1, head_length=F*0.1,
                     fc='#7c3aed', ec='#7c3aed', linewidth=3.5, zorder=3, alpha=0.85)
            
            # Componentes
            ax2.arrow(0, 0, Fx, 0, head_width=F*0.08, head_length=F*0.08,
                     fc='#3b82f6', ec='#3b82f6', linewidth=3, zorder=2, alpha=0.8)
            ax2.arrow(Fx, 0, 0, Fy, head_width=F*0.08, head_length=F*0.08,
                     fc='#f59e0b', ec='#f59e0b', linewidth=3, zorder=2, alpha=0.8)

            # Proyección punteada
            ax2.plot([Fx, Fx], [0, Fy], '--', color='#94a3b8', linewidth=1.8, alpha=0.6, zorder=1)

            # Arco ángulo
            angle_arc_r = F * 0.3
            angle_arc = Arc((0, 0), 2*angle_arc_r, 2*angle_arc_r,
                           angle=0, theta1=0, theta2=np.degrees(theta),
                           color='#ef4444', linewidth=3.5, linestyle='-', zorder=3)
            ax2.add_patch(angle_arc)

            # Etiquetas
            ax2.text(Fx/2, -F*0.2, f"Fx = {Fx:+.4f} N\nF·cos(θ)", 
                    ha='center', fontsize=10, color='#3b82f6', fontweight='700',
                    bbox=dict(boxstyle='round,pad=0.5', fc='#dbeafe', ec='#60a5fa', alpha=0.97, linewidth=2))
            
            ax2.text(Fx+F*0.2, Fy/2, f"Fy = {Fy:+.4f} N\nF·sin(θ)", 
                    ha='left', fontsize=10, color='#f59e0b', fontweight='700',
                    bbox=dict(boxstyle='round,pad=0.5', fc='#fef3c7', ec='#fcd34d', alpha=0.97, linewidth=2))
            
            ax2.text(Fx/2*0.7, Fy/2*0.7+F*0.12, f"|F| = {F:.4f} N\nθ = {p['theta']:.2f}°", 
                    ha='center', fontsize=10, color='#7c3aed', fontweight='700',
                    bbox=dict(boxstyle='round,pad=0.5', fc='#f3e8ff', ec='#d8b4fe', alpha=0.97, linewidth=2))

            ax2.set_xlabel("Fx (Newtons)", fontsize=12, color='#1e293b', fontweight='700')
            ax2.set_ylabel("Fy (Newtons)", fontsize=12, color='#1e293b', fontweight='700')
            ax2.tick_params(colors='#64748b', labelsize=10, width=2, length=6)
            for spine in ax2.spines.values():
                spine.set_edgecolor('#cbd5e1')
                spine.set_linewidth(1.5)
            ax2.set_title(f"Descomposición: {NAMES[p['i']]} ↔ {NAMES[p['j']]}",
                         fontsize=13, color='#1e3a8a', fontweight='700', pad=16)

        plt.tight_layout(pad=2.0)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Fórmulas
        st.markdown('<hr class="div">', unsafe_allow_html=True)
        st.markdown('<div class="card"><div class="card-title">📐 Cómo el Ángulo θ Afecta las Componentes</div>',
                    unsafe_allow_html=True)

        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            st.markdown("**Ley de Coulomb**")
            st.latex(r"F = k_e \frac{|q_i \cdot q_j|}{r^2}")
        with col_f2:
            st.markdown("**Ángulo desde eje X**")
            st.latex(r"\theta = \arctan\left(\frac{\Delta y}{\Delta x}\right)")
        with col_f3:
            st.markdown("**Componentes**")
            st.latex(r"F_x = F\cos(\theta),\ F_y = F\sin(\theta)")

        st.markdown(f"""
        <div class="fbox">
            <b style="color:#4f46e5;">θ (Theta)</b> es el ángulo que forma la línea entre dos cargas respecto al eje X positivo.
            Si θ cambia (cargas en diferentes posiciones), las componentes Fx y Fy cambian aunque |F| sea igual.
            <br><br>
            <b style="color:#6d28d9;">Ejemplo:</b> Si F = 10 N y θ = 30°, entonces Fx ≈ 8.66 N y Fy = 5 N.
            Si θ = 60°, entonces Fx = 5 N y Fy ≈ 8.66 N. El ángulo distribuye la fuerza en X e Y.
        </div></div>
        """, unsafe_allow_html=True)
