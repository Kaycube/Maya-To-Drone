import os, json, math
import tkFileDialog as tk
import ps_drone
import time
import sys
from threading import Thread

drone = ps_drone.Drone()
currentHeight = 0.0


def MaxValue2DList(List):
    Max = 0.0
    for i in List:
        if i > Max:
            Max = i

    return Max


def DroneData():
    global currentHeight
    end = False
    NDC = drone.NavDataCount
    while not end:
        while drone.NavDataCount == NDC:
            time.sleep(0.001)
        currentHeight = drone.NavData["demo"][3]


def Camera(fileName):
    global maxHeightInAnimation
    maxHeightInAnimation = 0.0

    #make sure file exist
    if not os.path.exists(fileName):
        print "File does not exist"
        sys.exit()

    fin = open(fileName, "r")
    cameraData = json.load(fin)
    fin.close()

    Initialize()

    #set frame range
    start = cameraData["frameStart"]
    end = cameraData["frameEnd"]

    for x in range(int(start), int(end)+1):
        t = cameraData['frames']["Translation"][str(x)]
        maxHeightInAnimation = MaxValue2DList(t)

    print "Maximum Animation height: " + str(maxHeightInAnimation)
    accomplishedHeight = []
    print accomplishedHeight

    #import translations and rotations for every frame
    for i in range(int(start), int(end)+1):
        trans = cameraData["frames"]["Translation"][str(i)]
        rot = cameraData["frames"]["Rotation"][str(i)]

        if (maxHeightInAnimation in accomplishedHeight) and (i != int(end)+1):
            yStatus = add(float(currentHeight), float(trans[1]))
            accomplishedHeight.append(yStatus)
            print "neg " + str(yStatus)
            MoveDrone(float(-rot[2]), float(-rot[0]), float(-yStatus), float(-rot[1]))
        else:
            yStatus = add(float(currentHeight), float(trans[1]))
            accomplishedHeight.append(yStatus)
            print "pos " + str(yStatus)
            MoveDrone(float(rot[2]), float(rot[0]), float(yStatus), float(rot[1]))

        # for x in range(len(translation)):
        #     print "Frame " + str(i) + " , tx " + str(translation[0]) + " ty " + str(translation[1]) + " tz " + str(translation[2])
        # for y in range(len(rotation)):
        #     print "Frame " + str(i) + " , rx " + str(rotation[0]) + " ry " + str(rotation[1]) + " rz " + str(rotation[2])
    drone.stop()
    time.sleep(2)
    drone.land()
    print "Animation done!"
    sys.exit()

def Initialize():
    print "initializing...."
    drone.startup()
    drone.reset()
    while drone.getBattery()[0] == -1:
        time.sleep(0.1)
    if str(drone.NavData["demo"][1]) < "20":
        drone.printRed("LOW BATTERY")
        drone.printRed("Battery: " + str(drone.NavData["demo"][1]) + "%")
    else:
        drone.printBlue("Battery: " + str(drone.NavData["demo"][1]) + "%")
    if drone.getBattery()[1] == "empty":
        sys.exit()
    drone.useDemoMode(True)
    drone.getNDpackage(["demo"])
    time.sleep(0.5)
    drone.trim()
    drone.getSelfRotation(5)
    print "Calibration Done!"
    drone.takeoff()
    while drone.NavData["demo"][0][2]:
        time.sleep(0.1)

def add(x, y):
    return x + y

def MoveDrone(rz, rx, ty, ry):
    drone.move(rz, rx, ty, ry)

if __name__ == "__main__":
    file = tk.askopenfilename()
    p1 = Thread(target=Camera(Camera(file)))
    p2 = Thread(target=DroneData)
    p1.start()
    p2.daemon = True
    p2.start()
    p1.join()
