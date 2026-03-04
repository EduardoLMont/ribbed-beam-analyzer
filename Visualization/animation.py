import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np

# ---------------------------------
# ANIMATION WINDOW
# ---------------------------------
def animate_buckling(I_total, config):

    x = np.linspace(0, config.L, 200)

    fig, ax = plt.subplots()
    line, = ax.plot([], [])

    ax.set_xlim(0, config.L)
    ax.set_ylim(-0.02, 0.02)
    ax.set_title("Buckling Animation")
    ax.set_xlabel("Length (m)")
    ax.set_ylabel("Lateral Deflection (m)")

    def update(frame):
        A = 0.01 * np.sin(frame / 10)

        bending = config.P * x**2 * (3*config.L - x) / (6 * config.E * I_total)
        buckling = A * (1 - np.cos(np.pi * x / (2 * config.L)))

        y = bending + buckling

        line.set_data(x, y)
        return line,

    ani = matplotlib.animation.FuncAnimation(fig, update, frames=200, interval=30)
    plt.show()