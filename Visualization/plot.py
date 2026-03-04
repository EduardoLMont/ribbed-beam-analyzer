import matplotlib.pyplot as plt
import numpy as np
from core.mechanics import stress_distribution
# -----------------------------
#STATIC DASHBOARD FUNCTION
# -----------------------------
def plot_dashboard(h_opt, I_total, y_bar, total_height, rib_heights, optimal_thickness, masses, config):

    fig = plt.figure(figsize=(14, 10))

    # ---------------------------------
    # 1) CROSS SECTION
    # ---------------------------------
    ax1 = fig.add_subplot(2, 2, 1)

    ax1.add_patch(plt.Rectangle((0, 0), config.b_plate, h_opt, fill=False))

    rib_x = (config.b_plate - config.rib_thickness) / 2
    ax1.add_patch(plt.Rectangle((rib_x, h_opt), config.rib_thickness, config.rib_height, fill=False))

    ax1.axhline(y=y_bar, linestyle="--")
    ax1.set_xlim(0, config.b_plate)
    ax1.set_ylim(0, total_height)
    ax1.set_title("Cross Section")
    ax1.set_aspect('equal', adjustable='box')


    # ---------------------------------
    # 2) DEFLECTION CURVE
    # ---------------------------------
    ax2 = fig.add_subplot(2, 2, 2)

    x = np.linspace(0, config.L, 200)
    delta_curve = config.P * x**2 * (3*config.L - x) / (6 * config.E * I_total)

    ax2.plot(x, delta_curve * 1000)
    ax2.set_title("Deflection Curve")
    ax2.set_xlabel("Length (m)")
    ax2.set_ylabel("Deflection (mm)")

    # ---------------------------------
    # 3) STRESS DISTRIBUTION
    # ---------------------------------
    ax3 = fig.add_subplot(2, 2, 3)
    
    y_vals, sigma_vals = stress_distribution(I_total, y_bar, total_height, config)

    ax3.plot(sigma_vals / 1e6, y_vals)
    ax3.axhline(y=y_bar, linestyle="--")
    ax3.set_title("Stress Distribution")
    ax3.set_xlabel("Stress (MPa)")
    ax3.set_ylabel("Height (m)")

    # ---------------------------------
    # 4) PARAMETRIC STUDY
    # ---------------------------------
    ax4 = fig.add_subplot(2, 2, 4)

    ax4.plot(rib_heights, np.array(optimal_thickness) * 1000)
    ax4.set_title("Rib Height vs Required Plate Thickness")
    ax4.set_xlabel("Rib Height (m)")
    ax4.set_ylabel("Plate Thickness (mm)")

    plt.tight_layout()
    plt.show()
