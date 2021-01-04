# Data dictionary

## About
This file contains an overview of the attributes (columns), types and descriptions for all tables used in the project.

### Tables

#### Fact_Immigration_Data

|Column|Type|
|-------|----|
|id	    |integer
|cicid	|integer
|i94yr	|varchar(256)
|i94mon	|varchar(256)
|i94cit	|varchar(256)
|i94res	|varchar(256)
|i94port	|varchar(256)
|arrdate	|varchar(256)
|i94mode	|varchar(256)
|i94addr	|varchar(256)
|depdate	|varchar(256)
|i94bir	|varchar(256)
|i94visa	|varchar(256)
|_count	|integer
|dtadfile	|varchar(256)
|visapost	|varchar(256)
|occup	|varchar(256)
|entdepa	|varchar(256)
|entdepd	|varchar(256)
|entdepu	|varchar(256)
|matflag	|varchar(256)
|biryear	|varchar(256)
|dtaddto	|varchar(256)
|gender	|varchar(256)
|insnum	|varchar(256)
|airline	|varchar(256)
|admnum	|varchar(256)
|fltno	|varchar(256)
|visatype|	varchar(256)

#### Dim Airport Codes

| Column | Type | 
| --- | --- |
| ident | varchar(256) | 
| type | varchar(256) | 
| name | varchar(256) | 
| elevation_ft | decimal | 
| continent | varchar(256) | 
| iso_country | varchar(256) | 
| iso_region | varchar(256) | 
| municipality | varchar(256) | 
| gps_code | varchar(256) | 
| iata_code | varchar(256) | 
| local_code | varchar(256) | 
| coordinates | varchar(256) |

#### Dim Date Hierarchy

| Column | Type | 
| --- | --- | 
Date_key | Integer | 
Date_Val | Date | 
Month_Val | integer | 
Year_Val | integer |

#### Sources

| Column | Type |
| --- | --- | 
Visa_Type_id | Integer | 
Visa_Type | varchar(256) |

