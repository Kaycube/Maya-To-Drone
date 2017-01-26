import os, json, math


def ImportCamera(fileName):

    #make sure file exist
    if not os.path.exists(fileName):
        print "File does not exist"
        return -1

    fin = open(fileName, "r")
    cameraData = json.load(fin)
    fin.close()

    #set frame range
    start= cameraData["frameStart"]
    end = cameraData["frameEnd"]

    #import transformations for every frame
    for i in range(int(start), int(end)+1):
        matrixIn = cameraData["frames"]["matrix_world"][str(i)]
        pass

    #Insert manipulation for drone code here