import math
import datetime
import matplotlib.pyplot as plt

plt.style.use('_mpl-gallery')

# All values in meters
tankArea = 0.32 * 0.36
pipeDiameter = 0.00794
pipeArea = math.pi / 4 * pipeDiameter ** 2
gravity = 9.81
# Kinematic viscosity of water at 1atm, ~25C from textbook p. 809
kinVisWater = 9.0e-7
# print("kinVisWater", kinVisWater)

def findLosses (length, velocity, height):
    if velocity == 0:
        velocity = 0.01
    # Laminar Friction Factor using 64/Re
    lFrictionFactor = (64 * kinVisWater) / (velocity * pipeDiameter)
    # Transition / Turbulent Friction factor from Moody diagram
    tFrictionFactor = 0.02
    # This is a guess
    distanceLaminar = 0.2 + (length - 0.2)*0.4
    percentLaminar = distanceLaminar / length
    effectiveFrictionFactor = percentLaminar * lFrictionFactor + (1 - percentLaminar) * tFrictionFactor
    frictionLoss = effectiveFrictionFactor * (length * velocity ** 2) / (pipeDiameter * 2 * gravity)
    # Need to add in Minor Losses
    # Calculate Minor Losses For Contraction and Expansion
    # The 0.1 is just to make things work. Now physics based
    contractionFactor = 0.1 * 0.42 * (1 - (pipeDiameter ** 2) / (height ** 2))
    contractionLoss = contractionFactor * (velocity ** 2) / (2 * gravity)
    return frictionLoss + contractionLoss 

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
        losses = findLosses(length, velocity, height)
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