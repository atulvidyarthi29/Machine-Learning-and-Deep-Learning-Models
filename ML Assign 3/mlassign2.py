'''
Cross entropy method
'''


import random
import pprint
import math

###file handling


training_data = 5128
total_data = 6523 
n_class = 4
target = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
rows = []                   ## contains the attributes
label = []                  ## contains the label for each instance correspondingly 
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
# rows = [[1,0,0],[1,0,1],[1,1,0],[1,1,1]]
# label = [[1,0],[0,1],[0,1],[1,0]]

###parameters

w1 = []
w2 = []


def sigmoid(x):
  return 1 / (1 + math.exp(-x))


def neural_network(nH):
    for i in range(nH):
        w1.append([])
        w1[i] = [0.1 * random.uniform(0.0,1.0) for j in range(len(rows[0]))]
    for i in range(n_class):
        w2.append([])
        w2[i] = [0.1 * random.uniform(0.0,1.0) for j in range(nH+1)]

def hiddenlayer(index,nH):
    hid_layer = [1.0 for i in range(nH+1)]
    for i in range(nH):
        temp = 0
        for j in range(len(rows[index])):
            temp = temp + rows[index][j] * w1[i][j]
        hid_layer[i+1] = sigmoid(temp)
    return hid_layer

def output_layer(hid_layer):
    Z = [0 for i in range(n_class)]
    for i in range(n_class):
        temp = 0
        for j in range(len(hid_layer)):
            temp = temp + hid_layer[j] * w2[i][j]
        Z[i] = sigmoid(temp)
    return Z
        

def back_propogation(index,hid_layer,output):
    for i in range(n_class):
        for j in range(len(hid_layer)):
            del2 = (label[index][i]/output[i]) * output[i] * (1-output[i]) * hid_layer[j]
            if (j!=0):
                for k in range(len(rows[index])):
                    del1 = (label[index][i]/output[i]) * output[i] * (1-output[i]) * w2[i][j] * hid_layer[j] * (1-hid_layer[j]) * rows[index][k]
                    w1[j-1][k] += 0.001 * del1
            w2[i][j] += 0.001 * del2

def error(index, output):
    sum1 = 0 
    for i in range(len(output)):
        sum1 += label[index][i]* math.log(output[i])
    return delta/2.0



def main():
    nH = 10
    print("training nH=",nH,"...\n")
    neural_network(nH)
    for i in range(10):
        print(i)
        for i in range(training_data):
            hid_layer = hiddenlayer(i,nH)
            output = output_layer(hid_layer)
            back_propogation(i,hid_layer,output)
    
    
    ## calculating training error
    print("calculating training error...\n")
    no_corrects = 0
    for i in range(training_data):
        hid_layer = hiddenlayer(i,nH)
        output = output_layer(hid_layer)
        class_label = output.index(max(output))
        if (class_label == label[i].index(1)):
            no_corrects = no_corrects + 1
    training_accuracy = (no_corrects*100)/float(training_data)
    print("training accuracy = ",training_accuracy,"\n")
    
    
    
    if (training_data != total_data):
        print("calculating testing error...\n")
        no_corrects = 0
        for i in range(training_data,total_data):
            hid_layer = hiddenlayer(i,nH)
            output = output_layer(hid_layer)
            class_label = output.index(max(output))
            if (class_label == label[i].index(1)):
                no_corrects = no_corrects + 1
        testing_accuracy = (no_corrects*100)/float(total_data-training_data)
        print("testing accuracy = ",testing_accuracy,"\n")
    
    



main()












