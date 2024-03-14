import Buginator
import xml.etree.ElementTree as ET 
import mujoco as mj
import mujoco_viewer
import numpy as np
import random
import math
import csv
import time 

filename = 'testResults.csv'



# Fitness multipliers
weightMultiplier = 0.5
distanceMultiplier = 1

# Test parameters 
generationSize = 250
numGenerations = 10
numChildren = 5
numParents = 50

generationalSeeds = []

# Create a csv file to store data of bugs with best fit
header = ['Generation', 'Fitness', 'Num Segments', 'Speed', 'Wiggle Torque', 'Stomp Torque', "Num Legs", "Leg Positions", "bodyHinges", "legHinges"]

with open(filename, 'w', newline="") as file:
    csv.writer(file).writerow(header)

# Randomly generate the parent generation (generation 0)
for i in range(generationSize):
    print("generation0 child", i)
    # Create random initial traits
    numSegments = random.randint(20,60)
    numLegs = random.randint(4,14)
    legPos = []
    bodyHinges = [] 
    legHinges = []

    speed = random.randint(10,100)

    for x in range(numLegs):
        legPos.append(random.uniform(-.3, .3))
        legHinges.append(random.randint(0,2))

    for z in range(numSegments):
        bodyHinges.append(random.randint(0,2))


    wiggleTorque = random.randint(1,200)
    stompTorque = random.randint(1,200)

    # generate xml file and motor torques
    fitness = Buginator.testSeed(numSegments, numLegs, legPos, bodyHinges, legHinges, speed, wiggleTorque, stompTorque, weightMultiplier, distanceMultiplier)

    # save specimen data 
    generationalSeeds.append([fitness, numSegments, speed, wiggleTorque, stompTorque, numLegs, legPos, bodyHinges, legHinges])

generationalSeeds.sort(key=lambda x: x[0])

parents = []


for i in range(1, numParents+1):
    parents.append(generationalSeeds[-i])
    
with open(filename, 'a', newline="") as file:
    for i in generationalSeeds:
        row = [0, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
        csv.writer(file).writerow(row)


# iterate through generations 
for i in range(numGenerations):
    generationalSeeds = []
    for individual in parents:
        for x in range(numChildren):
            print("generation", i + 1, " child", x)

            numSegments, speed, wiggleTorque, stompTorque, numLegs, legPos, bodyHinges, legHinges = Buginator.mutate(individual[1], individual[2], individual[3], individual[4], individual[5], individual[6], individual[7], individual[8])
            fitness = Buginator.testSeed(numSegments, numLegs, legPos, bodyHinges, legHinges, speed, wiggleTorque, stompTorque, weightMultiplier, distanceMultiplier)

            generationalSeeds.append([fitness, numSegments, speed, wiggleTorque, stompTorque, numLegs, legPos, bodyHinges, legHinges])

    generationalSeeds.sort(key=lambda x: x[0])

    parents = []

    for z in range(1, numParents+1):
        parents.append(generationalSeeds[-z])

    with open(filename, 'a', newline="") as file:
        for j in generationalSeeds:
            row = [i + 1, j[0], j[1], j[2], j[3], j[4], j[5], j[6], j[7], j[8]]
            csv.writer(file).writerow(row)
