cities = LOAD '/home/hduser/data/weather_ru_cities' USING PigStorage(';') AS (
        id:chararray,
        city:chararray
);

rawdata = LOAD '/home/hduser/data/*.csv' USING PigStorage(';','-tagFile') AS (
        file:chararray,
	day:int,
        hour:int,
        temp:long,
        wind_dir:chararray,
        wind_speed:chararray,
        kind:chararray,
        cloudiness:int,
        visibility:int,
        humidity:int,
        pressure:int
);

count_total = FOREACH (GROUP rawdata ALL) GENERATE COUNT(rawdata); 

cities = FOREACH cities GENERATE $0 AS id, REGEX_EXTRACT($1,'\'(.*)\'',1) AS city;

data = FOREACH rawdata GENERATE
	REGEX_EXTRACT($0, '(\\d{5})', 1) AS id,
	REGEX_EXTRACT($0, '\\d{5}_(\\d{4})', 1) AS year,
	REGEX_EXTRACT($0, '\\d{5}_\\d{4}-(\\d{2})', 1) AS month,
	$1,$2,$3,$4,$5,$6,$7,$8,$9,$10;

full_data = JOIN data BY id, cities BY id;

full_gdata = GROUP full_data BY (city, year, month, day);
city_daily_temp = FOREACH full_gdata GENERATE
	FLATTEN (group) AS (city, year, month, day),
	AVG(full_data.temp) AS avrg_t,
	MAX(full_data.temp) AS max_t,
	MIN(full_data.temp) AS min_t;

full_gdata = GROUP full_data BY (city, month, day);
city_avrg_temp = FOREACH full_gdata GENERATE
	FLATTEN (group) AS (city, month, day),
	AVG(full_data.temp) AS avrg_t;

encode_data = FOREACH full_data GENERATE
	city,
	year,
	month,
	day,
	(CASE kind
		WHEN 'CL' THEN 1
		WHEN 'BR' THEN 1
		WHEN 'FG' THEN 2
		WHEN 'RA' THEN 3
		WHEN 'SHRA' THEN 4
		WHEN 'SNRA' THEN 4
		WHEN 'SN' THEN 2
		WHEN 'SHSN' THEN 3
		WHEN 'TS' THEN 4
		WHEN 'DZ' THEN 3
		WHEN 'FZ' THEN 2
		WHEN 'HL' THEN 4
	END) AS wencode,
	((REGEX_EXTRACT(wind_speed, '([0-9]+)', 1) IS NULL)?0:(int)wind_speed) AS wind_speed,
	cloudiness;
encodeg_data = GROUP encode_data BY (city, year, month, day);
city_common = FOREACH encodeg_data GENERATE 
	FLATTEN (group) AS (city, year, month, day),
	AVG(encode_data.wencode) AS wencode,
	AVG(encode_data.wind_speed) AS wind_speed,
	AVG(encode_data.cloudiness) AS cloudiness;
encodeg_data = GROUP city_common BY (city, year, month, day);
city_common = FOREACH encodeg_data GENERATE
	group.city,
	AVG(city_common.wencode) AS wencode,
	AVG(city_common.wind_speed) AS wind_speed,
	AVG(city_common.cloudiness) AS cloudiness,
	COUNT(city_common);

STORE count_total INTO 'weather_ru_out_count';
STORE city_daily_temp INTO 'weather_ru_out_daily';
STORE city_avrg_temp INTO 'weather_ru_out_avrg';
STORE city_common INTO 'weather_ru_out_common';
