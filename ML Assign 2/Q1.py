import random
import pprint


# calculates XW
def mult1D2D(par , ft):
	product  = []
	for i in range(0, len(ft)):
		s = 0.0
		for j in range(0, len(par)):
			s = s + par[j]*ft[i][j]
		product.append(s)
	return product

# calculates XW - Y
def diff1D1D(A, B):
	C = []
	for i in range(0, len(A)):
		C.append(A[i]-B[i])
	return C

# Calculates (XW-Y)(X)
def mult2D1D(p, x):
	prod = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	for i in range(0,len(p)):
		for j in range(0,len(x[i])):
			prod[j] = prod[j] + x[i][j] * p[i]
	return prod


# Calculates the gradient
def differenciate(w, x, y, n, N):
	t = mult1D2D(w,x)
	p = diff1D1D(t, y)
	q = mult2D1D(p,x)
	for j in range(0, len(q)):
		q[j] = 2*n * q[j] / N
	return q
	
# calculates the error
def error(w, x, y, N):
	t = mult1D2D(w, x)
	p = diff1D1D(t, y)
	error = 0.0
	for i in range(0,len(p)):
		error = error + (p[i] * p[i])
	return error/(N)



N = 200
file =  open("yacht_hydrodynamics.data", "r")
lt = file.readlines()
lt.remove('\n')
listrows = []

tot = 308
for i in range(0,N):
	listrows.append(lt.pop(random.randint(0,tot-1)))
	tot = tot-1

w = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]		# feature parameters
x = []									# to store the feature space data
y = []									# to store the actual data
n = 0.01								# eta


for i in range(0, N):
	listrows[i] = listrows[i][0:-1].strip()
	listrows[i] =  listrows[i].split(" ")
	x.append([1])
	for j in range(0,len(listrows[i])-1):
		if listrows[i][j] == '':
			pass
		else:
			x[i].append(float(listrows[i][j]))
	y.append(float(listrows[i][len(listrows[i])-1]))


# training
e1 = 0.0
while(True):
	diff = differenciate(w, x, y, n, N)
	for j in range(0,len(w)):
		w[j] =  w[j] - diff[j]
	e2 = error(w,x,y,N)
	if (abs(e1-e2)< 0.000001):
		print("Parameters:\t",w,"\nTraining Error:\n", e2)
		break
	e1 = e2


#testing
xtest = []
ytest = []

for i in range(0, len(lt)):
	lt[i] = lt[i][0:-1].strip()
	lt[i] =  lt[i].split(" ")
	xtest.append([1])
	for j in range(0,len(lt[i])-1):
		if lt[i][j] == '':
			pass
		else:
			xtest[i].append(float(lt[i][j]))
	ytest.append(float(lt[i][len(lt[i])-1]))


trainingerror =  error(w, xtest, ytest, len(lt))
print("Testing Error: ",trainingerror)
