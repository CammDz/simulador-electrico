import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

# Constante de Coulomb en el vacío (N*m^2/C^2)
K = 8.99e9

st.set_page_config(page_title="Simulador Ley de Coulomb", layout="wide")

# CSS personalizado
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    body {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .hero-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        display: flex;
        align-items: center;
        gap: 20px;
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
    
    .hero-logo {
        font-size: 80px;
        animation: pulse-glow 2s ease-in-out infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% {
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
            transform: scale(1);
        }
        50% {
            text-shadow: 0 0 40px rgba(255, 215, 0, 0.8);
            transform: scale(1.1);
        }
    }
    
    .hero-title {
        color: white;
        font-size: 2.8rem;
        font-weight: 900;
        margin: 0;
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: -1px;
    }
    
    .hero-sub {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin: 5px 0 0 0;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border-left: 5px solid #667eea;
    }
    
    .section-header {
        color: #1e293b;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 30px 0 20px 0;
        font-family: 'Rajdhani', sans-serif;
        padding-bottom: 10px;
        border-bottom: 3px solid #667eea;
    }
    
    .charge-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border-top: 5px solid;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    
    .charge-card:hover {
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        transform: translateY(-5px);
    }
    
    .charge-card.color-1 { border-top-color: #ef4444; }
    .charge-card.color-2 { border-top-color: #3b82f6; }
    .charge-card.color-3 { border-top-color: #f59e0b; }
    .charge-card.color-4 { border-top-color: #10b981; }
    .charge-card.color-5 { border-top-color: #8b5cf6; }
    .charge-card.color-6 { border-top-color: #ec4899; }
    
    .charge-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 15px;
        color: #1e293b;
    }
    
    .input-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin-bottom: 10px;
    }
    
    .btn-calculate {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 18px 40px;
        font-size: 1.15rem;
        font-weight: 600;
        border-radius: 12px;
        cursor: pointer;
        margin: 30px 0;
        width: 100%;
        max-width: 400px;
        display: block;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .btn-calculate:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }
    
    .btn-calculate:active {
        transform: translateY(-2px);
    }
    
    .result-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 15px;
        border-left: 5px solid;
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
    }
    
    .result-card.attraction { border-left-color: #10b981; }
    .result-card.repulsion { border-left-color: #ef4444; }
    
    .result-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 10px;
    }
    
    .result-value {
        font-size: 1.3rem;
        font-weight: 600;
        color: #667eea;
        font-family: 'Rajdhani', monospace;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        border-bottom: 3px solid #e2e8f0;
    }
    
    .stTabs [role="tablist"] button {
        padding: 15px 20px;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 8px 8px 0 0;
        background: #f1f5f9;
        color: #64748b;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [role="tablist"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stTabs [role="tablist"] button:hover {
        background: #e2e8f0;
        color: #1e293b;
    }
    
    .equation-box {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
        font-family: 'Rajdhani', monospace;
        font-size: 0.95rem;
        color: #1e293b;
    }
    
    .info-badge {
        display: inline-block;
        background: #dbeafe;
        color: #1e40af;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 5px 5px 0;
    }
    
    .success-badge {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 5px 5px 0;
    }
    
    .warning-badge {
        display: inline-block;
        background: #fef3c7;
        color: #92400e;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 5px 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# Hero Banner
st.markdown("""
<div class="hero-banner">
    <div class="hero-logo">⚡</div>
    <div>
        <div class="hero-title">Proyecto de Simulador de Fuerza Eléctrica</div>
        <div class="hero-sub">Ley de Coulomb · Cálculo y visualización de fuerzas electrostáticas en sistemas 2D</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Selector de número de cargas
st.markdown('<div class="section-header">⚙️ Configuración del Sistema</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 3])

with col1:
    num_cargas = st.selectbox(
        "Número de cargas a simular:",
        [2, 3, 4, 5, 6],
        index=0,
        help="Selecciona cuántas cargas quieres incluir en la simulación"
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
            <div class="charge-title">⚡ Carga {i+1} ({colores_nombres[i]})</div>
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
st.markdown("""
<div style="text-align: center; margin: 30px 0;">
""", unsafe_allow_html=True)

btn_col = st.columns([1, 2, 1])[1]
with btn_col:
    calcular = st.button("🚀 CALCULAR Y VISUALIZAR", key="btn_calc", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

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
            col_badge, col_content = st.columns([1, 4])
            
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
    
    # TAB 3: Gráfica 2D
    with tab3:
        st.markdown('<div class="section-header">Visualización del Sistema Electrostático</div>', unsafe_allow_html=True)
        
        # Crear figura con dos subplots
        fig = plt.figure(figsize=(18, 8))
        
        # Subplot 1: Sistema completo
        ax1 = plt.subplot(1, 2, 1)
        
        # Definir límites
        x_coords = [c['x'] for c in cargas_coulombs]
        y_coords = [c['y'] for c in cargas_coulombs]
        
        x_min, x_max = min(x_coords) - 2, max(x_coords) + 2
        y_min, y_max = min(y_coords) - 2, max(y_coords) + 2
        
        # Asegurar que los límites sean cuadrados
        x_range = x_max - x_min
        y_range = y_max - y_min
        max_range = max(x_range, y_range)
        
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        
        x_min = x_center - max_range / 2 - 1
        x_max = x_center + max_range / 2 + 1
        y_min = y_center - max_range / 2 - 1
        y_max = y_center + max_range / 2 + 1
        
        # Grid y ejes
        ax1.grid(True, alpha=0.3, linestyle='--', linewidth=0.8)
        ax1.axhline(0, color='#94a3b8', linewidth=1.8, alpha=0.8, linestyle='-')
        ax1.axvline(0, color='#94a3b8', linewidth=1.8, alpha=0.8, linestyle='-')
        
        # Dibujar cargas
        for c, fn in zip(cargas_coulombs, fuerzas_netas):
            # Círculo de carga
            circle = plt.Circle((c['x'], c['y']), 0.25, color=fn['color'], alpha=0.8, zorder=3)
            ax1.add_patch(circle)
            
            # Símbolo +/-
            signo = '+' if c['q'] > 0 else '−'
            ax1.text(c['x'], c['y'], signo, ha='center', va='center', 
                    color='white', fontsize=16, fontweight='bold', zorder=4)
            
            # Etiqueta de carga
            ax1.text(c['x'], c['y'] - 0.6, f'Q{c["indice"]}\n{cargas[c["indice"]-1]["q"]:.1f}µC',
                    ha='center', va='top', fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
            
            # Vector de fuerza neta
            if fn['F'] > 0.01:
                escala = min(max_range / 8, 1.5)
                fx_visual = (fn['Fx'] / (fn['F'] + 1e-9)) * escala
                fy_visual = (fn['Fy'] / (fn['F'] + 1e-9)) * escala
                
                ax1.arrow(c['x'], c['y'], fx_visual, fy_visual,
                         head_width=0.25, head_length=0.2, fc=fn['color'], ec=fn['color'],
                         linewidth=3.5, zorder=2, alpha=0.9)
                
                # Etiqueta de fuerza neta
                ax1.text(c['x'] + fx_visual * 1.3, c['y'] + fy_visual * 1.3,
                        f'F={fn["F"]:.3f}N\nθ={fn["theta"]:.1f}°',
                        ha='center', fontsize=9, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.4', facecolor=fn['color'], 
                                 alpha=0.3, edgecolor=fn['color'], linewidth=2))
        
        # Dibujar líneas entre pares y ángulos
        for par in pares_info:
            c1 = cargas_coulombs[par['i']-1]
            c2 = cargas_coulombs[par['j']-1]
            
            # Línea punteada entre cargas
            ax1.plot([c1['x'], c2['x']], [c1['y'], c2['y']], 'k--', alpha=0.3, linewidth=1.5, zorder=1)
            
            # Distancia en el medio
            mid_x = (c1['x'] + c2['x']) / 2
            mid_y = (c1['y'] + c2['y']) / 2
            ax1.text(mid_x, mid_y + 0.35, f'r={par["r"]:.2f}m', ha='center', fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.6))
            
            # Arco de ángulo
            dx = c2['x'] - c1['x']
            dy = c2['y'] - c1['y']
            angle_rad = math.atan2(dy, dx)
            
            arc_radius = 0.7
            theta_arc = np.linspace(0, angle_rad, 30)
            ax_arc = arc_radius * np.cos(theta_arc) + c1['x']
            ay_arc = arc_radius * np.sin(theta_arc) + c1['y']
            
            ax1.plot(ax_arc, ay_arc, color=cargas[par['i']-1]['color'], linewidth=2.5, alpha=0.7)
            
            # Etiqueta del ángulo
            mid_angle = angle_rad / 2
            label_x = c1['x'] + arc_radius * 1.3 * math.cos(mid_angle)
            label_y = c1['y'] + arc_radius * 1.3 * math.sin(mid_angle)
            ax1.text(label_x, label_y, f'{par["theta"]:.1f}°', fontsize=8, fontweight='bold',
                    color=cargas[par['i']-1]['color'])
        
        ax1.set_xlim(x_min, x_max)
        ax1.set_ylim(y_min, y_max)
        ax1.set_aspect('equal')
        ax1.set_xlabel('X (metros)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Y (metros)', fontsize=12, fontweight='bold')
        ax1.set_title('Sistema Electrostático Completo', fontsize=14, fontweight='bold', pad=15)
        
        # Subplot 2: Diagrama de descomposición del primer par
        if len(pares_info) > 0:
            ax2 = plt.subplot(1, 2, 2)
            
            par_demo = pares_info[0]
            F = par_demo['F']
            Fx = par_demo['Fx']
            Fy = par_demo['Fy']
            theta = math.radians(par_demo['theta'])
            
            # Ejes
            ax2.arrow(0, 0, 4, 0, head_width=0.15, head_length=0.2, fc='#94a3b8', ec='#94a3b8', linewidth=2)
            ax2.arrow(0, 0, 0, 4, head_width=0.15, head_length=0.2, fc='#94a3b8', ec='#94a3b8', linewidth=2)
            ax2.text(4.3, 0, 'X', fontsize=12, fontweight='bold')
            ax2.text(0, 4.3, 'Y', fontsize=12, fontweight='bold')
            
            # Vector principal
            escala_demo = 3 / (max(abs(Fx), abs(Fy)) + 0.1)
            fx_demo = Fx * escala_demo
            fy_demo = Fy * escala_demo
            f_demo = F * escala_demo / max(abs(Fx), abs(Fy), F)
            
            ax2.arrow(0, 0, fx_demo, fy_demo, head_width=0.2, head_length=0.25, 
                     fc='#a855f7', ec='#a855f7', linewidth=4, zorder=3, label='F (Fuerza Total)')
            
            # Componentes
            ax2.arrow(0, 0, fx_demo, 0, head_width=0.15, head_length=0.2, 
                     fc='#3b82f6', ec='#3b82f6', linewidth=3.5, alpha=0.8, linestyle='--', label=f'Fx = {Fx:.4f}N')
            ax2.arrow(fx_demo, 0, 0, fy_demo, head_width=0.15, head_length=0.2, 
                     fc='#f97316', ec='#f97316', linewidth=3.5, alpha=0.8, linestyle='--', label=f'Fy = {Fy:.4f}N')
            
            # Arco de ángulo
            arc_angle = np.linspace(0, theta, 40)
            arc_r = 0.8
            ax_arc_demo = arc_r * np.cos(arc_angle)
            ay_arc_demo = arc_r * np.sin(arc_angle)
            ax2.plot(ax_arc_demo, ay_arc_demo, 'r-', linewidth=2.5, label=f'θ = {par_demo["theta"]:.2f}°')
            
            # Etiqueta del ángulo
            angle_label_x = 1.1 * np.cos(theta / 2)
            angle_label_y = 1.1 * np.sin(theta / 2)
            ax2.text(angle_label_x, angle_label_y, f'{par_demo["theta"]:.2f}°', fontsize=11, fontweight='bold', color='red')
            
            # Ecuaciones
            ax2.text(0.5, -1.5, f'Fx = F × cos(θ) = {F:.4f} × cos({par_demo["theta"]:.2f}°) = {Fx:.4f} N',
                    fontsize=10, fontweight='bold', color='#3b82f6',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='#dbeafe', alpha=0.8))
            
            ax2.text(0.5, -2.3, f'Fy = F × sin(θ) = {F:.4f} × sin({par_demo["theta"]:.2f}°) = {Fy:.4f} N',
                    fontsize=10, fontweight='bold', color='#f97316',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='#fed7aa', alpha=0.8))
            
            ax2.set_xlim(-1.5, 5)
            ax2.set_ylim(-3, 5)
            ax2.set_aspect('equal')
            ax2.grid(True, alpha=0.2, linestyle='--')
            ax2.set_title(f'Descomposición de Fuerza (Q{par_demo["i"]} ← Q{par_demo["j"]})', 
                         fontsize=14, fontweight='bold', pad=15)
            ax2.legend(loc='upper right', fontsize=10, framealpha=0.95)
            ax2.set_facecolor('#f8f9fa')
        
        plt.tight_layout(pad=2.0)
        st.pyplot(fig, use_container_width=True)
        
        # Leyenda final
        st.markdown('<div class="section-header">📖 Leyenda</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="info-badge">⚡ Círculos de Carga</div>
            Tamaño proporcional a la magnitud (mostrado con +/−)
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="success-badge">→ Vectores de Fuerza</div>
            Dirección y magnitud de la fuerza neta sobre cada carga
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="warning-badge">θ Ángulos</div>
            Ángulos de inclinación de cada fuerza respecto al eje X
            """, unsafe_allow_html=True)

st.markdown("""
---
<div style="text-align: center; color: #64748b; font-size: 0.9rem; margin-top: 40px;">
    <p>⚡ <strong>Simulador de Fuerza Eléctrica</strong> | Basado en la Ley de Coulomb</p>
    <p>Constante de Coulomb: K = 8.99 × 10⁹ N·m²/C²</p>
</div>
""", unsafe_allow_html=True)
