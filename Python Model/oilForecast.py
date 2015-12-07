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
wtiData.info()
print(wtiData.tail())

wti = p.date_range('2014-12-25', '2015-12-01', freq = 'D')

#plt.plot(wtiData.index['2014-12-25':'2015-11-29'], wtiData['2014-12-25':'2015-11-29'])
#plt.title('WTI Daily Spot Prices (1986 - 2015)')
#plt.xlabel('Year')
#plt.ylabel('$/bbl')
#plt.show()
wtiShort = wtiData['2014-12-25':'2015-11-29']
#wtiShort.plot()
#plt.show()
wtiShortWeekly = wtiShort.resample('W-Fri')
ts.adfuller(wtiShortWeekly, 1)