import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import base64
import math
from pathlib import Path

K = 8.99e9

st.set_page_config(
    page_title="Simulador de Fuerza Eléctrica — Ley de Coulomb",
    page_icon="⚡",
    layout="centered"
)

# ─── State ────────────────────────────────────────────────────────────────────
if "charges" not in st.session_state:
    st.session_state.charges = [
        {"x": 0.0, "y": 0.0, "q": 5.0},
        {"x": 2.0, "y": 0.0, "q": -3.0},
    ]

# ─── Logo ─────────────────────────────────────────────────────────────────────
def get_logo_b64(path: str) -> str:
    try:
        return base64.b64encode(Path(path).read_bytes()).decode()
    except Exception:
        return ""

logo_b64 = get_logo_b64("logo.png")

if logo_b64:
    logo_html = f'''
    <div style="background:#fff;border-radius:10px;padding:4px;
                box-shadow:0 2px 8px rgba(0,0,0,0.08);flex-shrink:0;
                display:inline-flex;">
        <img src="data:image/png;base64,{logo_b64}"
             style="height:64px;width:64px;object-fit:contain;display:block;" />
    </div>'''
else:
    logo_html = '<span style="font-size:44px;line-height:1;flex-shrink:0;">⚡</span>'

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, section.main {
    background-color: #f8fafc !important;
}
[data-testid="stHeader"] { background: #f8fafc !important; }
[data-testid="stToolbar"] { display: none !important; }
#MainMenu, footer { visibility: hidden !important; }

body, .stApp { font-family: 'Inter', sans-serif; }

/* ─── Hero ──────────────────────────────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, #0f0c29 0%, #1e1b4b 50%, #312e81 100%);
    border-radius: 16px;
    padding: 22px 26px;
    margin-bottom: 26px;
    display: flex;
    align-items: center;
    gap: 18px;
    box-shadow: 0 6px 22px rgba(30,27,75,0.22);
    overflow: hidden;
}
.hero-title {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.5rem !important;
    line-height: 1.25 !important;
    margin: 0 0 3px 0 !important;
    color: #fde047 !important;
    letter-spacing: -0.3px !important;
}
.hero-sub {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 400 !important;
    color: #e0e7ff !important;
    margin: 0 !important;
}

/* ─── Section badge ─────────────────────────────────────── */
.section-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 4px 14px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.75rem;
    color: #1e293b;
    letter-spacing: 0.3px;
    margin-bottom: 14px;
}

/* ─── Form card ─────────────────────────────────────────── */
[data-testid="stForm"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px !important;
    padding: 18px 20px 4px 20px !important;
    margin-bottom: 14px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03) !important;
}

/* ─── Inputs compactos ──────────────────────────────────── */
[data-testid="stNumberInput"] {
    margin-bottom: 0 !important;
}
[data-testid="stNumberInput"] label p {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.78rem !important;
    color: #334155 !important;
    margin-bottom: 1px !important;
}
[data-testid="stNumberInput"] input {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    padding: 2px 6px !important;
    border-radius: 7px !important;
    border: 1.5px solid #e2e8f0 !important;
    min-height: 30px !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: #4338ca !important;
    box-shadow: 0 0 0 2px rgba(67,56,202,0.12) !important;
}

/* ─── Buttons ───────────────────────────────────────────── */
.stButton > button,
[data-testid="stFormSubmitButton"] > button {
    width: 100% !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 8px 0 !important;
    cursor: pointer !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s ease !important;
}
.stButton > button {
    background: #ffffff !important;
    color: #475569 !important;
    border: 1.5px solid #e2e8f0 !important;
    box-shadow: none !important;
}
.stButton > button:hover {
    background: #f1f5f9 !important;
    border-color: #cbd5e1 !important;
}
[data-testid="stFormSubmitButton"] > button {
    background: #1e1b4b !important;
    color: #ffffff !important;
    box-shadow: 0 3px 10px rgba(30,27,75,0.15) !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
    background: #312e81 !important;
    box-shadow: 0 5px 16px rgba(30,27,75,0.25) !important;
}

/* ─── Result cards ──────────────────────────────────────── */
.result-card {
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    border: 1.5px solid;
}
.result-card.blue {
    background: linear-gradient(135deg,#eff6ff,#dbeafe);
    border-color: #93c5fd;
}
.result-card.green {
    background: linear-gradient(135deg,#f0fdf4,#dcfce7);
    border-color: #86efac;
}
.result-card.red {
    background: linear-gradient(135deg,#fff7ed,#fee2e2);
    border-color: #fca5a5;
}
.result-icon { font-size: 1.6rem; flex-shrink: 0; }
.result-label {
    font-size: 0.72rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    color: #475569;
    margin-bottom: 2px;
    font-family: 'Inter', sans-serif;
}
.result-value {
    font-family: 'Inter', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #1e3a8a;
    line-height: 1.1;
}
.result-value.green { color: #166534; }
.result-value.red { color: #991b1b; }

/* ─── Charge input row ──────────────────────────────────── */
.charge-label {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.82rem;
    color: #1e293b;
    padding-top: 18px;
    white-space: nowrap;
}
.input-header {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.7rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding-bottom: 2px;
}

/* ─── Divider ───────────────────────────────────────────── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg,transparent,#e2e8f0 25%,#e2e8f0 75%,transparent);
    border: none;
    margin: 22px 0;
}

/* ─── Formula grid ──────────────────────────────────────── */
.formula-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 4px;
}
.formula-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 14px 14px;
    text-align: center;
}
.formula-title {
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #475569;
    margin-bottom: 8px;
    font-family: 'Inter', sans-serif;
}
.formula-desc {
    font-size: 0.68rem;
    color: #94a3b8;
    margin-top: 4px;
    font-family: 'Inter', sans-serif;
    font-style: italic;
}
.formula-equation {
    min-height: 2.6em;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ─── Values box ────────────────────────────────────────── */
.values-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 11px;
    padding: 12px 18px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #1e293b;
    margin-top: 16px;
    line-height: 1.8;
}

/* ─── Plot ──────────────────────────────────────────────── */
[data-testid="stPlot"], .stPlot {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
    background: #ffffff;
    padding: 4px;
}

/* ─── Responsive ────────────────────────────────────────── */
@media (max-width: 768px) {
    .hero-banner {
        flex-direction: column;
        text-align: center;
        padding: 18px 16px;
    }
    .hero-title { font-size: 1.25rem !important; }
    .hero-sub { font-size: 0.78rem !important; }
    [data-testid="stForm"] { padding: 14px 14px 2px 14px !important; }
    .result-card { padding: 12px 14px; }
    .result-value { font-size: 1.1rem; }
    .formula-grid { grid-template-columns: 1fr; gap: 10px; }
    .values-box { font-size: 0.72rem !important; padding: 10px 12px !important; }
}
@media (max-width: 480px) {
    .hero-title { font-size: 1.05rem !important; }
    .hero-sub { font-size: 0.72rem !important; }
    .result-value { font-size: 1rem; }
    .result-label { font-size: 0.65rem; }
}

/* ─── Transitions ───────────────────────────────────────── */
* { transition: background-color 0.15s ease, box-shadow 0.15s ease, transform 0.15s ease; }
</style>
""", unsafe_allow_html=True)

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
    {logo_html}
    <div>
        <div class="hero-title">Proyecto de Simulador de Fuerza Eléctrica</div>
        <p class="hero-sub">Ley de Coulomb &nbsp;·&nbsp; Cálculo vectorial de fuerzas electrostáticas en 2D</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Parámetros ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-badge">⚙️ &nbsp; Parámetros de entrada</div>', unsafe_allow_html=True)

# Add / Remove buttons
cols = st.columns([1, 1, 6])
with cols[0]:
    if st.button("+ Añadir carga", key="add", use_container_width=True):
        if len(st.session_state.charges) < 8:
            st.session_state.charges.append({"x": 0.0, "y": 0.0, "q": 1.0})
        st.rerun()
with cols[1]:
    if st.button("− Eliminar", key="remove", use_container_width=True):
        if len(st.session_state.charges) > 2:
            st.session_state.charges.pop()
        st.rerun()

with st.form("param-form", border=False):
    # Header row
    hcols = st.columns([1.2, 2, 2, 2])
    with hcols[0]:
        st.markdown("")
    with hcols[1]:
        st.markdown('<div class="input-header">X (m)</div>', unsafe_allow_html=True)
    with hcols[2]:
        st.markdown('<div class="input-header">Y (m)</div>', unsafe_allow_html=True)
    with hcols[3]:
        st.markdown('<div class="input-header">q (µC)</div>', unsafe_allow_html=True)

    for i, charge in enumerate(st.session_state.charges):
        cols = st.columns([1.2, 2, 2, 2])
        with cols[0]:
            st.markdown(f'<div class="charge-label">Carga {i + 1}</div>', unsafe_allow_html=True)
        with cols[1]:
            charge["x"] = st.number_input(
                f"x_{i}", key=f"x_{i}", value=charge["x"],
                step=0.5, format="%.2f", label_visibility="collapsed"
            )
        with cols[2]:
            charge["y"] = st.number_input(
                f"y_{i}", key=f"y_{i}", value=charge["y"],
                step=0.5, format="%.2f", label_visibility="collapsed"
            )
        with cols[3]:
            charge["q"] = st.number_input(
                f"q_{i}", key=f"q_{i}", value=charge["q"],
                step=0.5, format="%.1f", label_visibility="collapsed"
            )

    calcular = st.form_submit_button("⚡  Calcular y visualizar")

# ─── Cálculo vectorial ───────────────────────────────────────────────────────
if calcular:
    charges = st.session_state.charges
    n = len(charges)
    q_si = [c["q"] * 1e-6 for c in charges]

    # Force components on each charge
    fx = [0.0] * n
    fy = [0.0] * n

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = charges[j]["x"] - charges[i]["x"]
            dy = charges[j]["y"] - charges[i]["y"]
            r2 = dx * dx + dy * dy
            if r2 < 1e-12:
                continue
            r = math.sqrt(r2)
            fx[i] += K * q_si[i] * q_si[j] / (r2 * r) * dx
            fy[i] += K * q_si[i] * q_si[j] / (r2 * r) * dy

    fmag = [math.sqrt(fx[i] ** 2 + fy[i] ** 2) for i in range(n)]

    # Tipo general del sistema
    total_product = sum(q_si[i] * q_si[j] for i in range(n) for j in range(i + 1, n))
    if total_product < 0:
        sys_tipo = "Atracción predominante"
        sys_color = "#059669"
        sys_card = "green"
        sys_icon = "🟢"
    elif total_product > 0:
        sys_tipo = "Repulsión predominante"
        sys_color = "#dc2626"
        sys_card = "red"
        sys_icon = "🔴"
    else:
        sys_tipo = "Sistema equilibrado"
        sys_color = "#64748b"
        sys_card = "blue"
        sys_icon = "⚪"

    # ─── Resultados ───────────────────────────────────────────────────────────
    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-badge">📊 &nbsp; Resultados analíticos</div>', unsafe_allow_html=True)

    # One row per charge
    for i in range(n):
        cols = st.columns([1, 1])
        with cols[0]:
            st.markdown(f"""
            <div class="result-card blue">
                <div class="result-icon">⚡</div>
                <div>
                    <div class="result-label">Carga {i + 1} — Fuerza neta</div>
                    <div class="result-value">{fmag[i]:.6f} N</div>
                </div>
            </div>""", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"""
            <div class="result-card {sys_card}">
                <div class="result-icon">{sys_icon}</div>
                <div>
                    <div class="result-label">Componentes vectoriales</div>
                    <div class="result-value" style="font-size:1rem;">
                        Fx = {fx[i]:.6f} N<br>Fy = {fy[i]:.6f} N
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ─── Gráfica vectorial 2D ────────────────────────────────────────────────
    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-badge">🎨 &nbsp; Representación vectorial 2D</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    all_x = [c["x"] for c in charges]
    all_y = [c["y"] for c in charges]
    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = min(all_y), max(all_y)
    x_range = max(x_max - x_min, 1.0) * 1.6
    y_range = max(y_max - y_min, 1.0) * 1.6
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    ax.set_xlim(x_center - x_range / 2, x_center + x_range / 2)
    ax.set_ylim(y_center - y_range / 2, y_center + y_range / 2)

    ax.grid(True, linestyle='--', linewidth=0.4, color='#e2e8f0', alpha=0.7)
    ax.axhline(0, color='#cbd5e1', linewidth=0.5)
    ax.axvline(0, color='#cbd5e1', linewidth=0.5)

    for i in range(n):
        color = '#ef4444' if charges[i]["q"] > 0 else '#3b82f6'
        ax.scatter(charges[i]["x"], charges[i]["y"], s=700, c=color,
                   edgecolors='white', linewidths=2.5, zorder=4)
        sign = '+' if charges[i]["q"] > 0 else '−'
        ax.text(charges[i]["x"], charges[i]["y"], sign, ha='center', va='center',
                fontsize=13, fontweight='bold', color='white', zorder=5)
        ax.text(charges[i]["x"], charges[i]["y"] + 0.08 * y_range,
                f'q{i + 1} = {charges[i]["q"]:.1f} µC', ha='center', fontsize=8,
                fontweight='bold', color=color)

    # Force vectors (scaled)
    max_f = max(fmag) if max(fmag) > 0 else 1
    scale = min(x_range, y_range) * 0.12 / max_f

    for i in range(n):
        if fmag[i] > 1e-12:
            ax.annotate(
                '', xy=(charges[i]["x"] + fx[i] * scale, charges[i]["y"] + fy[i] * scale),
                xytext=(charges[i]["x"], charges[i]["y"]),
                arrowprops=dict(arrowstyle='->', color='#7c3aed', lw=1.8, mutation_scale=16)
            )
            ax.text(
                charges[i]["x"] + fx[i] * scale * 0.55,
                charges[i]["y"] + fy[i] * scale * 0.55 + 0.03 * y_range,
                f'F{i + 1}', ha='center', color='#7c3aed', fontsize=8.5, fontweight='bold'
            )

    patches = [
        mpatches.Patch(color='#ef4444', label='Carga positiva (+)'),
        mpatches.Patch(color='#3b82f6', label='Carga negativa (−)'),
        mpatches.Patch(color='#7c3aed', label='Fuerza neta'),
    ]
    ax.legend(handles=patches, loc='upper right', fontsize=7.5,
              framealpha=0.9, edgecolor='#e2e8f0')

    ax.set_xlabel('x (m)', fontsize=8.5, color='#64748b')
    ax.set_ylabel('y (m)', fontsize=8.5, color='#64748b')
    ax.tick_params(labelsize=7.5, colors='#64748b')

    st.pyplot(fig)

    # ─── Fórmulas ─────────────────────────────────────────────────────────────
    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-badge">📐 &nbsp; Marco teórico</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-grid">
        <div class="formula-card">
            <div class="formula-title">Ley de Coulomb (vectorial)</div>
            <div class="formula-equation">$$\\vec{F}_{ij} = k_e \\frac{q_i q_j}{r^3} \\vec{r}_{ij}$$</div>
            <div class="formula-desc">Fuerza electrostática entre dos cargas puntuales</div>
        </div>
        <div class="formula-card">
            <div class="formula-title">Distancia euclidiana</div>
            <div class="formula-equation">$$r = \\sqrt{(x_j - x_i)^2 + (y_j - y_i)^2}$$</div>
            <div class="formula-desc">Distancia real entre dos puntos en el plano 2D</div>
        </div>
        <div class="formula-card">
            <div class="formula-title">Componentes de la fuerza</div>
            <div class="formula-equation">$$F_x = F \\cos\\theta \\quad F_y = F \\sin\\theta$$</div>
            <div class="formula-desc">Descomposición vectorial en ejes cartesianos</div>
        </div>
        <div class="formula-card">
            <div class="formula-title">Fuerza neta</div>
            <div class="formula-equation">$$\\vec{F}_{net} = \\sum_{j \\neq i} \\vec{F}_{ij}$$</div>
            <div class="formula-desc">Suma vectorial de todas las fuerzas sobre una carga</div>
        </div>
        <div class="formula-card">
            <div class="formula-title">Campo eléctrico</div>
            <div class="formula-equation">$$\\vec{E} = k_e \\frac{q}{r^2} \\hat{r}$$</div>
            <div class="formula-desc">Campo eléctrico generado por una carga puntual</div>
        </div>
        <div class="formula-card">
            <div class="formula-title">Potencial eléctrico</div>
            <div class="formula-equation">$$V = k_e \\frac{q}{r}$$</div>
            <div class="formula-desc">Potencial electrostático escalar</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="values-box">
        <b>kₑ</b> = 8.99 × 10⁹ N·m²/C² &nbsp;&nbsp;|&nbsp;&nbsp;
        <b>Cargas</b>: {len(charges)} &nbsp;&nbsp;|&nbsp;&nbsp;
        <b>Tipo</b>: {sys_tipo} &nbsp;&nbsp;|&nbsp;&nbsp;
        <b>F₁</b> = {fmag[0]:.6f} N {('|  <b>F₂</b> = ' + f'{fmag[1]:.6f}' + ' N') if n >= 2 else ''}
    </div>
    """, unsafe_allow_html=True)
