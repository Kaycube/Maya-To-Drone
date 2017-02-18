import os, json, math
import tkFileDialog as tk
import ps_drone
import time
import sys
from threading import Thread

drone = ps_drone.Drone()
currentHeight = 0.0


def DroneData():
    global currentHeight
    end = False
    NDC = drone.NavDataCount
    while not end:
        while drone.NavDataCount == NDC:
            time.sleep(0.001)
        currentHeight = drone.NavData["demo"][3]
        #print currentHeight

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


def moveUpft(goal):
    global currentHeight
    currentHeight = drone.NavData['demo'][3]
    if currentHeight > 0.0:
        goal *= 0.3048
        target_height = currentHeight + goal
        print "target height: ", target_height
        drone.moveUp(target_height)
        while currentHeight < target_height:
            retarget = currentHeight - target_height
            drone.moveUp(retarget)
            print "retargeted height: ", retarget
    drone.stop()
    time.sleep(2)
    print "mission accomplished: ", currentHeight
    drone.land()

if __name__ == "__main__":
    Initialize()
    p1 = Thread(target=DroneData)
    p2 = Thread(target=moveUpft(1))
    p1.daemon = True
    p1.start()
    time.sleep(7)
    p2.start()
    p2.join()
    #DroneData()
