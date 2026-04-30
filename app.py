import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import base64
from pathlib import Path

K = 8.99e9

st.set_page_config(
    page_title="Proyecto de Simulador de Fuerza Eléctrica",
    page_icon="⚡",
    layout="centered"
)

# ─── Cargar logo (mismo directorio que app.py) ────────────────────────────────
def get_logo_b64(path: str) -> str:
    try:
        return base64.b64encode(Path(path).read_bytes()).decode()
    except Exception:
        return ""

logo_b64 = get_logo_b64("logo.png")

if logo_b64:
    logo_html = f'''<img src="data:image/png;base64,{logo_b64}"
        style="height:90px;width:90px;object-fit:contain;
               border-radius:14px;flex-shrink:0;
               filter:drop-shadow(0 0 14px rgba(255,215,0,0.5));" />'''
else:
    logo_html = '<span style="font-size:72px;line-height:1;flex-shrink:0;">⚡</span>'

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, section.main {
    background-color: #ffffff !important;
}
[data-testid="stHeader"]   { background: #ffffff !important; }
[data-testid="stToolbar"]  { display: none !important; }
#MainMenu, footer          { visibility: hidden !important; }

body, .stApp { font-family: 'IBM Plex Sans', sans-serif; }

.hero-banner {
    background: linear-gradient(130deg, #0d0b22 0%, #1e1b4b 45%, #312e81 100%);
    border-radius: 20px;
    padding: 30px 36px;
    margin-bottom: 36px;
    display: flex;
    align-items: center;
    gap: 28px;
    box-shadow: 0 12px 40px rgba(30,27,75,0.35), 0 2px 8px rgba(0,0,0,0.15);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content:""; position:absolute; top:-80px; right:-80px;
    width:260px; height:260px;
    background: radial-gradient(circle, rgba(255,215,0,0.12) 0%, transparent 65%);
    border-radius:50%; pointer-events:none;
}
.hero-banner::after {
    content:""; position:absolute; bottom:-50px; left:20%;
    width:350px; height:130px;
    background: radial-gradient(ellipse, rgba(129,140,248,0.1) 0%, transparent 70%);
    pointer-events:none;
}
.hero-title {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.95rem !important;
    line-height: 1.15 !important;
    margin: 0 0 8px 0 !important;
    color: #fcd34d !important;
    text-shadow: 0 0 30px rgba(252,211,77,0.4) !important;
}
.hero-sub {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 300 !important;
    color: rgba(199,210,254,0.8) !important;
    margin: 0 !important;
    letter-spacing: 0.2px !important;
}
.section-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: #eef2ff; border: 1.5px solid #c7d2fe;
    border-radius: 100px; padding: 5px 16px;
    font-family: 'Rajdhani', sans-serif; font-weight: 600;
    font-size: 0.78rem; color: #4338ca;
    letter-spacing: 1px; text-transform: uppercase; margin-bottom: 16px;
}
.param-card {
    background: #fafbff; border: 1.5px solid #e0e7ff;
    border-radius: 16px; padding: 24px 24px 12px 24px;
    margin-bottom: 18px; box-shadow: 0 2px 12px rgba(67,56,202,0.06);
}
[data-testid="stNumberInput"] label p {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 500 !important; font-size: 0.9rem !important;
    color: #3730a3 !important;
}
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #1e1b4b 0%, #4338ca 100%) !important;
    color: #fcd34d !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important; font-size: 1.1rem !important;
    letter-spacing: 1.5px !important; text-transform: uppercase !important;
    border: none !important; border-radius: 12px !important;
    padding: 14px 0 !important; margin-top: 12px !important;
    box-shadow: 0 4px 20px rgba(67,56,202,0.3) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(67,56,202,0.45) !important;
    background: linear-gradient(135deg, #312e81 0%, #4f46e5 100%) !important;
}
.result-card {
    border-radius: 16px; padding: 20px 24px; margin-bottom: 14px;
    display: flex; align-items: center; gap: 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.result-card.fuerza {
    background: linear-gradient(135deg,#eff6ff,#dbeafe);
    border: 1.5px solid #93c5fd;
}
.result-card.atraccion {
    background: linear-gradient(135deg,#f0fdf4,#dcfce7);
    border: 1.5px solid #86efac;
}
.result-card.repulsion {
    background: linear-gradient(135deg,#fff7ed,#fee2e2);
    border: 1.5px solid #fca5a5;
}
.result-icon { font-size: 2.2rem; flex-shrink: 0; }
.result-label {
    font-size: 0.72rem; font-weight: 500;
    text-transform: uppercase; letter-spacing: 1px;
    color: #6b7280; margin-bottom: 3px;
    font-family: 'IBM Plex Sans', sans-serif;
}
.result-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.6rem; font-weight: 700;
    color: #1e3a8a; line-height: 1;
}
.result-value.green { color: #166534; }
.result-value.red   { color: #991b1b; }
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #c7d2fe 30%, #c7d2fe 70%, transparent);
    border: none; margin: 30px 0;
}
.formula-box {
    background: #f8faff; border: 1.5px solid #e0e7ff;
    border-radius: 14px; padding: 18px 24px;
    font-family: 'IBM Plex Sans', monospace;
    font-size: 0.88rem; color: #374151;
    margin-top: 12px; line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

# ─── Hero Banner ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
    {logo_html}
    <div>
        <div class="hero-title">Proyecto de Simulador<br>de Fuerza Eléctrica</div>
        <p class="hero-sub">Ley de Coulomb &nbsp;·&nbsp; Cálculo y visualización vectorial de fuerzas entre cargas</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Parámetros ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-badge">⚙️ &nbsp; Parámetros de entrada</div>', unsafe_allow_html=True)
st.markdown('<div class="param-card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    q1_micro = st.number_input("⊕  Carga 1 (µC)", value=5.0, step=0.5)
with col2:
    q2_micro = st.number_input("⊖  Carga 2 (µC)", value=-3.0, step=0.5)

r = st.number_input("📏  Distancia entre las cargas (metros)", min_value=0.01, value=2.0, step=0.1)
st.markdown('</div>', unsafe_allow_html=True)
calcular = st.button("⚡  Calcular y Visualizar")

# ─── Resultados ──────────────────────────────────────────────────────────────
if calcular:
    q1 = q1_micro * 1e-6
    q2 = q2_micro * 1e-6
    fuerza = K * abs(q1 * q2) / r ** 2

    if (q1 * q2) < 0:
        tipo = "Atracción"; mpl_color = "#059669"
        card_tipo = "atraccion"; icono_tipo = "🟢"; val_class = "green"; dir_vector = -1
    else:
        tipo = "Repulsión"; mpl_color = "#dc2626"
        card_tipo = "repulsion"; icono_tipo = "🔴"; val_class = "red"; dir_vector = 1

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-badge">📊 &nbsp; Resultados Analíticos</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="result-card fuerza">
            <div class="result-icon">🔬</div>
            <div>
                <div class="result-label">Magnitud de la Fuerza</div>
                <div class="result-value">{fuerza:.4f} N</div>
            </div>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="result-card {card_tipo}">
            <div class="result-icon">{icono_tipo}</div>
            <div>
                <div class="result-label">Tipo de Interacción</div>
                <div class="result-value {val_class}">{tipo}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-badge">🎨 &nbsp; Representación Vectorial</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(9, 3.4))
    fig.patch.set_facecolor('#f8faff')
    ax.set_facecolor('#f8faff')

    c_colors = ['#ef4444' if q1 > 0 else '#3b82f6',
                '#ef4444' if q2 > 0 else '#3b82f6']

    ax.plot([0, r], [0, 0], color='#94a3b8', linestyle='--', linewidth=1.5, alpha=0.6, zorder=1)
    ax.annotate('', xy=(r, -0.3), xytext=(0, -0.3),
                arrowprops=dict(arrowstyle='<->', color='#64748b', lw=1.3))
    ax.text(r/2, -0.42, f'd = {r} m', ha='center', fontsize=9,
            color='#64748b', style='italic', fontfamily='monospace')
    ax.scatter([0, r], [0, 0], s=1000, c=c_colors, edgecolors='white', linewidths=3, zorder=3)
    ax.text(0, 0, '+' if q1>0 else '−', ha='center', va='center',
            fontsize=14, fontweight='bold', color='white', zorder=4)
    ax.text(r, 0, '+' if q2>0 else '−', ha='center', va='center',
            fontsize=14, fontweight='bold', color='white', zorder=4)

    sign1 = '+' if q1_micro >= 0 else ''
    sign2 = '+' if q2_micro >= 0 else ''
    ax.text(0, 0.25, f'q₁ = {sign1}{q1_micro} µC', ha='center',
            fontsize=10, fontweight='bold', color=c_colors[0])
    ax.text(r, 0.25, f'q₂ = {sign2}{q2_micro} µC', ha='center',
            fontsize=10, fontweight='bold', color=c_colors[1])

    escala = r * 0.24
    ax.annotate('', xy=(-dir_vector*escala, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=mpl_color, lw=2.5, mutation_scale=20))
    ax.text(-dir_vector*(escala+0.08*r), -0.25,
            'F₁', ha='center', color=mpl_color, fontsize=11, fontweight='bold')
    ax.annotate('', xy=(r+dir_vector*escala, 0), xytext=(r, 0),
                arrowprops=dict(arrowstyle='->', color=mpl_color, lw=2.5, mutation_scale=20))
    ax.text(r+dir_vector*(escala+0.08*r), -0.25,
            'F₂', ha='center', color=mpl_color, fontsize=11, fontweight='bold')

    patches = [
        mpatches.Patch(color='#ef4444', label='Carga positiva (+)'),
        mpatches.Patch(color='#3b82f6', label='Carga negativa (−)'),
        mpatches.Patch(color=mpl_color, label=f'Fuerza de {tipo}'),
    ]
    ax.legend(handles=patches, loc='upper right', fontsize=8.5,
              framealpha=0.95, edgecolor='#e0e7ff', fancybox=True)

    ax.set_xlim(-r*0.55, r*1.6)
    ax.set_ylim(-0.6, 0.55)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    st.pyplot(fig)

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-badge">📐 &nbsp; Fórmula Aplicada</div>', unsafe_allow_html=True)
    st.latex(r"F = k_e \cdot \frac{|q_1 \cdot q_2|}{r^2}")
    st.markdown(f"""
    <div class="formula-box">
        <b>kₑ</b> = 8.99 × 10⁹ N·m²/C² &nbsp;&nbsp;|&nbsp;&nbsp;
        <b>q₁</b> = {q1_micro} µC &nbsp;&nbsp;|&nbsp;&nbsp;
        <b>q₂</b> = {q2_micro} µC &nbsp;&nbsp;|&nbsp;&nbsp;
        <b>r</b> = {r} m &nbsp;&nbsp;|&nbsp;&nbsp;
        <b>F</b> = {fuerza:.4f} N
    </div>
    """, unsafe_allow_html=True)