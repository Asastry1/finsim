# Dependencies
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook

### Let's get some descriptive stats ###
def descriptiveStats(list):
	stats = {
		'mean': np.mean(list),
		'std dev': np.std(list),
		'min' : np.amin(list),
		'max' : np.amax(list),
		'var' : np.var(list)
	}
	return stats

### Pre-Discovery Cost Model ###
# Triangular distribution of siesmic mapping per square KM in 1000s
#!# Returns: 1 random draw
def preHydrocarbonExpense():
	seismicCost = np.random.triangular(8,16,50) #single value for simulation
	seismicCost += 0.5 # Add processing cost of $500/km
	seismicCost += np.random.triangular(100,500,1000) # Add the cost of analysis of the data
	return seismicCost

### Probability Model for Dry Well ###
# Note: Norm dist is not bounded to upper limit of 1
def dryWellProb():
	techDisc = 0.25 # discount % for technology improvements since below forecasts were published
	techDisc = 1 - techDisc
	pHydrocarbons = np.random.normal(.99,(.05*techDisc))
	pStructure = 1
	pReservoir = np.random.normal(.75,(.1*techDisc))
	pSeal = 1

	pSuccess = pHydrocarbons * pStructure * pReservoir * pSeal
	return pSuccess

# Does our well produce?
#!# Returns: True = Good Well, False = Dry Well
def dryWellBinary():
	if np.random.random() < dryWellProb:
		return False
	else:
		return True

# Distribution graphing
'''z=[]
for i in range(10000):
	z.append((dryWellProb()))
r = plt.hist(z, bins = 100)
plt.show()
stats = descriptiveStats(z)
for i in stats:
	print(str(i) + " = " + str(stats[i]))'''

### Drilling Time Estimation ###
#!# Returns 1 random draw
def expDrillTime():
	pDelay = 0.15 #Probability of a significant delay
	projectTime = np.random.normal(60, 7) ## Base drilling time in days
	if np.random.random()>= (1-pDelay): # Delay 
		projectTime += np.random.random_integers(21, 42) # Delay duration
	return projectTime

# Distribution graphing
'''z=[]
for i in range(10000):
	z.append((expDrillTime()))
r = plt.hist(z, bins = 100)
plt.show()
stats = descriptiveStats(z)
for i in stats:
	print(str(i) + " = " + str(stats[i]))'''

### Well Depth Forecast ###
#!# Returns: [spot estimate, upper bound 95% CI, lower bound 95% CI]
def forecastDepth(year):
	wb = load_workbook('EIA_Report.xlsx')
	dataSheet = wb['data']
	exploratoryDepths = []
	for i in range(60):
		exploratoryDepths.append(int(dataSheet['D'+ str(i+4)].value))
	#print(exploratoryDepths)
	#print(descriptiveStats(exploratoryDepths))
	x = [i+1.0 for i in range(60)] # Build 1-60 for LSRL X values
	y = exploratoryDepths
	x = np.array(x)
	y = np.array(y)
	A = np.vstack([x,np.ones(len(x))]).T
	m, c = np.linalg.lstsq(A,y)[0]  # Where m = b1, c = b0
	#print("slope = " + str(m) + "\n" + "intercept = " + str(c)) 

	# Regression graphing
	'''plt.plot(x,y,'o',label = 'Actual')
	plt.plot(x, m*x + c, 'r', label = 'Regression')
	plt.legend()
	plt.show()'''

	return [(c + m*(year-1948)),(c + m*(year-1948))+1.96*(1013.568999323128/np.sqrt(60)),(c + m*(year-1948))-1.96*(1013.568999323128/np.sqrt(60))]

#!!! Values stored for computational speed, MUST BE UPDATED IF PARAMS CHANGED
wellDepthPt = 8075.97367787
wellDepthL = 7819.50533537
wellDepthH = 8332.44202037

### Analysis Costs ###
#!# Returns 1 draw
def loggingCost():
	depth = np.random.uniform(wellDepthL,wellDepthH) # Didn't call forecastDepth() since my data isn't changing currently
	cost = np.random.uniform(150,200)
	return (cost*(depth*0.3048))/1000 # convert to meters, and stay in 1000s of dollars

'''z=[]
for i in range(10000):
	z.append((loggingCost()))
r = plt.hist(z, bins = 100)
plt.show()
stats = descriptiveStats(z)
for i in stats:
	print(str(i) + " = " + str(stats[i]))'''

### Probability of a Blowout ###
#!# Returns: True = disaster, False = good drill
def disaster():
	if np.random.random()*100000 <= 49:
		return True
	else:
		return False

### Drilling Cost Per Day ###
#!# Returns: 1 Draw
def drillDaycost():
	return np.random.triangular(14.9,17,23)