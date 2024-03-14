import xml.etree.ElementTree as ET 
import mujoco as mj
import mujoco_viewer
import numpy as np
import random
import math
import time 
import glfw

# This function creates an xml file with the given seed and saves it, returning a list of joints (named motorList) to later be used in the simulation
def createXML(numSegments, numLegs, legPos, bodyHinges, legHinges):
    # create elements/subelements
    mujoco = ET.Element('mujoco')

    option = ET.SubElement(mujoco, 'option')
    option.text = 'timestep="0.1"'

    worldbody = ET.SubElement(mujoco, 'worldbody')
    actuator = ET.SubElement(mujoco, 'actuator')


    # create floor
    floorSize = 100
    light = ET.SubElement(worldbody, 'light', diffuse=".5 .5 .5", pos="0 0 3", dir="0 0 1")
    floor = ET.SubElement(worldbody, 'geom', name="floor", type="plane", size=f"{floorSize} {floorSize} 0.1", rgba=".914 .863 .789 1")


    # make the head
    bodyFrame = ET.SubElement(worldbody, 'body', name="head")
    freeJoint = ET.SubElement(bodyFrame, 'freejoint', name="root")
    head = ET.SubElement(bodyFrame, 'geom', name="head", pos="0 0 0.4", type="box", size="0.3 0.2 0.2", rgba="1 .75 0 1")


    # create an empty array for all motor types (legs or body to actuate later) 
    motorList = np.array([])

    # for each body segments, create a body and attach legs

    for i in range(numSegments):  

        MotorGear = f"100"
        bodyName = f'body{i}Body'
        jointName = f"body{i}Joint"
        hingeName = f"body{i}Hinge"
        bodyBody = ET.SubElement(bodyFrame, 'body', name = bodyName, pos = f'{(i+1)*0.65} 0 0.4')
        bodyGeom = ET.SubElement(bodyBody, 'geom', type = "box", size = "0.3 0.2 0.2", rgba = "0.75 1 0 1")

        if bodyHinges[i] == 0:
            bodyHinge = ET.SubElement(bodyBody, 'joint', name=jointName, pos = "-0.15 0 0", axis = "0 0 1", range = "-20 20", limited ="true")
        if bodyHinges[i] == 1:
            bodyHinge = ET.SubElement(bodyBody, 'joint', name=jointName, pos = "-0.15 0 0", axis = "0 1 0", range = "-20 20", limited ="true")
        if bodyHinges[i] == 2:
            bodyHinge = ET.SubElement(bodyBody, 'joint', name=jointName, pos = "-0.15 0 0", axis = "1 0 0", range = "-20 20", limited ="true")


        bodyMotor = ET.SubElement(actuator, 'motor', name=hingeName, gear="10", joint=jointName)

        motorList = np.append(motorList, 1)

        #add legs to the body
        motorList = np.append(motorList, 4)
        even = 0
        for j in range(numLegs):

            legName = f"body{i}leg{j}"
            legHinge = f"body{i}leg{j}Hinge"
            
            leg2Name = f"body{i}leg{j}Part2"
            leg2Hinge = f"body{i}leg{j}Part2Hinge"


            Pos= str(legPos[j])


            if even == 0:

                legBody = ET.SubElement(bodyBody, 'body', name= legName)
                legGeom = ET.SubElement(legBody, 'geom', pos= f"{Pos} 0.35 0.05", type = 'box', size = '0.05 0.15 0.05')
                if legHinges[j] == 0:    
                    legJoint = ET.SubElement(legBody, 'joint', name = legHinge, pos="0 0 0.5", axis="1 0 0", range="-10 10", limited="true")
                if legHinges[j] == 1:    
                    legJoint = ET.SubElement(legBody, 'joint', name = legHinge, pos="0 0 0.5", axis="0 1 0", range="-10 10", limited="true")
                if legHinges[j] == 2:    
                    legJoint = ET.SubElement(legBody, 'joint', name = legHinge, pos="0 0 0.5", axis="0 0 1", range="-10 10", limited="true")
                legMotor = ET.SubElement(actuator, 'motor', name=legHinge, gear=MotorGear, joint=legHinge)
                
                
                leg2Body = ET.SubElement(bodyBody, 'body', name= leg2Name)
                leg2Geom = ET.SubElement(legBody, 'geom', pos= f"{Pos} 0.45 -.1", type = 'box', size = '0.05 0.05 0.2')
                even = 2

            if even == 1: 

                legBody = ET.SubElement(bodyBody, 'body', name= legName)
                legGeom = ET.SubElement(legBody, 'geom', pos= f"{Pos} -0.35 0.05", type = 'box', size = '0.05 0.15 0.05')
                legJoint = ET.SubElement(legBody, 'joint', name = legHinge, pos="0 0 0.5", axis="1 0 0", range="-10 10", limited="true")
                legMotor = ET.SubElement(actuator, 'motor', name=legHinge, gear=MotorGear, joint=legHinge)
                
                leg2Body = ET.SubElement(bodyBody, 'body', name= leg2Name)
                leg2Geom = ET.SubElement(legBody, 'geom', pos= f"{Pos} -0.45 -.1", type = 'box', size = '0.05 0.05 0.2')    
            
            even = even-1

        
    # write to XML file 
    tree = ET.ElementTree(mujoco)
    tree.write('bug.xml')
    return motorList

# Each individual has a loop of two steps (ie. up and down for each joint), this function generates those two steps
def createSteps(motorList, wiggleTorque, stompTorque, numLegs):

    step1 = np.array([])
    step2 = np.array([])

    counter = 1
    count = 0

    # create 2 arrays for each step taken by the bug
    for i in motorList:
        if i == 1:
            if counter == 1:
                step1 = np.append(step1, wiggleTorque)
                step2 = np.append(step2, wiggleTorque * -1)

                counter = 2

            if counter == 0:
                step1 = np.append(step1, wiggleTorque * -1)
                step2 = np.append(step2, wiggleTorque)
                counter = 1

            if counter == 2:
                counter = 0


        if i == 4:
            for x in range(numLegs):
                if count == 1:
                    step1 = np.append(step1, stompTorque)
                    step2 = np.append(step2, stompTorque * -1)
                    count = 2

                if count == 0: 
                    step1 = np.append(step1, stompTorque * -1)
                    step2 = np.append(step2, stompTorque)

                if count == 2:
                    count = 0

    stepList = np.array([step1, step2])

    return stepList

# This function takes the data and simulates it and returns the initial and final position of the individual
def animate(stepList, speed):
    step1 = stepList[0]
    step2 = stepList[1]
    model = mj.MjModel.from_xml_path('bug.xml')
    data = mj.MjData(model)

    viewer = mujoco_viewer.MujocoViewer(model, data)

    motors = model.nu


    data.ctrl[:motors] = step2
    count = 0

    # create empty arrays to record each position
    pos1 = np.array([])

    # simulate the bugs 
    for i in range(300):
        if i == 1:
            pos1 = data.body('body0Body').xpos
        if viewer.is_alive:

            if i%speed == 0:
                step = stepList[count]
            
                count = count + 1
                if count == 2:
                    count = 0
            data.ctrl[:motors] = step
            mj.mj_step(model, data)
            viewer.render()
        
        else:
            break
    pos2 = data.body('head').xpos

    glfw.destroy_window(viewer.window)
    return pos1, pos2
    

# the fitness is determined by both the weight of the bug and the distance it is able to travel
# more weight = needs more sustenance = in a competitive environment it might not be able to eat enough to survive 
# more distance = faster = better at evading theoretical predators = survival! :) 

def calcFitness(numSegments, weightMultiplier, distanceMultiplier, pos1, pos2):
    weight = (numSegments + 1) * weightMultiplier
    
    # How to best calc distance travelled for best evolution? 
    distance = abs(distanceMultiplier * (math.sqrt(pos1[0]**2 + pos1[1]**2) - math.sqrt(pos2[0]**2 + pos2[1]**2)))
    
    #distance = abs(pos1[0] - pos2[0])
   
    # calc fitness and return
    fitness = (distance*distance)/weight
    #fitness = distance + weight

    return fitness

# This function takes the parent seeds and randomly mutates them 
def mutate(numSegments, speed, wiggleTorque, stompTorque, numLegs, legPos, bodyHinges, legHinges):
    mutation = random.randint(0,10)
    newLegPos = []
    
    if mutation == 3:
        numSegments = numSegments + random.randint(-5,10)
        for i in bodyHinges:
            bodyHinges[i] = random.randint(0,2)
    

    mutation = random.randint(0,10)
    if mutation == 4:
        wiggleTorque = wiggleTorque + random.randint(-20, 20)
    mutation = random.randint(0,10)
    if mutation == 5:
        stompTorque = stompTorque + random.randint(-20, 20)
    mutation = random.randint(0,10)
    if mutation == 6:
        numLegs = numLegs + random.randint(-3,3)

        for x in legPos:
            newLegPos.append(x + random.uniform(-.2,.2))
        for z in range(len(legHinges)):
            legHinges[z] = random.randint(0,2)

    mutation = random.randint(0,10)
    if mutation == 7:
        speed = speed + random.randint(-20, 20)


    while numLegs >= len(newLegPos):
        for x in legPos:
            newLegPos.append(x)

    if numSegments < 1:
        numSegments = 1
    speed = abs(speed)

    while len(bodyHinges) <= numSegments + 1:
        bodyHinges.append(random.randint(0,2))
    while len(legHinges) <= numLegs:
        legHinges.append(random.randint(0,2))

    return numSegments, speed, wiggleTorque, stompTorque, numLegs, newLegPos, bodyHinges, legHinges

# This function simulates each individual and returns the individuals fitness
def testSeed(numSegments, numLegs, legPos, bodyHinges, legHinges, speed, wiggleTorque, stompTorque, weightMultiplier, distanceMultiplier):
    motorList = createXML(numSegments, numLegs, legPos, bodyHinges, legHinges)
    stepList = createSteps(motorList, wiggleTorque, stompTorque, numLegs)

    [pos1, pos2] = animate(stepList, speed)

    fitness = calcFitness(numSegments, weightMultiplier, distanceMultiplier, pos1, pos2)

    return fitness

    

