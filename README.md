
# Analysis of Exploration and Production of Crude Oil
By Aditya Sastry <br>
QTM32625 - Financial Simulation <br>
December 3, 2015 <br>

-------------
## Table of Contents

- Will be generated here upon completion

## Introduction
-------------
### The  Oil Industry
There activities of the Oil and Gas (O&G) industry are split into three major components: upstream, midstream, and downstream. This report is concerned only with the upstream segment of the industry in the production of crude oil from onshore reserves. The search for oil, exploration, as well as the extraction of the oil from the ground, production, are the major functions of upstream production of crude oil. The exploration for reserves is carried out with seismic sensors that can scan swatches of land in 2d or 3d. This strategy is especially cheap and effective over water as a boat with the sensor can easily position and maneuver to cover large amounts of ground. On land this task is more difficult with a ground team needing to set up the technology at multiple consecutive locations to gather the required data. Depending on the terrain, this can be a time consuming and expensive task. Once this data is analyzed, and indicates the presence of hydrocarbons at a mineable depth, the next step is to to take samples of the area that is being prospected. Based on the data collected, a model is built for the quantity of oil in the ground (original oil in place) in the sampled area.<br><br>If the ground samples indicate a presence of hydrocarbons with suitable geological conditions, an exploratory well is drilled to the depth of the reserve. This task can be extremely expensive, and can vary greatly in the time taken to complete. As this is generally done by specialized drilling firms due to the cost and difficulty of transport of the drilling rigs, the O&G company generally only takes the risk of not finding oil but sometimes is also liable for worker safety and other factors depending on contract specifics. During and after the drilling process, samples are being taken from the extracted rock and reserve if oil is found. These are used to increase the accuracy of the reserve estimation and to gain a better understanding for the nature of the rock, reserve, and many other geological features that determine the ability to produce from the well. If all these factors are analyzed and indeed positive, the firm moves forward to drill a production well. Oftentimes, many wells are drilled in the same oilfield, but for the sake of this model the assumption of one well being drilled is taken for simplicity. It is possible to extend this model to multiple wells. Once the production well is drilled, a steel casing is fitted to maintain the integrity of the well with a specialized valve secured to the top. From this stage, crude oil production begins.<br><br>
The next stage in the process is reffered to as the *midstream*. This includes the transportation and storage of the recovered crude product from the upstream operation to the downstream. Refining and point of sale operations are the bulk of the downstream business.<br>


### Goals and Narrative for the Proposed Model

This paper and accompanying Python model are designed to simulate the profitability of the exploration, production, and sale of crude oil from an O&G firm's risk management standpoint. The location of Texas for E&P was chosen due to the availibilty of data and the large market for "light, sweet crude", benchmarked by the West Texas Intermediate commodity spot price traded out of Cushing, Oklahoma. This largely eliminates transportation and storage costs, however the model does allow for this to be included despite it being upstream focused. The current state of the model makes assumptions for the entire process from a time before any work is started, however it would most effectively be used when assumptions are updated on an ongoing basis with real values as work is carried out. <br><br>
The firm is looking to drill a single well in Texas after being tipped off to possible oil reserves. They will simulate the entire process of exploraton and production to understand the present value and risks of the project. As the firm is from Europe, their knowledge of the U.S. market is naive so they have decided to utilize Monte-Carlo simulation for all major parameters with conservative values to understand whether they are interested in investing. They are very concerned about the recent collapse in crude prices as well as the very large cash outlay required to undertake any E&P venture.

## Modeling the Profitability of Oil Exploration
-------------

### Exploration Costs Pre-Discovery of Hydrocarbons
Costs for on-shore seismic methods are estimated to be between \$8,000 and $50,000 per square kilometer depending on the terrain and the quality of method used to perform the scanning operation. In the case of Texas, the flat land and low-risk environment suggests a cost on the lower end of the range. As this price derives its value from a number of underlying factors such as manpower, movement and lease of equipment, number of days required, a triangular distribution was chosen. An additional \$500 per kilometer was added to include the cost of processing. Finally, a second triangular distribution for the analysis of the data was added. This distribution was once again chosen as the cost of the analsysis is based on the terrain, equipment used, and challenge of interpretation. The stated range of \$100,000 - \$1,000,000 includes values from the most simple output, to the most challenging. As Texas is a desert with minimal surface features such as mountains or other major geological feautures, a low cost is realistic. However, due to a lack of experience in the industry, a conservative mode of \$500,000 was chosen. The time spent on this stage is not factored into the overall project duration as it is only after this stage that the commitment to drilling the exploratory well is taken. Before this decision is made, the following models would need to be re-run with the actual cost of the initial study included.


```python
import numpy as np
import matplotlib.pyplot as plt

def preHydrocarbonExpense():
	seismicCost = np.random.triangular(8,16,50) #single value for simulation
	seismicCost += 0.5 # Add processing cost of $500/km
	seismicCost += np.random.triangular(100,500,1000) # Add the cost of analysis of the data
	return seismicCost
```

**Distribution with  n= 10,000**
![Total Seismic Cost](http://i.imgur.com/fHKxZNU.png?1)
**Descriptive Statistics**<br>

### Probability of Finding Oil
Now that the initial study has found appropriate sites for drilling, there is still a chance that the well does not actually strike oil. This situation is called a *dry well* or *dry hole.* The model for this probability is provided by the following equation:
> $$ P_{Successful\ Well} = P_{Hydrocarbons} \times P_{Reservoir} \times P_{Seal} \times P_{Structure} $$

Mun's model for the probabilty of a dry-hole is one of the few availible, however technology has significantly improved since the publication of the book CITE. Due to this the standard deviation of the $P_{Hydrocarbons}$ and $P_{Reservoir}$ has been decreased by 25% in the provided model. 


```python
def dryWellProb():
	techDisc = 0.25
	techDisc = 1 - techDisc

	pHydrocarbons = np.random.normal(.99,(.05*techDisc))
	pStructure = np.random.normal(1,0)
	pReservoir = np.random.normal(.75,(.1*techDisc))
	pSeal = np.random.normal(1,0)

	pSuccess = pHydrocarbons * pStructure * pReservoir * pSeal
	return pSuccess
```

**Distribution with  n= 10,000**
![Successful Well Drilling Distribution](https://i.imgur.com/lvgAsjR.png)
**Descriptive Statistics**<br>
mean = 0.743627352943 <br>
var = 0.00619156981964<br>
max = 1.07112346165<br>
std dev = 0.0786865288321<br>
min = 0.446050355766

### Exploratory Well Drilling
With an idea of the probability of not finding oil, the time and cost of drilling the first well to test the underground reserves that are hopefully found. While the inital stages of off-shore exploration are significantly cheaper than onshore, the drilling cost can be orders of magnitude more expensive. Both methods use a similar amount of time, but the nature of deep see, and even shallow water operations make them far more costly. As oil companies as well as E&P firms rarely own their own drilling platforms, the service must be contracted out to specialized firms.
The cost of these operations vary according to two major factors: the time it takes to drill and the depth of the hole.
> Some 70-75% of the drilling costs are proportional to the duration of the drilling ... Only 25-30% pf the drilling costs acan therefore be estimated with a reasonable degree of precision. These are the costs which depend on the depth drilled(essentially the casing), the cost of the wellhead, etc.

Based on the above statement, estimating the days required as well as the depth and other known costs seems to be an effective way to analyze the cost of the well. Contracts for drilling are generally quoted on a *dayrate*, but infrequently there are contracts for a fixed value granted.

*First draft note*: I found liturature on the JAS and MRI models of drilling price estimation (after completing this section), which seems to be superior to what I used. I will apply this model and compare it to mine in the final draft.  It's based on a regression with known independent variables and dummy variables.

#### Drilling Time
Estimations of onshore drilling have a range of 20 days to 120 days based on examining multiple sources. This variablity is often due to geographical challenges and hazards as well as somewhat frequent delays that occur. As Texas, specifically West and North Texas where oil is relatively abundant, there are not major geographical or geological challenges. Due to this, a normal distribution with $\mu = 60\  days,\ \sigma = 7\ days$ was chosen. The assumption that projects that do not face significant delays have a 95.45% chance of being completed +/- two weeks of the 60 day estimate seems reasonable based on emperical evidence.<br><br>
However, as there are "frequent" delays, a number that is not explicitly quantified in any of the literature reviewed, this must be taken into account. Based on capital budgeting projects from other industries, the assumed frequency of significant delays (exceeding the included two week margin) is assumed at 15% of projects. In the case of a delay, a duration of three to six weeks is chosen uniformly due to the number of possible issues that could lead to an unpredictable range of delays.


```python
def expDrillTime():
	pDelay = 0.15 #Probability of a significant delay
	projectTime = np.random.normal(60, 7) ## Base drilling time in days
	if np.random.random()>= (1-pDelay): # Delay 
		projectTime += np.random.random_integers(21, 42) # Delay duration
	return projectTime
```

**Distribution with  n= 10,000**
![Distribution of Drill Time](https://i.imgur.com/ldEuoNf.png?1)
**Descriptive Statistics**<br>
var = 182.833607838<br>
max = 121.444493103<br>
min = 35.9150658456<br>
std dev = 13.5215978286<br>
mean = 64.6659908965

#### Drilling Depth
There are a few quantitative models for estimating drilling depth based on a number of geological factors. However, rather than crudely estimating these paramteres, forecasting the average drilling depth in the United States for exploratory Oil wells based on the U.S. Energy Information Administration (EIA) reports seemed more prudent. With either industry data or experimental results, using geological simulation would very likely result in a more accurate outcome.
<br><br>
The EIA provides average well depths for a number of parameters including the type of resource such as oil, natural gass, etc., as well as the three types of wells: dry, exploratory, and development. Last updated in August 2015, data from 1949 to 2008 is provided. A simple linear regression of the coded year, 1-60 rather than 1949-2008, as the independent variable with the depth of wells as the dependent variable yields a strong explanatory model. With an $R^2$ value of 83.79% and P-Values significant at $\alpha = 0.05$ for both the slope and intercept, the least squares regression appears to be a strong fit. This equation was then used to forecast for well depth in the year 2016, the estimated completion year of the Texas project.
*First Draft Note* I plan on updating the regression to a time series model before the final paper


```python
def forecastDepth(year):
	wb = load_workbook('EIA_Report.xlsx') #EIA data
	dataSheet = wb['data'] # Cells D4:D63 contain the time series
	exploratoryDepths = []
	for i in range(60): # Extract data into python
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

	'''plt.plot(x,y,'o',label = 'Actual')
	plt.plot(x, m*x + c, 'r', label = 'Regression')
	plt.legend()
	plt.show()'''

	return [(c + m*(year-1948)),(c + m*(year-1948))+1.96*(1013.568999323128/np.sqrt(60)),(c + m*(year-1948))-1.96*(1013.568999323128/np.sqrt(60))]
```

**Regression Fit**
![LSRL Fit](http://imgur.com/A5R8VMe.png?1)
**Metrics**<br>
Slope = 53.5730758544<br>
Intercept = 4433.00451977<br>
$R^2$ = 0.83789022<br>
Standard Error = 415.0682772<br>
P Value of Slope = $1.93 \times 10^{-44}$<br>
P Value of Intercept = $1.38 \times 10^{-24}$

**Forecast**<br>
2016 Point Forecast = 8075.97 ft<br>
95% Interval Assuming Normality = {7819.50 ft,8332.44 ft}

#### Logging
During the process and after the exploratory well is drilled, the extracted mud as well as contents of the well is scientifically tested on an ongoing basis for hydrocarbons and various properties of the surrounding geology. The cost driver for this operation is simplified to a price per meter drilled at a rateof \$150 - \$200 per meter. This is simulated below based on two uniform distributions, the depth based on the confidence interval, and the cost based on the price estimate discussed above.


```python
def loggingCost():
	depth = np.random.uniform(wellDepthL,wellDepthH) # Didn't call forecastDepth() since my data isn't changing currently
	cost = np.random.uniform(150,200)
	return (cost*(depth*0.3048))/1000 # convert to meters, and stay in 1000s of dollars
```

**Distribution with  n= 10,000**
![Logging Cost](http://imgur.com/h2euTuJ.png?1)
**Descriptive Statistics**<br>
mean = 430.620158006 <br>
max = 507.001264337 <br>
min = 358.009308527 <br>
var = 1331.10505205 <br>
std dev = 36.4843124102 <br>

### Simulating Exploration Cost
Now that a model for the cost drivers, probabilities, and some of the costs are established, a Monte Carlo simulation can be developed. The follwing model will be the basis of the trials
$$  Cost_{Exploration} = Cost_{Pre-Discovery} + Binary_{Dry\ Well} \times Cost_{Dry\ Well} + Drill\ Time \times Cost_{Daycost} + Cost_{Logging} + Binary_{Blowout} \times Cost_{Blowout}$$ 
#### Blowout Probability
Despite the safety advanced in the industry, oilfield engineering and services remain as some of the most dangerous jobs in America. This is due to hazardous machinery, working conditions, and the chance of blowouts. The probability of a blowout must be included in the model as they do occur with some frequency. The Alberta Energy and Utilities Board provides the frequency of onshore drilling blowouts as $4.9 \times 10^{-4}$ per well drilled. This includes both exploratory and development wells. As this is not a development well and there is no oil being extracted, the cost would be related to equipment damage and perosnal injury. Due to this, a uniform distribution from \$1-$10 million was chosen. This number is low as the contracting out of the drilling limits the liability exposure of the oil producing firm.


```python
def disaster():
	if np.random.random()*100000 <= 49:
		return True
	else:
		return False
```

#### Simulation Parameters
Due to the low probability of blowouts, 100,000 iterations are used. This should result in approximately 49 blowouts.


```python
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
for i in range(100000):
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
```

**Results**
![Imgur](http://i.imgur.com/E22x1kf.png?1)<br>
**Descriptive Statistics of Distributions** <br><br>
Pre Discovery <br>
{'min': 118.13273740013858, 'mean': 558.52465853312526, 'max': 1036.231553353226, 'std dev': 184.40997012647824, 'var': 34007.037082048599}<br><br>
Dry Well<br>
{'min': 0.0, 'mean': 230.38033958811891, 'max': 1927.7981618156189, 'std dev': 404.02718578433763, 'var': 163237.96685281169}<br>
Number of Dry Holes: 25857<br><br>
Drilling Cost<br>
{'min': 0.0, 'mean': 876.93401096964806, 'max': 2586.5669671874443, 'std dev': 568.00266905455442, 'var': 322627.03205309768}<br><br>
Logging Cost<br>
{'min': 0.0, 'mean': 319.4819701434327, 'max': 507.72216355231461, 'std dev': 191.25481412734604, 'var': 36578.40392688568}<br><br>
Blowout Expense<br>
{'min': 0.0, 'mean': 2.8805883214128825, 'max': 9880.2628265295079, 'std dev': 136.46317034458568, 'var': 18622.196860495409}<br>
Number of Blowouts: 55<br><br>
Total Cost<br>
{'min': 691.92367861168032, 'mean': 1988.2015675557375, 'max': 11747.77587031666, 'std dev': 468.40263224528638, 'var': 219401.025894313}

## Simulation of Crude Oil Production: Costs, Output & Revenue
-------------
### Prospect evaluation, how much Oil is there?
The standard model for prosepect evaluation of onshore oil reserves is the *Original Oil In Place* (OOIP) equation:
$$ N = \frac{7758Ah\phi(1-S_w)}{B_{oi}}\ \times\ E $$
Where:<br> $A$ = reservoir area (Acres) <br> $h$ = thickness (Feet) <br> $\phi$ = Porosity REF <br> $S_w$ = Water Saturation <br> $B_{oi}$ = Formation volume factor <br> $E$ = Recovery Factor<br><br>
As these are specific to observed soil samples and analysis of drilled mud, a simplified model will be used for the scope of this simulation:
$$ N = Area\ \times\ Net\ Thickness\ \times\ Recovery\ Factor$$
### Production Duration
The lifetime production of an oil well is constantly decreasing at a growing rate as the pressure and volume decreases. The standard equation to model this is:$$q_t\ =\ q_ie^{-Dt}$$<br>
Where:<br>$q_t\ =\ Rate\ of\ production\ at\ time\ t$<br>$q_i\ =\ Initial\ rate\ of\ production$<br>$D\ =\ decline\ rate\ \% $<br>$t\ =\ time$
<br><br>
To model this, a further simulation will be used based on the follwing table from Oil and Gas Monitor, except with the start dates being sampled from the exploration simulation: <br>

|Factor|Distribution   | Low | Mid  | High  |
|---|---|---|---|---|
| qi  | Lognormal  |90   | 100  |125   |
| D  | Beta  |0.5%   |1%   | 7.5%  |
| Minimum  | Constant  | 20  | 20  | 20  |
<br>
### Production Cost
### Future Value of Oil
The West Texas Intermediate (WTI) commodity spot price will be used to benchmark the value of produced crude. Numerous quantitative and analytical models have been used to forecast the price of the commodity, however due to the recent collapse of the price of the asset, there is a great deal of uncertainty. Tradional econometric time series models such as auto-regressive moving-average models are unlikely to perform favorably despite being considered the most accurate in the short and medium term. (HMM possible) Financial models using future prices to estimate changes in spot prices has historically shown that future prices are not efficiently priced, rather than having predictive power over spot prices. Models that rely on economic data would seemingly have the best accuracy in a market so heavily impacted by supply/demand shifts and global manipulation of prices. Factoring in OPEC behavior, EIA reports GDP, and other economic variables has been tested but is most effective with an analytical neural network (ANN). ANNs seem to outperform econometric models in long term forecasts as well.
<br>
![Imgur](http://i.imgur.com/xOIGwvr.png?1)
<br>
There is an ongoing economic debate about whether the build in prices from 2004 to 2014 was irrational, and the price drop in late 2014 is the return to rational prices. Due to the recent nature of the price drop and the lack of literature on the current state of the asset, I will be using a geometric random walk to simulate the price process of crude oil during the production phase. Arguments exist for both mean reverting and random walk models for oil, however the current situation calls for consvertism in forecasting. This is why a geometric random walk was chosen rather than a mean reverting process.
<br>
![Imgur](http://i.imgur.com/O6IN8Pp.png)
<br>


```python
import Quandl as q
from datetime import datetime
import numpy as np
import pandas as p
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as ts

apiKey = "JqjPBo2L93BKkEh3fEo2"
#wtiData = q.get("EIA/PET_RWTC_D", authtoken=apiKey) # pull in data from the EIA on spot price of WTI
#wtiData.to_excel('WTI.xlsx', 'wti') # store it so I don't exceed my 50 api call limit
wtiData = p.read_excel('WTI.xlsx','wti', index_col= None, na_values = ['NA'])
wtiData = p.DataFrame(wtiData)
wtiData = wtiData.set_index('Date')
wtiShort = wtiData['2014-12-25':'2015-11-29'].values # Conver to Numpy array for iterating

for i in wtiShort: # could have done this faster with matrix operations
	last = 0
	count = 0
	logDiff = []
	if count == 0:
		count += 1
		last = i
	elif count > 0:
		logDiff.append(np.log(i/last))
		last = i
	else:
		print("You goofed in calculating log diffs")
		break

sigma = np.std(logDiff)
print("Sigma = " + str(sigma))
mu = np.mean(logDiff) + (0.5*sigma)**2
print("Mu = " + str(mu))

def gmr(mu, sigma, s, t, dt):
	n = round(t/dt)
	t = np.linspace(0,t,n)
	w = np.random.standard_normal(size = n)
	w = np.cumsum(w)*np.sqrt(dt)
	x = (mu-0.5*sigma**2)*t + sigma*w
	s = s*np.exp(x)
	return np.array(s)

def makeWalks(itr, mu, sigma, s, t, dt):
	randwalk = np.array([])
	randwalk = gmr(mu, sigma, s, t, dt)
	for i in range(itr-1):
		randwalk =np.column_stack((randwalk, gmr(mu, sigma, s, t, dt)))
	return randwalk

randwalk = makeWalks(500, mu, sigma, 40.3, 100, 1) # 40.3 being latest wti-spot price
plt.plot(randwalk)
plt.show()
```

**100 Day N=5 GMR Simulation**
![Imgur](http://i.imgur.com/MAH84dK.png)
**100 Day N=500 GMR Simulation**
![Imgur](http://i.imgur.com/YUxInH8.png)
<br>
All the values are stored in a two dimensional array so any oil produced can be marked to market at the appropriate day. This model assumes that oil is only produced and sold during trading days, not Saturday or Sunday. To add this would simply involve duplicating Friday values for the following two periods. Additionally it assumes that produced crude is being sold at closing prices, not intraday prices.

## Bringing it All Together: Analysis of the Drilling Opportunity

### Simulation of E&P
#### Results
#### Analysis

# Conclusion

## First Draft Notes

- After trasferring my notebook from TeX to Jupyter/iPython I'm having trouble getting my bibliography and citations to work right and export from BibTeX. I will work this out by the final draft, and a I do have all my sources cited thoroughly.

- The Notebook code segments do not currently generate the correct output. I have a rough idea of why this is happening, but as I need to use for loops in each code segment to run the trials, it seems more prudent to simply input the images and raw output from the local instance of the console.

- Ordering of descriptive stats is random as they are printed from a python dictionary


```python
def descriptiveStats(list):
	stats = {
		'mean': np.mean(list),
		'std dev': np.std(list),
		'min' : np.amin(list),
		'max' : np.amax(list),
		'var' : np.var(list)
	}
	return stats
```

# Bibliography

- Markdown destroyed all formatting. Will revise.

“Average Depth of Crude Oil and Natural Gas Wells.” 8–31 2015. Web. <br><br>
Behmiri, Niaz B., and José R. Pires Manso. “Crude Oil Price Forecasting Techniques: A Comprehensive Review of Literature.” Web.<br><br>
“Blowout Frequencies.” Mar. 2010. Web.<br><br>
Bret-Rouzaut, Nadine, and Jean-Pierre Favennec. Oil and Gas Exploration and Production: Reserves, Costs, Contracts. Editions TECHNIP, 2011. Print.<br><br>
Charpentier, Ronald R., and T.R. Klett. “A Monte Carlo Simulation Method for the Assessment of Undiscovered, Conventional Oil and Gas.” 2008. Web.<br><br>
Duara, Nigel. “In West Texas Oil Boomtowns, ‘the End Is near.’” latimes.com. N.p., 3 Mar. 2015. Web. 3 Dec. 2015. <br><br>
“ESTIMATING DRILLING COSTS-2: Indices Describe Complexity of Drilling Directional, Extended-Reach Wells.” Oil & Gas Journal 105.30 (2007): n. pag. Web. 3 Dec. 2015. <br><br>
Kaiser, Mark J. “A Survey of Drilling Cost and Complexity Estimation Models.” International Journal of Petroleum Science and Technology 1.1 (2007): 1–22. Web. <br><br>
---. “ESTIMATING DRILLING COSTS-1: Joint Association Survey, Mechanical Risk Index Methods Common in GOM.” Oil & Gas Journal 105.32 (2007): n. pag. Web. <br><br>
Mun, Johnathan. Modeling Risk: Applying Monte Carlo Simulation, Real Options Analysis, Forecasting, and Optimization Techniques. John Wiley & Sons, 2006. Print. <br><br>
“Probabilistic Approach to Oil and Gas Prospect Evaluation Using the Microsoft Excel Spreadsheet.” Web.<br><br>
Pulsipher, Allan G. “ESTIMATING DRILLING COSTS-Conclusion: Systems Approach Combines Hybrid Drilling Cost Functions.” Oil & Gas Journal 105.32 (2007): n. pag. Web. 3 Dec. 2015. <br><br>
Sustakoski, Rick J., and Diana Morton-Thompson. “Reserves Estimation.” Web.
“The Land Rig Newsletter.” Apr. 2015. Web. <br><br>
Toews, Gerhard, and Alexander Naumov. “The Relationship Between Oil Price and Costs in the Oil and Gas Industry.” Web.
