import sys
import os
from ast import literal_eval as make_tuple
import maya.cmds as cmds
import maya.mel as mel
#
# prjName ='DroneMaya'
# scriptsPath = "/home/r2d2/maya/2015-x64/DroneStuff/Scripts"
# iconsPath = os.environ.get('ICONS_PATH', None)
# configsPath = os.environ.get('CONFIGS_PATH', None)
# prjConfFiles = os.path.join(configsPath, prjName)
# sys.path.append(scriptsPath)
#

HOST = "127.0.0.1"
PORT = 631

melproc = """
global proc Port(string $data){
    python(("Port(\\"" + $data + "\\")"));
}
"""
mel.eval(melproc)


def Port(data):
    print "Recieved: ", data

    Alt = float(make_tuple(data)[0])
    Pit = float(make_tuple(data)[1])
    yaw = float(make_tuple(data)[2])
    Roll = float(make_tuple(data)[3])
    x = float(make_tuple(data)[4])
    z = float(make_tuple(data)[5])

    cmds.setAttr('DroneCam.translateX', x)
    cmds.setAttr('DroneCam.translateY', Alt)
    cmds.setAttr('DroneCam.translateZ', z)
    cmds.setAttr('DroneCam.rotateX', Pit)
    cmds.setAttr('DroneCam.rotateY', yaw)
    cmds.setAttr('DroneCam.rotateZ', Roll)

print "Success! Port " + str(PORT) + " is Listening..."
cmds.commandPort(name=HOST + ":" + str(PORT), echoOutput=False, noreturn=False, prefix='Port',
             returnNumCommands=True)


