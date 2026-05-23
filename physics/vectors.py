import math


def obtener_cuadrante(fx, fy):
    if fx > 0 and fy > 0:
        return ("noreste (primer cuadrante)", 1, "Fx > 0 y Fy > 0, ambas positivas")
    elif fx < 0 and fy > 0:
        return ("noroeste (segundo cuadrante)", 2, "Fx < 0 y Fy > 0, horizontal negativa y vertical positiva")
    elif fx < 0 and fy < 0:
        return ("suroeste (tercer cuadrante)", 3, "Fx < 0 y Fy < 0, ambas negativas")
    elif fx > 0 and fy < 0:
        return ("sureste (cuarto cuadrante)", 4, "Fx > 0 y Fy < 0, horizontal positiva y vertical negativa")
    elif fx > 0:
        return ("este (horizontal derecha)", 0, "Fx > 0")
    elif fx < 0:
        return ("oeste (horizontal izquierda)", 0, "Fx < 0")
    elif fy > 0:
        return ("norte (vertical arriba)", 0, "Fy > 0")
    else:
        return ("sur (vertical abajo)", 0, "Fy < 0")


def obtener_cuadrante_corto(fx, fy):
    nombre, _, _ = obtener_cuadrante(fx, fy)
    return nombre


def obtener_direccion_descripcion(ang):
    ang_abs = abs(ang)
    if ang_abs < 15:
        if ang >= 0:
            return "predominantemente horizontal hacia la derecha"
        return "predominantemente horizontal hacia la izquierda"
    elif ang_abs > 75:
        if ang > 0:
            return "predominantemente vertical hacia arriba"
        return "predominantemente vertical hacia abajo"
    else:
        if ang > 0:
            return f"diagonal ascendente ({ang:.1f}° sobre la horizontal)"
        return f"diagonal descendente ({abs(ang):.1f}° bajo la horizontal)"


def obtener_componente_dominante(fx, fy):
    if abs(fx) > abs(fy) * 1.5:
        return "Horizontal (Fx)", fx
    elif abs(fy) > abs(fx) * 1.5:
        return "Vertical (Fy)", fy
    return "Balanceada", None


def obtener_direccion_neta_descripcion(fx, fy):
    nombre = obtener_cuadrante_corto(fx, fy)
    return nombre


def descomposicion_vectorial(F, theta_deg):
    theta_rad = math.radians(theta_deg)
    Fx = F * math.cos(theta_rad)
    Fy = F * math.sin(theta_rad)
    return Fx, Fy, theta_rad
