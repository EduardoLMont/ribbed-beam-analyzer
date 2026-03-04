import numpy as np

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


