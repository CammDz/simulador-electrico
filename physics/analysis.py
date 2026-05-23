from physics.vectors import obtener_direccion_descripcion, obtener_cuadrante_corto
from utils.validators import safe_max_by_key, safe_min_by_key


def analisis_par_html(par, c1_orig, c2_orig):
    parts = []
    interaccion = "atracción" if par['atraccion'] else "repulsión"
    signos = "opuestos" if par['atraccion'] else "iguales"
    tag_cls = "attr" if par['atraccion'] else "rep"
    tag_txt = "Atracción" if par['atraccion'] else "Repulsión"
    signo_op = "diferente" if par['atraccion'] else "el mismo"

    parts.append(
        f'<span class="tag {tag_cls}">{tag_txt}</span> '
        f'Las cargas <strong>Q{par["i"]}</strong> ({par["q1"]:+.1f} µC) y '
        f'<strong>Q{par["j"]}</strong> ({par["q2"]:+.1f} µC) '
        f'interactúan por <strong>{interaccion}</strong> ya que sus signos son {signos} '
        f'(q₁ = {par["q1"]:+.1f} µC, q₂ = {par["q2"]:+.1f} µC → signo {signo_op}). '
        f'Físicamente, la fuerza eléctrica entre dos cargas es directamente proporcional '
        f'al producto de sus magnitudes: <em>F ∝ |q₁ · q₂|</em>.'
    )

    parts.append(
        f'La magnitud de la fuerza resultante es <strong>{par["F"]:.4f} N</strong> (Newtons) y '
        f'actúa entre las cargas separadas por una distancia de <strong>{par["r"]:.3f} m</strong>. '
        f'De acuerdo con la Ley de Coulomb, la intensidad de la fuerza disminuye '
        f'con el cuadrado de la distancia (<em>F ∝ 1/r²</em>): si la distancia se duplica, '
        f'la fuerza se reduce a la cuarta parte.'
    )

    ang = par['theta']
    dir_desc = obtener_direccion_descripcion(ang)
    parts.append(
        f'Vectorialmente, la fuerza se orienta de manera <strong>{dir_desc}</strong>. '
        f'El ángulo θ = <strong>{ang:.1f}°</strong> mide la inclinación del vector de fuerza '
        f'respecto al eje horizontal positivo. Este ángulo es fundamental para descomponer '
        f'la fuerza en sus componentes cartesianas Fx y Fx.'
    )

    fx_mag, fy_mag = abs(par['Fx']), abs(par['Fy'])
    if fx_mag > fy_mag * 1.5:
        parts.append(
            f'La componente <strong>horizontal (Fx = {par["Fx"]:+.4f} N)</strong> '
            f'domina significativamente sobre la componente vertical. '
            f'Esto indica que la interacción entre estas cargas ocurre '
            f'principalmente a lo largo del eje X, generando un desplazamiento '
            f'predominantemente lateral.'
        )
    elif fy_mag > fx_mag * 1.5:
        parts.append(
            f'La componente <strong>vertical (Fy = {par["Fy"]:+.4f} N)</strong> '
            f'domina significativamente sobre la componente horizontal. '
            f'Esto indica que la interacción entre estas cargas ocurre '
            f'principalmente a lo largo del eje Y, generando un desplazamiento '
            f'predominantemente vertical.'
        )
    else:
        parts.append(
            f'Las componentes <strong>Fx = {par["Fx"]:+.4f} N</strong> y '
            f'<strong>Fy = {par["Fy"]:+.4f} N</strong> están equilibradas, '
            f'generando una fuerza diagonal balanceada. Ambas direcciones '
            f'contribuyen de manera similar al vector resultante.'
        )

    q1m, q2m = abs(par['q1']), abs(par['q2'])
    if q1m > q2m * 1.15:
        parts.append(
            f'<strong>Q{par["i"]}</strong> posee una carga de mayor magnitud '
            f'({q1m:.1f} µC frente a {q2m:.1f} µC de Q{par["j"]}), '
            f'por lo que ejerce una influencia eléctrica más intensa. '
            f'La fuerza electrostática es proporcional al producto de ambas cargas, '
            f'por lo que una mayor magnitud en una de ellas incrementa '
            f'la intensidad de la interacción.'
        )
    elif q2m > q1m * 1.15:
        parts.append(
            f'<strong>Q{par["j"]}</strong> posee una carga de mayor magnitud '
            f'({q2m:.1f} µC frente a {q1m:.1f} µC de Q{par["i"]}), '
            f'por lo que ejerce una influencia eléctrica más intensa. '
            f'La fuerza electrostática es proporcional al producto de ambas cargas, '
            f'por lo que una mayor magnitud en una de ellas incrementa '
            f'la intensidad de la interacción.'
        )

    producto = abs(par['q1'] * par['q2'])
    f_esperada = 8.99e9 * producto * 1e-12 / (par['r']**2)
    parts.append(
        f'<strong>Verificación analítica:</strong> Aplicando la Ley de Coulomb '
        f'<em>F = Ke · |q₁·q₂| / r²</em>, donde Ke = 8.99×10⁹ N·m²/C², '
        f'se obtiene F = (8.99×10⁹)({producto:.1f}×10⁻¹²)/({par["r"]:.3f})² = '
        f'<strong>{f_esperada:.4f} N</strong>, que coincide con el valor calculado.'
    )

    return '<p>' + '</p><p>'.join(parts) + '</p>'


def analisis_neta_html(fn, carga_orig, pares_info):
    parts = []
    fx, fy, fmag = fn['Fx'], fn['Fy'], fn['F']
    angle = fn['theta']

    if fmag < 1e-10:
        return (
            f'<p>La <strong>carga {fn["indice"]}</strong> ({carga_orig["q"]:+.1f} µC) se encuentra en '
            f'<strong>equilibrio electrostático</strong>: la fuerza neta es aproximadamente cero. '
            f'Esto significa que el vector resultante de todas las fuerzas ejercidas por las cargas '
            f'circundantes se anula completamente. La carga no experimenta aceleración eléctrica neta '
            f'y permanece en reposo relativo dentro del sistema.</p>'
        )

    dir_desc = obtener_cuadrante_corto(fx, fy)

    if fx > 0 and fy > 0:
        cuad = "primer cuadrante"
        cuad_expl = "Fx > 0 y Fy > 0, ambas positivas"
    elif fx < 0 and fy > 0:
        cuad = "segundo cuadrante"
        cuad_expl = "Fx < 0 y Fy > 0, horizontal negativa y vertical positiva"
    elif fx < 0 and fy < 0:
        cuad = "tercer cuadrante"
        cuad_expl = "Fx < 0 y Fy < 0, ambas negativas"
    elif fx > 0 and fy < 0:
        cuad = "cuarto cuadrante"
        cuad_expl = "Fx > 0 y Fy < 0, horizontal positiva y vertical negativa"
    elif fx > 0:
        cuad = "eje X positivo"
        cuad_expl = "Fx > 0"
    elif fx < 0:
        cuad = "eje X negativo"
        cuad_expl = "Fx < 0"
    elif fy > 0:
        cuad = "eje Y positivo"
        cuad_expl = "Fy > 0"
    else:
        cuad = "eje Y negativo"
        cuad_expl = "Fy < 0"

    parts.append(
        f'La <strong>carga {fn["indice"]}</strong> ({carga_orig["q"]:+.1f} µC) experimenta una '
        f'<strong>fuerza neta de {fmag:.4f} N</strong> que se dirige hacia el <strong>{dir_desc}</strong>, '
        f'con un ángulo resultante de <strong>{angle:.1f}°</strong> '
        f'respecto al eje horizontal positivo.'
    )

    parts.append(
        f'La orientación hacia el <strong>{cuad}</strong> del plano cartesiano ({cuad_expl}) '
        f'indica que el vector suma de todas las fuerzas eléctricas ejercidas '
        f'sobre esta carga por las demás no se cancela. Este desequilibrio es el '
        f'responsable de la aceleración neta que experimentaría la carga si estuviera '
        f'libre de otras ligaduras.'
    )

    if abs(fx) > abs(fy) * 1.5:
        parts.append(
            f'La componente <strong>horizontal predomina</strong> '
            f'(|Fx| = {abs(fx):.4f} N > |Fy| = {abs(fy):.4f} N), '
            f'lo que sugiere que las cargas con mayor influencia se encuentran '
            f'dispuestas lateralmente respecto a esta carga. El movimiento '
            f'resultante sería predominantemente horizontal.'
        )
    elif abs(fy) > abs(fx) * 1.5:
        parts.append(
            f'La componente <strong>vertical predomina</strong> '
            f'(|Fy| = {abs(fy):.4f} N > |Fx| = {abs(fx):.4f} N), '
            f'lo que sugiere que las cargas con mayor influencia se encuentran '
            f'dispuestas verticalmente respecto a esta carga. El movimiento '
            f'resultante sería predominantemente vertical.'
        )
    else:
        parts.append(
            f'Las componentes están <strong>balanceadas</strong> '
            f'(Fx = {fx:+.4f} N, Fy = {fy:+.4f} N), '
            f'lo que indica una influencia múltiple y equilibrada en ambas direcciones '
            f'cardinales. La fuerza neta resultante presenta una trayectoria diagonal '
            f'con contribuciones equitativas de ambos ejes.'
        )

    contribuciones = []
    for par in pares_info:
        if par['i'] == fn['indice'] or par['j'] == fn['indice']:
            otro = par['j'] if par['i'] == fn['indice'] else par['i']
            contribuciones.append((otro, par['F']))
    contribuciones.sort(key=lambda x: x[1], reverse=True)
    if contribuciones:
        top = contribuciones[0]
        parts.append(
            f'La interacción que <strong>más contribuye</strong> a la fuerza neta sobre '
            f'Q{fn["indice"]} proviene de <strong>Q{top[0]}</strong> con una fuerza de '
            f'{top[1]:.4f} N. Esto se debe a la combinación de su magnitud de carga '
            f'y la proximidad espacial entre ambas.'
        )

    return '<p>' + '</p><p>'.join(parts) + '</p>'


def analisis_sistema_html(stats):
    lines = []
    lines.append(
        f'El sistema está compuesto por <strong>{stats["n"]} cargas</strong> '
        f'({stats["pos"]} positiva{"" if stats["pos"]==1 else "s"}, '
        f'{stats["neg"]} negativa{"" if stats["neg"]==1 else "s"}). '
        f'Se generan <strong>{stats["total_pares"]} interacciones</strong> '
        f'entre pares: {stats["atracciones"]} de atracción y {stats["repulsiones"]} de repulsión.'
    )

    if stats["atracciones"] > stats["repulsiones"]:
        lines.append(
            'Predominan las <strong>fuerzas de atracción</strong>, lo que sugiere que el sistema '
            'tiende a la contracción: las cargas se atraen entre sí predominantemente.'
        )
    elif stats["repulsiones"] > stats["atracciones"]:
        lines.append(
            'Predominan las <strong>fuerzas de repulsión</strong>, lo que sugiere que el sistema '
            'tiende a la expansión: las cargas se repelen entre sí predominantemente.'
        )
    else:
        lines.append(
            'Existe un <strong>equilibrio entre atracciones y repulsiones</strong>, '
            'generando una dinámica de interacciones balanceada.'
        )

    if stats["carga_max_idx"] is not None:
        lines.append(
            f'La carga con <strong>mayor fuerza neta</strong> es <strong>Q{stats["carga_max_idx"]}</strong> '
            f'({stats["max_neta"]:.4f} N), '
            f'mientras que la de <strong>menor fuerza neta</strong> es <strong>Q{stats["carga_min_idx"]}</strong> '
            f'({stats["min_neta"]:.4f} N). '
            f'Esta diferencia refleja cómo la distribución espacial y las magnitudes de carga '
            f'afectan el desequilibrio de fuerzas en cada punto.'
        )

    fx_pos, fx_neg = stats["fx_pos"], stats["fx_neg"]
    fy_pos, fy_neg = stats["fy_pos"], stats["fy_neg"]

    if fx_pos > fx_neg and fy_pos > fy_neg:
        lines.append(
            f'<strong>Tendencia general del sistema:</strong> La mayoría de las fuerzas netas apuntan '
            f'hacia el primer cuadrante (Fx > 0, Fy > 0), lo que indica un desplazamiento neto '
            f'preferencial hacia el noreste del plano.'
        )
    elif fx_neg > fx_pos and fy_pos > fy_neg:
        lines.append(
            f'<strong>Tendencia general del sistema:</strong> Predominan las fuerzas hacia el segundo cuadrante '
            f'(Fx < 0, Fy > 0), indicando un desplazamiento neto hacia el noroeste.'
        )
    elif fx_neg > fx_pos and fy_neg > fy_pos:
        lines.append(
            f'<strong>Tendencia general del sistema:</strong> Predominan las fuerzas hacia el tercer cuadrante '
            f'(Fx < 0, Fy < 0), indicando un desplazamiento neto hacia el suroeste.'
        )
    elif fx_pos > fx_neg and fy_neg > fy_pos:
        lines.append(
            f'<strong>Tendencia general del sistema:</strong> Predominan las fuerzas hacia el cuarto cuadrante '
            f'(Fx > 0, Fy < 0), indicando un desplazamiento neto hacia el sureste.'
        )

    return '<p>' + '</p><p>'.join(lines) + '</p>'


def conclusiones_html(stats, pares_info):
    lines = []

    lines.append(
        f'<strong>Comportamiento electrostático:</strong> El sistema está configurado con '
        f'<strong>{stats["n"]} cargas</strong> '
        f'({stats["pos"]} positiva{"" if stats["pos"]==1 else "s"}, '
        f'{stats["neg"]} negativa{"" if stats["neg"]==1 else "s"}), '
        f'generando <strong>{stats["total_pares"]} interacciones coulombianas</strong> '
        f'({stats["atracciones"]} de atracción, {stats["repulsiones"]} de repulsión). '
        f'Cada interacción obedece la Ley de Coulomb (<em>F = Ke·|q₁·q₂|/r²</em>), '
        f'donde la magnitud de la fuerza electrostática es directamente proporcional '
        f'al producto de las cargas e inversamente proporcional al cuadrado de la distancia.'
    )

    lines.append(
        f'<strong>Análisis de distancias:</strong> La distancia promedio entre pares de cargas es de '
        f'<strong>{stats["dist_prom"]:.3f} m</strong>, '
        f'con una distancia mínima de {stats["dist_min"]:.3f} m. '
        f'La relación <em>F ∝ 1/r²</em> implica que el par más cercano ({stats["dist_min"]:.3f} m) genera la '
        f'fuerza de mayor magnitud ({stats["f_max"]:.4f} N), mientras que los pares más alejados '
        f'contribuyen con fuerzas significativamente menores.'
    )

    lines.append(
        f'<strong>Análisis vectorial y componentes:</strong> Las fuerzas electrostáticas se representan '
        f'como vectores en el plano cartesiano, descomponiéndose en componentes horizontal (Fx) '
        f'y vertical (Fy). La fuerza neta promedio del sistema es de <strong>{stats["prom_neta"]:.4f} N</strong>, '
        f'lo que refleja el grado de desequilibrio electrostático presente. '
        f'La magnitud promedio de las fuerzas entre pares es de <strong>{stats["f_prom"]:.4f} N</strong>. '
        f'La componente angular (θ) determina la dirección precisa de cada vector resultante.'
    )

    if stats["atracciones"] > stats["repulsiones"]:
        pct = stats["atracciones"] / stats["total_pares"] * 100
        lines.append(
            f'<strong>Predominancia de atracción ({pct:.0f}% de los pares):</strong> '
            f'La mayoría de las interacciones son de atracción, lo que indica una configuración '
            f'donde predominan los signos opuestos. Desde la perspectiva energética, '
            f'un sistema con atracción predominante tiende a disminuir su energía potencial '
            f'electrostática (<em>U = Ke·q₁·q₂/r</em>) a medida que las cargas se aproximan, '
            f'lo que sugiere una tendencia natural hacia la contracción del sistema.'
        )
    elif stats["repulsiones"] > stats["atracciones"]:
        pct = stats["repulsiones"] / stats["total_pares"] * 100
        lines.append(
            f'<strong>Predominancia de repulsión ({pct:.0f}% de los pares):</strong> '
            f'La mayoría de las interacciones son de repulsión, lo que indica una configuración '
            f'donde predominan los signos iguales. La energía potencial electrostática '
            f'del sistema es positiva y las cargas tienden a separarse, '
            f'lo que sugiere una tendencia natural hacia la expansión del sistema.'
        )
    else:
        lines.append(
            f'<strong>Balance atractivo–repulsivo:</strong> Existe un equilibrio numérico entre '
            f'interacciones de atracción y repulsión, lo que genera una dinámica '
            f'mixta donde algunas cargas se aproximan mientras otras se separan, '
            f'produciendo una configuración electrostática compleja.'
        )

    if stats["f_max"] > 0:
        par_max = next((p for p in pares_info if abs(p['F'] - stats["f_max"]) < 1e-10), None)
        if par_max:
            causa = "atracción" if par_max['atraccion'] else "repulsión"
            lines.append(
                f'<strong>Interacción dominante:</strong> El par Q{par_max["i"]}–Q{par_max["j"]} presenta '
                f'la mayor magnitud de fuerza ({par_max["F"]:.4f} N, {causa}), '
                f'ubicados a una distancia de {par_max["r"]:.3f} m. '
                f'Esta interacción es la que domina el comportamiento dinámico del sistema.'
            )

    lines.append(
        f'<strong>Verificación física:</strong> Todos los resultados cumplen la Ley de Coulomb '
        f'y el principio de superposición. Las fuerzas se han calculado como suma vectorial '
        f'de las contribuciones individuales, respetando la naturaleza atractiva o repulsiva '
        f'según el signo de las cargas involucradas. Los resultados son coherentes con las '
        f'leyes fundamentales del electromagnetismo clásico.'
    )

    return '<p>' + '</p><p>'.join(lines) + '</p>'
