import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
import base64
import os

# Constante de Coulomb en el vacío (N*m^2/C^2)
K = 8.99e9

st.set_page_config(page_title="Simulador Ley de Coulomb", layout="wide")

# ==================== CSS REDISEÑADO ====================
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    /* FONDO BLANCO PURO */
    body, .stApp {
        background-color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
    }
    
    /* HERO BANNER - DEGRADADO VIOLETA */
    .hero-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 35px 30px;
        border-radius: 16px;
        margin-bottom: 35px;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.25);
        display: flex;
        align-items: center;
        gap: 25px;
        animation: slideDown 0.6s ease-out;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* LOGO */
    .hero-logo-img {
        height: 90px;
        width: 90px;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        object-fit: contain;
        background: white;
        padding: 8px;
    }
    
    .hero-emoji {
        font-size: 90px;
        animation: pulse-glow 2.5s ease-in-out infinite;
        filter: drop-shadow(0 8px 20px rgba(255, 215, 0, 0.3));
    }
    
    @keyframes pulse-glow {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.08);
        }
    }
    
    /* TÍTULOS */
    .hero-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    
    .hero-sub {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1rem;
        margin: 8px 0 0 0;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    
    /* SECCIÓN HEADERS */
    .section-header {
        color: #1a202c;
        font-size: 1.7rem;
        font-weight: 800;
        margin: 40px 0 25px 0;
        padding-bottom: 12px;
        border-bottom: 4px solid #667eea;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* TARJETAS DE CARGAS */
    .charge-card {
        background: #f8f9ff;
        padding: 28px;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border-left: 6px solid;
        margin-bottom: 18px;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .charge-card:hover {
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
        transform: translateY(-4px);
        background: white;
    }
    
    .charge-card.color-1 { border-left-color: #ef4444; }
    .charge-card.color-2 { border-left-color: #3b82f6; }
    .charge-card.color-3 { border-left-color: #f59e0b; }
    .charge-card.color-4 { border-left-color: #10b981; }
    .charge-card.color-5 { border-left-color: #8b5cf6; }
    .charge-card.color-6 { border-left-color: #ec4899; }
    
    .charge-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* BOTÓN CALCULAR - GRANDE Y VISIBLE */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 20px 60px !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        cursor: pointer !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.35) !important;
        transition: all 0.35s ease !important;
        width: 100% !important;
        max-width: 450px !important;
        display: block !important;
        margin: 35px auto !important;
        position: relative !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-6px) !important;
        box-shadow: 0 16px 45px rgba(102, 126, 234, 0.5) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) !important;
    }
    
    /* TARJETAS DE RESULTADOS */
    .result-card {
        background: #ffffff;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border-left: 5px solid;
        margin-bottom: 18px;
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.12);
        transform: translateX(5px);
    }
    
    .result-card.attraction { border-left-color: #10b981; }
    .result-card.repulsion { border-left-color: #ef4444; }
    
    .result-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 12px;
    }
    
    .result-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        font-family: 'Courier New', monospace;
        letter-spacing: 0.3px;
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        border-bottom: 3px solid #e5e7eb;
        background: white;
    }
    
    .stTabs [role="tablist"] button {
        padding: 16px 24px;
        font-size: 1.05rem;
        font-weight: 600;
        border-radius: 10px 10px 0 0;
        background: #f3f4f6 !important;
        color: #4b5563 !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    
    .stTabs [role="tablist"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stTabs [role="tablist"] button:hover {
        background: #e5e7eb !important;
        color: #1a202c !important;
    }
    
    /* ECUACIÓN BOX */
    .equation-box {
        background: #f0f4ff;
        padding: 18px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 15px 0;
        font-family: 'Courier New', monospace;
        font-size: 0.95rem;
        color: #1a202c;
        line-height: 1.6;
    }
    
    /* BADGES */
    .info-badge {
        display: inline-block;
        background: #dbeafe;
        color: #1e40af;
        padding: 8px 14px;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 6px 6px 6px 0;
        border-left: 3px solid #3b82f6;
    }
    
    .success-badge {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
        padding: 8px 14px;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 6px 6px 6px 0;
        border-left: 3px solid #10b981;
    }
    
    .warning-badge {
        display: inline-block;
        background: #fef3c7;
        color: #92400e;
        padding: 8px 14px;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 6px 6px 6px 0;
        border-left: 3px solid #f59e0b;
    }
    
    /* INPUT STYLING */
    .stNumberInput > div > div > input {
        background-color: white !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .stSelectbox > div > div > div {
        background-color: white !important;
    }
    
    /* FOOTER */
    .footer-text {
        text-align: center;
        color: #6b7280;
        font-size: 0.95rem;
        margin-top: 50px;
        padding-top: 30px;
        border-top: 2px solid #e5e7eb;
    }
    
</style>
""", unsafe_allow_html=True)

# ==================== CARGAR LOGO ====================
logo_base64 = None
if os.path.exists("logo.png"):
    with open("logo.png", "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode()

# ==================== HERO BANNER ====================
if logo_base64:
    st.markdown(f"""
    <div class="hero-banner">
        <img src="data:image/png;base64,{logo_base64}" class="hero-logo-img" alt="Logo">
        <div>
            <div class="hero-title">⚡ Simulador de Fuerza Eléctrica</div>
            <div class="hero-sub">Ley de Coulomb · Cálculo y visualización de fuerzas electrostáticas en sistemas 2D</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-emoji">⚡</div>
        <div>
            <div class="hero-title">⚡ Simulador de Fuerza Eléctrica</div>
            <div class="hero-sub">Ley de Coulomb · Cálculo y visualización de fuerzas electrostáticas en sistemas 2D</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== CONFIGURACIÓN ====================
st.markdown('<div class="section-header">⚙️ Configuración del Sistema</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.5, 2, 2])

with col1:
    num_cargas = st.selectbox(
        "Número de cargas:",
        [2, 3, 4, 5, 6],
        index=0
    )

# Colores para las cargas
colores = ['#ef4444', '#3b82f6', '#f59e0b', '#10b981', '#8b5cf6', '#ec4899']
colores_nombres = ['Rojo', 'Azul', 'Ámbar', 'Verde', 'Púrpura', 'Rosa']

st.markdown('<div class="section-header">📍 Parámetros de Cargas</div>', unsafe_allow_html=True)

# Contenedor para las cargas
cargas = []

for i in range(num_cargas):
    col_num = i % 2
    
    if col_num == 0:
        cols = st.columns(2)
    
    with cols[col_num]:
        st.markdown(f"""
        <div class="charge-card color-{i+1}">
            <div class="charge-title">⚡ Carga {i+1} - {colores_nombres[i]}</div>
        """, unsafe_allow_html=True)
        
        col_q, col_x, col_y = st.columns(3)
        
        with col_q:
            q = st.number_input(
                f"Q{i+1} (µC)",
                value=float([5.0, -3.0, 2.5, -4.0, 3.5, -2.0][i]),
                step=0.5,
                key=f"q{i}"
            )
        
        with col_x:
            x = st.number_input(
                f"X{i+1} (m)",
                value=float([0.0, 3.0, 1.5, 4.0, 2.0, 5.0][i]),
                step=0.1,
                key=f"x{i}"
            )
        
        with col_y:
            y = st.number_input(
                f"Y{i+1} (m)",
                value=float([0.0, 0.0, 2.5, 1.5, -2.0, 3.0][i]),
                step=0.1,
                key=f"y{i}"
            )
        
        cargas.append({'q': q, 'x': x, 'y': y, 'indice': i+1, 'color': colores[i]})
        
        st.markdown("</div>", unsafe_allow_html=True)

# Botón Calcular
calcular = st.button("🚀 CALCULAR Y VISUALIZAR", use_container_width=True)

# Conversión a Coulombs
cargas_coulombs = [{'q': c['q'] * 1e-6, 'x': c['x'], 'y': c['y'], 'indice': c['indice'], 'color': c['color']} for c in cargas]

if calcular:
    # Validar que no haya cargas en la misma posición
    posiciones = [(c['x'], c['y']) for c in cargas]
    if len(posiciones) != len(set(posiciones)):
        st.error("❌ Error: Dos o más cargas no pueden estar en la misma posición")
        st.stop()
    
    # Calcular distancias y ángulos entre pares
    pares_info = []
    
    for i in range(len(cargas_coulombs)):
        for j in range(i+1, len(cargas_coulombs)):
            c1, c2 = cargas_coulombs[i], cargas_coulombs[j]
            
            dx = c2['x'] - c1['x']
            dy = c2['y'] - c1['y']
            r = math.sqrt(dx**2 + dy**2)
            
            if r < 0.01:
                st.error(f"❌ Cargas {c1['indice']} y {c2['indice']} están demasiado cerca")
                st.stop()
            
            theta_rad = math.atan2(dy, dx)
            theta_deg = math.degrees(theta_rad)
            
            # Magnitud de la fuerza
            F = K * abs(c1['q'] * c2['q']) / (r**2)
            
            # Componentes
            Fx = F * math.cos(theta_rad)
            Fy = F * math.sin(theta_rad)
            
            # Tipo de interacción
            tipo = "Atracción 🟢" if (c1['q'] * c2['q']) < 0 else "Repulsión 🔴"
            
            pares_info.append({
                'i': c1['indice'],
                'j': c2['indice'],
                'q1': cargas[i]['q'],
                'q2': cargas[j]['q'],
                'r': r,
                'theta': theta_deg,
                'F': F,
                'Fx': Fx,
                'Fy': Fy,
                'tipo': tipo,
                'atraccion': (c1['q'] * c2['q']) < 0
            })
    
    # Calcular fuerza neta sobre cada carga
    fuerzas_netas = []
    
    for i in range(len(cargas_coulombs)):
        Fx_neto = 0
        Fy_neto = 0
        
        for j in range(len(cargas_coulombs)):
            if i == j:
                continue
            
            c_origen = cargas_coulombs[i]
            c_destino = cargas_coulombs[j]
            
            dx = c_destino['x'] - c_origen['x']
            dy = c_destino['y'] - c_origen['y']
            r = math.sqrt(dx**2 + dy**2)
            
            theta_rad = math.atan2(dy, dx)
            F = K * abs(c_origen['q'] * c_destino['q']) / (r**2)
            
            # Dirección según atracción o repulsión
            if (c_origen['q'] * c_destino['q']) < 0:
                # Atracción: fuerza hacia c_destino
                Fx = F * math.cos(theta_rad)
                Fy = F * math.sin(theta_rad)
            else:
                # Repulsión: fuerza alejándose de c_destino
                Fx = -F * math.cos(theta_rad)
                Fy = -F * math.sin(theta_rad)
            
            Fx_neto += Fx
            Fy_neto += Fy
        
        F_neto = math.sqrt(Fx_neto**2 + Fy_neto**2)
        theta_neto = math.degrees(math.atan2(Fy_neto, Fx_neto))
        
        fuerzas_netas.append({
            'indice': i+1,
            'Fx': Fx_neto,
            'Fy': Fy_neto,
            'F': F_neto,
            'theta': theta_neto,
            'color': cargas[i]['color']
        })
    
    # TABS para resultados
    tab1, tab2, tab3 = st.tabs(["📊 Fuerzas Entre Pares", "🔢 Fuerza Neta por Carga", "🎨 Gráfica 2D"])
    
    # TAB 1: Fuerzas entre pares
    with tab1:
        st.markdown('<div class="section-header">Análisis de Pares de Cargas</div>', unsafe_allow_html=True)
        
        for par in pares_info:
            col_badge, col_content = st.columns([0.8, 4])
            
            with col_badge:
                badge_class = "success-badge" if par['atraccion'] else "warning-badge"
                st.markdown(f'<div class="{badge_class}">{par["tipo"]}</div>', unsafe_allow_html=True)
            
            with col_content:
                st.markdown(f"""
                <div class="result-card {'attraction' if par['atraccion'] else 'repulsion'}">
                    <div class="result-title">Q{par['i']} ↔ Q{par['j']}</div>
                    <p><strong>Distancia (r):</strong> {par['r']:.4f} m</p>
                    <p><strong>Ángulo (θ):</strong> {par['theta']:.2f}°</p>
                    <div class="equation-box">
                    <strong>Magnitud de Fuerza:</strong><br>
                    |F| = K × |Q{par['i']} × Q{par['j']}| / r² = {par['F']:.6f} N
                    </div>
                    <div class="equation-box">
                    <strong>Descomposición Vectorial (θ = {par['theta']:.2f}°):</strong><br>
                    Sobre Q{par['i']}:<br>
                    Fx = {par['Fx']:+.6f} N = {par['F']:.6f} × cos({par['theta']:.2f}°)<br>
                    Fy = {par['Fy']:+.6f} N = {par['F']:.6f} × sin({par['theta']:.2f}°)
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # TAB 2: Fuerza neta
    with tab2:
        st.markdown('<div class="section-header">Fuerza Neta por Carga</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        for idx, fn in enumerate(fuerzas_netas):
            with col1 if idx % 2 == 0 else col2:
                st.markdown(f"""
                <div class="result-card" style="border-left-color: {fn['color']};">
                    <div class="result-title">⚡ Carga {fn['indice']}</div>
                    <div class="result-value">{fn['F']:.6f} N</div>
                    <div class="equation-box">
                    <strong>Componentes:</strong><br>
                    Fx,neto = {fn['Fx']:+.6f} N<br>
                    Fy,neto = {fn['Fy']:+.6f} N<br>
                    θ resultante = {fn['theta']:.2f}°
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # TAB 3: Gráfica 2D - LIMPIA Y MINIMALISTA
    with tab3:
        st.markdown('<div class="section-header">Visualización del Sistema Electrostático</div>', unsafe_allow_html=True)
        
        col_grafica1, col_grafica2 = st.columns(2)
        
        # GRÁFICA 1: Sistema de cargas
        with col_grafica1:
            fig1 = plt.figure(figsize=(10, 10))
            fig1.patch.set_facecolor('#ffffff')
            ax1 = fig1.add_subplot(111)
            ax1.set_facecolor('#ffffff')
            
            # Definir límites automáticos
            x_coords = [c['x'] for c in cargas_coulombs]
            y_coords = [c['y'] for c in cargas_coulombs]
            
            x_min, x_max = min(x_coords) - 2.5, max(x_coords) + 2.5
            y_min, y_max = min(y_coords) - 2.5, max(y_coords) + 2.5
            
            # Hacer los límites cuadrados
            x_range = x_max - x_min
            y_range = y_max - y_min
            max_range = max(x_range, y_range)
            x_center = (x_min + x_max) / 2
            y_center = (y_min + y_max) / 2
            
            x_min = x_center - max_range / 2 - 0.5
            x_max = x_center + max_range / 2 + 0.5
            y_min = y_center - max_range / 2 - 0.5
            y_max = y_center + max_range / 2 + 0.5
            
            # Grid minimalista
            ax1.grid(True, alpha=0.15, linestyle='-', linewidth=0.5, color='#e5e7eb')
            ax1.axhline(0, color='#9ca3af', linewidth=1.5, alpha=0.5, linestyle='-')
            ax1.axvline(0, color='#9ca3af', linewidth=1.5, alpha=0.5, linestyle='-')
            
            # Dibujar SOLO cargas y vectores de fuerza (LIMPIO)
            for c, fn in zip(cargas_coulombs, fuerzas_netas):
                # Círculo de carga - SIN ETIQUETAS ENCIMA
                circle = plt.Circle((c['x'], c['y']), 0.3, color=fn['color'], alpha=0.85, zorder=3, edgecolor='white', linewidth=2)
                ax1.add_patch(circle)
                
                # Símbolo +/-
                signo = '+' if c['q'] > 0 else '−'
                ax1.text(c['x'], c['y'], signo, ha='center', va='center', 
                        color='white', fontsize=18, fontweight='bold', zorder=4)
                
                # Etiqueta BAJO la carga
                ax1.text(c['x'], c['y'] - 0.75, f'Q{c["indice"]}\n{cargas[c["indice"]-1]["q"]:.1f}µC',
                        ha='center', va='top', fontsize=9, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                                 edgecolor=fn['color'], linewidth=1.5, alpha=0.92))
                
                # Vector de fuerza neta
                if fn['F'] > 0.01:
                    escala = min(max_range / 6, 1.2)
                    fx_visual = (fn['Fx'] / (fn['F'] + 1e-9)) * escala
                    fy_visual = (fn['Fy'] / (fn['F'] + 1e-9)) * escala
                    
                    ax1.arrow(c['x'], c['y'], fx_visual, fy_visual,
                             head_width=0.25, head_length=0.2, fc=fn['color'], ec=fn['color'],
                             linewidth=3.5, zorder=2, alpha=0.9)
            
            ax1.set_xlim(x_min, x_max)
            ax1.set_ylim(y_min, y_max)
            ax1.set_aspect('equal')
            ax1.set_xlabel('X (metros)', fontsize=11, fontweight='bold', color='#1a202c')
            ax1.set_ylabel('Y (metros)', fontsize=11, fontweight='bold', color='#1a202c')
            ax1.set_title('Sistema de Cargas', fontsize=13, fontweight='bold', pad=12, color='#1a202c')
            ax1.tick_params(colors='#4b5563', labelsize=9)
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            
            st.pyplot(fig1, use_container_width=True)
        
        # GRÁFICA 2: Descomposición vectorial del primer par
        with col_grafica2:
            if len(pares_info) > 0:
                fig2 = plt.figure(figsize=(10, 10))
                fig2.patch.set_facecolor('#ffffff')
                ax2 = fig2.add_subplot(111)
                ax2.set_facecolor('#ffffff')
                
                par_demo = pares_info[0]
                F = par_demo['F']
                Fx = par_demo['Fx']
                Fy = par_demo['Fy']
                theta_rad = math.radians(par_demo['theta'])
                
                # Normalizar para visualización
                max_comp = max(abs(Fx), abs(Fy), F) + 0.1
                fx_norm = (Fx / max_comp) * 3
                fy_norm = (Fy / max_comp) * 3
                f_norm = (F / max_comp) * 3
                
                # EJES COORDENADOS
                ax2.arrow(0, 0, 4, 0, head_width=0.15, head_length=0.2, fc='#9ca3af', ec='#9ca3af', linewidth=2, zorder=0)
                ax2.arrow(0, 0, 0, 4, head_width=0.15, head_length=0.2, fc='#9ca3af', ec='#9ca3af', linewidth=2, zorder=0)
                ax2.text(4.3, -0.2, 'X', fontsize=12, fontweight='bold', color='#4b5563')
                ax2.text(-0.3, 4.3, 'Y', fontsize=12, fontweight='bold', color='#4b5563')
                
                # VECTOR PRINCIPAL (Morado)
                ax2.arrow(0, 0, fx_norm, fy_norm, head_width=0.2, head_length=0.25, 
                         fc='#a855f7', ec='#a855f7', linewidth=4, zorder=3, alpha=0.9)
                ax2.text(fx_norm*0.5, fy_norm*0.5 + 0.3, 'F', fontsize=11, fontweight='bold', 
                        color='#a855f7', bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.85))
                
                # COMPONENTE X (Azul)
                ax2.arrow(0, 0, fx_norm, 0, head_width=0.15, head_length=0.18, 
                         fc='#3b82f6', ec='#3b82f6', linewidth=3, zorder=2, alpha=0.8)
                ax2.text(fx_norm*0.5, -0.35, f'Fx\n{Fx:.3f}N', fontsize=9, fontweight='bold', 
                        color='#3b82f6', ha='center', bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85))
                
                # COMPONENTE Y (Naranja)
                ax2.arrow(fx_norm, 0, 0, fy_norm, head_width=0.15, head_length=0.18, 
                         fc='#f97316', ec='#f97316', linewidth=3, zorder=2, alpha=0.8)
                ax2.text(fx_norm + 0.4, fy_norm*0.5, f'Fy\n{Fy:.3f}N', fontsize=9, fontweight='bold', 
                        color='#f97316', bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85))
                
                # ARCO DE ÁNGULO (Rojo)
                arc_angle = np.linspace(0, theta_rad, 40)
                arc_r = 0.7
                ax_arc = arc_r * np.cos(arc_angle)
                ay_arc = arc_r * np.sin(arc_angle)
                ax2.plot(ax_arc, ay_arc, color='#ef4444', linewidth=2.5, alpha=0.7, zorder=1)
                
                # Etiqueta del ángulo
                angle_mid = theta_rad / 2
                ax2.text(0.95 * np.cos(angle_mid), 0.95 * np.sin(angle_mid), f'{par_demo["theta"]:.1f}°', 
                        fontsize=11, fontweight='bold', color='#ef4444',
                        bbox=dict(boxstyle='round,pad=0.25', facecolor='white', 
                                 edgecolor='#ef4444', linewidth=1.5, alpha=0.9))
                
                # INFORMACIÓN
                info_text = f'Q{par_demo["i"]} ← Q{par_demo["j"]}\n|F| = {F:.4f} N\nθ = {par_demo["theta"]:.2f}°'
                ax2.text(0.5, 3.5, info_text, fontsize=10, fontweight='bold', 
                        color='#1a202c', bbox=dict(boxstyle='round,pad=0.5', facecolor='#f0f4ff', 
                                                  edgecolor='#667eea', linewidth=2, alpha=0.95))
                
                ax2.set_xlim(-0.8, 4.5)
                ax2.set_ylim(-0.8, 4.5)
                ax2.set_aspect('equal')
                ax2.grid(True, alpha=0.1, linestyle='-', linewidth=0.5, color='#e5e7eb')
                ax2.set_title(f'Descomposición Vectorial', fontsize=13, fontweight='bold', pad=12, color='#1a202c')
                ax2.tick_params(colors='#4b5563', labelsize=9)
                ax2.spines['top'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                
                st.pyplot(fig2, use_container_width=True)
        
        # Leyenda final
        st.markdown('<div class="section-header">📖 Leyenda</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="info-badge">⚡ Círculos de Carga</div>
            Representan las cargas con sus signos (+/−)
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="success-badge">→ Vectores de Fuerza</div>
            Dirección y magnitud de fuerza neta
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="warning-badge">θ Ángulos</div>
            Inclinación respecto al eje X
            """, unsafe_allow_html=True)

st.markdown("""
<div class="footer-text">
    <p>⚡ <strong>Simulador de Fuerza Eléctrica</strong> | Basado en la Ley de Coulomb</p>
    <p>Constante de Coulomb: K = 8.99 × 10⁹ N·m²/C²</p>
</div>
""", unsafe_allow_html=True)
