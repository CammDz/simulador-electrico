import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math
import base64
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ElectroSim · Coulomb Lab",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# DESIGN SYSTEM & CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:           #080c14;
  --surface-1:    #0d1220;
  --surface-2:    #111827;
  --surface-3:    #1a2236;
  --border:       rgba(255,255,255,0.07);
  --border-glow:  rgba(56,189,248,0.25);
  --text:         #e2e8f0;
  --text-muted:   #64748b;
  --text-faint:   #5b6e8a;
  --blue:         #38bdf8;
  --blue-dim:     rgba(56,189,248,0.12);
  --purple:       #a78bfa;
  --purple-dim:   rgba(167,139,250,0.10);
  --red:          #f87171;
  --green:        #34d399;
  --mono:         'JetBrains Mono', monospace;
  --sans:         'Inter', -apple-system, sans-serif;
  --radius-sm:    8px;
  --radius-md:    12px;
  --radius-lg:    18px;
  --radius-xl:    24px;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"] {
  background: var(--bg) !important;
  font-family: var(--sans) !important;
  color: var(--text) !important;
}

[data-testid="stDecoration"],
[data-testid="stHeader"],
footer { display: none !important; }

[data-testid="block-container"] {
  padding: 0 2rem 4rem !important;
  max-width: 1400px !important;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--surface-3); border-radius: 999px; }

/* ── HEADER ── */
.app-header {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 26px 32px;
  margin: 24px 0 28px;
  background: linear-gradient(135deg, rgba(56,189,248,0.05) 0%, rgba(167,139,250,0.03) 100%);
  border: 1px solid var(--border);
  border-top: 1px solid rgba(56,189,248,0.15);
  border-radius: var(--radius-xl);
  box-shadow: 0 1px 0 rgba(255,255,255,0.03) inset, 0 20px 60px rgba(0,0,0,0.45);
}

.app-header-logo {
  flex-shrink: 0;
  width: 64px; height: 64px;
  border-radius: var(--radius-md);
  border: 1px solid rgba(255,255,255,0.1);
  background: #ffffff;
  box-shadow: 0 0 0 1px rgba(255,255,255,0.06), 0 4px 16px rgba(0,0,0,0.3);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.8rem;
  overflow: hidden;
}

.app-header-logo img {
  width: 100%; height: 100%;
  object-fit: contain; padding: 6px;
  filter: drop-shadow(0 1px 2px rgba(0,0,0,0.1));
}

.app-title {
  font-size: 1.65rem;
  font-weight: 700;
  letter-spacing: -0.03em;
  background: linear-gradient(90deg, var(--blue) 0%, var(--purple) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.2;
}

.app-subtitle {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-top: 5px;
  font-weight: 400;
  letter-spacing: 0.02em;
}

.app-badges {
  margin-left: auto;
  display: flex; gap: 8px;
}

.badge {
  font-size: 0.71rem;
  font-weight: 600;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  color: var(--text-muted);
  background: var(--surface-2);
}

.badge.live {
  border-color: rgba(56,189,248,0.3);
  color: var(--blue);
  background: var(--blue-dim);
}

/* ── INFO ROW ── */
.info-row {
  display: flex; gap: 10px; flex-wrap: wrap;
  margin: 0 0 24px;
}

.info-chip {
  font-size: 0.74rem;
  font-weight: 500;
  color: #94a3b8;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 6px 14px;
  display: flex; align-items: center; gap: 6px;
}

.info-chip { color: var(--text-muted); }
.info-chip b { color: #e2e8f0; }

/* ── SECTION LABEL ── */
.section-label {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 28px 0 14px;
  font-size: 0.73rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.section-label::before {
  content: '';
  display: block;
  width: 3px; height: 13px;
  border-radius: 2px;
  background: linear-gradient(180deg, var(--blue), var(--purple));
}

.section-label::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}

/* ── FORMULA PILL ── */
.formula-pill {
  font-family: var(--mono);
  font-size: 0.78rem;
  color: #7dd3fc;
  background: var(--blue-dim);
  border: 1px solid rgba(56,189,248,0.25);
  border-radius: 999px;
  padding: 6px 14px;
  display: inline-block;
  margin-top: 28px;
}

/* ── CHARGE CARDS ── */
.charge-card {
  background: var(--surface-1);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 16px 18px 10px;
  margin-bottom: 12px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.charge-card:hover {
  border-color: rgba(255,255,255,0.11);
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

.charge-header {
  display: flex;
  align-items: center;
  gap: 9px;
  margin-bottom: 12px;
}

.charge-dot {
  width: 9px; height: 9px;
  border-radius: 50%;
  flex-shrink: 0;
}

.charge-name {
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.09em;
  text-transform: uppercase;
}

.charge-idx {
  margin-left: auto;
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--text-muted);
}

.input-row-labels {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
  margin-bottom: 3px;
}

.input-col-label {
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--text-muted);
  padding-left: 2px;
}

/* ── STREAMLIT INPUT OVERRIDES ── */
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {
  font-size: 0.68rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.09em !important;
  text-transform: uppercase !important;
  color: var(--text-faint) !important;
  font-family: var(--sans) !important;
}

div[data-testid="stNumberInput"] input {
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text) !important;
  font-family: var(--mono) !important;
  font-size: 0.88rem !important;
  font-weight: 500 !important;
  padding: 8px 10px !important;
  transition: border-color 0.15s, box-shadow 0.15s !important;
}

div[data-testid="stNumberInput"] input:focus {
  border-color: var(--border-glow) !important;
  box-shadow: 0 0 0 3px rgba(56,189,248,0.08) !important;
  outline: none !important;
}

div[data-testid="stNumberInput"] button {
  background: var(--surface-3) !important;
  border: 1px solid var(--border) !important;
  color: var(--text-muted) !important;
  border-radius: 6px !important;
}

div[data-testid="stNumberInput"] button:hover {
  background: var(--blue-dim) !important;
  border-color: var(--border-glow) !important;
  color: var(--blue) !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text) !important;
  font-family: var(--mono) !important;
  font-size: 0.88rem !important;
  min-height: 40px !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover {
  border-color: var(--border-glow) !important;
}

[data-baseweb="popover"] ul {
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  padding: 4px !important;
}

[data-baseweb="popover"] li {
  border-radius: var(--radius-sm) !important;
  font-family: var(--mono) !important;
  font-size: 0.85rem !important;
  color: var(--text) !important;
}

[data-baseweb="popover"] li:hover {
  background: var(--blue-dim) !important;
  color: var(--blue) !important;
}

/* ── BUTTON ── */
div[data-testid="stButton"] > button {
  width: 100% !important;
  padding: 14px 28px !important;
  font-family: var(--sans) !important;
  font-size: 0.85rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.07em !important;
  text-transform: uppercase !important;
  color: #fff !important;
  background: linear-gradient(135deg, #0ea5e9 0%, #7c3aed 100%) !important;
  border: none !important;
  border-radius: var(--radius-md) !important;
  cursor: pointer !important;
  box-shadow: 0 1px 0 rgba(255,255,255,0.12) inset,
              0 6px 20px rgba(14,165,233,0.18) !important;
  transition: transform 0.15s, box-shadow 0.15s !important;
}

div[data-testid="stButton"] > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 1px 0 rgba(255,255,255,0.15) inset,
              0 10px 30px rgba(14,165,233,0.32) !important;
}

div[data-testid="stButton"] > button:active {
  transform: translateY(0) !important;
  opacity: 0.9 !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface-1) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  padding: 4px !important;
  gap: 2px !important;
}

.stTabs [role="tablist"] button {
  background: transparent !important;
  border: none !important;
  border-radius: calc(var(--radius-md) - 4px) !important;
  color: var(--text-muted) !important;
  font-family: var(--sans) !important;
  font-size: 0.76rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.04em !important;
  padding: 8px 18px !important;
  transition: all 0.15s !important;
}

.stTabs [role="tablist"] button[aria-selected="true"] {
  background: var(--surface-3) !important;
  color: var(--text) !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.3) !important;
}

.stTabs [role="tablist"] button:hover {
  color: var(--text) !important;
  background: rgba(255,255,255,0.04) !important;
}

.stTabs [data-baseweb="tab-panel"] { padding-top: 20px !important; }

/* ── RESULT CARDS ── */
.result-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 12px;
}

.rcard {
  background: var(--surface-1);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 18px 20px;
  transition: border-color 0.2s;
}

.rcard:hover { border-color: rgba(255,255,255,0.1); }

.rcard.net-force {
  border-top: 2px solid var(--blue);
  background: linear-gradient(180deg, rgba(56,189,248,0.04) 0%, var(--surface-1) 100%);
}

.rcard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.rcard-title {
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.rcard-badge {
  font-size: 0.63rem;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 999px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.rcard-badge.attract {
  background: rgba(52,211,153,0.1);
  color: var(--green);
  border: 1px solid rgba(52,211,153,0.2);
}

.rcard-badge.repel {
  background: rgba(248,113,113,0.1);
  color: var(--red);
  border: 1px solid rgba(248,113,113,0.2);
}

.rcard-value {
  font-family: var(--mono);
  font-size: 1.45rem;
  font-weight: 600;
  color: var(--text);
  letter-spacing: -0.02em;
  margin-bottom: 12px;
}

.rcard-value span {
  font-size: 0.78rem;
  font-weight: 400;
  color: var(--text-muted);
  margin-left: 4px;
}

.rcard-meta { display: flex; flex-direction: column; gap: 5px; }

.rcard-row { display: flex; justify-content: space-between; font-size: 0.74rem; }
.rcard-row .lbl { color: var(--text-muted); }
.rcard-row .val { font-family: var(--mono); color: var(--text); font-weight: 500; }

/* ── CHART WRAPPER ── */
.chart-wrap {
  background: var(--surface-1);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 4px;
  overflow: hidden;
}

.chart-label {
  font-size: 0.67rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
  padding: 12px 16px 4px;
}

/* ── ERROR ── */
div[data-testid="stAlert"] {
  background: rgba(248,113,113,0.06) !important;
  border: 1px solid rgba(248,113,113,0.22) !important;
  border-radius: var(--radius-md) !important;
  color: var(--red) !important;
  font-size: 0.84rem !important;
}

/* ── FOOTER ── */
.app-footer {
  text-align: center;
  padding: 28px 0 6px;
  font-size: 0.7rem;
  color: var(--text-faint);
  letter-spacing: 0.04em;
  border-top: 1px solid var(--border);
  margin-top: 48px;
}

/* ── RESPONSIVE ── */
@media (max-width: 900px) {
  [data-testid="block-container"] { padding: 0 1rem 3rem !important; }
  .app-header { flex-wrap: wrap; padding: 20px 18px; gap: 14px; }
  .app-title { font-size: 1.25rem; }
  .app-badges { margin-left: 0; }
  .app-header-logo { width: 52px; height: 52px; }
}

@media (max-width: 640px) {
  .app-header { flex-direction: column; text-align: center; padding: 16px 14px; }
  .app-title { font-size: 1.05rem; }
  .app-subtitle { font-size: 0.7rem; }
  .app-header-logo { width: 48px; height: 48px; }
  .info-row { gap: 6px; }
  .info-chip { font-size: 0.65rem; padding: 4px 10px; }
  .section-label { font-size: 0.65rem; margin: 20px 0 10px; }
  .charge-card { padding: 12px 14px 8px; }
  .result-grid { grid-template-columns: 1fr; }
  .stTabs [role="tablist"] button { font-size: 0.65rem !important; padding: 6px 10px !important; }
  .rcard-value { font-size: 1.15rem; }
}

@media (max-width: 480px) {
  [data-testid="block-container"] { padding: 0 0.5rem 2rem !important; }
  .app-title { font-size: 0.9rem; }
  .app-subtitle { font-size: 0.62rem; }
  .section-label { font-size: 0.6rem; }
  .input-col-label { font-size: 0.62rem; }
  .rcard { padding: 14px 14px; }
  .rcard-value { font-size: 1rem; }
  .rcard-meta { gap: 3px; }
  .rcard-row { font-size: 0.65rem; }
}
</style>
""", unsafe_allow_html=True)

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
logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="logo">' if logo_base64 else "⚡"

st.markdown(f"""
<div class="app-header">
  <div class="app-header-logo">{logo_html}</div>
  <div>
    <div class="app-title">ElectroSim · Coulomb Lab</div>
    <div class="app-subtitle">Simulación interactiva · Ley de Coulomb · Análisis vectorial 2D</div>
  </div>
  <div class="app-badges">
    <span class="badge live">Live</span>
    <span class="badge">v2.0</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
K = 8.99e9
st.markdown("""
<div class="info-row">
  <span class="info-chip"><b>Ke</b> = 8.99 × 10⁹ N·m²/C²</span>
  <span class="info-chip"><b>F</b> = Ke · |q₁ · q₂| / r²</span>
  <span class="info-chip">Coordenadas en <b>metros</b> · Cargas en <b>µC</b></span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHARGE SELECTOR
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">Configuración del sistema</div>', unsafe_allow_html=True)

col_sel, col_pill, _ = st.columns([0.18, 0.38, 0.44], gap="medium")
with col_sel:
    num_cargas = st.selectbox("Número de cargas", [2, 3, 4, 5, 6], index=0)
with col_pill:
    st.markdown(f'<span class="formula-pill">F = Ke·|q₁q₂|/r²&nbsp; · &nbsp;{num_cargas} cargas activas</span>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PALETTE
# ─────────────────────────────────────────────
COLORS = ['#38bdf8', '#a78bfa', '#f87171', '#fbbf24', '#34d399', '#f472b6']
NAMES  = ['Cian',   'Violeta', 'Rojo',    'Ámbar',   'Esmeralda','Rosa']
Q_DEF  = [5.0, -3.0, 2.5, -4.0, 3.5, -2.0]
X_DEF  = [0.0,  3.0, 1.5,  4.0, 2.0,  5.0]
Y_DEF  = [0.0,  0.0, 2.5,  1.5,-2.0,  3.0]

# ─────────────────────────────────────────────
# CHARGE INPUTS
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">Parámetros de cargas</div>', unsafe_allow_html=True)

cargas = []
col_a, col_b = st.columns(2, gap="medium")

for i in range(num_cargas):
    target = col_a if i % 2 == 0 else col_b
    with target:
        c = COLORS[i]
        st.markdown(f"""
        <div class="charge-card">
          <div class="charge-header">
            <span class="charge-dot" style="background:{c}; box-shadow:0 0 6px {c}66;"></span>
            <span class="charge-name" style="color:{c};">{NAMES[i]}</span>
            <span class="charge-idx">Q{i+1}</span>
          </div>
          <div class="input-row-labels">
            <span class="input-col-label">Carga (µC)</span>
            <span class="input-col-label">X (m)</span>
            <span class="input-col-label">Y (m)</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3, gap="small")
        with c1:
            q = st.number_input("q", value=float(Q_DEF[i]), step=0.1, key=f"q{i}", label_visibility="collapsed")
        with c2:
            x = st.number_input("x", value=float(X_DEF[i]), step=0.1, key=f"x{i}", label_visibility="collapsed")
        with c3:
            y = st.number_input("y", value=float(Y_DEF[i]), step=0.1, key=f"y{i}", label_visibility="collapsed")
        cargas.append({'q': q, 'x': x, 'y': y, 'indice': i+1, 'color': c})

# ─────────────────────────────────────────────
# BUTTON
# ─────────────────────────────────────────────
st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
_, btn_col, _ = st.columns([0.25, 0.5, 0.25])
with btn_col:
    calcular = st.button("⚡  Calcular simulación", use_container_width=True)

# ─────────────────────────────────────────────
# PHYSICS ENGINE (lógica matemática sin cambios)
# ─────────────────────────────────────────────
cargas_coulombs = [{'q': c['q'] * 1e-6, 'x': c['x'], 'y': c['y'],
                    'indice': c['indice'], 'color': c['color']} for c in cargas]

if calcular:
    # Validación
    posiciones = [(c['x'], c['y']) for c in cargas]
    if len(posiciones) != len(set(posiciones)):
        st.error("Error: Dos o más cargas ocupan la misma posición.")
        st.stop()

    # Pares
    pares_info = []
    for i in range(len(cargas_coulombs)):
        for j in range(i + 1, len(cargas_coulombs)):
            c1, c2 = cargas_coulombs[i], cargas_coulombs[j]
            dx = c2['x'] - c1['x']
            dy = c2['y'] - c1['y']
            r = math.sqrt(dx**2 + dy**2)
            if r < 0.01:
                st.error(f"Error: Cargas {c1['indice']} y {c2['indice']} están demasiado cerca.")
                st.stop()
            theta_rad = math.atan2(dy, dx)
            theta_deg = math.degrees(theta_rad)
            F = K * abs(c1['q'] * c2['q']) / (r**2)
            Fx = F * math.cos(theta_rad)
            Fy = F * math.sin(theta_rad)
            tipo = "Atracción" if (c1['q'] * c2['q']) < 0 else "Repulsión"
            pares_info.append({
                'i': c1['indice'], 'j': c2['indice'],
                'q1': cargas[i]['q'], 'q2': cargas[j]['q'],
                'r': r, 'theta': theta_deg, 'F': F, 'Fx': Fx, 'Fy': Fy,
                'tipo': tipo, 'atraccion': (c1['q'] * c2['q']) < 0
            })

    # Fuerzas netas
    fuerzas_netas = []
    for i in range(len(cargas_coulombs)):
        Fx_neto = Fy_neto = 0.0
        for j in range(len(cargas_coulombs)):
            if i == j: continue
            co, cd = cargas_coulombs[i], cargas_coulombs[j]
            dx = cd['x'] - co['x']
            dy = cd['y'] - co['y']
            r = math.sqrt(dx**2 + dy**2)
            theta_rad = math.atan2(dy, dx)
            F = K * abs(co['q'] * cd['q']) / (r**2)
            if (co['q'] * cd['q']) < 0:
                Fx, Fy = F * math.cos(theta_rad), F * math.sin(theta_rad)
            else:
                Fx, Fy = -F * math.cos(theta_rad), -F * math.sin(theta_rad)
            Fx_neto += Fx
            Fy_neto += Fy
        F_neto = math.sqrt(Fx_neto**2 + Fy_neto**2)
        theta_neto = math.degrees(math.atan2(Fy_neto, Fx_neto))
        fuerzas_netas.append({
            'indice': i+1, 'Fx': Fx_neto, 'Fy': Fy_neto,
            'F': F_neto, 'theta': theta_neto, 'color': cargas[i]['color']
        })

    # ─────────────────────────────────────────
    # RESULTS
    # ─────────────────────────────────────────
    st.markdown('<div class="section-label">Análisis de resultados</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Fuerzas entre pares", "Fuerza neta por carga", "Visualización 2D"])

    with tab1:
        html = '<div class="result-grid">'
        for par in pares_info:
            bc = "attract" if par['atraccion'] else "repel"
            bt = "Atracción" if par['atraccion'] else "Repulsión"
            html += f"""
            <div class="rcard">
              <div class="rcard-header">
                <span class="rcard-title">Q{par['i']} ↔ Q{par['j']}</span>
                <span class="rcard-badge {bc}">{bt}</span>
              </div>
              <div class="rcard-value">{par['F']:.4f}<span>N</span></div>
              <div class="rcard-meta">
                <div class="rcard-row"><span class="lbl">q₁</span><span class="val">{par['q1']:+.2f} µC</span></div>
                <div class="rcard-row"><span class="lbl">q₂</span><span class="val">{par['q2']:+.2f} µC</span></div>
                <div class="rcard-row"><span class="lbl">r</span><span class="val">{par['r']:.4f} m</span></div>
                <div class="rcard-row"><span class="lbl">θ</span><span class="val">{par['theta']:.2f}°</span></div>
                <div class="rcard-row"><span class="lbl">Fx</span><span class="val">{par['Fx']:+.4f} N</span></div>
                <div class="rcard-row"><span class="lbl">Fy</span><span class="val">{par['Fy']:+.4f} N</span></div>
              </div>
            </div>"""
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    with tab2:
        html = '<div class="result-grid">'
        for fn in fuerzas_netas:
            html += f"""
            <div class="rcard net-force">
              <div class="rcard-header">
                <span class="rcard-title" style="color:{fn['color']}99;">Q{fn['indice']}</span>
                <span class="rcard-badge attract">Neta</span>
              </div>
              <div class="rcard-value">{fn['F']:.4f}<span>N</span></div>
              <div class="rcard-meta">
                <div class="rcard-row"><span class="lbl">Fx neto</span><span class="val">{fn['Fx']:+.4f} N</span></div>
                <div class="rcard-row"><span class="lbl">Fy neto</span><span class="val">{fn['Fy']:+.4f} N</span></div>
                <div class="rcard-row"><span class="lbl">θ resultante</span><span class="val">{fn['theta']:.2f}°</span></div>
              </div>
            </div>"""
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    with tab3:
        col_g1, col_g2 = st.columns(2, gap="medium")

        # Gráfica 1: Sistema de cargas
        with col_g1:
            st.markdown('<div class="chart-wrap"><div class="chart-label">Sistema de cargas · Vectores de fuerza neta</div>', unsafe_allow_html=True)
            fig1, ax1 = plt.subplots(figsize=(7, 7))
            fig1.patch.set_facecolor('#080c14')
            ax1.set_facecolor('#0d1220')

            xs = [c['x'] for c in cargas_coulombs]
            ys = [c['y'] for c in cargas_coulombs]
            margin = 2.5
            xc = (min(xs) + max(xs)) / 2
            yc = (min(ys) + max(ys)) / 2
            half = max(max(xs)-min(xs), max(ys)-min(ys)) / 2 + margin
            ax1.set_xlim(xc - half, xc + half)
            ax1.set_ylim(yc - half, yc + half)
            ax1.set_aspect('equal')

            ax1.grid(True, color='#1a2236', linewidth=0.5, alpha=0.5)
            ax1.axhline(0, color='#1e3a5f', linewidth=0.8, alpha=0.6)
            ax1.axvline(0, color='#1e3a5f', linewidth=0.8, alpha=0.6)

            for p in pares_info:
                ci = cargas_coulombs[p['i']-1]
                cj = cargas_coulombs[p['j']-1]
                ls = '--' if p['atraccion'] else ':'
                ax1.plot([ci['x'], cj['x']], [ci['y'], cj['y']],
                         color='#1e3a5f', linewidth=0.7, linestyle=ls, alpha=0.35, zorder=1)

            for c, fn in zip(cargas_coulombs, fuerzas_netas):
                col = fn['color']
                ax1.scatter(c['x'], c['y'], s=210, color=col, zorder=4,
                            edgecolors='white', linewidths=1.5, alpha=0.95)
                signo = '+' if c['q'] > 0 else '−'
                ax1.text(c['x'], c['y'], signo, ha='center', va='center',
                         color='white', fontsize=12, fontweight='bold', zorder=5)
                ax1.text(c['x'], c['y'] - half * 0.12,
                         f"Q{c['indice']}  {cargas[c['indice']-1]['q']:.1f}µC",
                         ha='center', va='top', fontsize=7.5, color='#94a3b8',
                         fontfamily='monospace',
                         bbox=dict(boxstyle='round,pad=0.2', facecolor='#080c14',
                                   edgecolor=col+'44', linewidth=0.8), zorder=5)
                if fn['F'] > 1e-6:
                    scale = half * 0.3
                    fx_v = (fn['Fx'] / fn['F']) * scale
                    fy_v = (fn['Fy'] / fn['F']) * scale
                    ax1.annotate('', xy=(c['x']+fx_v, c['y']+fy_v),
                                 xytext=(c['x'], c['y']),
                                 arrowprops=dict(arrowstyle='->', color=col, lw=2.5, mutation_scale=15),
                                 zorder=3)
            ax1.set_xlabel('X (m)', fontsize=8.5, color='#64748b', fontfamily='monospace')

            ax1.set_ylabel('Y (m)', fontsize=8.5, color='#64748b', fontfamily='monospace')
            ax1.tick_params(colors='#64748b', labelsize=8)
            ax1.spines[:].set_color('#1a2236')
            plt.tight_layout(pad=1.2)
            st.pyplot(fig1, use_container_width=True)
            plt.close(fig1)
            st.markdown('</div>', unsafe_allow_html=True)

        # Gráfica 2: Descomposición vectorial
        with col_g2:
            st.markdown('<div class="chart-wrap"><div class="chart-label">Descomposición vectorial · Primer par</div>', unsafe_allow_html=True)
            if pares_info:
                fig2, ax2 = plt.subplots(figsize=(7, 7))
                fig2.patch.set_facecolor('#080c14')
                ax2.set_facecolor('#0d1220')

                par = pares_info[0]
                F, Fx, Fy = par['F'], par['Fx'], par['Fy']
                theta_rad = math.radians(par['theta'])
                max_c = max(abs(Fx), abs(Fy), F, 0.01)
                norm = 3.5 / max_c
                fx_n, fy_n = Fx * norm, Fy * norm
                f_nx = F * norm * math.cos(theta_rad)
                f_ny = F * norm * math.sin(theta_rad)

                ax2.set_xlim(-0.8, 5.0)
                ax2.set_ylim(-0.8, 5.0)
                ax2.set_aspect('equal')
                ax2.grid(True, color='#1a2236', linewidth=0.5, alpha=0.5)

                for ox, oy, ddx, ddy in [(0,0,4.5,0),(0,0,0,4.5)]:
                    ax2.annotate('', xy=(ox+ddx, oy+ddy), xytext=(ox,oy),
                                 arrowprops=dict(arrowstyle='->', color='#1e3a5f', lw=1.5))
                ax2.text(4.7, -0.18, 'X', fontsize=9, color='#64748b', fontfamily='monospace', fontweight='bold')
                ax2.text(-0.18, 4.7, 'Y', fontsize=9, color='#64748b', fontfamily='monospace', fontweight='bold')

                ax2.plot([fx_n, fx_n], [0, fy_n], color='#475569', linewidth=0.9, linestyle='--', alpha=0.5)
                ax2.plot([0, fx_n], [fy_n, fy_n], color='#475569', linewidth=0.9, linestyle='--', alpha=0.5)

                ax2.annotate('', xy=(fx_n, 0), xytext=(0,0),
                             arrowprops=dict(arrowstyle='->', color='#38bdf8', lw=2.5, mutation_scale=14))
                ax2.annotate('', xy=(fx_n, fy_n), xytext=(fx_n, 0),
                             arrowprops=dict(arrowstyle='->', color='#f97316', lw=2.5, mutation_scale=14))
                ax2.annotate('', xy=(f_nx, f_ny), xytext=(0,0),
                             arrowprops=dict(arrowstyle='->', color='#a78bfa', lw=3, mutation_scale=16))

                if abs(theta_rad) > 0.01:
                    arc = np.linspace(0, theta_rad, 60)
                    ax2.plot(0.65*np.cos(arc), 0.65*np.sin(arc), color='#f87171', linewidth=2, alpha=0.8)
                    mid = theta_rad / 2
                    ax2.text(0.92*math.cos(mid), 0.92*math.sin(mid),
                             f'{par["theta"]:.1f}°', fontsize=8, color='#f87171',
                             fontfamily='monospace', ha='center', va='center')

                ax2.text(fx_n/2, -0.38, f'Fx = {Fx:+.3f} N', ha='center', fontsize=8,
                         color='#38bdf8', fontfamily='monospace',
                         bbox=dict(boxstyle='round,pad=0.3', facecolor='#080c14', edgecolor='#38bdf830', linewidth=1))
                ax2.text(fx_n+0.28, fy_n/2, f'Fy = {Fy:+.3f} N', ha='left', fontsize=8,
                         color='#f97316', fontfamily='monospace',
                         bbox=dict(boxstyle='round,pad=0.3', facecolor='#080c14', edgecolor='#f9731630', linewidth=1))
                ax2.text(f_nx*0.5-0.3, f_ny*0.5+0.22, f'|F| = {F:.3f} N', ha='center', fontsize=8,
                         color='#a78bfa', fontfamily='monospace',
                         bbox=dict(boxstyle='round,pad=0.3', facecolor='#080c14', edgecolor='#a78bfa30', linewidth=1))

                legend_items = [
                    mpatches.Patch(color='#a78bfa', label=f'Q{par["i"]}↔Q{par["j"]}  |F|={F:.4f}N'),
                    mpatches.Patch(color='#38bdf8', label=f'Fx = {Fx:+.4f} N'),
                    mpatches.Patch(color='#f97316', label=f'Fy = {Fy:+.4f} N'),
                ]
                leg = ax2.legend(handles=legend_items, loc='lower right', fontsize=7.5,
                                 framealpha=0.85, facecolor='#0d1220', edgecolor='#1a2236',
                                 labelcolor='#94a3b8')
                leg.get_frame().set_linewidth(0.8)

                ax2.tick_params(colors='#64748b', labelsize=8)
                ax2.spines[:].set_color('#1a2236')
                plt.tight_layout(pad=1.2)
                st.pyplot(fig2, use_container_width=True)
                plt.close(fig2)
            st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
  Proyecto de Cargas de Coulomb · Electromagnetismo &nbsp;·&nbsp; UTS
</div>
""", unsafe_allow_html=True)
