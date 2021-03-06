

<br><br><br><br><br><br><br><br><br><br>




<br><br><br>








# Analysis of Exploration and Production of Crude Oil











By Aditya Sastry <br>
QTM32625 - Financial Simulation <br>
December 14, 2015 <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>



## Executive Summary
------------
While it is likely the tip that has been received by our company about the presence of oil in a one square kilometer region in Northern Texas is accurate, the risk management department cannot recommend any projects at this time. The extreme cost of exploration will not be recovered by the production of crude oil at this time due to the current low price of the West Texas Intermediate spot commodity, and the risk of it dropping further. The long life of these projects makes them even more risky, as well as our lack of information about the specifics of the site in Texas strengthens the strong belief that this project is not possible at this time. This is even more so due to the average simulated loss of \$2 million 5 years into the project despite this being the required breakeven period. 

## Analysis
-------------
### The  Oil Industry
The activities of the Oil and Gas (O&G) industry are split into three major components: upstream, midstream, and downstream. This report is concerned exclusively with the upstream segment of the industry, specifically in the production of crude oil from onshore reserves. The search for oil, exploration, as well as the extraction of the oil from the ground, production, are the major functions of upstream sector of crude oil. <br><br>The exploration for reserves is carried out with seismic sensors that can scan swatches of land in 2d or 3d (Bret-Rouzaut and Favennec 126). This strategy is especially cheap and effective over water as a boat with the sensor can easily position and maneuver to cover large amounts of ground. On land this task is more difficult with a ground team needing to set up the technology at multiple consecutive locations to gather the required data (Bret-Rouzaut and Favennec 126). Depending on the terrain, this can be a time consuming and expensive task. Once the data is analyzed, and indicates the presence of hydrocarbons at a mineable depth, the next step is to take samples of the area that is being prospected. Based on the data collected, a model is built for the quantity of oil in the ground reserves of (original oil in place) the sampled area. If the ground samples indicate a presence of hydrocarbons with suitable geological conditions, an exploratory well is drilled to the depth of the reserve. This task can be extremely expensive and can vary greatly in the time taken to complete. As this is generally done by specialized drilling firms due to the cost and difficulty of transporting oil rigs, the O&G company generally only takes the risk of not finding oil but sometimes is also liable for worker safety and other factors depending on contract specifics. During and after the drilling process, samples are taken from the extracted rock and reserve if oil is found. These are used to increase the accuracy of the reserve estimation and to gain a better understanding for the nature of the rock, reserve, and many other geological features that determine the ability to produce from the well. If all these factors are analyzed and indeed positive, the firm moves forward to drill a production well after conducting extensive engineering and design studies. Oftentimes, multiple wells are drilled in the same oilfield, but for the sake of this model the assumption of one well being drilled is taken for simplicity. It is possible to extend this model to multiple wells. Once the production well is drilled, a steel casing is fitted to maintain the integrity of the hole with a specialized valve secured to the top. From this stage, crude oil production begins.<br><br>
The next step in the process is referred to as the *midstream*. This includes the transportation and storage of the recovered crude product, linking the upstream operation to the downstream. Refining, marketing and point of sale operations make up the downstream business.<br>


### Goals and Narrative for the Proposed Model

This paper and accompanying Python model are designed to simulate the profitability of the exploration, production, and sale of crude oil from an O&G firm's risk management standpoint. The location of Texas for E&P was chosen due to the availability of data and the large market for "light, sweet crude", benchmarked by the West Texas Intermediate commodity spot price traded out of Cushing, Oklahoma. This largely eliminates transportation and storage costs, however the model does allow for this to be included despite it being upstream focused. The current state of the simulation makes assumptions for the entire process from a time before any work is started, however it would most effectively be used when assumptions are updated on an ongoing basis with real values as work is carried out. <br><br>
The firm is looking to drill a single well in Texas after being tipped off to possible oil reserves. They will simulate the entire process of exploration and production to understand the present value and risks of the project. As the firm is from Europe, their knowledge of the U.S. market is naive so they have decided to utilize Monte-Carlo simulation for all major parameters with conservative values to understand whether they are interested in investing. They are very concerned about the recent collapse in crude prices as well as the very large cash outlay required to undertake any E&P venture. There have however been positive signs in Texas as production values continue to rise. Additionally, they plan on selling the oil on a Mercantile Exchange rather than going through the trouble of carrying out midstream or downstream work. They also have decided, against risk managements advice, to not hedge their production with WTI futures. The firm is also only interested in a project that can generate profits within 5 years of beginning the exploration process.
<br>

### Exploration Costs Pre-Discovery of Hydrocarbons
Costs for onshore seismic methods are estimated to be between \$8,000 and \$50,000 per square kilometer depending on the terrain and the technology used to perform the scanning operation (Bret-Rouzaut and Favennec 125)(Cooper). In the case of Texas, the flat land and low-risk environment suggests a cost on the lower end of the range. As this price derives its value from a number of underlying factors such as manpower, movement and lease of equipment, number of days required, a triangular distribution was chosen. An additional \$500 per kilometer was added to include the cost of processing (Bret-Rouzaut and Favennec 127). Finally, a second triangular distribution for the analysis of the data was added. This distribution was once again chosen as the cost of the analysis is based on the terrain, equipment used, and challenge of interpretation. The stated range of \$100,000 - \$1,000,000 includes values from the simplest output, to the most challenging (Bret-Rouzaut and Favennec 127). As Texas is a desert with minimal surface features such as mountains or other major geological features, a low cost is realistic. However, due to a lack of experience in the industry, a conservative mode of \$500,000 was chosen. The time spent on this stage is not factored into the overall project duration as it is only after this stage that the commitment to drilling the exploratory well is taken. Before this decision is made, the following models would need to be re-run with the actual cost of the initial study included.


```python
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
> $$ P_{Successful\ Well} = P_{Hydrocarbons} \times P_{Reservoir} \times P_{Seal} \times P_{Structure} $$ (Mun 18)

Mun's model for the probability of a dry-hole is one of the few available, however technology has significantly improved since the publication of the book (Mun 19). Due to this, the standard deviation of the $P_{Hydrocarbons}$ and $P_{Reservoir}$ has been decreased by 25% in the provided model. This probability will be used to calculate when a well is successful or not in the final simulation.


```python
def dryWellProb():
	techDisc = 0.25 # Discount % for improved technology
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
mean = 0.74 <br>
var = 0.006<br>
max = 1.07<br>
std dev = 0.07<br>
min = 0.44

### Exploratory Well Drilling
As oil companies as well as E&P firms rarely own their own drilling platforms, the service must be contracted out to specialized firms.
The cost of these operations vary according to two major factors: the time it takes to drill and the depth of the hole.

> Some 70-75% of the drilling costs are proportional to the duration of the drilling ... Only 25-30% pf the drilling costs can therefore be estimated with a reasonable degree of precision. These are the costs which depend on the depth drilled (essentially the casing), the cost of the wellhead, etc.

(Bret-Rouzaut and Favennec 125)

Based on the above statement, estimating the days required as well as the depth and other known costs seems to be an effective way to analyze the cost of the well. Contracts for drilling are generally quoted at a *dayrate* rather than a lump-sum value, however the latter case does occur in special situations (Pulsipher).

#### Drilling Time
Estimations of onshore drilling have a range of 20 days to 120 days based on examining Bret-Rouzaut and Favennec's estimates as well as the Energen2015 annual report (Bret-Rouzaut and Favennec 128). This variability is often due to geographical challenges and hazards as well as somewhat frequent delays that occur. As Texas, specifically West and North Texas where oil is relatively abundant, the assumption that there are not major geographical or geological challenges is made. Due to this, a normal distribution with $\mu = 60\  days,\ \sigma = 7\ days$ was chosen. The assumption that projects that do not face significant delays have a 95.45% chance of being completed +/- two weeks of the 60 day estimate seems reasonable based on collected data.<br><br>
However, as there are "frequent" delays, a number that is not explicitly quantified in any of the literature reviewed, a penalty period must be added in a certain number of cases. Based on capital budgeting projects from other industries, the assumed frequency of significant delays (exceeding the included two week margin) is assumed at 15% of projects. In the case of a delay, a duration of three to six weeks is chosen uniformly due to the number of possible issues that could lead to an unpredictable range of delays.


```python
def expDrillTime():
	pDelay = 0.15 # Probability of a significant delay
	projectTime = np.random.normal(60, 7) # Base drilling time in days
	if np.random.random()>= (1-pDelay): # Delay occurs
		projectTime += np.random.random_integers(21, 42) # Penalty duration added
	return projectTime # Total drilling time
```

**Distribution with  n= 10,000**
![Distribution of Drill Time](https://i.imgur.com/ldEuoNf.png?1)
**Descriptive Statistics**<br>
var = 182.83<br>
max = 121.44<br>
min = 35.91<br>
std dev = 13.52<br>
mean = 64.66

#### Drilling Depth
There are a few quantitative models for estimating drilling depth based on a number of geological factors. Rather than crudely estimating these parameters, forecasting the drilling depth in the United States for exploratory Oil wells based on the U.S. Energy Information Administration (EIA) reports seemed more reliable. With either industry data or experimental results, using geological simulation would very likely result in a more accurate outcome however neither were available at the time of this report.
<br><br>
The EIA provides average well depths for a number of parameters including the type of resource such as oil or natural gas, as well as the three types of wells: dry, exploratory, and development. Last updated in August 2015, data from 1949 to 2008 is provided for the depth of exploratory oil wells (“Average Depth of Crude Oil and Natural Gas Wells.”). A simple linear regression of the coded year, 1-60 rather than 1949-2008, as the independent variable with the depth of wells as the dependent variable yields a strong explanatory model. With an $R^2$ value of 83.79% and P-Values significant at $\alpha = 0.05$ for both the slope and intercept, the least squares regression appears to be a strong fit. This equation was then used to forecast for well depth in the year 2016, the estimated completion year of the Texas project.


```python
def forecastDepth(year):
	wb = load_workbook('EIA_Report.xlsx') #EIA data
	dataSheet = wb['data'] # Cells D4:D63 contain the time series
	exploratoryDepths = []
	for i in range(60): # Extract data into python
		exploratoryDepths.append(int(dataSheet['D'+ str(i+4)].value))
	x = [i+1.0 for i in range(60)] # Build 1-60 for LSRL X values
	y = exploratoryDepths
	x = np.array(x)
	y = np.array(y)
	A = np.vstack([x,np.ones(len(x))]).T
	m, c = np.linalg.lstsq(A,y)[0]  # Where m = b1, c = b0
	return [(c + m*(year-1948)),(c + m*(year-1948))+1.96*(1013.568999323128/np.sqrt(60)),(c + m*(year-1948))-1.96*(1013.568999323128/np.sqrt(60))]
```

**Regression Fit**
![LSRL Fit](http://imgur.com/A5R8VMe.png?1)
**Metrics**<br>
Slope = 53.57<br>
Intercept = 4433.00<br>
$R^2$ = 83.78%<br>
Standard Error = 415.06<br>
P Value of Slope = $1.93 \times 10^{-44}$<br>
P Value of Intercept = $1.38 \times 10^{-24}$

**Forecast**<br>
2016 Point Forecast = 8075.97 ft<br>
95% Interval Assuming Normality = {7819.50 ft,8332.44 ft}

#### Logging
During the process and after the exploratory well is drilled, the extracted mud as well as contents of the well is scientifically tested on an ongoing basis for hydrocarbons and various properties of the surrounding geology. The cost driver for this operation is simplified to a price per meter drilled at a rate of \$150 - \$200 per meter (Bret-Rouzaut and Favennec 130). This is simulated below based on two uniform distributions, the depth based on the confidence interval, and the cost based on the price estimate discussed above.


```python
def loggingCost():
	depth = np.random.uniform(wellDepthL,wellDepthH) # Didn't call forecastDepth() since the year isn't changing currently
	cost = np.random.uniform(150,200)
	return (cost*(depth*0.3048))/1000 # convert to meters, and stay in 1000s of dollars
```

**Distribution with  n= 10,000**
![Logging Cost](http://imgur.com/h2euTuJ.png?1)
**Descriptive Statistics**<br>
mean = 430.62 <br>
max = 507.00 <br>
min = 358.00 <br>
var = 1331.10 <br>
std dev = 36.48 <br>

### Simulating Exploration Cost
Now that a model for the cost drivers, probabilities, and some of the costs are established, a Monte Carlo simulation can be developed. The following model will be the basis of the trials
$$  Cost_{Exploration} = Cost_{Pre-Discovery} + (Binary_{Dry\ Well} \times Cost_{Dry\ Well}) + (Drill\ Time \times Cost_{Daycost}) + Cost_{Logging} + (Binary_{Blowout} \times Cost_{Blowout})$$ 
#### Blowout Probability
Despite the safety advances in the industry, oilfield engineering and services remain as some of the most dangerous jobs in America. This is due to hazardous machinery, working conditions, and the chance of blowouts. The probability of a blowout must be included in the model as they do occur with some frequency. The Alberta Energy and Utilities Board provides the frequency of onshore drilling blowouts as $4.9 \times 10^{-4}$ per well drilled (“Blowout Frequencies.”). This includes both exploratory and development wells. As this is not a development well and there is no oil being extracted, the cost would be related to equipment damage and personal injury. Due to this, a uniform distribution from \$1-$10 million was chosen. This number is low as the contracting out of the drilling limits the liability exposure of the oil producing firm.


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
cExploration = [] # Cost of Exploration
cPreDiscover = [] # Pre-discovery costs
cDryWell = [] # Dry well cost
cDrill = [] # Drilling cost
cLogging = [] # Logging cost
cBlowout = [] # Blowout cost

numDryHole = 0 # Number of dry holes simulated
numBlowOut = 0 # Number of blowouts simulated
for i in range(100000): # 100,000 iterations
	drillTime = expDrillTime()
	dayCost = drillDaycost()
	cPreDiscover.append(preHydrocarbonExpense())
	blowout = disaster()
	blowoutExpense = np.random.uniform(1000,10000)
	if np.random.random() < dryWellProb():
		cDryWell.append(0)
		cDrill.append(drillTime*dayCost)
		cLogging.append(loggingCost())
	else:
		cDryWell.append(drillTime*dayCost*0.75)
		cDrill.append(0)
		cLogging.append(0)
		numDryHole += 1
	if blowout:
		cBlowout.append(blowoutExpense)
		numBlowOut += 1
	else:
		cBlowout.append(0)
	cExploration.append(cPreDiscover[i]+cDryWell[i]+cDrill[i]+cLogging[i]+cBlowout[i])
```

**Results**
![Imgur](http://i.imgur.com/E22x1kf.png?1)<br>
**Descriptive Statistics of Total Cost** <br><br>
min: 691.92<br> mean: 1988.20<br> max: 11747.77<br> std dev: 468.40<br> var: 219401.02

** Analysis**

90% of the Total Cost falls below \$2,563,143, however the maximum value is nearly $12 million. This is due to the occurrence of blowouts that incur a significant cost. This risk could bankrupt the company if it is not managed during the exploratory drilling process. The right skewed nature of the total cost is a positive sign as the cost is more likely to fall in the fat left tail. Subtracting the total cost from the present value of production profits will give the total project value.

### Prospect evaluation, how much Oil is there?
The standard model for prospect evaluation of onshore oil reserves is the *Original Oil In Place* (OOIP):
$$ N = \frac{7758Ah\phi(1-S_w)}{B_{oi}}\ \times\ E $$
Where:<br> $A$ = reservoir area (Acres) <br> $h$ = thickness (Feet) <br> $\phi$ = Porosity REF <br> $S_w$ = Water Saturation <br> $B_{oi}$ = Formation volume factor <br> $E$ = Recovery Factor<br><br>

(Sustakoski and Morton-Thompson 513)

As these are specific to observed soil samples and analysis of drilled mud, a function to output this value has been written; however, for the scope of this report a simplified model will be used. As there is a 5 year cap on breaking even, the model will only use the production duration calculated below to asses this project under the assumption that there is more oil than can be extracted in 5 years - (exploration + production). The data available on porosity and other factors seems to be rarely published, or behind a paywall and any kind of distributional analysis seems to be absent. Some example simulations exist, however they seem to have entirely fabricated data. 
### Production Duration
Due to the fact that a time limit has been imposed on the project, the model will assume that the entire reserve of the well will not be exhausted in the given timeframe. The lifetime production of an oil well is constantly decreasing at a growing rate as the pressure and volume decreases. The standard equation to model this is the exponential decline function ("Traditional Decline Curve Analysis"):$$q_t\ =\ q_ie^{-Dt}$$<br>
Where:<br>$q_t\ =\ Rate\ of\ production\ at\ time\ t$<br>$q_i\ =\ Initial\ rate\ of\ production$<br>$D\ =\ decline\ rate\ \% $<br>$t\ =\ time$
<br><br>
To model this, a further simulation will be used based on the following table from Oil and Gas Monitor, except with the start dates being sampled from the exploration simulation ("Risk Analysis and Oil Production Curves"): <br>

|Factor|Distribution   | Low | Mode  | High  |
|---|---|---|---|---|
| qi  | Lognormal<br>(10%,50%,90%)  |90   | 100  |125   |
| D  | Beta  |0.5%   |1%   | 7.5%  |
| Minimum  | Constant  | 20  | 20  | 20  |
<br>
As this data was provided in Low, Mode, High format, triangular distributions will be fitted to best match the CDF of the suggest distributions. While this is not ideal, it does drastically decrease the positive tail probabilities while still capturing the majority of the negative tail making it more conservative. Based on visual analysis of the distributions, the following table is used.
<br>

|Factor|Distribution   | Low | Mode  | High  |
|---|---|---|---|---|
| qi  | Triangular  |85   | 98  |128   |
| D  | Triangular  |0.5%   |1.2%   | 5%  |
| Minimum  | Constant  | 20  | 20  | 20  |
<br>


```python
def prodQt(t):
	qi = np.random.triangular(85,96,125)
	D = np.random.triangular(0.005,0.012, 0.05)
	minimum = 20.0
	qt = qi*exp(-1*D*t)
	return qt
```

**Example Exponential Production Curve n = 2 years (480 production days)**
![Imgur](http://i.imgur.com/nRs6Ny3.png?1)
Barrel output per day reaches minimum value of 20 and stabilizes

### Future Value of Oil
The West Texas Intermediate (WTI) commodity spot price will be used to benchmark the value of produced crude. Numerous quantitative and analytical models have been used to forecast the price of the commodity, however due to the recent collapse of the price of the asset, there is a great deal of uncertainty. Traditional econometric time series models such as auto-regressive moving-average models are unlikely to perform favorably despite being considered the most accurate in the short and medium term (Behmiri and Manso 32). Financial models using future prices to estimate changes in spot prices has historically shown that future prices are not efficiently priced, rather than having predictive power over spot prices (Behmiri and Manso 35). Models that rely on economic data would seemingly have the best accuracy in a market so heavily impacted by supply/demand shifts and global manipulation of prices. Factoring in OPEC behavior, EIA reports GDP, and other economic variables has been tested but is most effective with an analytical neural network (ANN) (Behmiri and Manso 39). ANNs seem to outperform econometric models in long term forecasts as well (Behmiri and Manso 41).
<br>
![Imgur](http://i.imgur.com/xOIGwvr.png?1)
<br>
There is an ongoing economic debate about whether the build in prices from 2004 to 2014 was irrational, and the price drop in late 2014 is the return to rational prices. Due to the recent nature of the price drop and the lack of literature on the current state of the asset, I will be using a geometric random walk to simulate the price process of crude oil during the production phase. Arguments exist for both mean reverting and random walk models for oil, however the current situation calls for a conservative approach in forecasting. This is why a geometric random walk was chosen rather than a mean reverting process.
<br>
![Imgur](http://i.imgur.com/O6IN8Pp.png)
<br>


```python
apiKey = "JqjPBo2L93BKkEh3fEo2"
#wtiData = q.get("EIA/PET_RWTC_D", authtoken=apiKey) # pull in data from the EIA on spot price of WTI via Quandl
#wtiData.to_excel('WTI.xlsx', 'wti') # store it so I don't exceed my 50 api call limit
wtiData = p.read_excel('WTI.xlsx','wti', index_col= None, na_values = ['NA'])
wtiData = p.DataFrame(wtiData)
wtiData = wtiData.set_index('Date')
wtiShort = wtiData['2014-12-25':'2015-11-29'].values # Conver to Numpy array for iterating

for i in wtiShort:
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
		print("Diffing error")
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
```

**100 Day n = 5 GMR Simulation**
![Imgur](http://i.imgur.com/MAH84dK.png)
**100 Day n = 500 GMR Simulation**
![Imgur](http://i.imgur.com/YUxInH8.png)
<br>
All the values are stored in an array so any oil produced can be marked to market at the appropriate day and discounted. This model assumes that oil is only produced and sold during trading days, not Saturday or Sunday. To add this would simply involve duplicating Friday values for the following two periods. Additionally it assumes that produced crude is being sold at daily closing prices, not intraday prices.

### Cost of Oil
A triangular distribution was used once more for the cost of oil per barrel as the only current data found on onshore crude production listed a minimum, maximum and average cost with minimal accompanying data (Ro). 


```python
def prodCostBarrel():
	return np.random.triangular(22,51,72)
```

### Bringing it All Together: Analysis of the Drilling Opportunity
To simulate the value of the drilling project, the following expressions were used in each simulation.


$ t\ =\ (5\ \times\ 240)\ -\ exploration\ drilling\ time\ -\ production\ drilling\ time $

$ Production\ Revenue\ = \sum_{n=1}^{t}\ \frac{Q_n\ \times\ P_n}{(1+r)^n} $

$ Production\ Cost\ = \sum_{n=1}^{t}\ \frac{Q_n\ \times\ C_n}{(1+r)^n} $

$ Production\ PL\ = \sum_{n=1}^{t}\ \frac{(Q_n\ \times\ P_n) - (Q_n\ \times\ C_n)}{(1+r)^n} $

$ Project\ Revenue\ =\ Production\ PL\ -\ Exploration\ Cost $

Where:

Q = Quantity of Oil Produced

P = Price of WTI per barrel

C = Cost of extraction per barrel

r = 0.0061 (Risk-free rate adjusted to daily)

Due to issues with the Python compiler being used, 1,000 simulations were run instead of the ideal 10,000 or more. Despite this, blowouts and dry wells were represented in the data set. 

![Imgur](http://i.imgur.com/BEO9FQw.png?1)

The first and most apparent conclusion from the simulation is that the firm should absolutely not pursue a well drilling project. In no simulation does the company make money, instead there is an average expected loss of \$2,035,980. The firm stands a 10\% chance of losing more than \$2,632,737 and A 90\% chance of losing over \$1,389,944. Due to the current price of oil even the production segment, the profit driver, loses money in over 70 \% of simulations. This became even clearer when the simulation was run again (shown below) with a starting WTI price of \$100 per barrel instead of the \$40.1 used in the real simulation. The extreme project P&L minimum values in excess of $5 million are due to blowouts, and would exist regardless of market conditions and does not impact our current assessment.<br>
![Imgur](http://i.imgur.com/kuayslz.png?1)<br>
Before the 2014 crash in Oil prices, \$80-\$100 was often thought to be the steady price of oil. Due to this, a number of oil companies likely used high expected prices and paths for risk management and budgeting, explaining the recent number of cancelled projects and layoffs in the E&P industry. The large number of iterations with a value of 0 is due to there being no production cost when a dry well is found. While in most economic climates, a dry well being found would be a poor outcome, currently it is favorable compared to actual production. The incredible cost of exploration means that any project that continues into production must produce a very large quantity of oil, over a long period of time, to break even. As production quantity drops over time and revenues are discounted in the above model, the production time must increase drastically to result in a noticeable increase in profit. While the assumptions used in the simulation are conservative and likely to change over time, updating the values over the process of E&P as well as using more accurate estimates could paint a more optimistic picture. At this time however, the recommendation to the firm is to cease all new exploration and production operations.


```python
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
		`
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
```


## Appendix
------
** Simulation Results **
<br>*Format:*
<br>Name
<br>{Descriptive Statistics}
<br>[Percentiles]
<br>
<br>Pre Discovery
<br>{'mean': 562.03926603371247, 'std dev': 188.8102373815004, 'max': 1002.736354673645, 'var': 35649.305740058531, 'min': 134.<br>09206779667483}
<br>['10: 316.061217604', '20: 396.284903526', '30: 459.418153416', '40: 506.730084727', '50: 556.792664327', '60: 605.322845165', <br>'70: 668.409878583', '80: 734.188122264', '90: 823.836450267']
<br>Dry Well
<br>{'mean': 223.89129296051036, 'std dev': 398.68431853822466, 'max': 1587.3717803736035, 'var': 158949.18584828859, 'min': 0.0}
<br>['10: 0.0', '20: 0.0', '30: 0.0', '40: 0.0', '50: 0.0', '60: 0.0', '70: 0.0', '80: 717.262476505', '90: 889.444560622']
<br>Number of Dry Holes: 252
<br>Drilling Cost
<br>{'mean': 891.93995361879706, 'std dev': 571.26439707928023, 'max': 2447.8439782889777, 'var': 326343.01137035352, 'min': 0.0}
<br>['10: 0.0', '20: 0.0', '30: 871.092968943', '40: 967.159532969', '50: 1046.22947771', '60: 1103.50965817', '70: 1186.42701256', <br>'80: 1305.39326872', '90: 1529.91690756']
<br>Logging Cost
<br>{'mean': 321.95135055281793, 'std dev': 189.59599887558517, 'max': 504.54455695548518, 'var': 35946.642789630889, 'min': 0.0}
<br>['10: 0.0', '20: 0.0', '30: 377.68827432', '40: 393.450397835', '50: 406.523574394', '60: 423.789512314', '70: 441.451911716', <br>'80: 459.880763914', '90: 478.408375147']
<br>Blowout Expense
<br>{'mean': 0.0, 'std dev': 0.0, 'max': 0, 'var': 0.0, 'min': 0}
<br>['10: 0.0', '20: 0.0', '30: 0.0', '40: 0.0', '50: 0.0', '60: 0.0', '70: 0.0', '80: 0.0', '90: 0.0']
<br>Number of Blowouts: 0
<br>Total Cost
<br>{'mean': 1999.8218631658376, 'std dev': 452.12613896222518, 'max': 3394.5342751554631, 'var': 204418.04553288937, 'min': 802.<br>0887645307015}
<br>['10: 1387.44243615', '20: 1602.20589428', '30: 1776.39849354', '40: 1923.98636223', '50: 2020.78120996', '60: 2114.00663996', <br>'70: 2225.13299659', '80: 2353.22673226', '90: 2563.14352962']
<br>Production Quantity
<br>{'mean': 24593.783221369689, 'std dev': 11558.757286696486, 'max': 107773.52020511097, 'var': 133604870.0127591, 'min': 19900.0}
<br>['10: 20840.8543773', '20: 21170.644232', '30: 21360.0', '40: 21480.0', '50: 21580.0', '60: 21660.0', '70: 21780.0', '80: 21960.<br>0', '90: 26810.6967839']
<br>Production Cost
<br>{'mean': 180600.56475079348, 'std dev': 89526.527435297045, 'max': 927942.20158407593, 'var': 8014999114.6229935, 'min': <br>74762.47083026031}
<br>['10: 111751.993359', '20: 128641.417331', '30: 145726.607828', '40: 154543.310252', '50: 165544.399775', '60: 176204.819702', <br>'70: 188825.159778', '80: 202534.218156', '90: 225300.235761']
<br>Production Revenue
<br>{'mean': 132260.21472351087, 'std dev': 77997.174157468035, 'max': 901850.11987878103, 'var': 6083559176.5503998, 'min': 56270.<br>076099441714}
<br>['10: 83366.2128816', '20: 90172.0997635', '30: 98233.9558192', '40: 105556.742014', '50: 114716.497777', '60: 122105.174426', <br>'70: 132899.933516', '80: 150190.425672', '90: 179284.418118']
<br>Production P&L
<br>{'mean': -36158.581820407388, 'std dev': 58006.559466172577, 'max': 450093.43988665711, 'var': 3364760941.1026158, 'min': -433560<br>.09068986354}
<br>['10: -103067.831768', '20: -80086.6217162', '30: -59643.6336856', '40: -44230.2948473', '50: -27351.5067762', '60: <br>-6398.83127636', '70: 0.0', '80: 0.0', '90: 9850.64743371']
<br>Oil Value
<br>{'mean': 5704.8686312025193, 'std dev': 1445.7371974868429, 'max': 11594.257227718441, 'var': 2090156.0441971105, 'min': <br>2813.5038049720865}
<br>['10: 4062.83022011', '20: 4459.96297224', '30: 4827.41001581', '40: 5163.56302879', '50: 5511.58861644', '60: 5814.4463779', <br>'70: 6203.08727534', '80: 6759.53262447', '90: 7656.72316838']
<br>Project Revenue
<br>{'mean': -2035980.4449862451, 'std dev': 470728.54406257899, 'max': -802088.76453070145, 'var': 221585362195.27536, 'min': <br>-3393967.5004291041}
<br>['10: -2632737.84894', '20: -2408686.40792', '30: -2270802.29861', '40: -2170765.64786', '50: -2063421.80385', '60: <br>-1945886.96034', '70: -1800935.04599', '80: -1625987.55222', '90: -1389944.37319']


# Bibliography

<div style="line-height: 2; padding-left: 2em; text-indent:-2em;" class="csl-bib-body">
  <div class="csl-entry">“Average Depth of Crude Oil and Natural Gas Wells.” 31 Aug. 2015. Web.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=document&amp;rft.title=Average%20Depth%20of%20Crude%20Oil%20and%20Natural%20Gas%20Wells&amp;rft.publisher=U.S.%20Energy%20Information%20Administration&amp;rft.identifier=https%3A%2F%2Fwww.eia.gov%2Fdnav%2Fpet%2Fpet_crd_welldep_s1_a.htm&amp;rft.date=2015-08-31"></span>
  <div class="csl-entry">Behmiri, Niaz B., and José R. Pires Manso. “Crude Oil Price Forecasting Techniques: A Comprehensive Review of Literature.” Web.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=document&amp;rft.title=Crude%20Oil%20Price%20Forecasting%20Techniques%3A%20a%20Comprehensive%20Review%20of%20Literature&amp;rft.publisher=Chartered%20Alternative%20Investment%20Analyst%20Association&amp;rft.identifier=https%3A%2F%2Fwww.caia.org%2Fsites%2Fdefault%2Ffiles%2F3.RESEARCH%2520REVIEW.pdf&amp;rft.aufirst=Niaz%20B.&amp;rft.aulast=Behmiri&amp;rft.au=Niaz%20B.%20Behmiri&amp;rft.au=Jos%C3%A9%20R.%20Pires%20Manso"></span>
  <div class="csl-entry">“Blowout Frequencies.” Mar. 2010. Web.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=document&amp;rft.title=Blowout%20Frequencies&amp;rft.publisher=OGP&amp;rft.identifier=http%3A%2F%2Fwww.ogp.org.uk%2Fpubs%2F434-02.pdf&amp;rft.date=2010-03"></span>
  <div class="csl-entry">Bret-Rouzaut, Nadine, and Jean-Pierre Favennec. <i>Oil and Gas Exploration and Production: Reserves, Costs, Contracts</i>. Editions TECHNIP, 2011. Print.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_id=urn%3Aisbn%3A978-2-7108-0975-3&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&amp;rft.genre=book&amp;rft.btitle=Oil%20and%20Gas%20Exploration%20and%20Production%3A%20Reserves%2C%20Costs%2C%20Contracts&amp;rft.publisher=Editions%20TECHNIP&amp;rft.aufirst=Nadine&amp;rft.aulast=Bret-Rouzaut&amp;rft.au=Nadine%20Bret-Rouzaut&amp;rft.au=Jean-Pierre%20Favennec&amp;rft.date=2011&amp;rft.tpages=328&amp;rft.isbn=978-2-7108-0975-3&amp;rft.language=en"></span>
  <div class="csl-entry">Charpentier, Ronald R., and T.R. Klett. “A Monte Carlo Simulation Method for the Assessment of Undiscovered, Conventional Oil and Gas.” 2008. Web.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=document&amp;rft.title=A%20Monte%20Carlo%20Simulation%20Method%20for%20the%20Assessment%20of%20Undiscovered%2C%20Conventional%20Oil%20and%20Gas&amp;rft.publisher=U.S.%20Geological%20Survey&amp;rft.identifier=https%3A%2F%2Fpubs.er.usgs.gov%2Fpublication%2Fpp171326&amp;rft.aufirst=Ronald%20R.&amp;rft.aulast=Charpentier&amp;rft.au=Ronald%20R.%20Charpentier&amp;rft.au=T.R.%20Klett&amp;rft.date=2008"></span>
  <div class="csl-entry">Cooper, N.M. “The Value Of 3d Seismic In Today’s Exploration Environment&nbsp; – In Canada And Around The World.” : n. pag. Print.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=document&amp;rft.title=The%20Value%20Of%203d%20Seismic%20In%20Today%E2%80%99s%20Exploration%20Environment%20%20%E2%80%93%20In%20Canada%20And%20Around%20The%20World&amp;rft.aufirst=N.M.&amp;rft.aulast=Cooper&amp;rft.au=N.M.%20Cooper"></span>
  <div class="csl-entry">Duara, Nigel. “In West Texas Oil Boomtowns, ‘the End Is near.’” <i>latimes.com</i>. N.p., 3 Mar. 2015. Web. 3 Dec. 2015.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=webpage&amp;rft.title=In%20West%20Texas%20oil%20boomtowns%2C%20'the%20end%20is%20near'&amp;rft.description=Fear%20blew%20in%20fierce%20over%20a%20patch%20of%20West%20Texas%20late%20last%20year%2C%20falling%20fast%20and%20without%20warning%20through%20gray%20skies%20to%20alight%20on%20the%20shoulders%20of%20men%20and%20women%20who%20depend%20on%20oil%20for%20their%20livelihoods.&amp;rft.identifier=http%3A%2F%2Fwww.latimes.com%2Fnation%2Fla-na-texas-oil-20150303-story.html&amp;rft.aufirst=Nigel&amp;rft.aulast=Duara&amp;rft.au=Nigel%20Duara&amp;rft.date=2015-03-03"></span>
  <div class="csl-entry">“ESTIMATING DRILLING COSTS-2: Indices Describe Complexity of Drilling Directional, Extended-Reach Wells.” <i>Oil &amp; Gas Journal</i> 105.30 (2007): n. pag. Web. 3 Dec. 2015.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.atitle=ESTIMATING%20DRILLING%20COSTS-2%3A%20Indices%20describe%20complexity%20of%20drilling%20directional%2C%20extended-reach%20wells&amp;rft.jtitle=Oil%20%26%20Gas%20Journal&amp;rft.volume=105&amp;rft.issue=30&amp;rft.date=2007-08-13"></span>
  <div class="csl-entry">Kaiser, Mark J. “A Survey of Drilling Cost and Complexity Estimation Models.” <i>International Journal of Petroleum Science and Technology</i> 1.1 (2007): 1–22. Print.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.atitle=A%20Survey%20of%20Drilling%20Cost%20and%20Complexity%20Estimation%20Models&amp;rft.jtitle=International%20Journal%20of%20Petroleum%20Science%20and%20Technology&amp;rft.volume=1&amp;rft.issue=1&amp;rft.aufirst=Mark%20J.&amp;rft.aulast=Kaiser&amp;rft.au=Mark%20J.%20Kaiser&amp;rft.date=2007&amp;rft.pages=1-22&amp;rft.spage=1&amp;rft.epage=22&amp;rft.issn=0973-6328"></span>
  <div class="csl-entry">---. “ESTIMATING DRILLING COSTS-1: Joint Association Survey, Mechanical Risk Index Methods Common in GOM.” <i>Oil &amp; Gas Journal</i> 105.32 (2007): n. pag. Web.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.atitle=ESTIMATING%20DRILLING%20COSTS-1%3A%20Joint%20association%20survey%2C%20mechanical%20risk%20index%20methods%20common%20in%20GOM&amp;rft.jtitle=Oil%20%26%20Gas%20Journal&amp;rft.volume=105&amp;rft.issue=32&amp;rft.aufirst=Mark%20J.&amp;rft.aulast=Kaiser&amp;rft.au=Mark%20J.%20Kaiser&amp;rft.date=2007-08-27"></span>
  <div class="csl-entry">Mun, Johnathan. <i>Modeling Risk: Applying Monte Carlo Simulation, Real Options Analysis, Forecasting, and Optimization Techniques</i>. John Wiley &amp; Sons, 2006. Print.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_id=urn%3Aisbn%3A978-0-470-00977-2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&amp;rft.genre=book&amp;rft.btitle=Modeling%20Risk%3A%20Applying%20Monte%20Carlo%20Simulation%2C%20Real%20Options%20Analysis%2C%20Forecasting%2C%20and%20Optimization%20Techniques&amp;rft.publisher=John%20Wiley%20%26%20Sons&amp;rft.aufirst=Johnathan&amp;rft.aulast=Mun&amp;rft.au=Johnathan%20Mun&amp;rft.date=2006-07-21&amp;rft.tpages=627&amp;rft.isbn=978-0-470-00977-2&amp;rft.language=en"></span>
  <div class="csl-entry">“Probabilistic Approach to Oil and Gas Prospect Evaluation Using the Microsoft Excel Spreadsheet.” Web.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=document&amp;rft.title=Probabilistic%20Approach%20to%20Oil%20and%20Gas%20Prospect%20Evaluation%20Using%20the%20Microsoft%20Excel%20Spreadsheet&amp;rft.publisher=Louisiana%20State%20University&amp;rft.identifier=http%3A%2F%2Fwww.enrg.lsu.edu%2Fenergydata%2Fpast%2Fprobapproach"></span>
  <div class="csl-entry">Pulsipher, Allan G. “ESTIMATING DRILLING COSTS-Conclusion: Systems Approach Combines Hybrid Drilling Cost Functions.” <i>Oil &amp; Gas Journal</i> 105.32 (2007): n. pag. Web. 3 Dec. 2015.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.atitle=ESTIMATING%20DRILLING%20COSTS-Conclusion%3A%20Systems%20approach%20combines%20hybrid%20drilling%20cost%20functions&amp;rft.jtitle=Oil%20%26%20Gas%20Journal&amp;rft.volume=105&amp;rft.issue=32&amp;rft.aufirst=Allan%20G.&amp;rft.aulast=Pulsipher&amp;rft.au=Allan%20G.%20Pulsipher&amp;rft.date=2007-08-27"></span>
  <div class="csl-entry">“Risk Analysis and Oil Production Curves - Oil + Gas Monitor.” <i>Oil + Gas Monitor</i>. N.p., n.d. Web. 8 Dec. 2015.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=blogPost&amp;rft.title=Risk%20Analysis%20and%20Oil%20Production%20Curves%20-%20Oil%20%2B%20Gas%20Monitor&amp;rft.description=Rafael%20Hartke%20%7C%20Palisade%20Corporation%20The%20use%20of%20risk%20analysis%20in%20the%20oil%20and%20gas%20industry%20can%20take%20many%20forms.%20Whether%20it%E2%80%99s%20safety%20risk%2C%20economic%20risk%20or%20schedule-based%20risk%2C%20it%20is%20critical%20to%20know%20what%20risk%20factors%20exist%20and%20the%20likelihood%20that%20they%20may%20occur.%20Doing%20so%20allows%20decision-makers%20to%20plan%20in%20a%20manner%20that%20%E2%80%A6&amp;rft.identifier=http%3A%2F%2Fwww.oilgasmonitor.com%2Frisk-analysis-oil-production-curves%2F6103%2F"></span>
  <div class="csl-entry">Ro, Sam et al. “The Middle East Has A Huge Advantage In The Global Oil Market.” <i>Business Insider</i>. N.p., n.d. Web. 15 Dec. 2015.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=webpage&amp;rft.title=The%20Middle%20East%20Has%20A%20Huge%20Advantage%20In%20The%20Global%20Oil%20Market&amp;rft.description=The%20American%20Shale%20Boom%20is%20not%20cheap.&amp;rft.identifier=http%3A%2F%2Fwww.businessinsider.com%2Fcrude-oil-cost-of-production-2014-5&amp;rft.aufirst=Sam&amp;rft.aulast=Ro&amp;rft.au=Sam%20Ro&amp;rft.au=2014%20May%2013&amp;rft.au=181%2046&amp;rft.au=2"></span>
  <div class="csl-entry">Sustakoski, Rick J., and Diana Morton-Thompson. “Reserves Estimation.” Web.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=document&amp;rft.title=Reserves%20estimation&amp;rft.publisher=American%20Association%20of%20Petroleum%20Geologists%20Wiki&amp;rft.description=To%20better%20understand%20reserves%20estimation%2C%20a%20few%20important%20terms%20require%20definition.%20Original%20oil%20in%20place%20(OOIP)%20and%20original%20gas%20in%20place%20(OGIP)%20refer%20to%20the%20total%20volume%20of%20hydrocarbon%20stored%20in%20a%20reservoir%20prior%20to%20production.%20Reserves%20or%20recoverable%20reserves%20are%20the%20volume%20of%20hydrocarbons%20that%20can%20be%20profitably%20extracted%20from%20a%20reservoir%20using%20existing%20technology.%20Resources%20are%20reserves%20plus%20all%20other%20hydrocarbons%20that%20may%20eventually%20become%20producible%3B%20this%20includes%20known%20oil%20and%20gas%20deposits%20present%20that%20cannot%20be%20technologically%20or%20economically%20recovered%20(OOIP%20and%20OGIP)%20as%20well%20as%20other%20undiscovered%20potential%20reserves.&amp;rft.identifier=http%3A%2F%2Fwiki.aapg.org%2FReserves_estimation&amp;rft.aufirst=Rick%20J.&amp;rft.aulast=Sustakoski&amp;rft.au=Rick%20J.%20Sustakoski&amp;rft.au=Diana%20Morton-Thompson"></span>
  <div class="csl-entry">“The Land Rig Newsletter.” Apr. 2015. Web.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=document&amp;rft.title=The%20Land%20Rig%20Newsletter&amp;rft.publisher=RigData&amp;rft.identifier=http%3A%2F%2Fwww.rigdata.com%2Fsamples%2FNELR.pdf&amp;rft.date=2015-04"></span>
  <div class="csl-entry">Toews, Gerhard, and Alexander Naumov. “The Relationship Between Oil Price and Costs in the Oil and Gas Industry.” Web.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=document&amp;rft.title=The%20Relationship%20Between%20Oil%20Price%20and%20Costs%20in%20the%20Oil%20and%20Gas%20Industry&amp;rft.publisher=University%20of%20Oxford&amp;rft.identifier=http%3A%2F%2Fwww.economics.ox.ac.uk%2Fmaterials%2Fpapers%2F13819%2Fpaper152.pdf&amp;rft.aufirst=Gerhard&amp;rft.aulast=Toews&amp;rft.au=Gerhard%20Toews&amp;rft.au=Alexander%20Naumov"></span>
  <div class="csl-entry">“Traditional Decline Curve Analysis.” Web.</div>
  <span class="Z3988" title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=document&amp;rft.title=Traditional%20Decline%20Curve%20Analysis&amp;rft.publisher=Petrocenter&amp;rft.identifier=http%3A%2F%2Fwww.petrocenter.com%2Freservoir%2FDCA_theory.htm"></span>
</div>
