import Quandl as q
from datetime import datetime
import numpy as np
import pandas as p
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as ts

apiKey = "JqjPBo2L93BKkEh3fEo2"
#wtiData = q.get("EIA/PET_RWTC_D", authtoken=apiKey)
#wtiData.to_excel('WTI.xlsx', 'wti')
wtiData = p.read_excel('WTI.xlsx','wti', index_col= None, na_values = ['NA'])
wtiData = p.DataFrame(wtiData)
wtiData = wtiData.set_index('Date')
#print(wtiData['2014-12-25':'2015-11-29'].head())
#print(wtiData['2014-12-25':'2015-11-29'].tail())

wti = p.date_range('2014-12-25', '2015-12-01', freq = 'D')

#plt.plot(wtiData['2014-12-25':'2015-11-29'].index, wtiData['2014-12-25':'2015-11-29'])
#plt.title('WTI Daily Spot Prices (2014-12-15 - 2015-11-29)')
#plt.xlabel('Year')
#plt.ylabel('$/bbl')
#plt.show()
wtiShort = wtiData['2014-12-25':'2015-11-29'].values # Conver to Numpy array for iterating


def gmr(s, t, dt):
	last = 0
	count = 0
	logDiff = []
	for i in wtiShort:
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
	#print("Sigma = " + str(sigma))
	mu = np.mean(logDiff) + (0.5*sigma)**2
	#print("Mu = " + str(mu))
	n = round(t/dt)
	t = np.linspace(0,t,n)
	w = np.random.standard_normal(size = n)
	w = np.cumsum(w)*np.sqrt(dt)
	x = (mu-0.5*sigma**2)*t + sigma*w
	s = s*np.exp(x)
	return np.array(s)

def makeWalks(itr, s, t, dt):
	randwalk = np.array([])
	randwalk = gmr(mu, sigma, s, t, dt)
	for i in range(itr-1):
		randwalk =np.column_stack((randwalk, gmr(mu, sigma, s, t, dt)))
	return randwalk

#randwalk = makeWalks(500, mu, sigma, 40.3, 100, 1) # 40.3 being latest oil price
#print(randwalk)
#plt.plot(randwalk)
#plt.show()