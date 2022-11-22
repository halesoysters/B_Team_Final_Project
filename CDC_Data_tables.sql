DROP TABLE IF EXISTS county_info CASCADE;
CREATE TABLE county_info (
    CountyFIPS VARCHAR PRIMARY KEY NOT NULL, 
    Density VARCHAR,
	total_population VARCHAR,
	ruralUrban VARCHAR
);


DROP TABLE IF EXISTS county_info CASCADE;
CREATE TABLE county_info (
    CountyFIPS VARCHAR PRIMARY KEY NOT NULL, 
    countyname VARCHAR,
	statedesc VARCHAR
)

DROP TABLE IF EXISTS health_outcomes CASCADE;
CREATE TABLE health_outcomes (
    CountyFIPS VARCHAR PRIMARY KEY NOT NULL,
    ARTHRITIS VARCHAR,
    CASTHMA VARCHAR,
    BPHIGH VARCHAR,
    CANCER VARCHAR,
    HIGHCHOL VARCHAR,
    KIDNEY VARCHAR,
    COPD VARCHAR,
    CHD VARCHAR,
    DEPRESSION VARCHAR,
    DIABETES VARCHAR,
    OBESITY VARCHAR,
    TEETHLOST VARCHAR,
    STROKE VARCHAR
);


DROP TABLE IF EXISTS health_risk_behaviors CASCADE;
CREATE TABLE health_risk_behaviors (
    CountyFIPS VARCHAR PRIMARY KEY NOT NULL,
    BINGE VARCHAR,
    CSMOKING VARCHAR,
    LPA VARCHAR,
    SLEEP VARCHAR
);


DROP TABLE IF EXISTS health_status CASCADE;
CREATE TABLE health_status (
    CountyFIPS VARCHAR PRIMARY KEY NOT NULL,
    MHLTH VARCHAR,
    PHLTH VARCHAR,
    GHLTH VARCHAR
);


DROP TABLE IF EXISTS prevention CASCADE;
CREATE TABLE prevention (
    CountyFIPS VARCHAR PRIMARY KEY NOT NULL,
    ACCESS VARCHAR,
    CHECKUP VARCHAR,
    DENTAL VARCHAR,
    BPMED VARCHAR,
    CHOLSCREEN VARCHAR,
    MAMMOUSE VARCHAR,
    CERVICAL VARCHAR,
    COLON_SCREEN VARCHAR,
    COREM VARCHAR,
    COREW VARCHAR
);

SELECT COUNT(*) AS count_countyfips
from county_population;

SELECT ci.countyname, ci.countyfips,
	   cp.density, cp.total_population, cp.ruralurban 
INTO county_merged
FROM county_info as ci
JOIN county_population as cp
ON ci.countyfips = cp.countyfips

SELECT COUNT(*) AS count_merged
from county_merged;