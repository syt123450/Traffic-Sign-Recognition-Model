from PIL import Image
img = Image.open("./00000_00000.ppm")
img.save("./test.jpg")

import os

sign_number = 0

if not os.path.exists("./images/"):
    os.makedirs('./images/')

for folder_number in range(0, 43):
    folder_path = "./GTSRB/Final_Training/Images/" + str(folder_number).zfill(5) + '/'
    output_base_dir = './images/' + str(folder_number).zfill(5) + '/'
    if not os.path.exists(output_base_dir):
        os.makedirs(output_base_dir)
    print(folder_path)
    for situation_number in range(0, 1000):
        situation_number_format = str(situation_number).zfill(5)
        first_situation_path = folder_path + \
                               str(situation_number).zfill(5) + '_00000.ppm'
        if not os.path.exists(first_situation_path):
            break
        for sign_situation_number in range(0, 1000):
            input_image_path = folder_path + \
                         str(situation_number).zfill(5) + '_' + str(sign_situation_number).zfill(5) + '.ppm'
            if os.path.exists(input_image_path):
                output_image_name = str(situation_number).zfill(5) + '_' + str(sign_situation_number).zfill(5) + '.jpg'
                output_image_path = output_base_dir + output_image_name
                img = Image.open(input_image_path)
                img.save(output_image_path)
            else:
                break
