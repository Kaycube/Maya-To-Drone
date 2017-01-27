import os, json
import maya.cmds as cmds

#Maya Camera export
def exportCamera(Camera=None, fileName=None):

    if not Camera:
        #get the current selection
        selection = cmds.ls(selection=True)

        #if nothing is selected, stop
        if len(selection) == 0:
            print "Select export Camera"
            return -1

        #if more than one item is selected, stop
        if len(selection) > 1:
            print "Select one export Camera"
            return -1

        #if there is only one thing selected, store it
        Camera = selection[0]

    #make sure the selected object is a camera
    if cmds.nodeType(Camera) == "transform":
        cameraShape = cmds.listRelatives(Camera, children=True)[0]

        #if children is camera, continue
        if cmds.nodeType(cameraShape) != "camera":
            print "Selected object is not a camera"
            return -1

    #check if file is provided
    if not fileName:
        #run file dialog
        basicFilter = ".json"
        retval = cmds.fileDialog2(dialogStyle=2, fm=0)

        #if file is selected
        if retval:
            file,ext = os.path.splitext(retval[0])

            #if the extensioin is not '.json'
            if ext != '.json':
                fileName = file + ".json"
            else:
                fileName = retval[0]

    #print fileName

    frameStart = cmds.playbackOptions(q=True, min=True)
    frameEnd = cmds.playbackOptions(q=True, max=True)

    outData = {
        "cameraName": Camera,
        "frameStart": frameStart,
        "frameEnd": frameEnd,
        "vfov": cmds.camera(Camera, q=True, verticalFieldOfView=True),
        "hfov": cmds.camera(Camera, q=True, horizontalFieldOfView=True),
        "frames": {"Translation": {}, "Rotation": {}}
        }
    #loop over animation frames
    for i in range(int(frameStart), int(frameEnd)+1):
        #set the current frame
        cmds.currentTime(i)
        #get camera matrix in ws
        outData["frames"]["Translation"][str(i)] = cmds.xform(Camera, q=True, translation=True, worldSpace=True)
        outData["frames"]["Rotation"][str(i)] = cmds.xform(Camera, q=True, rotation=True, worldSpace=True)

    cmds.currentTime(frameStart)

    #save data to json
    fout = open(fileName,'w')
    json.dump(outData, fout, indent=2)
    fout.close()

    print "Exported successfully to %s" %fileName