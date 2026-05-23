import streamlit as st
import base64
import os

from ui.styles import get_css
from ui.components import (
    render_header,
    render_info_row,
    render_section_label,
    render_charge_card_html,
    render_rcard_pair,
    render_rcard_net,
    render_footer,
)
from ui.charts import (
    plot_sistema_cargas,
    plot_descomposicion_vectorial,
    render_system_vector_summary,
    render_decomposition_panel,
)
from physics.coulomb import K, calcular_pares, calcular_fuerzas_netas
from physics.analysis import analisis_par_html, analisis_neta_html, analisis_sistema_html, conclusiones_html
from utils.helpers import precompute_stats

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Simulador de Cargas Eléctricas",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown(get_css(), unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOGO
# ─────────────────────────────────────────────
logo_base64 = None
if os.path.exists("logo.png"):
    with open("logo.png", "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
render_header(logo_base64)

# ─────────────────────────────────────────────
# CONSTANTS & INFO
# ─────────────────────────────────────────────
render_info_row()

# ─────────────────────────────────────────────
# CHARGE SELECTOR
# ─────────────────────────────────────────────
render_section_label("Configuración del sistema")

col_sel, col_pill, _ = st.columns([0.18, 0.38, 0.44], gap="medium")
with col_sel:
    num_cargas = st.selectbox("Número de cargas", [2, 3, 4, 5, 6], index=0)
with col_pill:
    st.markdown(
        f'<span class="formula-pill">F = Ke·|q₁q₂|/r²&nbsp; · &nbsp;{num_cargas} cargas activas</span>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# PALETTE & DEFAULTS
# ─────────────────────────────────────────────
COLORS = ['#38bdf8', '#a78bfa', '#f87171', '#fbbf24', '#34d399', '#f472b6']
NAMES = ['Cian', 'Violeta', 'Rojo', 'Ámbar', 'Esmeralda', 'Rosa']
Q_DEF = [5.0, -3.0, 2.5, -4.0, 3.5, -2.0]
X_DEF = [0.0, 3.0, 1.5, 4.0, 2.0, 5.0]
Y_DEF = [0.0, 0.0, 2.5, 1.5, -2.0, 3.0]

# ─────────────────────────────────────────────
# CHARGE INPUTS
# ─────────────────────────────────────────────
render_section_label("Parámetros de cargas")

cargas = []
col_a, col_b = st.columns(2, gap="medium")

for i in range(num_cargas):
    target = col_a if i % 2 == 0 else col_b
    with target:
        c = COLORS[i]
        signo = '+' if Q_DEF[i] > 0 else '−'
        st.markdown(render_charge_card_html(i, c, signo), unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3, gap="small")
        with c1:
            q = st.number_input("q", value=float(Q_DEF[i]), step=0.1, key=f"q{i}", label_visibility="collapsed")
        with c2:
            x = st.number_input("x", value=float(X_DEF[i]), step=0.1, key=f"x{i}", label_visibility="collapsed")
        with c3:
            y = st.number_input("y", value=float(Y_DEF[i]), step=0.1, key=f"y{i}", label_visibility="collapsed")
        cargas.append({'q': q, 'x': x, 'y': y, 'indice': i + 1, 'color': c})

# ─────────────────────────────────────────────
# BUTTON
# ─────────────────────────────────────────────
st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
_, btn_col, _ = st.columns([0.25, 0.5, 0.25])
with btn_col:
    calcular = st.button("⚡  Calcular simulación", use_container_width=True)

# ─────────────────────────────────────────────
# PHYSICS ENGINE
# ─────────────────────────────────────────────
cargas_coulombs = [
    {'q': c['q'] * 1e-6, 'x': c['x'], 'y': c['y'],
     'indice': c['indice'], 'color': c['color']}
    for c in cargas
]

if calcular:
    # Calcular pares y fuerzas netas (con validación incluida)
    try:
        pares_info = calcular_pares(cargas, cargas_coulombs)
        fuerzas_netas = calcular_fuerzas_netas(cargas_coulombs)
    except ValueError as e:
        st.error(str(e))
        st.stop()

    # Precalcular estadísticas globales (una sola vez)
    stats = precompute_stats(cargas, pares_info, fuerzas_netas)

    # ─────────────────────────────────────────
    # RESULTS
    # ─────────────────────────────────────────
    render_section_label("Análisis de resultados")
    tab1, tab2, tab3, tab4 = st.tabs([
        "Fuerzas entre pares",
        "Fuerza neta por carga",
        "Visualización 2D",
        "Análisis e interpretación",
    ])

    with tab1:
        html = '<div class="result-grid">'
        for par in pares_info:
            html += render_rcard_pair(par)
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    with tab2:
        html = '<div class="result-grid">'
        for fn in fuerzas_netas:
            html += render_rcard_net(fn)
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    with tab3:
        col_g1, col_g2 = st.columns(2, gap="medium")

        # Gráfica 1: Sistema de cargas
        with col_g1:
            st.markdown(
                '<div class="chart-wrap"><div class="chart-label">Sistema de cargas · Vectores de fuerza neta</div>',
                unsafe_allow_html=True,
            )
            plot_sistema_cargas(cargas_coulombs, pares_info, fuerzas_netas, cargas)
            st.markdown('</div>', unsafe_allow_html=True)

            # Panel de resumen vectorial del sistema
            neta_sum = max(fuerzas_netas, key=lambda x: x['F']) if fuerzas_netas else None
            render_system_vector_summary(neta_sum)

        # Gráfica 2: Descomposición vectorial
        with col_g2:
            st.markdown(
                '<div class="chart-wrap"><div class="chart-label">Descomposición vectorial · Primer par de cargas</div>',
                unsafe_allow_html=True,
            )
            if pares_info:
                par = pares_info[0]
                plot_descomposicion_vectorial(par)
                F, Fx, Fy, theta_deg = par['F'], par['Fx'], par['Fy'], par['theta']
                render_decomposition_panel(par, F, Fx, Fy, theta_deg)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        html = '<div style="display:flex;flex-direction:column;gap:4px;">'

        # 1. Resumen del sistema
        html += '<div class="analysis-card">'
        html += '<div class="analysis-card-title">📋 Resumen del sistema</div>'
        html += analisis_sistema_html(stats)
        html += '</div>'

        # 2. Análisis por pares
        html += '<div class="analysis-card">'
        html += '<div class="analysis-card-title">⚡ Análisis detallado por par</div>'
        for par in pares_info:
            c1 = cargas[par['i'] - 1]
            c2 = cargas[par['j'] - 1]
            html += (
                '<p style="margin-top:10px;font-size:0.78rem;font-weight:600;'
                'color:var(--text-muted);letter-spacing:0.05em;text-transform:uppercase;">'
                f'Par {par["i"]}–{par["j"]}</p>'
            )
            html += analisis_par_html(par, c1, c2)
        html += '</div>'

        # 3. Análisis de fuerza neta
        html += '<div class="analysis-card">'
        html += '<div class="analysis-card-title">🧭 Análisis de fuerza neta por carga</div>'
        for fn in fuerzas_netas:
            c = cargas[fn['indice'] - 1]
            html += (
                '<p style="margin-top:10px;font-size:0.78rem;font-weight:600;'
                'color:var(--text-muted);letter-spacing:0.05em;text-transform:uppercase;">'
                f'Carga {fn["indice"]}</p>'
            )
            html += analisis_neta_html(fn, c, pares_info)
        html += '</div>'

        # 4. Conclusiones
        html += '<div class="analysis-conclusion">'
        html += '<div class="analysis-conclusion-title">📐 Interpretación física del sistema</div>'
        html += conclusiones_html(stats, pares_info)
        html += '</div>'

        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
render_footer()
