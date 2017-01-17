import ps_drone
import pygame as game
import time
import math


def invert(x):
    return -x

def Joystick():

    drone = ps_drone.Drone()
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
    hovercount = 0
    prevstate = ""

    while done == False:
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
                    drone.takeoff()
                    while drone.NavData["demo"][0][2]:
                        time.sleep(0.1)
                    print "Take Off"
                elif event.button == 11:
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
                if event.value == 0:
                    joystate = "deadzone"
                    #print "current state: " + joystate + " previous state: " + prevstate
                    if joystate == prevstate:
                        pass
                    else:
                        prevstate = joystate
                        drone.stop()
                        print "hover"
                        time.sleep(0.5)

                elif event.axis == 1:
                    joystate = "Pitch"
                    #print "current state: " + joystate + " previous state: " + prevstate
                    if joystate == prevstate:
                        pass
                    else:
                        prevstate = joystate
                        Pitch = invert(event.value)
                        drone.move(Roll, Pitch, hatupdown, hatleftright)
                        print "Pitch value X :" + str(Pitch)

                elif event.axis == 0:
                    joystate = "Roll"
                    #print "current state: " + joystate + " previous state: " + prevstate
                    if joystate == prevstate:
                        pass
                    else:
                        prevstate = joystate
                        Roll = event.value
                        print "Roll " + str(Roll)
                        drone.move(Roll, Pitch, hatupdown, hatleftright)

                elif event.axis == 2:
                    Throttle = event.value
                    print "Throttle value :" + str(Throttle)

                elif event.axis == 3:
                    print "I think this is throttle"
                    pass

                elif event.axis == 4:
                    pass

            if event.type == game.JOYHATMOTION:
                if event.value == (0, 0):
                    joystate = "deadzone"
                    #print "current state: " + joystate + " previous state: " + prevstate
                    if joystate == prevstate:
                        continue
                    else:
                        prevstate = joystate
                        drone.stop()
                        print "hover"
                        time.sleep(2)

                if event.value == (-1, 0):
                    joystate = "HatLeft"
                    #print "current state: " + joystate + " previous state: " + prevstate
                    if joystate == prevstate:
                        continue
                    else:
                        prevstate = joystate
                        hatleftright = -1.0 * 10
                        drone.turnAngle(hatleftright, 1, 1)
                        print 'hat left'

                elif event.value == (1, 0):
                    joystate = "HatRight"
                    #print "current state: " + joystate + " previous state: " + prevstate
                    if joystate == prevstate:
                        continue
                    else:
                        prevstate = joystate
                        hatleftright = 1.0 * 10
                        drone.turnAngle(hatleftright, 1, 1)
                        print "hat right"

                elif event.value == (0, 1):
                    joystate = "HatUp"
                    #print "current state: " + joystate + " previous state: " + prevstate
                    if joystate == prevstate:
                        continue
                    else:
                        prevstate = joystate
                        hatupdown = 1.0
                        drone.move(Roll, Pitch, hatupdown, hatleftright)
                        print "hat up"

                elif event.value == (0, -1):
                    joystate = "HatDown"
                    #print "current state: " + joystate + " previous state: " + prevstate
                    if joystate == prevstate:
                        continue
                    else:
                        prevstate = joystate
                        hatupdown = -1.0
                        drone.move(Roll, Pitch, hatupdown, hatleftright)
                        print "hat down"
    game.quit()

if __name__ == "__main__":
    Joystick()