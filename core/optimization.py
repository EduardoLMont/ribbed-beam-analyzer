from .mechanics import structural_response
import numpy as np

def optimize_plate_thickness(config, thickness_range, safety_factor_target, delta_limit):
    valid_designs = []
    for h in thickness_range:
        SF, delta, mass, _, _, _ = structural_response(h, config)
        if SF >= safety_factor_target and delta <= delta_limit:
            valid_designs.append((h, SF, delta, mass))
    return valid_designs

def parametric_rib_height_study(config, rib_heights, thickness_range, safety_factor_target, delta_limit):
    optimal_thickness = []
    masses = []
    for rh in rib_heights:
        config.rib_height = rh
        found = False
        for h in thickness_range:
            SF, delta, mass, _, _, _ = structural_response(h, config)
            if SF >= safety_factor_target and delta <= delta_limit:
                optimal_thickness.append(h)
                masses.append(mass)
                found = True
                break
        if not found:
            optimal_thickness.append(np.nan)
            masses.append(np.nan)
    return optimal_thickness, masses