# from threading import Thread
#import time
#from pocketsphinx import LiveSpeech
import socket



HOST = '127.0.0.1'
PORT = 631

drone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
drone.bind((HOST, PORT))
drone.listen(1)
conn, addr = drone.accept()
print "Connected by ", addr
while 1:
    data = conn.recv(1024)
    print "Recieved from Maya: ", data
    if not data:
        break
    conn.send(data)
drone.close()

# spd = 1
# alt = 2
#
# def run(alt, spd):
#     while True:
#         print (" Altitude: " + str(alt) + " Speed: " + str(spd))
#         alt += 0.01
#         time.sleep(2)
#
# def logic(x, y):
#     while True:
#         input = raw_input("faster")
#
#         if input == "faster":
#             y += 1
#             x *= y
#     return y
# if __name__ == "__main__":
#     p1 = Thread(target=run(alt, spd))
#     p2 = Thread(target=logic(alt, spd))
#
#     p1.start()
#     p2.start()
#
#     p1.join()
#     p2.join()
# def frange(start, stop, step):
#     i = start
#     while i < stop:
#         yield i
#         i += step
# def speed_lvl(start, step):
#     spd = []
#     lvl = []
#     for i in frange(start, 1.0, step):
#         spd.append(i)
#     for i in range(len(spd)):
#         lvl.append(i)
#     lvl = lvl[1:]
#     #print lvl
#     #print spd
#     return spd
#
# speed = speed_lvl(0.1, 0.06)
# lvl = []
# [lvl.append(i) for i in range(len(speed))]
# lvl = lvl[1:]
# print speed
# print lvl[len(speed) - 2] #[len(speed_lvl(0.1, 0.01))-1]



# for phrase in LiveSpeech():
#     print "Listening ...."
#     print phrase



# from ast import literal_eval as make_tuple
# tup = str((20.0, 30.0, 40.0))
# print tup
# print make_tuple(tup)
#
# print type(tup)
# print type(make_tuple(tup))
#
# x = float(make_tuple(tup)[0])
# print x

# import subprocess
#
# pid = subprocess.Popen(args=[
#     "gnome-terminal", "--command=sudo python /home/wall-e/maya/2015-x64/DroneStuff/Scripts/DroneMayaCamControl.py"]).pid
# print pid

# import os
#
# os.system('gnome-terminal')




# import pygame as game
# import sys
# import time
#
# game.init()
# done = False
#
#
# try:
#     joystick = game.joystick
#     print str(joystick.get_count()) + " joystick Connected! "
#     #First connected joystick
#     Joystick = joystick.Joystick(0)
#     #initialize Joystick
#     Joystick.init()
#     print "Enabled joystick: " + Joystick.get_name()
# except game.error:
#     print "No Joystick found."
#     quit()
#
# while done == False:
#     for event in game.event.get():
#         if event.type == game.JOYBUTTONDOWN:
#             if event.button == 0:
#                 print "0"
#             elif event.button == 1:
#                 print "1"
#             elif event.button == 2:
#                 print "2"
#             elif event.button == 3:
#                 print "Initialize"
#             elif event.button == 4:
#                 print "Emergency Land"
#             elif event.button == 5:
#                 print "5"
#             elif event.button == 6:
#                 print "6"
#             elif event.button == 7:
#                 print "7"
#             elif event.button == 8:
#                 print "8"
#             elif event.button == 9:
#                 print "Clean shutdown"
#                 print "Quit"
#                 done = True
#             elif event.button == 10:
#                 print "Take Off"
#                 time.sleep(7)
#             elif event.button == 11:
#                 print "Land"
#                 time.sleep(1)
#             elif event.button == 12:
#                 print "12"
#             elif event.button == 13:
#                 print "13"
#             elif event.button == 14:
#                 print "14"
#
#         if event.type == game.JOYAXISMOTION:
#             if event.value == 0:
#                 print "hover"
#                 time.sleep(0.01)
#             elif event.axis == 1:
#                 Pitch = -event.value
#                 print "Pitch value X :" + str(Pitch)
#             elif event.axis == 0:
#                 Roll = event.value
#                 print "Roll value Y :" + str(Roll)
#             elif event.axis == 2:
#                 Throttle = event.value
#                 print "Throttle value :" + str(Throttle)
#             elif event.axis == 3:
#                 print "I think this is throttle"
#             elif event.axis == 4:
#                 Yaw = event.value
#                 print "Yaw value Z :" + str(Yaw)
#         if event.type == game.JOYHATMOTION:
#             if event.value == (0, 0):
#                 print "hover"
#                 time.sleep(0.5)
#             if event.value == (-1,0):
#                 print 'hat left'
#             elif event.value == (1, 0):
#                 print "hat right"
#             elif event.value == (0, 1):
#                 print "hat up"
#             elif event.value == (0, -1):
#                 print "hat down"
# game.quit()
