import math

#All values in meters
tankArea = 0.32 * 0.36
pipeArea = math.pi / 4 * 0.00794 ** 2
gravity = 9.81

def simulateDrain (vInitial, length, timeStep):
    volume = vInitial
    time = 0
    while volume >= 0:
        print("Volume: ", round(volume, 3))
        print("Time: ", round(time, 3))
        height = volume / tankArea + 0.02 + length / 150
        losses = 0
        velocity = math.sqrt(2 * gravity * (height - losses))
        flowRate = pipeArea * velocity
        volume -= timeStep * flowRate
        time += timeStep
    print("Model Done, Tank Drained in ", round(time, 3))

v1 = 0.36 * 0.32 * 0.08
# Pipe lengths: 0.2, 0.3, 0.4, 0.6
simulateDrain(v1, 0.2, 0.01)