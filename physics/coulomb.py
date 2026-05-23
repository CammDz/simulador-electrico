import math
from utils.validators import validate_positions, validate_distances

K = 8.99e9


def calcular_pares(cargas, cargas_coulombs):
    validate_positions(cargas)
    validate_distances(cargas_coulombs)

    pares_info = []
    for i in range(len(cargas_coulombs)):
        for j in range(i + 1, len(cargas_coulombs)):
            c1, c2 = cargas_coulombs[i], cargas_coulombs[j]
            dx = c2['x'] - c1['x']
            dy = c2['y'] - c1['y']
            r = math.sqrt(dx**2 + dy**2)
            theta_rad = math.atan2(dy, dx)
            theta_deg = math.degrees(theta_rad)
            F = K * abs(c1['q'] * c2['q']) / (r**2)
            Fx = F * math.cos(theta_rad)
            Fy = F * math.sin(theta_rad)
            atraccion = (c1['q'] * c2['q']) < 0
            tipo = "Atracción" if atraccion else "Repulsión"
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
                'atraccion': atraccion,
            })
    return pares_info


def calcular_fuerzas_netas(cargas_coulombs):
    fuerzas_netas = []
    for i in range(len(cargas_coulombs)):
        Fx_neto = Fy_neto = 0.0
        for j in range(len(cargas_coulombs)):
            if i == j:
                continue
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
            'indice': i + 1,
            'Fx': Fx_neto,
            'Fy': Fy_neto,
            'F': F_neto,
            'theta': theta_neto,
            'color': cargas_coulombs[i]['color'],
        })
    return fuerzas_netas
