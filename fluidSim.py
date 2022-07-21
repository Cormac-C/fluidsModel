import math
import datetime
import matplotlib.pyplot as plt

plt.style.use('_mpl-gallery')

# All values in meters
tankArea = 0.32 * 0.36
pipeDiameter = 0.00794
pipeArea = math.pi / 4 * pipeDiameter ** 2
gravity = 9.81

def findLosses (length, velocity):
    # Friction factor wrong
    frictionFactor = 0.01
    frictionLoss = frictionFactor * (length * velocity ** 2) / (pipeDiameter * 2 * gravity)
    # Need to add in Minor Losses
    return frictionLoss

def simulateDrain (vInitial, length, timeStep):
    # Initial Conditions
    volume = vInitial
    time = 0
    velocity = 0
    volumes = []
    velocities = []
    times = []
    while volume >= 0:
        height = volume / tankArea + 0.02 + length / 150
        # Calculates losses based on the velocity of the last time step
        losses = findLosses(length, velocity)
        velocity = math.sqrt(2 * gravity * (height - losses))
        velocities.append(velocity)
        flowRate = pipeArea * velocity
        volume -= timeStep * flowRate
        volumes.append(volume)
        times.append(time)
        time += timeStep
    print("Model Done (Length ", length, "), Tank Drained in ", round(time, 3), "s", datetime.timedelta(seconds = time))
    fig, ax = plt.subplots()
    ax.scatter(times, volumes)
    ax.set_xlabel("time (s)", fontsize=15)
    ax.set_ylabel("volume ($m^3$)", fontsize=15)
    ax.grid(True)
    fig.tight_layout()
    plt.show()
    fig2, ax2 = plt.subplots()
    ax2.scatter(times, velocities)
    ax2.set_xlabel("time (s)", fontsize=15)
    ax2.set_ylabel("velocity (m/s)", fontsize=15)
    ax2.grid(True)
    fig2.tight_layout()
    plt.show()

v1 = 0.36 * 0.32 * 0.08
# Pipe lengths: 0.2, 0.3, 0.4, 0.6
simulateDrain(v1, 0.2, 0.1)
simulateDrain(v1, 0.3, 0.1)
simulateDrain(v1, 0.4, 0.1)
simulateDrain(v1, 0.6, 0.1)