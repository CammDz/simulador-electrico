import streamlit as st


def render_header(logo_base64):
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="logo">' if logo_base64 else "⚡"
    st.markdown(
        f"""
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
    """,
        unsafe_allow_html=True,
    )


def render_info_row():
    st.markdown(
        """
    <div class="info-row">
      <span class="info-chip"><b>Ke</b> = 8.99 × 10⁹ N·m²/C² (constante de Coulomb)</span>
      <span class="info-chip"><b>F</b> = Ke · |q₁ · q₂| / r² (Ley de Coulomb)</span>
      <span class="info-chip"><b>µC</b> = microcoulomb (10⁻⁶ C) · <b>m</b> = metros</span>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_section_label(label):
    st.markdown(
        f'<div class="section-label">{label}</div>',
        unsafe_allow_html=True,
    )


def render_charge_card_html(i, color, signo):
    return f"""
    <div class="charge-card">
      <div class="charge-header">
        <span class="charge-dot" style="background:{color};"></span>
        <span class="charge-name">Carga {i+1}</span>
        <span class="charge-idx">Q{i+1} · {signo}</span>
      </div>
      <div class="input-row-labels">
        <span class="input-col-label">Valor Carga (µC)</span>
        <span class="input-col-label">Posición X (m)</span>
        <span class="input-col-label">Posición Y (m)</span>
      </div>
    </div>
    """


def render_formula_pill(text):
    st.markdown(f'<span class="formula-pill">{text}</span>', unsafe_allow_html=True)


def render_rcard_pair(par):
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
    return f"""
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


def render_rcard_net(fn):
    fx, fy = fn['Fx'], fn['Fy']
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
    return f"""
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


def render_vector_panel(title, items, subtitle=""):
    grid_rows = ""
    for lbl, val, style in items:
        style_attr = f'style="{style}"' if style else ""
        grid_rows += f'<div class="vp-item"><span class="lbl">{lbl}</span><span class="val" {style_attr}>{val}</span></div>\n'
    sub = f'<div class="vp-sub">{subtitle}</div>' if subtitle else ""
    return f"""
    <div class="vector-panel">
      <div class="vector-panel-title">{title}</div>
      <div class="vp-grid">
        {grid_rows}
      </div>
      {sub}
    </div>"""


def render_footer():
    st.markdown(
        """
    <div class="app-footer">
      Proyecto de Cargas de Coulomb &nbsp;·&nbsp; Electromagnetismo &nbsp;·&nbsp; UTS
    </div>
    """,
        unsafe_allow_html=True,
    )
