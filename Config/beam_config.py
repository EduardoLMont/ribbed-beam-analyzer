class BeamConfig:
    def __init__(self):
        # Loads
        self.P = 800           # Applied load in N
        self.L = 0.2           # Beam length in meters

        #Material properties
        self.E = 200e9         # Young's modulus in Pa
        self.yield_strength = 250e6
        self.density = 7850    # kg/m^3
        self.Kt = 2
        #Geometry
        self.b_plate = 0.04
        self.rib_height = 0.1
        self.rib_thickness = 0.006

        #Design constraints
        self.safety_factor_target = 1.5
        self.delta_limit = 0.005