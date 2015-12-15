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
SUMqProd =[]
NPVrevProd = []
NPVcProd = []
NPVnetProd = []
finalRev = []
numDryHole = 0
numBlowOut = 0
npvProd = []
yr = 0.02213
dailyRate = 0.0061
npvOilVal = []
# Assumptions
for i in range(1000):
	#Vars
	### EXPLORATION ###
	exDrillTime = expDrillTime()
	dayCost = drillDaycost()
	cPreDiscover.append(preHydrocarbonExpense())
	if np.random.random() < dryWellProb():
		cDryWell.append(exDrillTime*dayCost*0.75) # Only drilling time, no analysis with a discount for less processing and other costs
		cDrill.append(0)
		cLogging.append(0)
		dryWell = True
	else:
		cDryWell.append(0)
		cDrill.append(exDrillTime*dayCost)
		cLogging.append(loggingCost())
		numDryHole += 1
		dryWell = False
	blowout = disaster()
	blowoutExpense = np.random.uniform(1000,10000)
	if blowout:
		cBlowout.append(blowoutExpense)
		numBlowOut += 1
	else:
		cBlowout.append(0)
	#if i > 0:
	cExploration.append(cPreDiscover[i]+cDryWell[i]+cDrill[i]+cLogging[i]+cBlowout[i])

	### PRODUCTION ###
	if not dryWell:
		prodCost = prodCostBarrel()
		prodDrillTime = expDrillTime()
		timeRemaining = int(np.floor((5*240) - (exDrillTime + prodDrillTime))) # 5 years - exploration and production drill time
		randomWalk = gmr(40.3, timeRemaining, 1) # Generate spot oil prices for time remaining days
		# Arrays to be reset each simulation
		qProd =[]
		revProd = []
		cProd = []
		netProd = []
		oilVal = []
		for x in range(timeRemaining):
			prodQ = prodQt(i+1)
			qProd.append(prodQ)
			revProd.append(randomWalk[x]*prodQ)
			cProd.append(prodQ*prodCost)
			netProd.append(revProd[x]-cProd[x])
			oilVal.append(randomWalk[x])
		npvProd.append(np.npv(dailyRate, netProd))
		NPVcProd.append(np.npv(dailyRate, cProd))
		NPVrevProd.append(np.npv(dailyRate, revProd))
		SUMqProd.append(np.sum(qProd))
		npvOilVal.append(np.npv(dailyRate, oilVal))
		finalRev.append(np.npv(dailyRate, netProd)-1000.0*(cPreDiscover[i]+cDryWell[i]+cDrill[i]+cLogging[i]+cBlowout[i]))
	else:
		finalRev.append(-1000.0*(cPreDiscover[i]+cDryWell[i]+cDrill[i]+cLogging[i]+cBlowout[i]))
		npvProd.append(0)

print("Pre Discovery")
print(descriptiveStats(cPreDiscover))
print(percentilesC(cPreDiscover))
print("Dry Well")
print(descriptiveStats(cDryWell))
print(percentilesC(cDryWell))
print("Number of Dry Holes: " + str(numDryHole))
print("Drilling Cost")
print(descriptiveStats(cDrill))
print(percentilesC(cDrill))
print("Logging Cost")
print(descriptiveStats(cLogging))
print(percentilesC(cLogging))
print("Blowout Expense")
print(descriptiveStats(cBlowout))
print(percentilesC(cBlowout))
print("Number of Blowouts: " + str(numBlowOut))
print("Total Cost")
print(descriptiveStats(cExploration))
print(percentilesC(cExploration))


print("Production Quantity")
print(descriptiveStats(SUMqProd))
print(percentilesC(SUMqProd))
print("Production Cost")
print(descriptiveStats(NPVcProd))
print(percentilesC(NPVcProd))
print("Production Revenue")
print(descriptiveStats(NPVrevProd))
print(percentilesC(NPVrevProd))
print("Production P&L")
print(descriptiveStats(npvProd))
print(percentilesC(npvProd))
print("Oil Value")
print(descriptiveStats(npvOilVal))
print(percentilesC(npvOilVal))
print("Project Revenue")
print(descriptiveStats(finalRev))
print(percentilesC(finalRev))

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
plt.hist(cExploration, bins = 100)
plt.title('Total Cost')


plt.figure(2)
plt.subplot(321)
plt.hist(SUMqProd, bins = 100)
plt.title('Production Quantity')
plt.subplot(322)
plt.hist(NPVcProd, bins = 100)
plt.title('Production Cost')
plt.subplot(323)
plt.hist(NPVrevProd, bins = 100)
plt.title('Production Revenue')
plt.subplot(324)
plt.hist(npvProd, bins = 100)
plt.title('Production P&L')
plt.subplot(325)
plt.hist(npvOilVal, bins = 100)
plt.title('Oil Value')
plt.subplot(326)
plt.hist(finalRev, bins = 100)
plt.title('Project Revenue')
plt.show()

