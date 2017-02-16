from threading import Thread
import ps_drone
import JoyStickController
import pygame as game
import time
import sys
import socket
import numpy
import random
import MathFunc as func


drone = ps_drone.Drone()
HOST = "127.0.0.1"
PORT = 631
Data = ""

cam_heading = 0.0
cam_heading_speed = 100.0
cam_speed = 5.0
cam_pos = [0.0, 0.0, 0.0]
move = [0.0, 0.0, 0.0]
camMove = False
quat = []
mat4x4 = []
xaxis, yaxis, zaxis = [1, 0, 0], [0, 1, 0], [0, 0, 1]
pos_x = 0
pos_z = 0

fwd = [0.0, 0.0, -1.0]
rgt = [1.0, 0.0, 0.0]
up = [0.0, 1.0, 0.0]

v1 = [0.0, 0.0, -1.0, 0.0]
v2 = [1.0, 0.0, 0.0, 0.0]
v3 = [0.0, 1.0, 0.0, 0.0]


def invert(x):
    return -x


def quaternion(x, y, z, ax1, ax2, ax3):
    qp = func.quaternion_about_axis(x, ax1)
    qy = func.quaternion_about_axis(y, ax2)
    qr = func.quaternion_about_axis(z, ax3)
    q = func.quaternion_multiply(qp, qy)
    q = func.quaternion_multiply(q, qr)

    return q


def DroneData():
    global xaxis
    global yaxis
    global zaxis
    global fwd
    global rgt
    global up
    global pos_x
    global pos_z

    global PORT
    maya = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "socket created!"
    try:
        maya.connect((HOST, PORT))
        print "Connection sucessfull!"
    except socket.error, ex:
        print "Connection failed!"
        print ex

    end = False
    NDC = drone.NavDataCount
    while not end:
        global Data
        time.sleep(0.001)
        while drone.NavDataCount == NDC:
            time.sleep(0.001)

        Alt = drone.NavData["demo"][3] / 100
        Pit = drone.NavData["demo"][2][0]
        yaw = drone.NavData["demo"][2][1]
        roll = drone.NavData["demo"][2][2]

        finalquat = func.quaternion_multiply(quaternion(Pit, yaw, roll, rgt, up, fwd), quaternion(Pit, yaw, roll,
                                                                                                  xaxis, yaxis, zaxis))

        Data = Alt, finalquat[1], finalquat[2], finalquat[3], pos_x, pos_z
        Data = str(Data)
        maya.send(Data)
        print "Message Sent!!"
        ret = maya.recv(1024)
        print ret
    maya.close()
    print "Port " + str(PORT) + " is closed!!"

# Reset the sensors on the Drone!! ALWAYS USE FIRST BEFORE RUN METHODS
def Initialize():
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
    print "Initialization Done!"


def DroneRun():
    drone.setSpeed(0.1)
    game.init()
    done = False

    try:
        joystick = game.joystick
        print str(joystick.get_count()) + " joystick Connected! "
        # First connected joystick
        Joystick = joystick.Joystick(0)
        # initialize Joystick
        Joystick.init()
        print "Enabled joystick: " + Joystick.get_name()
    except game.error:
        print "No Joystick found."
        quit()

    global Pitch
    global Roll
    global hatupdown
    global hovercount
    global prevstate
    global joystate

    global camMove
    global cam_pos
    global pos_x
    global pos_z

    while done == False:
        previousSec = time.clock()
        currentSec = time.clock()
        elapsedTime = currentSec - previousSec
        previousSec = currentSec

        for event in game.event.get():
            Pitch = 0.0
            Roll = 0.0
            hatleftright = 0.0
            hatupdown = 0.0
            if event.type == game.JOYBUTTONDOWN:
                if event.button == 0:
                    pass
                    print "0"
                elif event.button == 1:
                    pass
                    print "1"
                elif event.button == 2:
                    pass
                    print "2"
                elif event.button == 3:
                    print "Initialize"
                elif event.button == 4:
                    drone.land()
                    print "Emergency Land"
                elif event.button == 5:
                    pass
                    print "5"
                elif event.button == 6:
                    pass
                    print "6"
                elif event.button == 7:
                    pass
                    print "7"
                elif event.button == 8:
                    pass
                    print "8"
                elif event.button == 9:
                    drone.shutdown()
                    # print "Clean shutdown"
                    # print "Quit"
                    done = True
                elif event.button == 10:
                    Initialize()
                    drone.takeoff()
                    camMove = True
                    time.sleep(7.5)
                    print "Take Off"
                elif event.button == 11:
                    camMove = True
                    drone.land()
                    print "Land"
                elif event.button == 12:
                    pass
                    print "12"
                elif event.button == 13:
                    pass
                    print "13"
                elif event.button == 14:
                    pass
                    print "14"

            if event.type == game.JOYAXISMOTION:

                if event.axis == 1:
                    joystate = "Pitch"
                    # print "current state: " + joystate + " previous state: " + prevstate
                    if joystate == prevstate:
                        pass
                    else:
                        prevstate = joystate
                        Pitch = invert(event.value)
                        drone.move(Roll, Pitch, hatupdown, hatleftright)
                        if Pitch < 0:
                            move[0] -= cam_speed * elapsedTime
                        else:
                            move[0] += cam_speed * elapsedTime
                        camMove = True
                        print "Pitch value X :" + str(Pitch)

                elif event.axis == 0:
                    joystate = "Roll"
                    # print "current state: " + joystate + " previous state: " + prevstate
                    if joystate == prevstate:
                        pass
                    else:
                        prevstate = joystate
                        Roll = event.value
                        print "Roll " + str(Roll)
                        drone.move(Roll, Pitch, hatupdown, hatleftright)
                        if Roll < 0:
                            move[2] -= cam_speed * elapsedTime
                        else:
                            move[2] += cam_speed * elapsedTime
                        camMove = True

                elif event.axis == 2:
                    Throttle = event.value
                    print "Throttle value :" + str(Throttle)

                elif event.axis == 3:
                    print "I think this is throttle"
                    pass

                elif event.axis == 4:
                    pass

                elif event.value == 0:
                    drone.stop()
                    print "hover"
                    time.sleep(2)

            if event.type == game.JOYHATMOTION:
                if event.value == (0, 0):
                    joystate = "deadzone"
                    # print "current state: " + joystate + " previous state: " + prevstate
                    if joystate == prevstate:
                        continue
                    else:
                        prevstate = joystate
                        drone.stop()
                        print "hover"
                        time.sleep(2)

                if event.value == (-1, 0):
                    joystate = "HatLeft"
                    # print "current state: " + joystate + " previous state: " + prevstate
                    if joystate == prevstate:
                        continue
                    else:
                        prevstate = joystate
                        hatleftright = -1.0 * 10
                        drone.turnAngle(hatleftright, 1, 1)
                        print 'hat left'

                elif event.value == (1, 0):
                    joystate = "HatRight"
                    # print "current state: " + joystate + " previous state: " + prevstate
                    if joystate == prevstate:
                        continue
                    else:
                        prevstate = joystate
                        hatleftright = 1.0 * 10
                        drone.turnAngle(hatleftright, 1, 1)
                        print "hat right"

                elif event.value == (0, 1):
                    joystate = "HatUp"
                    # print "current state: " + joystate + " previous state: " + prevstate
                    if joystate == prevstate:
                        continue
                    else:
                        prevstate = joystate
                        hatupdown = 1.0
                        drone.move(Roll, Pitch, hatupdown, hatleftright)
                        print "hat up"

                elif event.value == (0, -1):
                    joystate = "HatDown"
                    # print "current state: " + joystate + " previous state: " + prevstate
                    if joystate == prevstate:
                        continue
                    else:
                        prevstate = joystate
                        hatupdown = -1.0
                        drone.move(Roll, Pitch, hatupdown, hatleftright)
                        camMove = True
                        print "hat down"

            if camMove == True:
                for i in range(len(cam_pos)):
                    cam_pos[i] = cam_pos[i] + fwd[i] * -move[2]
                for i in range(len(cam_pos)):
                    cam_pos[i] = cam_pos[i] + up[i] * move[1]
                for i in range(len(cam_pos)):
                    cam_pos[i] = cam_pos[i] + rgt[i] * move[0]

                matxT = func.translation_matrix(cam_pos)
                finalTranslation = func.translation_from_matrix(matxT)
                pos_x = finalTranslation[0]
                pos_z = finalTranslation[2]

    game.quit()

def test():
    drone.takeoff()
    time.sleep(7.5)
    drone.moveForward()
    time.sleep(2)
    drone.stop()
    time.sleep(2)
    drone.turnLeft()
    time.sleep(10)
    drone.stop()
    time.sleep(2)
    drone.stop()
    time.sleep(2)

def test2():
    drone.takeoff()
    time.sleep(7.5)
    drone.moveUp()
    time.sleep(2)
    drone.moveBackward()
    time.sleep(2)
    drone.stop()
    time.sleep(2)
    drone.turnLeft()
    time.sleep(5)
    drone.stop()
    time.sleep(2)


def Animation():
    drone.anim(test(), 0)
    drone.anim(test2(), 2)
    drone.land()


    #JoyStickController.Joystick()

if __name__ == "__main__":
    Initialize()
    p1 = Thread(target=Animation)
    p2 = Thread(target=DroneData)
    p1.start()
    p2.daemon = True
    p2.start()
    p1.join()
    #DroneRun()
    #Animation()
    # DroneData()
