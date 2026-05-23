import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import base64
from pathlib import Path

K = 8.99e9

st.set_page_config(
    page_title="Simulador de Fuerza Eléctrica — Ley de Coulomb",
    page_icon="⚡",
    layout="centered"
)

# ─── Cargar logo ──────────────────────────────────────────────────────────────
def get_logo_b64(path: str) -> str:
    try:
        return base64.b64encode(Path(path).read_bytes()).decode()
    except Exception:
        return ""

logo_b64 = get_logo_b64("logo.png")

if logo_b64:
    logo_html = f'''
    <img src="data:image/png;base64,{logo_b64}"
         style="height:72px;width:72px;object-fit:contain;flex-shrink:0;
                border-radius:10px;" />
    '''
else:
    logo_html = '<span style="font-size:44px;line-height:1;flex-shrink:0;">⚡</span>'

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, section.main {
    background-color: #f4f6fa !important;
}
[data-testid="stHeader"] {
    background: #f4f6fa !important;
}
[data-testid="stToolbar"] { display: none !important; }
#MainMenu, footer { visibility: hidden !important; }

body, .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ─── Hero Banner ──────────────────────────────────────────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, #0f0c29 0%, #1e1b4b 50%, #312e81 100%);
    border-radius: 18px;
    padding: 26px 30px;
    margin-bottom: 30px;
    display: flex;
    align-items: center;
    gap: 22px;
    box-shadow: 0 8px 28px rgba(30, 27, 75, 0.28);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: "";
    position: absolute;
    top: -60px;
    right: -60px;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(255, 215, 0, 0.08) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-title {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.7rem !important;
    line-height: 1.25 !important;
    margin: 0 0 4px 0 !important;
    color: #fde047 !important;
    letter-spacing: -0.3px !important;
}
.hero-sub {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.93rem !important;
    font-weight: 400 !important;
    color: #e0e7ff !important;
    margin: 0 !important;
}

/* ─── Section Badge ────────────────────────────────────────────────────────── */
.section-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #e2e6ef;
    border-radius: 8px;
    padding: 6px 14px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.8rem;
    color: #1e1b4b;
    letter-spacing: 0.3px;
    margin-bottom: 18px;
}

/* ─── Parameter Card ───────────────────────────────────────────────────────── */
.param-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 26px 28px 18px 28px;
    margin-bottom: 18px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

[data-testid="stNumberInput"] label p {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.92rem !important;
    color: #1e293b !important;
}

/* ─── Button ───────────────────────────────────────────────────────────────── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #1e1b4b 0%, #4338ca 100%) !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 11px !important;
    padding: 11px 0 !important;
    margin-top: 6px !important;
    box-shadow: 0 4px 14px rgba(67, 56, 202, 0.22) !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(67, 56, 202, 0.32) !important;
    background: linear-gradient(135deg, #312e81 0%, #4f46e5 100%) !important;
}

/* ─── Result Cards ─────────────────────────────────────────────────────────── */
.result-card {
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
.result-card.fuerza {
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    border: 1.5px solid #93c5fd;
}
.result-card.atraccion {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border: 1.5px solid #86efac;
}
.result-card.repulsion {
    background: linear-gradient(135deg, #fff7ed, #fee2e2);
    border: 1.5px solid #fca5a5;
}
.result-icon {
    font-size: 1.8rem;
    flex-shrink: 0;
}
.result-label {
    font-size: 0.78rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    color: #475569;
    margin-bottom: 3px;
    font-family: 'Inter', sans-serif;
}
.result-value {
    font-family: 'Inter', sans-serif;
    font-size: 1.45rem;
    font-weight: 700;
    color: #1e3a8a;
    line-height: 1.1;
}
.result-value.green { color: #166534; }
.result-value.red { color: #991b1b; }

/* ─── Divider ──────────────────────────────────────────────────────────────── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #cbd5e1 25%, #cbd5e1 75%, transparent);
    border: none;
    margin: 26px 0;
}

/* ─── Formula Grid ─────────────────────────────────────────────────────────── */
.formula-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 6px;
}
.formula-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 22px 16px 18px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
.formula-card:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}
.formula-title {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #475569;
    margin-bottom: 10px;
    font-family: 'Inter', sans-serif;
}
.formula-desc {
    font-size: 0.72rem;
    color: #94a3b8;
    margin-top: 6px;
    font-family: 'Inter', sans-serif;
    font-style: italic;
}
.formula-equation {
    min-height: 2.8em;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ─── Values Box ──────────────────────────────────────────────────────────── */
.values-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 14px 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: #1e293b;
    margin-top: 20px;
    line-height: 1.9;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
}

/* ─── Plot Container ───────────────────────────────────────────────────────── */
[data-testid="stPlot"],
.stPlot {
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
    background: #ffffff;
    padding: 6px;
}

/* ─── Responsive ───────────────────────────────────────────────────────────── */
@media (max-width: 768px) {
    .hero-banner {
        flex-direction: column;
        text-align: center;
        padding: 22px 18px;
    }
    .hero-title {
        font-size: 1.35rem !important;
    }
    .hero-sub {
        font-size: 0.82rem !important;
    }
    .param-card {
        padding: 18px 14px 14px 14px;
    }
    .result-card {
        padding: 14px 16px;
    }
    .result-value {
        font-size: 1.25rem;
    }
    .formula-grid {
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }
}

@media (max-width: 520px) {
    .formula-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 480px) {
    .hero-title {
        font-size: 1.15rem !important;
    }
    .result-value {
        font-size: 1.1rem;
    }
    .result-label {
        font-size: 0.7rem;
    }
}

/* ─── Smooth Transitions ───────────────────────────────────────────────────── */
* {
    transition: background-color 0.15s ease, box-shadow 0.15s ease, transform 0.15s ease;
}
</style>
""", unsafe_allow_html=True)

# ─── Hero Banner ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
    {logo_html}
    <div>
        <div class="hero-title">Simulador de Fuerza Eléctrica</div>
        <p class="hero-sub">Ley de Coulomb &nbsp;·&nbsp; Cálculo y visualización vectorial de fuerzas electrostáticas</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Parámetros de Entrada ────────────────────────────────────────────────────
st.markdown('<div class="section-badge">⚙️ &nbsp; Parámetros de entrada</div>', unsafe_allow_html=True)
st.markdown('<div class="param-card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    q1_micro = st.number_input("⊕  Carga 1 (µC)", value=5.0, step=0.5)
with col2:
    q2_micro = st.number_input("⊖  Carga 2 (µC)", value=-3.0, step=0.5)

r = st.number_input("📏  Distancia entre las cargas (metros)", min_value=0.01, value=2.0, step=0.1)
st.markdown('</div>', unsafe_allow_html=True)

calcular = st.button("⚡  Calcular y visualizar")

# ─── Resultados ───────────────────────────────────────────────────────────────
if calcular:
    q1 = q1_micro * 1e-6
    q2 = q2_micro * 1e-6
    fuerza = K * abs(q1 * q2) / r ** 2

    if (q1 * q2) < 0:
        tipo = "Atracción"
        mpl_color = "#059669"
        card_tipo = "atraccion"
        icono_tipo = "🟢"
        val_class = "green"
        dir_vector = -1
    else:
        tipo = "Repulsión"
        mpl_color = "#dc2626"
        card_tipo = "repulsion"
        icono_tipo = "🔴"
        val_class = "red"
        dir_vector = 1

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-badge">📊 &nbsp; Resultados analíticos</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="result-card fuerza">
            <div class="result-icon">🔬</div>
            <div>
                <div class="result-label">Magnitud de la fuerza</div>
                <div class="result-value">{fuerza:.4f} N</div>
            </div>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="result-card {card_tipo}">
            <div class="result-icon">{icono_tipo}</div>
            <div>
                <div class="result-label">Tipo de interacción</div>
                <div class="result-value {val_class}">{tipo}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-badge">🎨 &nbsp; Representación vectorial</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(9, 4.0))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    c_colors = [
        '#ef4444' if q1 > 0 else '#3b82f6',
        '#ef4444' if q2 > 0 else '#3b82f6'
    ]

    ax.plot([0, r], [0, 0], color='#94a3b8', linestyle='--', linewidth=1.5, alpha=0.5, zorder=1)
    ax.annotate('', xy=(r, -0.3), xytext=(0, -0.3),
                arrowprops=dict(arrowstyle='<->', color='#64748b', lw=1.3))
    ax.text(r / 2, -0.42, f'd = {r} m', ha='center', fontsize=9,
            color='#64748b', style='italic', fontfamily='monospace')

    ax.scatter([0, r], [0, 0], s=1000, c=c_colors, edgecolors='white', linewidths=3, zorder=3)
    ax.text(0, 0, '+' if q1 > 0 else '−', ha='center', va='center',
            fontsize=14, fontweight='bold', color='white', zorder=4)
    ax.text(r, 0, '+' if q2 > 0 else '−', ha='center', va='center',
            fontsize=14, fontweight='bold', color='white', zorder=4)

    sign1 = '+' if q1_micro >= 0 else ''
    sign2 = '+' if q2_micro >= 0 else ''
    ax.text(0, 0.25, f'q₁ = {sign1}{q1_micro} µC', ha='center',
            fontsize=10, fontweight='bold', color=c_colors[0])
    ax.text(r, 0.25, f'q₂ = {sign2}{q2_micro} µC', ha='center',
            fontsize=10, fontweight='bold', color=c_colors[1])

    escala = r * 0.24
    ax.annotate('', xy=(-dir_vector * escala, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=mpl_color, lw=2.5, mutation_scale=20))
    ax.text(-dir_vector * (escala + 0.08 * r), -0.25,
            'F₁', ha='center', color=mpl_color, fontsize=11, fontweight='bold')
    ax.annotate('', xy=(r + dir_vector * escala, 0), xytext=(r, 0),
                arrowprops=dict(arrowstyle='->', color=mpl_color, lw=2.5, mutation_scale=20))
    ax.text(r + dir_vector * (escala + 0.08 * r), -0.25,
            'F₂', ha='center', color=mpl_color, fontsize=11, fontweight='bold')

    patches = [
        mpatches.Patch(color='#ef4444', label='Carga positiva (+)'),
        mpatches.Patch(color='#3b82f6', label='Carga negativa (−)'),
        mpatches.Patch(color=mpl_color, label=f'Fuerza de {tipo.lower()}'),
    ]

    ax.legend(
        handles=patches, loc='lower center', bbox_to_anchor=(0.5, -0.22),
        ncol=3, fontsize=8.5, framealpha=0.95, edgecolor='#e2e8f0', fancybox=True
    )

    ax.set_xlim(-r * 0.55, r * 1.6)
    ax.set_ylim(-0.75, 0.55)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    st.pyplot(fig)

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-badge">📐 &nbsp; Marco teórico</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-grid">
        <div class="formula-card">
            <div class="formula-title">Ley de Coulomb</div>
            <div class="formula-equation">$$F = k_e \\frac{|q_1 q_2|}{r^2}$$</div>
            <div class="formula-desc">Magnitud de la fuerza electrostática entre dos cargas puntuales</div>
        </div>
        <div class="formula-card">
            <div class="formula-title">Forma vectorial</div>
            <div class="formula-equation">$$\\vec{F}_{12} = k_e \\frac{q_1 q_2}{r^2} \\hat{r}_{12}$$</div>
            <div class="formula-desc">Fuerza como vector en la dirección radial unitaria</div>
        </div>
        <div class="formula-card">
            <div class="formula-title">Campo eléctrico</div>
            <div class="formula-equation">$$E = k_e \\frac{|q|}{r^2}$$</div>
            <div class="formula-desc">Magnitud del campo eléctrico generado por una carga puntual</div>
        </div>
        <div class="formula-card">
            <div class="formula-title">Potencial eléctrico</div>
            <div class="formula-equation">$$V = k_e \\frac{q}{r}$$</div>
            <div class="formula-desc">Potencial electrostático escalar de una carga puntual</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="values-box">
        <b>kₑ</b> = 8.99 × 10⁹ N·m²/C² &nbsp;&nbsp;|&nbsp;&nbsp;
        <b>q₁</b> = {q1_micro} µC &nbsp;&nbsp;|&nbsp;&nbsp;
        <b>q₂</b> = {q2_micro} µC &nbsp;&nbsp;|&nbsp;&nbsp;
        <b>r</b> = {r} m &nbsp;&nbsp;|&nbsp;&nbsp;
        <b>F</b> = {fuerza:.4f} N
    </div>
    """, unsafe_allow_html=True)
