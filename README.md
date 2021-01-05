# Capstone project

## Introduction
As the final project of the Udacity Data Engineering Nano-degree, we’re tasked with demonstrating the knowledge we’ve gathered regarding Data Modeling, AWS, Data lakes, Spark and Data pipelines using airflow by combining all these components to come up with a data engineering solution. For this purpose, we can either choose a dataset from the list of provided datasets for the project or pick one online and scope it. I’m going with the former option by picking the following two datasets:
1.	Immigration_Data.csv
2.	Airport_Codes.csv

## Dataset

-I94 Immigration Data: This data comes from the US National Tourism and Trade Office.It comes from here [Immigration Data](https://travel.trade.gov/research/reports/i94/historical/2016.html)

-Airport Code Table: This is a simple table of airport codes and corresponding cities. It comes from here [Airport Data](https://datahub.io/core/airport-codes#data)

### Implementation details

Since we need to store this dataset for further processing and as this data usually come in large quantities at fast speeds, we use [S3](https://aws.amazon.com/s3) before we finally stage it into [Redshift](https://aws.amazon.com/redshift). Since we do not want to run individual scripts to manually populate our data source, we use [Airflow](https://airflow.apache.org/) to create tablesin Redshift, stage data and derive fact and dimension tables.

### Data Model
Once this has been done we have access to the following star-schema based data model: 
 
| Table                |                      Description                 |
|----------------------|--------------------------------------------------|
| Fact_Immigration_Data| Is a fact comprising primarily of the immigration_data file. It stores information about immigration flights to the US
| Dim_Date_Hierarchy   | dimension table stores information about date,month, year etc 
| Dim_Airport_Codes    | dimension table stores information about airport on which immigration flights land
| Dim_Visa_Type        | dimension table contains information abour visa type of people immigrating to the US.

![alt text](https://github.com/SameenTahir/Capstone-Project/blob/main/DataModel.jpg)

Note: The data dictionary (c.f. `DATADICT.md`) contains a description of every attribute for all tables listed above.

### Handling scenarios
This section discusses strategies to deal with the following scenarios:
1. Data is increased 100x  
2. Data pipeline is run on daily basis by 7 am every day
3. Database needs to be accessed by 100+ users simultaneously

#### Data is increased 100x
Since we decided to use scalable, fully managed cloud services to store and process our data, we might only need to  increase the available resources (e.g. number/CPU/RAM of Redshift nodes) to handle an increase in data volume.

#### Data pipleline is run on a daily basis by 7 am every day
As the static datasets do not change on a daily basis, the major challenge here, is to process the amount of newly 
captured tourism data in an acceptable time. Fortunately, using AWS S3 makes it easy for us to schedule 
data loads, for example via another dedicated Airflow dag. Given an appropriate increase in Redshift resources, this 
should be sufficient to process data in time.

#### Database needs to be accessed by 100+ users simultaneously
Besides increasing Redshift resources as mentioned above, we could deal with an increase in users by precomputing the 
most complicated (in terms of required processing power) and/or most desired queries and store them in an additional 
table.

### Data Pipeline

The Data pipeline is comprises of the below mentioned tasks:
1.	Start Operator and End operator are tasks that start and end the dag. Both are dummy tasks
2.	`Load_Immig_Data_into_Redshift` is a dag that will load immigration_data into the redshift database on the cluster
3.	Similarly, `Load_Airport_Data_into_Redshift` is a dag that will load Airport data into redshift
4.	To load the dimension and fact tables in the model following dag’s are used:

        1.	load_fact_immigration_table
        2.	load_airportcodes_dimension_table
        3.	load_visatype_dimension_table
        4.	load_date_hierarchy_dimension_table
        
5.	To run data quality checks against the data loaded `run_data_quality_checks` dag is used

### Ingestion

The below given flow-chart illustrates the data ingestion process:

![alt text](https://github.com/SameenTahir/Capstone-Project/blob/main/FlowDiagram.jpg)

## Prerequisites

* AWS account with dedicated user including access key ID and secret access key
* Access to AWS Comprehend
* Access to a (running) AWS Redshift cluster, where access means:
    - Having created an attached a security group allowing access on port 5439
    - Having created an attached a role allowing Redshift to access buckets on AWS S3
    - Create/drop/insert/update rights for the Redshift instance
* Working installation of Airflow, where working means:
    - Airflow web server and scheduler are running
    - Connection to AWS is set up using `aws_default` ID
    - Connection to Redshift is set up using `redshift_default` ID
    - AWS IAM role is set up as Airflow variable using `aws_iam_role` as key
* Unix-like environment (Linux, macOS, WSL on Windows)
* Python 3.7+
* Python packages boto3, airflow, etc.

## Usage
1. Double check that you meet all prerequisites specified above
2. Trigger a DAG run via `airflow trigger_dag capstone_dag`
3. Have fun analyzing the data

### Data Processing & Analysis

For data processing and analysis sql queries have been used. These queries are called through the dags defined in the airflow pipeline process. Furthermore, attached below are some dashboards that have been developed using the insights generated from the data loaded through the pipeline explained here for the data model stated above:

![alt text](https://github.com/SameenTahir/Capstone-Project/blob/main/Analysis_1.png)

![alt text](https://github.com/SameenTahir/Capstone-Project/blob/main/Analysis_2.png)



