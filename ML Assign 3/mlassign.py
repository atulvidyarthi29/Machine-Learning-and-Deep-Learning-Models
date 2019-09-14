'''
Sum of squared deviation
'''


import random
import pprint
import math
import matplotlib.pyplot as plt
# file handling

eta = 0.1
# training_data = 50
# total_data = 60


training_data = 5128
total_data = 6523
n_class = 4
target = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
rows = []  # contains the attributes
label = []  # contains the label for each instance correspondingly
x = []
y = []
x1 = []
y1 = []
fil = open("Colon_Cancer_CNN_Features.csv", 'r')
data = fil.readlines()
random.shuffle(data)
k = 0
for each in data:
    rows.append([1])
    r = each.split(',')
    for i in range(len(r)-1):
        rows[k].append(float(r[i]))
    label.append(target[int(r[-1][0:-1])-1])
    k = k+1

# training_data = 4
# total_data = 4
# n_class = 2
# target = [1,0],[0,1]
# rows = [[1,0,0],[1,1,0],[1,1,1],[1,0,1]]
# label = [[1,0],[0,1],[1,0],[0,1]]

# parameters


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def neural_network(nH):
    w1 = []
    w2 = []

    for i in range(nH):
        w1.append([])
        w1[i] = [random.uniform(-1.0, 1.0) for j in range(len(rows[0]))]
    for i in range(n_class):
        w2.append([])
        w2[i] = [random.uniform(-1.0, 1.0) for j in range(nH+1)]
    return w1, w2


def hiddenlayer(index, nH, w1):
    hid_layer = [1.0 for i in range(nH+1)]
    for i in range(nH):
        temp = 0
        for j in range(len(rows[index])):
            temp = temp + rows[index][j] * w1[i][j]
        hid_layer[i+1] = sigmoid(temp)

    return hid_layer


def output_layer(hid_layer, w2):
    Z = [0 for i in range(n_class)]
    for i in range(n_class):
        temp = 0
        for j in range(len(hid_layer)):
            temp = temp + hid_layer[j] * w2[i][j]
        Z[i] = sigmoid(temp)
    # print(Z)
    return Z


def back_propogation(index, hid_layer, output, w1, w2):
    for i in range(n_class):
        for j in range(len(hid_layer)):
            del2 = (label[index][i]-output[i]) * \
                output[i] * (1-output[i]) * hid_layer[j]
            if (j != 0):
                for k in range(len(rows[index])):
                    del1 = (label[index][i]-output[i]) * output[i] * (1-output[i]) * \
                        w2[i][j] * hid_layer[j] * \
                        (1-hid_layer[j]) * rows[index][k]
                    w1[j-1][k] += eta * del1
            w2[i][j] += eta * del2
    # print("second:", w2)
    return w1, w2


def error(index, output):
    delta = 0
    for i in range(len(output)):
        dif = label[index][i]-output[i]
        delta += dif * dif
    return delta/2.0


def main():
    for nH in range(5, 16):
        print("training nH=", nH, "...\n")
        x.insert(nH, nH)
        x1.insert(nH, nH)
        w1, w2 = neural_network(nH)
        for i in range(10):
            print(i)
            for j in range(training_data):
                hid_layer = hiddenlayer(j, nH, w1)
                output = output_layer(hid_layer, w2)
                w1, w2 = back_propogation(j, hid_layer, output, w1, w2)

        # calculating training error
        print("calculating training error...\n")
        no_corrects = 0
        for i in range(training_data):
            hid_layer = hiddenlayer(i, nH, w1)
            output = output_layer(hid_layer, w2)
            class_label = output.index(max(output))
            if (class_label == label[i].index(1)):
                no_corrects = no_corrects + 1
            #     print(no_corrects)
            # print(output, "\t", label[i])
        training_accuracy = (no_corrects*100)/float(training_data)
        print("training accuracy = ", training_accuracy, "\n")
        y.append(training_accuracy)

        if (training_data != total_data):
            print("calculating testing error...\n")
            no_corrects = 0
            for i in range(training_data, total_data):
                hid_layer = hiddenlayer(i, nH, w1)
                output = output_layer(hid_layer, w2)
                class_label = output.index(max(output))
                if (class_label == label[i].index(1)):
                    no_corrects = no_corrects + 1
                #     print(no_corrects)
                # print(output,"\t",label[i])
            testing_accuracy = (no_corrects*100) / \
                float(total_data-training_data)
            print("testing accuracy = ", testing_accuracy, "\n")
            y1.append(testing_accuracy)


main()

plt.plot(x, y, label="line 1")
plt.plot(x1, y1, label="line 2")


plt.xlabel('traning error\n testing error')

plt.ylabel('nH')


plt.show()
