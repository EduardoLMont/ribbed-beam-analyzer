import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation


# -----------------------------
# SECTION PROPERTIES FUNCTION
# -----------------------------
def composite_section(h_plate, b_plate, rib_height, rib_thickness):

    # Areas
    A1 = b_plate * h_plate
    A2 = rib_thickness * rib_height

    # Centroids from bottom
    y1 = h_plate / 2
    y2 = h_plate + rib_height / 2

    # Neutral axis
    y_bar = (A1*y1 + A2*y2) / (A1 + A2)

    # Local inertias
    I1 = (b_plate * h_plate**3) / 12
    I2 = (rib_thickness * rib_height**3) / 12

    # Parallel axis theorem
    I_total = (
        I1 + A1*(y_bar - y1)**2 +
        I2 + A2*(y2 - y_bar)**2
    )

    total_height = h_plate + rib_height

    return I_total, y_bar, total_height


# -----------------------------
# STRUCTURAL RESPONSE FUNCTION
# -----------------------------
def structural_response(h_plate, params):

    I_total, y_bar, total_height = composite_section(h_plate, params["b_plate"], params["rib_height"], params["rib_thickness"])

    P = params["P"]
    L = params["L"]
    E = params["E"]
    yield_strength = params["yield_strength"]
    Kt = params["Kt"]

    M = P * L

    c= max(y_bar, total_height - y_bar)

    sigma = M * c / I_total
    tau = 1.5 * P / (params["b_plate"] * h_plate)

    sigma_vm = np.sqrt(sigma**2 + 3 * tau**2)
    sigma_real = Kt * sigma_vm

    SF = yield_strength / sigma_real

    delta = P * L**3 / (3 * E * I_total)

    volume = (L * params["b_plate"] * h_plate + L * params["rib_thickness"] * params["rib_height"])

    mass = volume * params["density"]

    return SF, delta, mass, I_total, y_bar, total_height


# -----------------------------
# STRESS DISTRIBUTION FUNCTION
# -----------------------------
def stress_distribution(I_total, y_bar, total_height, params):

    M = params["P"] * params["L"]

    y_vals = np.linspace(0, total_height, 300)
    sigma_vals = M * (y_vals - y_bar) / I_total

    return y_vals, sigma_vals


# -----------------------------
# BUCKLING CALCULATION
# -----------------------------
def buckling_load(I_total, params):

    E = params["E"]
    L = params["L"]
    K = 2  # Cantilever

    Pcr = (np.pi**2 * E * I_total) / ((K * L)**2)

    return Pcr


# -----------------------------
#STATIC DASHBOARD FUNCTION
# -----------------------------
def plot_dashboard(h_opt, I_total, y_bar, total_height, rib_heights, optimal_thickness, masses, params):

    fig = plt.figure(figsize=(14, 10))

    # ---------------------------------
    # 1) CROSS SECTION
    # ---------------------------------
    ax1 = fig.add_subplot(2, 2, 1)

    ax1.add_patch(plt.Rectangle((0, 0), params["b_plate"], h_opt, fill=False))

    rib_x = (params["b_plate"] - params["rib_thickness"]) / 2
    ax1.add_patch(plt.Rectangle((rib_x, h_opt), params["rib_thickness"], params["rib_height"], fill=False))

    ax1.axhline(y=y_bar, linestyle="--")
    ax1.set_xlim(0, params["b_plate"])
    ax1.set_ylim(0, total_height)
    ax1.set_title("Cross Section")
    ax1.set_aspect('equal', adjustable='box')


    # ---------------------------------
    # 2) DEFLECTION CURVE
    # ---------------------------------
    ax2 = fig.add_subplot(2, 2, 2)

    x = np.linspace(0, params["L"], 200)
    delta_curve = params["P"] * x**2 * (3*params["L"] - x) / (6 * params["E"] * I_total)

    ax2.plot(x, delta_curve * 1000)
    ax2.set_title("Deflection Curve")
    ax2.set_xlabel("Length (m)")
    ax2.set_ylabel("Deflection (mm)")

    # ---------------------------------
    # 3) STRESS DISTRIBUTION
    # ---------------------------------
    ax3 = fig.add_subplot(2, 2, 3)
    
    y_vals, sigma_vals = stress_distribution(I_total, y_bar, total_height, params)

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


# ---------------------------------
# ANIMATION WINDOW
# ---------------------------------
def animate_buckling(I_total, params):

    x = np.linspace(0, params["L"], 200)

    fig, ax = plt.subplots()
    line, = ax.plot([], [])

    ax.set_xlim(0, params["L"])
    ax.set_ylim(-0.02, 0.02)
    ax.set_title("Buckling Animation")
    ax.set_xlabel("Length (m)")
    ax.set_ylabel("Lateral Deflection (m)")

    def update(frame):
        A = 0.01 * np.sin(frame / 10)

        bending = params["P"] * x**2 * (3*params["L"] - x) / (6 * params["E"] * I_total)
        buckling = A * (1 - np.cos(np.pi * x / (2 * params["L"])))

        y = bending + buckling

        line.set_data(x, y)
        return line,

    ani = matplotlib.animation.FuncAnimation(fig, update, frames=200, interval=30)
    plt.show()


# -----------------------------
# PARAMETERS
# -----------------------------
params = {
    "P": 800,
    "L": 0.2,
    "b_plate": 0.04,
    "rib_height": 0.10,
    "rib_thickness": 0.006,
    "E": 200e9,
    "yield_strength": 250e6,
    "density": 7850,
    "Kt": 2
}

safety_factor_target = 2
delta_limit = 0.002

thickness_range = np.linspace(0.002, 0.02, 200)

valid_designs = []


# -----------------------------
# OPTIMIZATION LOOP
# -----------------------------
for h in thickness_range:

    SF, delta, mass, I_total, y_bar, total_height = structural_response(h, params)

    if SF >= safety_factor_target and delta <= delta_limit:
        valid_designs.append((h, SF, delta, mass))


# -----------------------------
# PARAMETRIC STUDY: Rib Height
# -----------------------------
rib_heights = np.linspace(0.02, 0.15, 15)

optimal_thickness = []
masses = []

for rh in rib_heights:

    params["rib_height"] = rh
    found = False

    for h in thickness_range:
        SF, delta, mass, _, _, _ = structural_response(h, params)

        if SF >= safety_factor_target and delta <= delta_limit:
            optimal_thickness.append(h)
            masses.append(mass)
            found = True
            break
    
    if not found :
        optimal_thickness.append(np.nan)
        masses.append(np.nan)


# -----------------------------
# RESULTS
# -----------------------------
if not valid_designs:
    print("No design satisfies constraints:")
else:
    optimal = valid_designs[0]
    h_opt = optimal[0]
    plot_dashboard(h_opt, I_total, y_bar, total_height,
               rib_heights, optimal_thickness, masses,
               params)

    animate_buckling(I_total, params)

    print("Optimal plate thickness (mm):", h_opt * 1000)
    print("Safety Factor:", optimal[1])
    print("Deflection (mm):", optimal[2] * 1000)
    print("Mass (kg):", optimal[3])