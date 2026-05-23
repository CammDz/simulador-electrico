def format_force(value, decimals=4):
    return f"{value:+.{decimals}f} N"

def format_charge(value):
    return f"{value:+.2f} µC"

def format_angle(value, decimals=1):
    return f"{value:.{decimals}f}°"

def format_distance(value, decimals=3):
    return f"{value:.{decimals}f} m"

def format_force_mag(value, decimals=4):
    return f"{value:.{decimals}f} N"
