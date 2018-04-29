import sys
import os
import random
import time
from collections import defaultdict

def generate_movement_list(root_path, new_path, suffix = '.jpg', ratio = 0.1):
    if ratio > 1 or ratio < 0:
        ratio = 0

    if not os.path.exists(new_path):
        os.mkdir(new_path)

    from_list = []
    to_list = []

    from_class_path = []
    to_class_path = []
    for file in os.listdir(root_path):
        if not file.startswith('.'):
            from_class_path.append(os.path.join(root_path, file))
            to_class_path.append(os.path.join(new_path, file))

    for file in to_class_path:
        if not os.path.exists(file):
            os.mkdir(file)

    for idx in range(len(from_class_path)):
        image_dict = defaultdict(list)
        for filename in os.listdir(from_class_path[idx]):
            if filename.endswith(suffix):
                basename, extension = os.path.splitext(filename)
                raw_id, sub_id = basename.split('_')
                image_dict[raw_id].append(sub_id)

        for k, v in image_dict.items():
            split_num = int(len(v) * ratio)
            split_num = 1 if split_num == 0 else split_num
            ids = random.sample(range(0, len(v)), split_num)
            for id in ids:
                from_list.append(os.path.join(from_class_path[idx], str(k) + '_' + str(v[id]) + suffix))
                to_list.append(os.path.join(to_class_path[idx], str(k) + '_' + str(v[id]) + suffix))

    start = time.time()
    for fp, tp in zip(from_list, to_list):
        os.rename(fp, tp)
    print("Moved {} files in {} seconds".format(len(from_list), time.time() - start))

    return

root_path = "/Users/zchholmes/src_images/testImages"
new_path = "/Users/zchholmes/src_images/movedImages"
suffix = '.jpg'
ratio = 0.1
generate_movement_list(root_path, new_path, suffix, ratio)

# print('arg_1', sys.argv[1])
# print('arg_2', sys.argv[2])
# print('arg_3', sys.argv[3])
# print('arg_4', sys.argv[4])

# generate_movement_list(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

# print(from_list[:5])
# print(to_list[:5])
#
# print(len(from_list))
# print(len(to_list))
