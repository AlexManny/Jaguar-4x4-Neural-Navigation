from xml.dom import minidom
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
xml_path = r"C:\Users\coste\OneDrive\Desktop\Python\A Star\36.xml"

def white_objects():
    doc = minidom.parse(xml_path)
    objects = doc.getElementsByTagName("object")
    jag_pos, red_pos = [], []

    for objecti in objects:
        name = objecti.getElementsByTagName("name")[0].childNodes[0].data
        if name == 'Jaguar':
            xmin = int(objecti.getElementsByTagName("xmin")[0].childNodes[0].data)
            ymin = int(objecti.getElementsByTagName("ymin")[0].childNodes[0].data)
            xmax = int(objecti.getElementsByTagName("xmax")[0].childNodes[0].data)
            ymax = int(objecti.getElementsByTagName("ymax")[0].childNodes[0].data)
            jag_pos.append((xmin, xmax, ymin, ymax))
        elif name == 'Red':
            xmin = int(objecti.getElementsByTagName("xmin")[0].childNodes[0].data)
            ymin = int(objecti.getElementsByTagName("ymin")[0].childNodes[0].data)
            xmax = int(objecti.getElementsByTagName("xmax")[0].childNodes[0].data)
            ymax = int(objecti.getElementsByTagName("ymax")[0].childNodes[0].data)
            red_pos.append((xmin, xmax, ymin, ymax))

    return jag_pos, red_pos


# l = white_objects()
# print(l)

if __name__ == "__main__":
    white_objects()