"""Get Jaguar 4x4 direction."""

import os
import cv2 as cv
import numpy as np
from xml.dom import minidom

def jag_dir(xml_path, image_path, objective):
    left, right, top, bottom = False, False, False, False
    isJaguar = False
    jag_dir = []
    doc = minidom.parse(xml_path)
    objects = doc.getElementsByTagName("object")

    for objecti in objects:
        name = objecti.getElementsByTagName("name")[0].childNodes[0].data
        if name == 'Jaguar':
            xmin = int(objecti.getElementsByTagName("xmin")[0].childNodes[0].data)
            ymin = int(objecti.getElementsByTagName("ymin")[0].childNodes[0].data)
            xmax = int(objecti.getElementsByTagName("xmax")[0].childNodes[0].data)
            ymax = int(objecti.getElementsByTagName("ymax")[0].childNodes[0].data)
            isJaguar = True

    if not isJaguar:
        return None

    image = cv.imread(image_path)
    img_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            if img_gray[x][y] < 250:
                img_gray[x][y] = 0
            else:
                img_gray[x][y] = 255

    jaguar = img_gray[xmin:xmax, ymin:ymax]

    if jaguar[:,:int(jaguar.shape[1]/2)].any():  #Left
        left = True

    if jaguar[:,int(jaguar.shape[1]/2):].any(): #Right
        right = True

    if left and right:
        left, right = False, False

    if jaguar[:int(jaguar.shape[0]/2),:].any(): #Top
        top = True

    if jaguar[int(jaguar.shape[0]/2):,:].any(): #Bottom
        bottom = True

    if top and bottom:
        top, bottom = False, False

    directions = {'left': left, 'right': right, 'top': top, 'bottom': bottom}
    for direction in directions:
        if directions[direction]:
            jag_dir.append(direction)

    ret, labels = cv.connectedComponents(jaguar)
    itemindex = np.where(labels == 1)

    if len(jag_dir) == 2:
        v = abs(jaguar.shape[0]/2 - itemindex[0][0])
        if v > jaguar.shape[0]/4:
            directions[jag_dir[0]] = False
            jag_dir.pop(0)
        else:
            directions[jag_dir[1]] = False
            jag_dir.pop(1)

    # print(jag_dir[0])
    if jag_dir[0] == 'top':
        dot = (int((xmin+xmax)/2), ymin)
        angle_j = 90
    elif jag_dir[0] == 'bottom':
        dot = (int((xmin+xmax)/2), ymax)
        angle_j = 270
    elif jag_dir[0] == 'left':
        dot = (xmin, int((ymin+ymax)/2))
        angle_j = 180
    elif jag_dir[0] == 'right':
        dot = (xmax, int((ymin+ymax)/2))
        angle_j = 0

    x_sign = objective[0] - dot[0]
    y_sign = objective[1] - dot[1]

    if x_sign > 0 and y_sign > 0:
        orientation = "SE"
        angle_o = 315
    elif x_sign < 0 and y_sign < 0:
        orientation = "NW"
        angle_o = 135
    elif x_sign < 0 and y_sign > 0:
        orientation = "SW"
        angle_o = 225
    elif x_sign > 0 and y_sign < 0:
        orientation = "NE"
        angle_o = 45
    elif x_sign == 0 and y_sign > 0:
        orientation = "S"
        angle_o = 270
    elif x_sign == 0 and y_sign < 0:
        orientation = "N"
        angle_o = 90
    elif x_sign < 0 and y_sign == 0:
        orientation = "W"
        angle_o = 180
    elif x_sign > 0 and y_sign == 0:
        orientation = "E"
        angle_o = 0

    angle = angle_j - angle_o

    xc = int((xmin+xmax)/2) 
    yc = int((ymin+ymax)/2)
    plus = xc + yc
    minus = xc - yc

    if jag_dir[0] == 'top':
        rx = plus - dot[1]
        lx = dot[1] + minus

    elif jag_dir[0] == 'bottom':
        rx = dot[1] + minus
        lx = plus - dot[1]

    elif jag_dir[0] == 'left':
        dotf = [plus - dot[1], dot[0] - minus]
        rx = dot[0]
        lx = plus - dotf[1]

    elif jag_dir[0] == 'right':
        dotf = [plus - dot[1], dot[0] - minus]
        rx = plus - dotf[1]
        lx = dot[0]

    drx = rx - objective[0]
    print(drx, "=", rx, '-', objective[0])
    dlx = lx - objective[0]

    print(orientation)
    base_orientations = ['N', 'S', 'E', 'W']
    base_directions = {'N': 'top',
                        'S': 'bottom',
                        'E': 'right',
                        'W': 'left'}

    if orientation in base_orientations:
        final_dir = base_directions[orientation]
    
    elif drx > 0 and dlx < 0:
        if orientation == 'SE' or orientation == 'SW':
            final_dir = 'bottom'

        elif orientation == 'NE' or orientation == 'NW':
            final_dir = 'top'    

    elif dlx > 0:
        final_dir = 'left'

    elif drx < 0:
        final_dir = 'right'

    final_turn = {'top': {'top': 0, 
                    'right': 1, 
                    'bottom': 2, 
                    'left': 3},
            'right': {'top': 3, 
                    'right': 0, 
                    'bottom': 1, 
                    'left': 2},
            'bottom': {'top': 2, 
                    'right': 3, 
                    'bottom': 0, 
                    'left': 1},
            'left': {'top': 1, 
                    'right': 2, 
                    'bottom': 3, 
                    'left': 0}}

    print(jag_dir[0], final_dir)
    final_index = final_turn[jag_dir[0]][final_dir]
    print(final_index)

    angle = 0
    if final_index == 1:
        dot = (plus - dot[1]-1, dot[0] - minus)
        angle = 90
    elif final_index == 2:
        dot = (plus - dot[1]-1, dot[0] - minus)
        dot = (plus - dot[1], dot[0] - minus)
        angle = 180
    elif final_index == 3:
        dot = (plus - dot[1]-1, dot[0] - minus)
        dot = (plus - dot[1], dot[0] - minus)
        dot = (plus - dot[1], dot[0] - minus)
        angle = -90

    return final_dir, dot, angle

if __name__ == "__main__":
    jag_dir(r"C:\Users\coste\OneDrive\Desktop\Python\A Star\36.xml", r"C:\Users\coste\OneDrive\Desktop\Python\A Star\36.png", (400, 0))