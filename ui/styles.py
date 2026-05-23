def get_css():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:           #f8fafc;
  --surface-1:    #ffffff;
  --surface-2:    #f1f5f9;
  --surface-3:    #e2e8f0;
  --border:       rgba(0,0,0,0.07);
  --border-glow:  rgba(2,132,199,0.18);
  --text:         #0f172a;
  --text-muted:   #64748b;
  --text-faint:   #94a3b8;
  --blue:         #0284c7;
  --blue-dim:     rgba(2,132,199,0.07);
  --purple:       #7c3aed;
  --purple-dim:   rgba(124,58,237,0.07);
  --red:          #dc2626;
  --green:        #059669;
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
footer,
header { display: none !important; }

[data-testid="stAppViewContainer"] { padding-top: 0 !important; }
[data-testid="stAppViewContainer"] > .main { padding-top: 0 !important; }

[data-testid="block-container"] {
  padding: 0.5rem 2rem 3rem !important;
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
  padding: 18px 28px;
  margin: 8px 0 20px;
  background: var(--surface-1);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.04);
}

.app-header-logo {
  flex-shrink: 0;
  width: 52px; height: 52px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  background: var(--surface-1);
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
}

.app-header-logo img {
  width: 100%; height: 100%;
  object-fit: contain; padding: 4px;
}

.app-header-text { flex: 1; min-width: 0; }

.app-title {
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text);
  line-height: 1.3;
}

.app-title .accent {
  background: linear-gradient(135deg, #0284c7, #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.app-subtitle {
  font-size: 0.74rem;
  color: var(--text-muted);
  margin-top: 2px;
  font-weight: 400;
  letter-spacing: 0.01em;
}

.app-badges { margin-left: auto; display: flex; gap: 8px; }

.badge {
  font-size: 0.69rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  color: var(--text-muted);
  background: var(--surface-2);
}

.badge.live {
  border-color: rgba(2,132,199,0.22);
  color: var(--blue);
  background: var(--blue-dim);
}

/* ── INFO ROW ── */
.info-row {
  display: flex; gap: 10px; flex-wrap: wrap;
  margin: 0 0 20px;
}

.info-chip {
  font-size: 0.74rem;
  font-weight: 500;
  color: var(--text-muted);
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 6px 14px;
  display: flex; align-items: center; gap: 6px;
}

.info-chip b { color: var(--text); }

/* ── SECTION LABEL ── */
.section-label {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 26px 0 14px;
  font-size: 0.73rem;
  font-weight: 600;
  letter-spacing: 0.1em;
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
  font-size: 0.77rem;
  color: var(--blue);
  background: var(--blue-dim);
  border: 1px solid rgba(2,132,199,0.18);
  border-radius: 999px;
  padding: 5px 14px;
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
  border-color: rgba(0,0,0,0.11);
  box-shadow: 0 4px 16px rgba(0,0,0,0.04);
}

.charge-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

.charge-dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 0 0 2px rgba(0,0,0,0.04);
}

.charge-name { font-size: 0.82rem; font-weight: 600; letter-spacing: 0.01em; }

.charge-idx {
  margin-left: auto;
  font-family: var(--mono);
  font-size: 0.7rem;
  font-weight: 500;
  color: var(--text-muted);
  background: var(--surface-2);
  padding: 2px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
}

.input-row-labels {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
  margin-bottom: 4px;
}

.input-col-label {
  font-size: 0.67rem;
  font-weight: 600;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--text-faint);
  padding-left: 2px;
}

/* ── STREAMLIT INPUT OVERRIDES ── */
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {
  display: none !important;
}

div[data-testid="stNumberInput"] input {
  background: #ffffff !important;
  border: 1px solid #d1d5db !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text) !important;
  font-family: var(--mono) !important;
  font-size: 0.88rem !important;
  font-weight: 500 !important;
  padding: 7px 10px !important;
  transition: border-color 0.15s, box-shadow 0.15s !important;
  box-shadow: 0 1px 2px rgba(0,0,0,0.03) !important;
}

div[data-testid="stNumberInput"] input:focus {
  border-color: #2563eb !important;
  box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
  outline: none !important;
}

div[data-testid="stNumberInput"] button {
  background: #f9fafb !important;
  border: 1px solid #d1d5db !important;
  color: #6b7280 !important;
  border-radius: 4px !important;
  font-size: 0.7rem !important;
  transition: background 0.15s, color 0.15s !important;
}

div[data-testid="stNumberInput"] button:hover {
  background: #eff6ff !important;
  border-color: #2563eb !important;
  color: #2563eb !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
  background: #ffffff !important;
  border: 1px solid #d1d5db !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text) !important;
  font-family: var(--mono) !important;
  font-size: 0.88rem !important;
  min-height: 38px !important;
  box-shadow: 0 1px 2px rgba(0,0,0,0.03) !important;
  transition: border-color 0.15s, box-shadow 0.15s !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover {
  border-color: #2563eb !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
  border-color: #2563eb !important;
  box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] svg,
div[data-testid="stSelectbox"] div[data-baseweb="select"] span[aria-hidden="true"] svg {
  fill: #6b7280 !important;
  color: #6b7280 !important;
  opacity: 1 !important;
  width: 14px !important;
  height: 14px !important;
}

[data-baseweb="popover"] ul {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: var(--radius-md) !important;
  padding: 4px !important;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
}

[data-baseweb="popover"] li {
  border-radius: var(--radius-sm) !important;
  font-family: var(--mono) !important;
  font-size: 0.85rem !important;
  color: var(--text) !important;
  padding: 6px 12px !important;
}

[data-baseweb="popover"] li:hover {
  background: #eff6ff !important;
  color: #2563eb !important;
}

/* ── BUTTON ── */
div[data-testid="stButton"] > button {
  width: 100% !important;
  padding: 12px 28px !important;
  font-family: var(--sans) !important;
  font-size: 0.88rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.05em !important;
  color: #ffffff !important;
  background: #2563eb !important;
  border: none !important;
  border-radius: var(--radius-md) !important;
  cursor: pointer !important;
  box-shadow: 0 4px 14px rgba(37,99,235,0.25) !important;
  transition: background 0.2s, box-shadow 0.2s, transform 0.15s !important;
}

div[data-testid="stButton"] > button:hover {
  background: #1d4ed8 !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px rgba(37,99,235,0.35) !important;
}

div[data-testid="stButton"] > button:active {
  background: #1e40af !important;
  transform: translateY(0) !important;
  box-shadow: 0 2px 8px rgba(37,99,235,0.2) !important;
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
  background: var(--surface-2) !important;
  color: var(--text) !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
}

.stTabs [role="tablist"] button:hover {
  color: var(--text) !important;
  background: rgba(0,0,0,0.03) !important;
}

.stTabs [data-baseweb="tab-panel"] { padding-top: 20px !important; }

/* ── RESULT CARDS ── */
.result-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 14px;
}

.rcard {
  background: var(--surface-1);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 18px 20px 14px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.rcard:hover {
  border-color: rgba(0,0,0,0.1);
  box-shadow: 0 4px 16px rgba(0,0,0,0.04);
}

.rcard.net-force { border-left: 3px solid var(--blue); }

.rcard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.rcard-title {
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.rcard-badge {
  font-size: 0.62rem;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 999px;
  letter-spacing: 0.05em;
}

.rcard-badge.attract {
  background: rgba(5,150,105,0.08);
  color: var(--green);
  border: 1px solid rgba(5,150,105,0.18);
}

.rcard-badge.repel {
  background: rgba(220,38,38,0.08);
  color: var(--red);
  border: 1px solid rgba(220,38,38,0.18);
}

.rcard-badge.net {
  background: rgba(2,132,199,0.08);
  color: var(--blue);
  border: 1px solid rgba(2,132,199,0.18);
}

.rcard-value {
  font-family: var(--mono);
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text);
  letter-spacing: -0.02em;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border);
}

.rcard-value span {
  font-size: 0.78rem;
  font-weight: 400;
  color: var(--text-muted);
  margin-left: 4px;
}

.rcard-meta { display: flex; flex-direction: column; gap: 4px; }

.rcard-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.74rem;
  padding: 2px 0;
}

.rcard-row + .rcard-row { border-top: 1px solid var(--border); }

.rcard-row .lbl { color: var(--text-muted); }
.rcard-row .val { font-family: var(--mono); color: var(--text); font-weight: 500; }
.rcard-row .val.pos { color: #059669; }
.rcard-row .val.neg { color: #dc2626; }

.rcard-interp {
  font-size: 0.72rem;
  line-height: 1.5;
  color: var(--text-muted);
  padding: 8px 0 2px;
  border-top: 1px solid var(--border);
  margin-top: 8px;
}

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
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--text-muted);
  padding: 10px 14px 2px;
}

/* ── ANALYSIS CARDS ── */
.analysis-card {
  background: var(--surface-1);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 18px 22px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}

.analysis-card-title {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--border);
  letter-spacing: 0.02em;
}

.analysis-card p {
  font-size: 0.85rem;
  line-height: 1.7;
  color: var(--text);
  margin-bottom: 8px;
}

.analysis-card p:last-child { margin-bottom: 0; }
.analysis-card strong { font-weight: 600; color: #0f172a; }

.analysis-card .tag {
  display: inline-block;
  font-size: 0.64rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 2px 8px;
  border-radius: 999px;
  margin-right: 4px;
  vertical-align: middle;
}

.analysis-card .tag.attr {
  background: rgba(5,150,105,0.1);
  color: var(--green);
  border: 1px solid rgba(5,150,105,0.2);
}

.analysis-card .tag.rep {
  background: rgba(220,38,38,0.1);
  color: var(--red);
  border: 1px solid rgba(220,38,38,0.2);
}

.analysis-card .tag.neut {
  background: rgba(2,132,199,0.08);
  color: var(--blue);
  border: 1px solid rgba(2,132,199,0.18);
}

.analysis-card .highlight-box {
  background: #f1f5f9;
  border-left: 3px solid var(--blue);
  padding: 10px 14px;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  margin: 8px 0;
  font-size: 0.83rem;
  line-height: 1.6;
}

.analysis-card .highlight-box.orange { border-left-color: #ea580c; }
.analysis-card .highlight-box.green { border-left-color: var(--green); }

.analysis-conclusion {
  background: linear-gradient(135deg, rgba(2,132,199,0.04), rgba(124,58,237,0.04));
  border: 1px solid rgba(2,132,199,0.15);
  border-radius: var(--radius-lg);
  padding: 18px 22px;
  margin-top: 4px;
}

.analysis-conclusion-title {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--blue);
  margin-bottom: 8px;
  letter-spacing: 0.04em;
}

.analysis-conclusion p {
  font-size: 0.85rem;
  line-height: 1.7;
  color: var(--text);
  margin-bottom: 6px;
}

.analysis-conclusion p:last-child { margin-bottom: 0; }

/* ── VECTOR PANEL ── */
.vector-panel {
  background: var(--surface-1);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 12px 16px;
  margin-top: 8px;
}

.vector-panel-title {
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 8px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.vp-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3px 20px;
}

.vp-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 3px 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.73rem;
}

.vp-item:nth-last-child(-n+2) { border-bottom: none; }

.vp-item .lbl { color: var(--text-muted); }
.vp-item .val {
  font-family: var(--mono);
  font-weight: 600;
  color: var(--text);
  font-size: 0.76rem;
}

.vp-sub {
  font-size: 0.68rem;
  color: var(--text-faint);
  padding: 3px 0;
  margin-top: 4px;
  border-top: 1px dashed var(--border);
  text-align: center;
}

/* ── ERROR ── */
div[data-testid="stAlert"] {
  background: rgba(220,38,38,0.06) !important;
  border: 1px solid rgba(220,38,38,0.2) !important;
  border-radius: var(--radius-md) !important;
  color: var(--red) !important;
  font-size: 0.84rem !important;
}

/* ── FOOTER ── */
.app-footer {
  text-align: center;
  padding: 24px 0 6px;
  font-size: 0.72rem;
  color: var(--text-faint);
  letter-spacing: 0.03em;
  border-top: 1px solid var(--border);
  margin-top: 48px;
}

.app-footer .ft-name {
  font-weight: 600;
  color: var(--text-muted);
}

/* ── RESPONSIVE ── */
@media (max-width: 900px) {
  [data-testid="block-container"] { padding: 0.3rem 1rem 2.5rem !important; }
  .app-header { flex-wrap: wrap; padding: 14px 18px; gap: 10px; margin: 4px 0 16px; }
  .app-title { font-size: 1.15rem; }
  .app-subtitle { font-size: 0.7rem; }
  .app-badges { margin-left: 0; }
  .app-header-logo { width: 44px; height: 44px; }
}

@media (max-width: 640px) {
  [data-testid="block-container"] { padding: 0.2rem 0.8rem 2rem !important; }
  .app-header { flex-wrap: nowrap; gap: 10px; padding: 12px 14px; margin: 2px 0 12px; }
  .app-title { font-size: 1rem; }
  .app-subtitle { font-size: 0.64rem; }
  .app-header-logo { width: 38px; height: 38px; }
  .badge { font-size: 0.6rem; padding: 2px 7px; }
  .info-row { gap: 5px; margin: 0 0 12px; }
  .info-chip { font-size: 0.62rem; padding: 3px 8px; }
  .section-label { font-size: 0.62rem; margin: 14px 0 8px; }
  .charge-card { padding: 10px 12px 6px; }
  .charge-header { margin-bottom: 10px; gap: 7px; }
  .charge-name { font-size: 0.72rem; }
  .charge-idx { font-size: 0.62rem; padding: 1px 7px; }
  .input-col-label { font-size: 0.6rem; }
  .result-grid { grid-template-columns: 1fr; gap: 10px; }
  .stTabs [role="tablist"] button { font-size: 0.6rem !important; padding: 5px 8px !important; }
  .rcard { padding: 12px 14px; }
  .rcard-value { font-size: 1.1rem; }
  .rcard-row { font-size: 0.68rem; }
  .rcard-interp { font-size: 0.65rem; }
  .analysis-card { padding: 14px 16px; }
  .analysis-card p { font-size: 0.78rem; }
  .analysis-conclusion { padding: 14px 16px; }
  .analysis-conclusion p { font-size: 0.78rem; }
}

@media (max-width: 480px) {
  [data-testid="block-container"] { padding: 0.1rem 0.5rem 1.5rem !important; }
  .app-header { flex-wrap: wrap; padding: 10px 12px; gap: 8px; }
  .app-title { font-size: 0.88rem; }
  .app-subtitle { font-size: 0.58rem; }
  .app-header-logo { width: 34px; height: 34px; }
  .section-label { font-size: 0.55rem; margin: 12px 0 6px; }
  .input-col-label { font-size: 0.55rem; }
  .charge-card { padding: 8px 10px 4px; }
  .charge-name { font-size: 0.65rem; }
  .rcard { padding: 10px 12px; }
  .rcard-value { font-size: 0.95rem; }
  .rcard-row { font-size: 0.62rem; }
  .stTabs [role="tablist"] button { font-size: 0.55rem !important; padding: 4px 6px !important; }
  .info-chip { font-size: 0.58rem; padding: 2px 6px; }
}
</style>
"""
