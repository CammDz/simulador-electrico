import math


def validate_positions(cargas):
    posiciones = [(c['x'], c['y']) for c in cargas]
    if len(posiciones) != len(set(posiciones)):
        raise ValueError("Dos o más cargas ocupan la misma posición.")


def validate_distances(cargas_coulombs, min_dist=0.01):
    for i in range(len(cargas_coulombs)):
        for j in range(i + 1, len(cargas_coulombs)):
            c1, c2 = cargas_coulombs[i], cargas_coulombs[j]
            dx = c2['x'] - c1['x']
            dy = c2['y'] - c1['y']
            r = math.sqrt(dx**2 + dy**2)
            if r < min_dist:
                raise ValueError(
                    f"Error: Cargas {c1['indice']} y {c2['indice']} están demasiado cerca."
                )


def safe_max(values, default=0):
    return max(values) if values else default


def safe_min(values, default=0):
    return min(values) if values else default


def safe_max_by_key(items, key, default=None):
    return max(items, key=key) if items else default


def safe_min_by_key(items, key, default=None):
    return min(items, key=key) if items else default


def safe_mean(values, default=0):
    return sum(values) / len(values) if values else default
