import math
import datetime
# import matplotlib.pyplot as plt

# plt.style.use('_mpl-gallery')

# All values in meters
tankArea = 0.32 * 0.36
pipeDiameter = 0.00794
pipeArea = math.pi / 4 * pipeDiameter ** 2
gravity = 9.81
teeJointLength = 0.04
# Kinematic viscosity of water at 1atm, ~25C from textbook p. 809
kinVisWater = 9.0e-7
# print("kinVisWater", kinVisWater)

def findLosses (length, velocity, height, teeJoint):
    if velocity == 0:
        velocity = 0.01
    # Laminar Friction Factor using 64/Re
    lFrictionFactor = (64 * kinVisWater) / (velocity * pipeDiameter)
    # Transition / Turbulent Friction factor from Moody diagram
    tFrictionFactor = 0.02
    # This is a guess
    distanceLaminar = 0.25 + (length - 0.3)*0.3
    percentLaminar = distanceLaminar / length
    effectiveFrictionFactor = percentLaminar * lFrictionFactor + (1 - percentLaminar) * tFrictionFactor
    frictionLoss = effectiveFrictionFactor * (length * velocity ** 2) / (pipeDiameter * 2 * gravity)
    
    # Calculate Minor Losses For Contraction and Expansion
    contractionFactor = 0.08 * 0.42 * (1 - (pipeDiameter ** 2) / (height ** 2))

    contractionLoss = contractionFactor * (velocity ** 2) / (2 * gravity)

    #to do: add tee joint friction and minor losses
    if teeJoint == True:
        # tentative loss factor
        teeJointLossFactor = 0.5

        teeFrictionLoss = (effectiveFrictionFactor * (teeJointLength * velocity ** 2) / (pipeDiameter * 2 * gravity))
        print("Tee friction loss is ", teeFrictionLoss)
        teeMinorLoss = teeJointLossFactor * (velocity ** 2) / (2 * gravity)
        print("Tee minor loss is ", teeMinorLoss)
        teeJointLoss = (teeFrictionLoss + teeMinorLoss) * 0.08
        print("Tee joint loss is ", teeJointLoss)
    else:
        teeJointLoss = 0
        
    losses = frictionLoss + contractionLoss + teeJointLoss

    # print("Losses are: ", losses)
    # print("Height is ", height)

    return losses


def simulateDrain (vInitial, length, timeStep, teeJoint):
    # Initial Conditions
    volume = vInitial
    time = 0
    velocity = 0
    while volume >= 0:
        height = volume / tankArea + 0.02 + length / 150
        print("Height is", height)
        # Calculates losses based on the velocity of the last time step
        losses = findLosses(length, velocity, height, teeJoint)
        velocity = math.sqrt(2 * gravity * (height - losses))
        flowRate = pipeArea * velocity
        volume -= timeStep * flowRate
        time += timeStep
    print("Model Done (Length ", length, "), Tank Drained in ", round(time, 3), "s", datetime.timedelta(seconds = time))


def simulateSimpleDrain(vInitial, length):
    # Initial conditions
    volume = vInitial
    time = 0
    velocity = 0

    height = volume / tankArea + 0.02 + length / 150
    velocity = math.sqrt(2 * gravity * height)
    flowRate = pipeArea * velocity
    time = volume / flowRate
    print("Simple Model Done (Length ", length, "), Tank Drained in ", round(time, 3), "s", datetime.timedelta(seconds = time))



v1 = 0.36 * 0.32 * 0.08
# Pipe lengths: 0.2, 0.3, 0.4, 0.6
# simulateDrain(v1, 0.2, 0.1, False)
simulateDrain(v1, 0.6, 1, True)
# simulateDrain(v1, 0.3, 0.1, False)
# simulateDrain(v1, 0.4, 0.1, False)
# simulateDrain(v1, 0.6, 1, False)
# simulateSimpleDrain(v1, 0.2)
# simulateSimpleDrain(v1, 0.3)
# simulateSimpleDrain(v1, 0.4)
# simulateSimpleDrain(v1, 0.6)