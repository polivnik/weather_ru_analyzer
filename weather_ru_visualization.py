#!/usr/bin/python
#
# Author: Leonid Polivnik
# Date: 12/03/2016
#

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#import seaborn as sns

mpl.rcParams['figure.max_open_warning'] = 0

daily = pd.read_table( \
	'/home/hduser/weather_ru_out_daily/part-r-00000', \
	sep='\s*', \
	header=None)
daily.columns = ['city','year','month','day','avrg_t','max_t','min_t']

for c in {'Moscow', 'St.Peterburg','Kaliningrad','Volgograd'}:
	plt.figure()
	result = daily[daily.city==c]
	result = pd.pivot_table(result,'avrg_t',['month','day'],'year')
	result.plot()
	plt.savefig('daily.'+c+'.png', format='png')
	del result
del daily


avrg = pd.read_table( \
	'/home/hduser/weather_ru_out_avrg/part-r-00000', \
	sep='\s*', \
	header=None)
avrg.columns = ['city','month','day','avrg_t']

for m in range(1, 13):
	plt.figure()
	result = avrg[avrg.month==m]
	result = pd.pivot_table(result,'avrg_t','day','city')
	result.boxplot(rot=90)
	plt.savefig('month_' + `m` + '.png', format='png')
	del result
del avrg


daily = pd.read_table( \
	'/home/hduser/weather_ru_out_common/part-r-00000', \
	sep='\s*', \
	header=None)
daily.columns = ['city','wencode','wind_speed','cloudiness','days']

for c in {'Moscow', 'St.Peterburg','Kaliningrad','Volgograd'}:
	plt.figure()
	result = daily[daily.city==c]
	GnYlRd=mpl.colors.LinearSegmentedColormap('GnYlRd', mpl.cm.revcmap(plt.get_cmap('RdYlGn')._segmentdata))
	plt.scatter(result.wind_speed,result.cloudiness,s=result.days*20,c=result.wencode,cmap=GnYlRd, edgecolors='None')
	plt.tight_layout()
	plt.savefig('common.'+c+'.png', format='png')
	del result
del daily


