import socket
import maya.cmds as cmds
import os as os
# import ps_drone

HOST = '127.0.0.1'
PORT = 631

# maya = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print "socket created!"
# try:
#     maya.connect((HOST, PORT))
#     print "Connection successful!"
# except socket.error, ex:
#     print "Connection failed!"
#     print ex

#os.system('sudo python /home/r2d2/maya/2015-x64/scripts/logicTest.py')

if cmds.objExists("DroneCam"):
    test = 0
    global data
    while True:
        print test
        translateX = cmds.getAttr('DroneCam.translateX')
        translateY = cmds.getAttr('DroneCam.translateY')
        translateZ = cmds.getAttr('DroneCam.translateZ')
        rotateX = cmds.getAttr('DroneCam.rotateX')
        rotateY = cmds.getAttr('DroneCam.rotateY')
        rotateZ = cmds.getAttr('DroneCam.rotateZ')

        MayaData = str(translateX), str(translateY), str(translateZ), str(rotateX), str(rotateY), str(rotateZ)
        MayaData = str(MayaData)
        #maya.send(MayaData)
        #data = maya.recv(1024)
        test += 1
        print MayaData
else:
    print "Warning: No DroneCam object."

#maya.close()
#print "Recieved ", repr(data)
