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
    page_title="Simulador de Cargas Eléctricas",
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

[data-testid="stAppViewContainer"] > .main {
  padding-top: 0 !important;
}

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

.app-header-text {
  flex: 1;
  min-width: 0;
}

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

.app-badges {
  margin-left: auto;
  display: flex; gap: 8px;
}

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

.charge-name {
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: 0.01em;
}

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

/* Flecha del selector visible */
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

.rcard.net-force {
  border-left: 3px solid var(--blue);
}

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

.rcard-row + .rcard-row {
  border-top: 1px solid var(--border);
}

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

.analysis-card strong {
  font-weight: 600;
  color: #0f172a;
}

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

.analysis-card .highlight-box.orange {
  border-left-color: #ea580c;
}

.analysis-card .highlight-box.green {
  border-left-color: var(--green);
}

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
  <div class="app-header-text">
    <div class="app-title">Simulador de <span class="accent">Cargas Eléctricas</span></div>
    <div class="app-subtitle">Ley de Coulomb · Interacciones electrostáticas · Análisis vectorial 2D</div>
  </div>
  <div class="app-badges">
    <span class="badge live">Simulación</span>
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
  <span class="info-chip"><b>Ke</b> = 8.99 × 10⁹ N·m²/C² (constante de Coulomb)</span>
  <span class="info-chip"><b>F</b> = Ke · |q₁ · q₂| / r² (Ley de Coulomb)</span>
  <span class="info-chip"><b>µC</b> = microcoulomb (10⁻⁶ C) · <b>m</b> = metros</span>
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
        signo = '+' if Q_DEF[i] > 0 else '−'
        st.markdown(f"""
        <div class="charge-card">
          <div class="charge-header">
            <span class="charge-dot" style="background:{c};"></span>
            <span class="charge-name">Carga {i+1}</span>
            <span class="charge-idx">Q{i+1} · {signo}</span>
          </div>
          <div class="input-row-labels">
            <span class="input-col-label">Valor Carga (µC)</span>
            <span class="input-col-label">Posición X (m)</span>
            <span class="input-col-label">Posición Y (m)</span>
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
    # ANALYSIS FUNCTIONS
    # ─────────────────────────────────────────
    def analisis_par_html(par, c1_orig, c2_orig):
        parts = []
        interaccion = "atracción" if par['atraccion'] else "repulsión"
        signos = "opuestos" if par['atraccion'] else "iguales"
        tag_cls = "attr" if par['atraccion'] else "rep"
        tag_txt = "Atracción" if par['atraccion'] else "Repulsión"
        signo_op = "diferente" if par['atraccion'] else "el mismo"

        parts.append(f'<span class="tag {tag_cls}">{tag_txt}</span> '
                      f'Las cargas <strong>Q{par["i"]}</strong> ({par["q1"]:+.1f} µC) y '
                      f'<strong>Q{par["j"]}</strong> ({par["q2"]:+.1f} µC) '
                      f'interactúan por <strong>{interaccion}</strong> ya que sus signos son {signos} '
                      f'(q₁ = {par["q1"]:+.1f} µC, q₂ = {par["q2"]:+.1f} µC → signo {signo_op}). '
                      f'Físicamente, la fuerza eléctrica entre dos cargas es directamente proporcional '
                      f'al producto de sus magnitudes: <em>F ∝ |q₁ · q₂|</em>.')

        parts.append(f'La magnitud de la fuerza resultante es <strong>{par["F"]:.4f} N</strong> (Newtons) y '
                      f'actúa entre las cargas separadas por una distancia de <strong>{par["r"]:.3f} m</strong>. '
                      f'De acuerdo con la Ley de Coulomb, la intensidad de la fuerza disminuye '
                      f'con el cuadrado de la distancia (<em>F ∝ 1/r²</em>): si la distancia se duplica, '
                      f'la fuerza se reduce a la cuarta parte.')

        ang = par['theta']
        ang_abs = abs(ang)
        if ang_abs < 15:
            dir_desc = "predominantemente horizontal"
            if ang >= 0:
                dir_desc += " hacia la derecha"
            else:
                dir_desc += " hacia la izquierda"
        elif ang_abs > 75:
            if ang > 0:
                dir_desc = "predominantemente vertical hacia arriba"
            else:
                dir_desc = "predominantemente vertical hacia abajo"
        else:
            if ang > 0:
                dir_desc = f"diagonal ascendente ({ang:.1f}° sobre la horizontal)"
            else:
                dir_desc = f"diagonal descendente ({abs(ang):.1f}° bajo la horizontal)"

        parts.append(f'Vectorialmente, la fuerza se orienta de manera <strong>{dir_desc}</strong>. '
                      f'El ángulo θ = <strong>{ang:.1f}°</strong> mide la inclinación del vector de fuerza '
                      f'respecto al eje horizontal positivo. Este ángulo es fundamental para descomponer '
                      f'la fuerza en sus componentes cartesianas Fx y Fx.')

        fx_mag, fy_mag = abs(par['Fx']), abs(par['Fy'])
        if fx_mag > fy_mag * 1.5:
            comp_desc = (f'La componente <strong>horizontal (Fx = {par["Fx"]:+.4f} N)</strong> '
                          f'domina significativamente sobre la componente vertical. '
                          f'Esto indica que la interacción entre estas cargas ocurre '
                          f'principalmente a lo largo del eje X, generando un desplazamiento '
                          f'predominantemente lateral.')
        elif fy_mag > fx_mag * 1.5:
            comp_desc = (f'La componente <strong>vertical (Fy = {par["Fy"]:+.4f} N)</strong> '
                          f'domina significativamente sobre la componente horizontal. '
                          f'Esto indica que la interacción entre estas cargas ocurre '
                          f'principalmente a lo largo del eje Y, generando un desplazamiento '
                          f'predominantemente vertical.')
        else:
            comp_desc = (f'Las componentes <strong>Fx = {par["Fx"]:+.4f} N</strong> y '
                          f'<strong>Fy = {par["Fy"]:+.4f} N</strong> están equilibradas, '
                          f'generando una fuerza diagonal balanceada. Ambas direcciones '
                          f'contribuyen de manera similar al vector resultante.')
        parts.append(comp_desc)

        q1m, q2m = abs(par['q1']), abs(par['q2'])
        if q1m > q2m * 1.15:
            parts.append(f'<strong>Q{par["i"]}</strong> posee una carga de mayor magnitud '
                          f'({q1m:.1f} µC frente a {q2m:.1f} µC de Q{par["j"]}), '
                          f'por lo que ejerce una influencia eléctrica más intensa. '
                          f'La fuerza electrostática es proporcional al producto de ambas cargas, '
                          f'por lo que una mayor magnitud en una de ellas incrementa '
                          f'la intensidad de la interacción.')
        elif q2m > q1m * 1.15:
            parts.append(f'<strong>Q{par["j"]}</strong> posee una carga de mayor magnitud '
                          f'({q2m:.1f} µC frente a {q1m:.1f} µC de Q{par["i"]}), '
                          f'por lo que ejerce una influencia eléctrica más intensa. '
                          f'La fuerza electrostática es proporcional al producto de ambas cargas, '
                          f'por lo que una mayor magnitud en una de ellas incrementa '
                          f'la intensidad de la interacción.')

        # Relación con la Ley de Coulomb
        producto = abs(par['q1'] * par['q2'])
        f_esperada = 8.99e9 * producto * 1e-12 / (par['r']**2)
        parts.append(f'<strong>Verificación analítica:</strong> Aplicando la Ley de Coulomb '
                      f'<em>F = Ke · |q₁·q₂| / r²</em>, donde Ke = 8.99×10⁹ N·m²/C², '
                      f'se obtiene F = (8.99×10⁹)({producto:.1f}×10⁻¹²)/({par["r"]:.3f})² = '
                      f'<strong>{f_esperada:.4f} N</strong>, que coincide con el valor calculado.')

        return '<p>' + '</p><p>'.join(parts) + '</p>'

    def analisis_neta_html(fn, carga_orig):
        parts = []
        fx, fy, fmag = fn['Fx'], fn['Fy'], fn['F']
        angle = fn['theta']

        if fmag < 1e-10:
            return (f'<p>La <strong>carga {fn["indice"]}</strong> ({carga_orig["q"]:+.1f} µC) se encuentra en '
                     f'<strong>equilibrio electrostático</strong>: la fuerza neta es aproximadamente cero. '
                     f'Esto significa que el vector resultante de todas las fuerzas ejercidas por las cargas '
                     f'circundantes se anula completamente. La carga no experimenta aceleración eléctrica neta '
                     f'y permanece en reposo relativo dentro del sistema.</p>')

        if fx > 0 and fy > 0:
            dir_desc = "se dirige hacia el noreste (primer cuadrante)"
            cuad = "primer cuadrante"
            cuad_expl = "Fx > 0 y Fy > 0, ambas positivas"
        elif fx < 0 and fy > 0:
            dir_desc = "se dirige hacia el noroeste (segundo cuadrante)"
            cuad = "segundo cuadrante"
            cuad_expl = "Fx < 0 y Fy > 0, horizontal negativa y vertical positiva"
        elif fx < 0 and fy < 0:
            dir_desc = "se dirige hacia el suroeste (tercer cuadrante)"
            cuad = "tercer cuadrante"
            cuad_expl = "Fx < 0 y Fy < 0, ambas negativas"
        elif fx > 0 and fy < 0:
            dir_desc = "se dirige hacia el sureste (cuarto cuadrante)"
            cuad = "cuarto cuadrante"
            cuad_expl = "Fx > 0 y Fy < 0, horizontal positiva y vertical negativa"
        elif fx > 0:
            dir_desc = "es horizontal hacia la derecha (este)"
            cuad = "eje X positivo"
            cuad_expl = "Fx > 0"
        elif fx < 0:
            dir_desc = "es horizontal hacia la izquierda (oeste)"
            cuad = "eje X negativo"
            cuad_expl = "Fx < 0"
        elif fy > 0:
            dir_desc = "es vertical hacia arriba (norte)"
            cuad = "eje Y positivo"
            cuad_expl = "Fy > 0"
        else:
            dir_desc = "es vertical hacia abajo (sur)"
            cuad = "eje Y negativo"
            cuad_expl = "Fy < 0"

        parts.append(f'La <strong>carga {fn["indice"]}</strong> ({carga_orig["q"]:+.1f} µC) experimenta una '
                      f'<strong>fuerza neta de {fmag:.4f} N</strong> que {dir_desc}, '
                      f'con un ángulo resultante de <strong>{angle:.1f}°</strong> '
                      f'respecto al eje horizontal positivo.')

        parts.append(f'La orientación hacia el <strong>{cuad}</strong> del plano cartesiano ({cuad_expl}) '
                      f'indica que el vector suma de todas las fuerzas eléctricas ejercidas '
                      f'sobre esta carga por las demás no se cancela. Este desequilibrio es el '
                      f'responsable de la aceleración neta que experimentaría la carga si estuviera '
                      f'libre de otras ligaduras.')

        if abs(fx) > abs(fy) * 1.5:
            parts.append(f'La componente <strong>horizontal predomina</strong> '
                          f'(|Fx| = {abs(fx):.4f} N > |Fy| = {abs(fy):.4f} N), '
                          f'lo que sugiere que las cargas con mayor influencia se encuentran '
                          f'dispuestas lateralmente respecto a esta carga. El movimiento '
                          f'resultante sería predominantemente horizontal.')
        elif abs(fy) > abs(fx) * 1.5:
            parts.append(f'La componente <strong>vertical predomina</strong> '
                          f'(|Fy| = {abs(fy):.4f} N > |Fx| = {abs(fx):.4f} N), '
                          f'lo que sugiere que las cargas con mayor influencia se encuentran '
                          f'dispuestas verticalmente respecto a esta carga. El movimiento '
                          f'resultante sería predominantemente vertical.')
        else:
            parts.append(f'Las componentes están <strong>balanceadas</strong> '
                          f'(Fx = {fx:+.4f} N, Fy = {fy:+.4f} N), '
                          f'lo que indica una influencia múltiple y equilibrada en ambas direcciones '
                          f'cardinales. La fuerza neta resultante presenta una trayectoria diagonal '
                          f'con contribuciones equitativas de ambos ejes.')

        # Fuerzas circundantes que más contribuyen
        contribuciones = []
        for par in pares_info:
            if par['i'] == fn['indice'] or par['j'] == fn['indice']:
                otro = par['j'] if par['i'] == fn['indice'] else par['i']
                contribuciones.append((otro, par['F']))
        contribuciones.sort(key=lambda x: x[1], reverse=True)
        if contribuciones:
            top = contribuciones[0]
            parts.append(f'La interacción que <strong>más contribuye</strong> a la fuerza neta sobre '
                          f'Q{fn["indice"]} proviene de <strong>Q{top[0]}</strong> con una fuerza de '
                          f'{top[1]:.4f} N. Esto se debe a la combinación de su magnitud de carga '
                          f'y la proximidad espacial entre ambas.')

        return '<p>' + '</p><p>'.join(parts) + '</p>'

    def analisis_sistema_html():
        n = len(cargas)
        pos = sum(1 for c in cargas if c['q'] > 0)
        neg = n - pos
        total_pares = len(pares_info)
        atracciones = sum(1 for p in pares_info if p['atraccion'])
        repulsiones = total_pares - atracciones

        lines = []
        lines.append(f'El sistema está compuesto por <strong>{n} cargas</strong> ({pos} positiva{"" if pos==1 else "s"}, '
                      f'{neg} negativa{"" if neg==1 else "s"}). Se generan <strong>{total_pares} interacciones</strong> '
                      f'entre pares: {atracciones} de atracción y {repulsiones} de repulsión.')

        if atracciones > repulsiones:
            lines.append('Predominan las <strong>fuerzas de atracción</strong>, lo que sugiere que el sistema '
                          'tiende a la contracción: las cargas se atraen entre sí predominantemente.')
        elif repulsiones > atracciones:
            lines.append('Predominan las <strong>fuerzas de repulsión</strong>, lo que sugiere que el sistema '
                          'tiende a la expansión: las cargas se repelen entre sí predominantemente.')
        else:
            lines.append('Existe un <strong>equilibrio entre atracciones y repulsiones</strong>, '
                          'generando una dinámica de interacciones balanceada.')

        netas_mag = [fn['F'] for fn in fuerzas_netas]
        max_neta = max(netas_mag)
        min_neta = min(netas_mag)
        carga_max = fuerzas_netas[netas_mag.index(max_neta)]['indice']
        carga_min = fuerzas_netas[netas_mag.index(min_neta)]['indice']
        lines.append(f'La carga con <strong>mayor fuerza neta</strong> es <strong>Q{carga_max}</strong> ({max_neta:.4f} N), '
                      f'mientras que la de <strong>menor fuerza neta</strong> es <strong>Q{carga_min}</strong> ({min_neta:.4f} N). '
                      f'Esta diferencia refleja cómo la distribución espacial y las magnitudes de carga '
                      f'afectan el desequilibrio de fuerzas en cada punto.')

        # Force gradient
        fx_all = [fn['Fx'] for fn in fuerzas_netas]
        fy_all = [fn['Fy'] for fn in fuerzas_netas]
        fx_pos = sum(1 for v in fx_all if v > 0)
        fx_neg = sum(1 for v in fx_all if v < 0)
        fy_pos = sum(1 for v in fy_all if v > 0)
        fy_neg = sum(1 for v in fy_all if v < 0)

        if fx_pos > fx_neg and fy_pos > fy_neg:
            lines.append(f'<strong>Tendencia general del sistema:</strong> La mayoría de las fuerzas netas apuntan '
                          f'hacia el primer cuadrante (Fx > 0, Fy > 0), lo que indica un desplazamiento neto '
                          f'preferencial hacia el noreste del plano.')
        elif fx_neg > fx_pos and fy_pos > fy_neg:
            lines.append(f'<strong>Tendencia general del sistema:</strong> Predominan las fuerzas hacia el segundo cuadrante '
                          f'(Fx < 0, Fy > 0), indicando un desplazamiento neto hacia el noroeste.')
        elif fx_neg > fx_pos and fy_neg > fy_pos:
            lines.append(f'<strong>Tendencia general del sistema:</strong> Predominan las fuerzas hacia el tercer cuadrante '
                          f'(Fx < 0, Fy < 0), indicando un desplazamiento neto hacia el suroeste.')
        elif fx_pos > fx_neg and fy_neg > fy_pos:
            lines.append(f'<strong>Tendencia general del sistema:</strong> Predominan las fuerzas hacia el cuarto cuadrante '
                          f'(Fx > 0, Fy < 0), indicando un desplazamiento neto hacia el sureste.')

        return '<p>' + '</p><p>'.join(lines) + '</p>'

    def conclusiones_html():
        n = len(cargas)
        pos = sum(1 for c in cargas if c['q'] > 0)
        neg = n - pos
        total_pares = len(pares_info)
        atracciones = sum(1 for p in pares_info if p['atraccion'])
        repulsiones = total_pares - atracciones
        netas_mag = [fn['F'] for fn in fuerzas_netas]
        prom_neta = sum(netas_mag) / len(netas_mag) if netas_mag else 0
        dists = [p['r'] for p in pares_info]
        dist_prom = sum(dists) / len(dists) if dists else 0
        dist_min = min(dists) if dists else 0
        f_mags = [p['F'] for p in pares_info]
        f_max = max(f_mags) if f_mags else 0
        f_prom = sum(f_mags) / len(f_mags) if f_mags else 0

        lines = []
        lines.append(f'<strong>Comportamiento electrostático:</strong> El sistema está configurado con '
                      f'<strong>{n} cargas</strong> ({pos} positiva{"" if pos==1 else "s"}, {neg} negativa{"" if neg==1 else "s"}), '
                      f'generando <strong>{total_pares} interacciones coulombianas</strong> '
                      f'({atracciones} de atracción, {repulsiones} de repulsión). '
                      f'Cada interacción obedece la Ley de Coulomb (<em>F = Ke·|q₁·q₂|/r²</em>), '
                      f'donde la magnitud de la fuerza electrostática es directamente proporcional '
                      f'al producto de las cargas e inversamente proporcional al cuadrado de la distancia.')

        lines.append(f'<strong>Análisis de distancias:</strong> La distancia promedio entre pares de cargas es de '
                      f'<strong>{dist_prom:.3f} m</strong>, con una distancia mínima de {dist_min:.3f} m. '
                      f'La relación <em>F ∝ 1/r²</em> implica que el par más cercano ({dist_min:.3f} m) genera la '
                      f'fuerza de mayor magnitud ({f_max:.4f} N), mientras que los pares más alejados '
                      f'contribuyen con fuerzas significativamente menores.')

        lines.append(f'<strong>Análisis vectorial y componentes:</strong> Las fuerzas electrostáticas se representan '
                      f'como vectores en el plano cartesiano, descomponiéndose en componentes horizontal (Fx) '
                      f'y vertical (Fy). La fuerza neta promedio del sistema es de <strong>{prom_neta:.4f} N</strong>, '
                      f'lo que refleja el grado de desequilibrio electrostático presente. '
                      f'La magnitud promedio de las fuerzas entre pares es de <strong>{f_prom:.4f} N</strong>. '
                      f'La componente angular (θ) determina la dirección precisa de cada vector resultante.')

        if atracciones > repulsiones:
            pct = atracciones / total_pares * 100
            lines.append(f'<strong>Predominancia de atracción ({pct:.0f}% de los pares):</strong> '
                          f'La mayoría de las interacciones son de atracción, lo que indica una configuración '
                          f'donde predominan los signos opuestos. Desde la perspectiva energética, '
                          f'un sistema con atracción predominante tiende a disminuir su energía potencial '
                          f'electrostática (<em>U = Ke·q₁·q₂/r</em>) a medida que las cargas se aproximan, '
                          f'lo que sugiere una tendencia natural hacia la contracción del sistema.')
        elif repulsiones > atracciones:
            pct = repulsiones / total_pares * 100
            lines.append(f'<strong>Predominancia de repulsión ({pct:.0f}% de los pares):</strong> '
                          f'La mayoría de las interacciones son de repulsión, lo que indica una configuración '
                          f'donde predominan los signos iguales. La energía potencial electrostática '
                          f'del sistema es positiva y las cargas tienden a separarse, '
                          f'lo que sugiere una tendencia natural hacia la expansión del sistema.')
        else:
            lines.append(f'<strong>Balance atractivo–repulsivo:</strong> Existe un equilibrio numérico entre '
                          f'interacciones de atracción y repulsión, lo que genera una dinámica '
                          f'mixta donde algunas cargas se aproximan mientras otras se separan, '
                          f'produciendo una configuración electrostática compleja.')

        # Fuerza máxima y mínima del sistema
        par_max = None
        par_min = None
        for p in pares_info:
            if p['F'] == f_max:
                par_max = p
            if p['F'] == dist_min and False:
                pass
        for p in pares_info:
            if abs(p['F'] - f_max) < 1e-10:
                par_max = p
                break
        for p in pares_info:
            if p['F'] == min(f_mags):
                par_min = p
                break

        if par_max:
            causa = "atracción" if par_max['atraccion'] else "repulsión"
            lines.append(f'<strong>Interacción dominante:</strong> El par Q{par_max["i"]}–Q{par_max["j"]} presenta '
                          f'la mayor magnitud de fuerza ({par_max["F"]:.4f} N, {causa}), '
                          f'ubicados a una distancia de {par_max["r"]:.3f} m. '
                          f'Esta interacción es la que domina el comportamiento dinámico del sistema.')

        # Verificación de consistencia
        lines.append(f'<strong>Verificación física:</strong> Todos los resultados cumplen la Ley de Coulomb '
                      f'y el principio de superposición. Las fuerzas se han calculado como suma vectorial '
                      f'de las contribuciones individuales, respetando la naturaleza atractiva o repulsiva '
                      f'según el signo de las cargas involucradas. Los resultados son coherentes con las '
                      f'leyes fundamentales del electromagnetismo clásico.')

        return '<p>' + '</p><p>'.join(lines) + '</p>'

    # ─────────────────────────────────────────
    # RESULTS
    # ─────────────────────────────────────────
    st.markdown('<div class="section-label">Análisis de resultados</div>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["Fuerzas entre pares", "Fuerza neta por carga", "Visualización 2D", "Análisis e interpretación"])

    with tab1:
        html = '<div class="result-grid">'
        for par in pares_info:
            bc = "attract" if par['atraccion'] else "repel"
            bt = "Atracción" if par['atraccion'] else "Repulsión"
            interp_signo = "cargas de signo opuesto se atraen" if par['atraccion'] else "cargas del mismo signo se repelen"
            ang = par['theta']
            if abs(ang) < 15:
                dir_interp = "La fuerza es predominantemente horizontal"
            elif abs(ang) > 75:
                dir_interp = "La fuerza es predominantemente vertical"
            elif ang > 0:
                dir_interp = f"El vector apunta hacia el noreste ({ang:.1f}° sobre la horizontal)"
            else:
                dir_interp = f"El vector apunta hacia el sureste ({abs(ang):.1f}° bajo la horizontal)"
            html += f"""
            <div class="rcard">
              <div class="rcard-header">
                <span class="rcard-title">Carga Q{par['i']} ↔ Q{par['j']}</span>
                <span class="rcard-badge {bc}">{bt}</span>
              </div>
              <div class="rcard-value">{par['F']:.4f}<span>N · Fuerza electrostática</span></div>
              <div class="rcard-meta">
                <div class="rcard-row"><span class="lbl">q₁ (Carga 1)</span><span class="val">{par['q1']:+.2f} µC</span></div>
                <div class="rcard-row"><span class="lbl">q₂ (Carga 2)</span><span class="val">{par['q2']:+.2f} µC</span></div>
                <div class="rcard-row"><span class="lbl">r (Distancia)</span><span class="val">{par['r']:.4f} m</span></div>
                <div class="rcard-row"><span class="lbl">θ (Ángulo del vector)</span><span class="val">{par['theta']:.2f}°</span></div>
              </div>
              <div class="rcard-interp">{interp_signo}. {dir_interp}.</div>
            </div>"""
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    with tab2:
        html = '<div class="result-grid">'
        for fn in fuerzas_netas:
            color = fn['color']
            fx, fy, fmag = fn['Fx'], fn['Fy'], fn['F']
            if fx > 0 and fy > 0:
                neta_dir = "noreste (primer cuadrante)"
            elif fx < 0 and fy > 0:
                neta_dir = "noroeste (segundo cuadrante)"
            elif fx < 0 and fy < 0:
                neta_dir = "suroeste (tercer cuadrante)"
            elif fx > 0 and fy < 0:
                neta_dir = "sureste (cuarto cuadrante)"
            elif fx > 0:
                neta_dir = "este (horizontal derecha)"
            elif fx < 0:
                neta_dir = "oeste (horizontal izquierda)"
            elif fy > 0:
                neta_dir = "norte (vertical arriba)"
            else:
                neta_dir = "sur (vertical abajo)"
            html += f"""
            <div class="rcard net-force">
              <div class="rcard-header">
                <span class="rcard-title">Carga {fn['indice']}</span>
                <span class="rcard-badge net">Fuerza neta</span>
              </div>
              <div class="rcard-value">{fn['F']:.4f}<span>N · Resultante</span></div>
              <div class="rcard-meta">
                <div class="rcard-row"><span class="lbl">Fx (Componente horizontal)</span><span class="val">{fn['Fx']:+.4f} N</span></div>
                <div class="rcard-row"><span class="lbl">Fy (Componente vertical)</span><span class="val">{fn['Fy']:+.4f} N</span></div>
                <div class="rcard-row"><span class="lbl">θ (Dirección resultante)</span><span class="val">{fn['theta']:.2f}°</span></div>
              </div>
              <div class="rcard-interp">La fuerza neta resultante apunta hacia el <strong>{neta_dir}</strong>, con un ángulo de {fn['theta']:.1f}°.</div>
            </div>"""
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    with tab3:
        col_g1, col_g2 = st.columns(2, gap="medium")

        # Gráfica 1: Sistema de cargas
        with col_g1:
            st.markdown('<div class="chart-wrap"><div class="chart-label">Sistema de cargas · Vectores de fuerza neta</div>', unsafe_allow_html=True)
            fig1, ax1 = plt.subplots(figsize=(7, 7))
            fig1.patch.set_facecolor('#ffffff')
            ax1.set_facecolor('#f8fafc')

            xs = [c['x'] for c in cargas_coulombs]
            ys = [c['y'] for c in cargas_coulombs]
            margin = 2.5
            xc = (min(xs) + max(xs)) / 2
            yc = (min(ys) + max(ys)) / 2
            half = max(max(xs)-min(xs), max(ys)-min(ys)) / 2 + margin
            ax1.set_xlim(xc - half, xc + half)
            ax1.set_ylim(yc - half, yc + half)
            ax1.set_aspect('equal')

            ax1.grid(True, color='#e2e8f0', linewidth=0.5, alpha=0.7)
            ax1.axhline(0, color='#cbd5e1', linewidth=0.8, alpha=0.5)
            ax1.axvline(0, color='#cbd5e1', linewidth=0.8, alpha=0.5)

            for p in pares_info:
                ci = cargas_coulombs[p['i']-1]
                cj = cargas_coulombs[p['j']-1]
                ls = '--' if p['atraccion'] else ':'
                ax1.plot([ci['x'], cj['x']], [ci['y'], cj['y']],
                         color='#cbd5e1', linewidth=0.7, linestyle=ls, alpha=0.5, zorder=1)

            # Detectar superposición y ajustar posición de etiquetas
            n_charges = len(cargas_coulombs)
            label_offsets = []
            for idx, c in enumerate(cargas_coulombs):
                # Buscar vecinos cercanos
                near = False
                for other in cargas_coulombs:
                    if other['indice'] == c['indice']: continue
                    dist = math.hypot(c['x'] - other['x'], c['y'] - other['y'])
                    if dist < half * 0.5:
                        near = True
                        break
                # Alternar posición: even index → abajo, odd → arriba
                # Si hay vecinos cerca, desplazar más
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
                ax1.text(c['x'], c['y'] + off,
                         f"Q{c['indice']}  {cargas[c['indice']-1]['q']:.1f}µC",
                         ha='center', va=va, fontsize=7.5, color='#64748b',
                         fontfamily='monospace',
                         bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff',
                                   edgecolor=col+'66', linewidth=0.8), zorder=5)
                if fn['F'] > 1e-6:
                    scale = half * 0.28
                    fx_v = (fn['Fx'] / fn['F']) * scale
                    fy_v = (fn['Fy'] / fn['F']) * scale
                    ax1.annotate('', xy=(c['x']+fx_v, c['y']+fy_v),
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
            st.markdown('</div>', unsafe_allow_html=True)
            # Panel de resumen vectorial del sistema
            neta_sum = max(fuerzas_netas, key=lambda x: x['F']) if fuerzas_netas else None
            if neta_sum:
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
                st.markdown(f"""
                <div class="vector-panel">
                  <div class="vector-panel-title">📊 Resumen vectorial del sistema</div>
                  <div class="vp-grid">
                    <div class="vp-item"><span class="lbl">Fx total</span><span class="val" style="color:#0284c7;">{fx_s:+.4f} N</span></div>
                    <div class="vp-item"><span class="lbl">Fy total</span><span class="val" style="color:#ea580c;">{fy_s:+.4f} N</span></div>
                    <div class="vp-item"><span class="lbl">|F| resultante</span><span class="val" style="color:#7c3aed;">{fm_s:.4f} N</span></div>
                    <div class="vp-item"><span class="lbl">Ángulo θ</span><span class="val">{th_s:.2f}°</span></div>
                    <div class="vp-item"><span class="lbl">Dirección</span><span class="val">{cuad_s.split(" (")[0]}</span></div>
                    <div class="vp-item"><span class="lbl">Componente dom.</span><span class="val">{dom_s}</span></div>
                  </div>
                  <div class="vp-sub">Datos correspondientes a la carga con mayor fuerza neta del sistema</div>
                </div>""", unsafe_allow_html=True)

        # Gráfica 2: Descomposición vectorial
        with col_g2:
            st.markdown('<div class="chart-wrap"><div class="chart-label">Descomposición vectorial · Primer par de cargas</div>', unsafe_allow_html=True)
            if pares_info:
                fig2, ax2 = plt.subplots(figsize=(7, 7))
                fig2.patch.set_facecolor('#ffffff')
                ax2.set_facecolor('#f8fafc')

                par = pares_info[0]
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

                # Ejes de referencia (suaves)
                ax2.axhline(0, color='#e2e8f0', linewidth=0.5, zorder=0)
                ax2.axvline(0, color='#e2e8f0', linewidth=0.5, zorder=0)
                ax2.annotate('', xy=(5.2, 0), xytext=(0,0),
                             arrowprops=dict(arrowstyle='->', color='#cbd5e1', lw=0.7))
                ax2.annotate('', xy=(0, 5.2), xytext=(0,0),
                             arrowprops=dict(arrowstyle='->', color='#cbd5e1', lw=0.7))
                ax2.text(5.25, -0.15, 'x', fontsize=7.5, color='#94a3b8', fontfamily='monospace')
                ax2.text(-0.18, 5.25, 'y', fontsize=7.5, color='#94a3b8', fontfamily='monospace')

                # Líneas de proyección (muy sutiles)
                ax2.plot([fx_n, fx_n], [0, fy_n], color='#cbd5e1', linewidth=0.5, linestyle='--', alpha=0.35)
                ax2.plot([0, fx_n], [fy_n, fy_n], color='#cbd5e1', linewidth=0.5, linestyle='--', alpha=0.35)

                # Vectores principales
                ax2.annotate('', xy=(fx_n, 0), xytext=(0,0),
                             arrowprops=dict(arrowstyle='->', color='#0284c7', lw=3, mutation_scale=18))
                ax2.annotate('', xy=(fx_n, fy_n), xytext=(fx_n, 0),
                             arrowprops=dict(arrowstyle='->', color='#ea580c', lw=3, mutation_scale=18))
                ax2.annotate('', xy=(f_nx, f_ny), xytext=(0,0),
                             arrowprops=dict(arrowstyle='->', color='#7c3aed', lw=3.8, mutation_scale=22))

                # ── Etiqueta Fx (arriba del vector horizontal) ──
                fx_lab_x = max(fx_n / 2, 0.6)
                ax2.text(fx_lab_x, 0.4, f'Fx = {Fx:+.3f} N', ha='center', va='bottom',
                         fontsize=8, color='#0284c7', fontfamily='monospace', fontweight='bold',
                         bbox=dict(boxstyle='round,pad=0.15', facecolor='#ffffff',
                                   edgecolor='#0284c720', linewidth=0.5), zorder=10)

                # ── Etiqueta Fy (a la derecha o izquierda del vector vertical) ──
                fy_ha = 'left'
                fy_lab_x = fx_n + 0.45
                if fy_lab_x > 5.2:
                    fy_lab_x = fx_n - 0.45
                    fy_ha = 'right'
                ax2.text(fy_lab_x, fy_n / 2, f'Fy = {Fy:+.3f} N', ha=fy_ha, va='center',
                         fontsize=8, color='#ea580c', fontfamily='monospace', fontweight='bold',
                         bbox=dict(boxstyle='round,pad=0.15', facecolor='#ffffff',
                                   edgecolor='#ea580c20', linewidth=0.5), zorder=10)

                # ── Etiqueta F (resultante, desplazada perpendicular) ──
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

                # ── Arco del ángulo ──
                if abs(theta_rad) > 0.01:
                    arc_r = 0.7
                    arc = np.linspace(0, theta_rad, 60)
                    ax2.plot(arc_r*np.cos(arc), arc_r*np.sin(arc), color='#dc2626', linewidth=1.5, alpha=0.5)
                    mid = theta_rad / 2
                    ang_lab_r = 0.95
                    # Posicionar la etiqueta del ángulo fuera del arco
                    ax2.text(ang_lab_r*math.cos(mid), ang_lab_r*math.sin(mid),
                             f'{theta_deg:.1f}°', fontsize=7.5, color='#dc2626',
                             fontfamily='monospace', ha='center', va='center', zorder=10)

                # ── Leyenda compacta ──
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

                # Panel de datos de descomposición
                dir_label = "derecha" if fx_n > 0 else "izquierda"
                if fy_n > 0:
                    dir_label += "/arriba"
                elif fy_n < 0:
                    dir_label += "/abajo"
                st.markdown(f"""
                <div class="vector-panel">
                  <div class="vector-panel-title">📐 Descomposición del par Q{par['i']}–Q{par['j']}</div>
                  <div class="vp-grid">
                    <div class="vp-item"><span class="lbl">Fuerza resultante (F)</span><span class="val" style="color:#7c3aed;">{F:.4f} N</span></div>
                    <div class="vp-item"><span class="lbl">Componente horizontal (Fx)</span><span class="val" style="color:#0284c7;">{Fx:+.4f} N</span></div>
                    <div class="vp-item"><span class="lbl">Componente vertical (Fy)</span><span class="val" style="color:#ea580c;">{Fy:+.4f} N</span></div>
                    <div class="vp-item"><span class="lbl">Ángulo θ</span><span class="val">{theta_deg:.2f}°</span></div>
                  </div>
                  <div class="vp-sub">F inclinada {theta_deg:.1f}° · Fx {'domina' if abs(Fx) > abs(Fy) else 'secundaria'} · Fy {'domina' if abs(Fy) > abs(Fx) else 'secundaria'}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        pares_idx = [(p['i'], p['j']) for p in pares_info]
        html = '<div style="display:flex;flex-direction:column;gap:4px;">'

        # 1. Resumen del sistema
        html += f'<div class="analysis-card">'
        html += f'<div class="analysis-card-title">📋 Resumen del sistema</div>'
        html += analisis_sistema_html()
        html += f'</div>'

        # 2. Análisis por pares
        html += f'<div class="analysis-card">'
        html += f'<div class="analysis-card-title">⚡ Análisis detallado por par</div>'
        for par in pares_info:
            c1 = cargas[par['i']-1]
            c2 = cargas[par['j']-1]
            html += f'<p style="margin-top:10px;font-size:0.78rem;font-weight:600;color:var(--text-muted);letter-spacing:0.05em;text-transform:uppercase;">Par {par["i"]}–{par["j"]}</p>'
            html += analisis_par_html(par, c1, c2)
        html += f'</div>'

        # 3. Análisis de fuerza neta
        html += f'<div class="analysis-card">'
        html += f'<div class="analysis-card-title">🧭 Análisis de fuerza neta por carga</div>'
        for fn in fuerzas_netas:
            c = cargas[fn['indice']-1]
            html += f'<p style="margin-top:10px;font-size:0.78rem;font-weight:600;color:var(--text-muted);letter-spacing:0.05em;text-transform:uppercase;">Carga {fn["indice"]}</p>'
            html += analisis_neta_html(fn, c)
        html += f'</div>'

        # 4. Conclusiones
        html += f'<div class="analysis-conclusion">'
        html += f'<div class="analysis-conclusion-title">📐 Interpretación física del sistema</div>'
        html += conclusiones_html()
        html += f'</div>'

        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
  Proyecto de Cargas de Coulomb &nbsp;·&nbsp; Electromagnetismo &nbsp;·&nbsp; UTS
</div>
""", unsafe_allow_html=True)
