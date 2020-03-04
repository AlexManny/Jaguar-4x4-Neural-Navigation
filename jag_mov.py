import socket

def jag_mov(path, start, angle):
    # Set the host ip and port
    tcp_ip = '192.168.0.101'
    tcp_port = 62727
    message = ""

    # This represent all the movement that Jaguar must execute to reach end spot
    vector = []

    # For every element in path calculate how Jaguar is moving in geographical coordonates
    for i in range(0, len(path) - 1):
        if path[i][0] == path[i + 1][0] and path[i][1] > path[i + 1][1]:  # south
            vector.append("top")
        if path[i][0] == path[i + 1][0] and path[i][1] < path[i + 1][1]:  # north
            vector.append("bottom")
        if path[i][0] < path[i + 1][0] and path[i][1] == path[i + 1][1]:  # west
            vector.append("right")
        if path[i][0] > path[i + 1][0] and path[i][1] == path[i + 1][1]:  # east
            vector.append("left")
        if path[i][0] < path[i + 1][0] and path[i][1] < path[i + 1][1]:  # north-west
            vector.append("bottom-right")
        if path[i][0] > path[i + 1][0] and path[i][1] > path[i + 1][1]:  # south-east
            vector.append("top-left")
        if path[i][0] < path[i + 1][0] and path[i][1] > path[i + 1][1]:  # south-west
            vector.append("top-right")
        if path[i][0] > path[i + 1][0] and path[i][1] < path[i + 1][1]:  # north-east
            vector.append("bottom-left")

    # This represents number of pixels driven by Jaguar
    steps = 0

    # Vector that consists of all directions of the path
    direction = []

    # Vector that consists of all real distances driven by Jaguar
    distance = []

    # Vector that consists of all rotation angles
    angles = []

    # Relation between pixel and cm
    measure = 0.7
    diagonal_measure = 1.2

    turns = {'top': {'top': 0, 
                    'right': 90, 
                    'left': -90, 
                    'top-right': 45,
                    'top-left': -45},
            'right': {'right': 0, 
                    'bottom': 90, 
                    'top': -90, 
                    'bottom-right': 45,
                    'top-right': -45},
            'bottom': {'bottom': 0, 
                    'left': 90, 
                    'right': -90, 
                    'bottom-left': 45,
                    'bottom-right': -45},
            'left': {'left': 0, 
                    'top': 90, 
                    'bottom': -90, 
                    'top-left': 45,
                    'bottom-left': -45}}

    diagonal = ['bottom-right', 'bottom-left', 'top-right', 'top-left']

    # Extract distance and orientation
    for i in range(1, len(vector)):
        if (vector[i] == vector[i - 1]):
            steps += 1
        else:
            direction.append(vector[i - 1])
            angles.append(turns[start][vector[i-1]])
            if vector[i-1] not in diagonal:
                distance.append((int)(steps * measure))
            else:
                distance.append((int)(steps * measure * diagonal_measure))
            steps = 0

    direction.append(vector[len(vector) - 1])
    angles.append(turns[start][vector[len(vector) - 1]])
    if vector[len(vector) - 1] not in diagonal:
        distance.append((int)(steps * measure))
    else:
        distance.append((int)(steps * measure * diagonal_measure))

        # comanda = ""
        # comanda = "sendCommand({0},{1})".format(angles[i], 0)

        #     # Create the client socket and send comand to the host via Jaguar wi-fi network
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect((tcp_ip, tcp_port))
        # message = comanda
        # arr = message.encode()
        # s.send(arr)
        # s.close()

        # print(comanda)

    # Build that command for the Jaguar, it can drive in 8 direction
    # for i in range(0, len(angles)):
    #     if (i == 0):
    #         continue

    comanda = ""
    comanda = "sendCommand({0},{1})".format(90, 0)
    comanda = "Hello!"

    # Create the client socket and send comand to the host via Jaguar wi-fi network
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((tcp_ip, tcp_port))
    message = comanda
    arr = message.encode()
    s.send(arr)
    s.close()

    print(comanda)

    # Send command that will mark the end of the image processing
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((tcp_ip, tcp_port))
    message = "endCommand"
    arr = message.encode()
    s.send(arr)
    s.close()

    print('directie', direction, 'distanta', distance, 'angles', angles)