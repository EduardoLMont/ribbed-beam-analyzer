import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
from Config.beam_config import BeamConfig
from core.optimization import optimize_plate_thickness, parametric_rib_height_study
from core.mechanics import structural_response, stress_distribution, buckling_load
from Visualization.plot import plot_dashboard
from Visualization.animation import animate_buckling







# -----------------------------
# PARAMETERS
# -----------------------------
config = BeamConfig()

thickness_range = np.linspace(0.002, 0.02, 200)
rib_heights = np.linspace(0.02, 0.15, 15)

valid_designs = optimize_plate_thickness(config, thickness_range, 2, 0.002)


if valid_designs:
    h_opt = valid_designs[0][0]
    SF, delta, mass, I_total, y_bar, total_height = structural_response(h_opt, config)
    optimal_thickness, masses = parametric_rib_height_study(config, rib_heights, thickness_range, 2, 0.002)

    plot_dashboard(h_opt, I_total, y_bar, total_height, rib_heights, optimal_thickness, masses, config)
    animate_buckling(I_total, config)

else:
   print("No design satisfies constraints:")