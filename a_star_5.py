import cv2
import numpy as np
import os
import math
from white_objects import white_objects
from jag_dir import jag_dir
from jag_mov import jag_mov

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):
    n = len(maze)
    m = len(maze[0])
    
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while open_list:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            while current_node is not None:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        children = []
        for new_position in [( 0, -1), ( 0,  1), (-1,  0), ( 1,  0), 
                             (-1, -1), (-1,  1), ( 1, -1), ( 1,  1)]:
            node_position = (current_node.position[0] + new_position[0], 
                             current_node.position[1] + new_position[1])

            if not (0 <= node_position[0] < n and 0 <= node_position[1] < m) or maze[node_position[1],node_position[0]].any():
                continue

            new_node = Node(current_node, node_position)
            
            children.append(new_node)

        for child in children:
            if child in closed_list or child in open_list:
                continue

            child.g = current_node.g + 1
            child.h = abs(child.position[0] - end_node.position[0]) + \
                      abs(child.position[1] - end_node.position[1]) 
            child.f = child.g + child.h

            open_list.append(child)

refPt = []

def set_se(event, x, y, flags, param):
	# grab references to the global variables
	global refPt
 
	# if the left mouse button was clicked, record the starting (x,y)
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
 
	# # check to see if the left mouse button was released
	# elif event == cv2.EVENT_LBUTTONUP:
	# 	# Record the ending (x, y) coordinates
	# 	refPt.append((x, y))

def main():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    path = "C:\\Users\\coste\\OneDrive\\Desktop\\Python\\A Star\\10.png"

    # Load image, clone it, and setup the mouse callback function
    image = cv2.imread(path, -1)
    # clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", set_se)

    # Keep looping until the 'q' key is pressed
    while True:

        # Display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # If the 'r' key is pressed, reset the query
        if key == ord('r'):
            image = clone.copy()

        # If the 'c' key is pressed, break from the loop
        elif key == ord('c'):
            break
    
    # if len(refPt) == 2:
    #     print(refPt)
    #     cv2.waitKey(0)

    cv2.circle(image, refPt[0], 3, (0,0,255), 2)
    # cv2.circle(image, refPt[1], 3, (0,0,255), 2)
    
    cv2.imwrite("end_start.png", image)
    
    # close all open windows
    cv2.destroyAllWindows()

    # spots = white_objects()
    direction = jag_dir(r"C:\Users\coste\OneDrive\Desktop\Python\A Star\10.xml", r"C:\Users\coste\OneDrive\Desktop\Python\A Star\10.png", refPt[0])
    print(direction)

    start = direction[1]
    end = refPt[0]

    # for i in spots[1]:
    #     image[i[2]:i[3],i[0]:i[1]] = [255,255,255]

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret,thresh1 = cv2.threshold(image,254,255,cv2.THRESH_BINARY)
    cv2.imshow('image',thresh1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    path = astar(thresh1, start, end)
    print(path)

    jag_mov(path, direction[0], direction[2])

    thresh1 = cv2.cvtColor(thresh1, cv2.COLOR_GRAY2BGR)
    for i in range (len(path)):
        thresh1[path[i][::-1]] = [0,0,255]

    cv2.imwrite("path.png", thresh1)

if __name__ == '__main__':
    main()   