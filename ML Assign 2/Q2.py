import random
import copy
import math


# calculates XW
def mult1D2D(par , ft):
	product  = []
	for i in range(0, len(ft)):
		s = 0.0
		for j in range(0, len(par)):
			s = s + par[j]*ft[i][j]
		s =(1/1+math.exp(s))  
		if(s > 0.4):
			product.append(-1)
		else:
			product.append(1)
	return product


#calculates XW - Y
def diff1D1D(A, B):
	C = []
	for i in range(0, len(A)):
		C.append(A[i]-B[i])
	return C

# Calculates (XW-Y)(X)

def mult2D1D(p, x):
	prod = [0.0,0.0,0.0,0.0,0.0]
	for i in range(0,len(p)):
		for j in range(0,len(x[i])):
			prod[j] = prod[j] + x[i][j] * p[i]
	return prod

# Calculates the gradient
def differenciate(w, x, y, n):
	t = mult1D2D(w,x)
	p = diff1D1D(t, y)
	q = mult2D1D(p,x)
	for j in range(0, len(q)):
		q[j] = n * q[j]
	return q
	

#sigmoid function
'''
def sigmoid(X):
	sigg = []
	for i in range(0,len(X)):
		for j in range(0,len(X[i])): 
			sigg.append(1/(1+math.exp(-X[i][j])))
	print(sigg)
	return sigg
'''

# calculates the error
def error(w, x, y):
	t = mult1D2D(w, x)
	p = diff1D1D(t, y)
	error = 0.0
	for i in range(0,len(p)):
		error = error + (p[i] * p[i])
	return error/2.0


N = 70
file =  open("iris.data", "r")
lrows = file.readlines()
lrows.remove('\n')
# print(lt)
lt = []
listrows = []

tot = len(lrows)
for i in range(0,tot):
	lrows[i] = lrows[i][0:-1].strip()
	lrows[i] =  lrows[i].split(",")
	if lrows[i][-1] != 'Iris-setosa':
		lt.append(lrows[i])


tot = len(lt)
for i in range(0,N):
	listrows.append(lt.pop(random.randint(0,tot-1)))
	tot = tot-1

w = [0.5,0.5,0.5,0.0,0.0]		# feature parameters
x = []									# to store the feature space data
y = []									# to store the actual data
n = 0.1								# eta


for i in range(0, N):
	x.append([1])
	for j in range(0,len(listrows[i])-1):
		x[i].append(float(listrows[i][j]))
	if ((listrows[i][len(listrows[i])-1]) == 'Iris-versicolor'):
		y.append(-1)
	elif((listrows[i][len(listrows[i])-1]) == 'Iris-virginica'):
		y.append(1)

# training

er = 9999
ermin = 9999
wmin = w
for i in range(100000):
	diff = differenciate(w, x, y, n)
	for j in range(0,len(w)):
		w[j] =  w[j] + diff[j]
	er = error(w,x,y)
	#print(w,'\t',er,'\n')
	if (er < ermin):
		ermin = copy.deepcopy(er)
		wmin = copy.deepcopy(w)
print("Training:\n")
print("Parameters: ",wmin,'\nError: ',ermin,'\n')

# testing
xtest = []
ytest = []

for i in range(0, len(lt)):
	xtest.append([1])
	if listrows[i][len(listrows[i])-1] == 'Iris-setosa':
		pass
	for j in range(0,len(lt[i])-1):
		xtest[i].append(float(lt[i][j]))
	if ((lt[i][len(lt[i])-1]) == 'Iris-versicolor'):
		ytest.append(-1)
	elif((lt[i][len(lt[i])-1]) == 'Iris-virginica'):
		ytest.append(1)

testingerror =  error(w, xtest, ytest)
print("Testing Error: ",testingerror)

