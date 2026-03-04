from .section import composite_section
import numpy as np


# -----------------------------
# STRUCTURAL RESPONSE FUNCTION
# -----------------------------
def structural_response(h_plate, config):

    I_total, y_bar, total_height = composite_section(h_plate, config.b_plate, config.rib_height, config.rib_thickness)

    P = config.P
    L = config.L
    E = config.E
    yield_strength = config.yield_strength
    Kt = config.Kt

    M = P * L

    c= max(y_bar, total_height - y_bar)

    sigma = M * c / I_total
    tau = 1.5 * P / (config.b_plate * h_plate)

    sigma_vm = np.sqrt(sigma**2 + 3 * tau**2)
    sigma_real = Kt * sigma_vm

    SF = yield_strength / sigma_real

    delta = P * L**3 / (3 * E * I_total)

    volume = (L * config.b_plate * h_plate + L * config.rib_thickness * config.rib_height)

    mass = volume * config.density

    return SF, delta, mass, I_total, y_bar, total_height


# -----------------------------
# STRESS DISTRIBUTION FUNCTION
# -----------------------------
def stress_distribution(I_total, y_bar, total_height, config):

    M = config.P * config.L

    y_vals = np.linspace(0, total_height, 300)
    sigma_vals = M * (y_vals - y_bar) / I_total

    return y_vals, sigma_vals


# -----------------------------
# BUCKLING CALCULATION
# -----------------------------
def buckling_load(I_total, config):

    E = config.E
    L = config.L
    K = 2  # Cantilever

    Pcr = (np.pi**2 * E * I_total) / ((K * L)**2)

    return Pcr