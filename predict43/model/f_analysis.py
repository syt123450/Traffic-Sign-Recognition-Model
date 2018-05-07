import numpy as np
import matplotlib.pyplot as plt

def read_in_file(file_name):
    with open(file_name) as fh:
        res = [list(map(float, line.split(","))) for line in fh]
    return res

def average_each_class(target_list):
    ret = [0 for i in range(len(target_list))]
    for idx in range(len(target_list)):
        # print(target_list[idx])
        ret[idx] = sum(target_list[idx])/float(len(target_list[idx]))
    return ret

if __name__ == "__main__":
    res = read_in_file("/Users/zchholmes/Desktop/255/Project/train_base/models/test_results/fscore.txt")
    print(type(res))
    print(len(res))

    accuracy_list = res[0::4]
    precision_list = res[1::4]
    recall_list = res[2::4]
    f_list = res[3::4]

    print(len(accuracy_list))
    print(len(precision_list))
    print(len(recall_list))
    print(len(f_list))

    avg_acc_list = average_each_class(accuracy_list)
    avg_pre_list = average_each_class(precision_list)
    avg_rec_list = average_each_class(recall_list)
    avg_f_list = average_each_class(f_list)
    print(avg_acc_list)
    print(avg_pre_list)
    print(avg_rec_list)
    print(avg_f_list)

    x_marks = ["Origin", "Impv1", "Impv2", "Impv3", "Impv4", "Impv5"]
    # plt.plot(x_marks, avg_acc_list, 'r-', label="Avg. Accuracy")
    plt.plot(x_marks, avg_pre_list, 'b-', label="Avg. Precision")
    plt.plot(x_marks, avg_rec_list, 'g-', label="Avg. Recall")
    plt.plot(x_marks, avg_f_list, 'r-', label="Avg. F Score")
    plt.show()