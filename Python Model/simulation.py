# Dependencies
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook

# Model Files
from explorationModel import *
from productionModel import *
from oilForecast import *

#### SIMULATION ####
# Vars
cExploration = []
cPreDiscover = []
cDryWell = []
cDrill = []
cLogging = []
cBlowout = []

numDryHole = 0
numBlowOut = 0
# Assumptions
for i in range(10000):
	#Vars
	if np.random.random() < dryWellProb():
			dryWell = False
	else:
		dryWell = True
		numDryHole += 1
	#print(dryWell)
	drillTime = expDrillTime()
	dayCost = drillDaycost()
	cPreDiscover.append(preHydrocarbonExpense())
	if dryWell:
		cDryWell.append(drillTime*dayCost*0.75) # Only drilling time, no analysis with a discount for less processing and other costs
		cDrill.append(0)
		cLogging.append(0)
	else:
		cDryWell.append(0)
		cDrill.append(drillTime*dayCost)
		cLogging.append(loggingCost())
	blowout = disaster()
	blowoutExpense = np.random.uniform(1000,10000)
	if blowout:
		cBlowout.append(blowoutExpense)
		numBlowOut += 1
	else:
		cBlowout.append(0)
	#if i > 0:
	cExploration.append(cPreDiscover[i]+cDryWell[i]+cDrill[i]+cLogging[i]+cBlowout[i])

print("Pre Discovery")
print(descriptiveStats(cPreDiscover))
print("Dry Well")
print(descriptiveStats(cDryWell))
print("Number of Dry Holes: " + str(numDryHole))
print("Drilling Cost")
print(descriptiveStats(cDrill))
print("Logging Cost")
print(descriptiveStats(cLogging))
print("Blowout Expense")
print(descriptiveStats(cBlowout))
print("Number of Blowouts: " + str(numBlowOut))
print("Total Cost")
print(descriptiveStats(cExploration))

plt.figure(1)
plt.subplot(321)
plt.hist(cPreDiscover, bins = 100)
plt.title('Pre-Discovery')
plt.subplot(322)
plt.hist(cDryWell, bins = 100)
plt.title('Dry Well')
plt.subplot(323)
plt.hist(cDrill, bins = 100)
plt.title('Drilling Cost')
plt.subplot(324)
plt.hist(cLogging, bins = 100)
plt.title('Logging Cost')
plt.subplot(325)
plt.hist(cBlowout, bins = 50)
plt.title('Blowout Cost')
plt.subplot(326)
f = plt.hist(cExploration, bins = 100)
plt.title('Total Cost')
plt.show()