Data Engineering Zoomcamp Project - Swiss Apartments

Description of the Dataset
The dataset contains data on 42,207 apartments in 3,903 buildings. It includes visual, acoustic, topologic and daylight features. The data is sourced from commercial clients of Archilyse AG specializing on the digitization and analysis of buildings. The dataset consists of two files: geometries.csv and simulations.csv. Geometeries illustrates how the apartments are layed out and simulations describes the different characteristic. 

Description of the Project
This is my final project for DEZ 2023. It uses data from collection about swiss dwellings. I chose it because it has some good traits for the skills that I've learned in this zoomcamp. It is a large dataset, nearly 3 million rows, has two related tables that I join into a single facts table, many different fields that can provide interesting infographics. It's a batch process as that dataset is static. The goal of this project is to find at least three different interesting trends in the dataset.

Data Source: https://zenodo.org/record/7070952#.Y0mACy0RqO0

Dataflow:

Data Source -> Google Cloud Bucket -> BigQuery -> dbt -> Bigquery -> Looker Studio

Data Source to Google Cloud Bucket:
    This fetches the data and transforms it into a parquet file. Normally some data type definitions would occur here, but the data set was already in a good state.

Google Cloud Bucket -> BigQuery:
    The tables are iterated through and uploaded to tables which have already been defined in BigQuery. 


BigQuery and dbt
    dbt is connected to BigQuery by a credendials provided by BigQuery. This allows BigQuery and dbt to interact. The two tables are joined on several values, allowing a single fact table to be queried. This gets more into fact table and dimension table design rules, but a denormalized table is preferred in data modeling because it requires less joins when querying. 

Bigquery -> Looker Studio
    BigQuery and Looker Studio have a nice interface to interact with each other. It's very easy to connect them. I found several interesting data points as can be seen below.

The Looker Report: https://lookerstudio.google.com/s/nbGxvA9oKKI

Notes on the Report:
I need to get better at making reports. There is room for improvement with my looker studio skills. Currently there are issues with apartment uniqueness in the second and third pages of the report. There are records for each room in an aparment which is skewing the overal counts. I'm also having issues filtering the data to ignore what I feel is erroneous records.

Conclusion:
The three interesting facts I was looking for: A ground floor dwelling is slightly more likely than not to have an elevator. I think this is because more apartments are in buildings with multiple floors. Next is that the second floor has the best water views in general. I wonder if this is because when you are on higher floors it's harder to see smaller water features. The last fact is that I need to do a better job filtering the data before it gets to the report. The third page has a good number of datapoints that make me question the quality of my dataset.

I've learned a lot and there's room to grow. 




 
