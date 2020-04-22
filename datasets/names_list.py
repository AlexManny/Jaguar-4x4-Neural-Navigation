import os

anno = os.listdir('jaguarVOC/Annotations')
imgs = os.listdir('jaguarVOC/Images')

with open("images_train.txt", "w") as file:
    for i in range(int(len(imgs)*0.8)):
        j = imgs[i].replace('.png', '')
        file.write(j + " -1" + "\n")

with open("images_val.txt", "w") as file:
    for i in range(int(len(imgs)*0.8), int(len(imgs))):
        j = imgs[i].replace('.png', '')
        file.write(j + " -1" + "\n")