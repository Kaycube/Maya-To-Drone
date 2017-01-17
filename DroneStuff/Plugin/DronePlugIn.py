import sys
import os
from xml.dom import minidom
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaMPx as OpenMayaMPx

prjName ='DroneMaya'
scriptsPath = "/home/r2d2/maya/2015-x64/DroneStuff/Scripts"
iconsPath = os.environ.get('ICONS_PATH', None)
configsPath = os.environ.get('CONFIGS_PATH', None)
prjConfFiles = os.path.join(configsPath, prjName)
sys.path.append(scriptsPath)


def initializePlugin(plugin):
    pluginFn = OpenMayaMPx.MFnPlugin(plugin)
    try:
        pluginFn.registerCommand(Drone_Plugin.PlugName, Drone_Plugin.creator)

    except:
        sys.stderr.write("Failed to register command: " + Drone_Plugin.PlugName)


def uninitializePlugin(plugin):
    pluginFn = OpenMayaMPx.MFnPlugin(plugin)
    try:
        mel.eval('if (`shelfLayout -exists DroneShelf `) deleteUI DroneShelf;')
        pluginFn.deregisterCommand(Drone_Plugin.PlugName)

    except:
        sys.stderr.write("Failed to register command: " + Drone_Plugin.PlugName)


class Drone_Plugin(OpenMayaMPx.MPxCommand):
    PlugName = "DronePlugin"

    Alt = 0.0
    Pit = 0.0
    yaw = 0.0
    Roll = 0.0

    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    @staticmethod
    def creator():
        return OpenMayaMPx.asMPxPtr(Drone_Plugin())

    def doIt(self, argsList):
        shelfConfFile = os.path.join(prjConfFiles, 'dynamicShelfConf.xml')
        mel.eval('if (`shelfLayout -exists DroneShelf `) deleteUI DroneShelf;')
        shelfTab = mel.eval('global string $gShelfTopLevel;')
        mel.eval('$DroneShelf = `shelfLayout -cellWidth 34 -cellHeight 34 -p $gShelfTopLevel DroneShelf`;')
        xmlMenuDoc = minidom.parse(shelfConfFile)
        for eachShelfItem in xmlMenuDoc.getElementsByTagName('shelfItem'):
            getIcon = eachShelfItem.attributes['icon'].value
            shelfBtnIcon = os.path.join(iconsPath, getIcon)
            getAnnotation = eachShelfItem.attributes['ann'].value
            getCommand = eachShelfItem.attributes['cmds'].value

            cmds.shelfButton(command=getCommand, annotation=getAnnotation, image=shelfBtnIcon)

        mel.eval('tabLayout -edit -tabLabel $DroneShelf " ' + prjName + '" $gShelfTopLevel;')
        print "Shelf has been created"
