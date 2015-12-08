# Dependencies
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from openpyxl import load_workbook

### Oil Production Model ###

## Reserve Analysis

def ooip(A, h, chi, sw, Boi, E):
	N = ((7758*A*h*chi*(1-sw))/Boi)*E
	return N
	
## Decline Analysis

def prodQt(t):
	qi = np.random.triangular(85,96,125)
	D = np.random.triangular(0.005,0.01, 0.05)
	minimum = 20.0
	qt = qi*np.exp(-1*D*t)
	if(qt<minimum):
		qt = minimum
	return qt

arr = []
for i in range(480):
	arr.append(prodQt(i))

plt.plot(arr)
plt.show()