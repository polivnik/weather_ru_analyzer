#!/usr/bin/python
#
# Author: Leonid Polivnik
# Date: 10.03.2016
#

import glob
import os
import pickle
import urllib2
import time
import zipfile

url0 = 'http://www.pogoda.by/zip/'
folder = '/home/hduser/data/'
years = range(2014, 2016)
#cities = {27612:'Moscow', 26063:'St.Peter-burg', 34214:'Belgorod', 26298:'Bologoe', 26898:'Bryansk', 27532:'Vladimir', 34560:'Volgograd', 27037:'Vologda', 34123:'Voronej', 22892:'Vyborg', 26702:'Kaliningrad', 27703:'Kaluga', 27627:'Kashira', 27333:'Kostroma', 34009:'Kursk', 27930:'Lipetsk', 27509:'Mojaysk', 27459:'N-Novgorod', 27906:'Orel', 27962:'Penza', 26258:'Pskov', 27329:'Rostov-Velikiy', 27730:'Ryazan', 27402:'Tver', 27719:'Tula', 27113:'Cherepovec'}
#cities = {27612:'Moscow', 26063:'St.Peter-burg'}

with open(folder + 'weather_ru_cities', 'wb') as f:
	for k,v in cities.items():
		f.write(`k`+';'+`v`+'\n')

start_time = time.time()

for k in cities.keys():
	for y in years:
		for m in range(1, 13):
			zip_file = `k` + '_' + `y` + '-' + (`0` if not m//10 else '') + `m` + '.zip'
			url = url0 + `y` + '/' + zip_file
			print ('File  ' + zip_file + '  downloading from  '+ url)
			with open(folder + zip_file, 'wb') as f:
				f.write(urllib2.urlopen(url).read())

end_time = time.time()
print ('Downloading completed in ' + `end_time - start_time` + ' seconds')

zip_files = glob.glob(folder + '*.zip')
for zip_file in zip_files:
	zip_handler = zipfile.ZipFile(zip_file, 'r')
	zip_handler.extractall(folder)
print ('CSV files unzipped')
for z in zip_files: 
	os.remove(z)
print ('Zip files deleted')
print ('Data loading completed')
