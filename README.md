# Crypto Data Trends Project


### INTRO
This purpose of this project is to download, consolidate, transform and prepare cryptocurrency price, volume and google trend data for analysis and exploration.<br/>
<br>
To accomplish this a list data was acquired from (3) different sources. The first was [coingecko API](https://www.coingecko.com/en/api) where a list of viable coin candidates were pulled along with information about each coin. Those coins ranked in the top ~50 by market cap that were supported on Binance. Binance was chosen for its ubiquity as a cryptocurrency exchange, strong API and fairly low trading fees. The historical data was then pulled from binance API with a [python wrapper](https://github.com/sammchardy/python-binance) using [USDT](https://tether.to/) as the base currency. The google trends data was pulled from google (a very time consuming process because google is very unfreindly to those who need their trends data) using a [pytrends](https://github.com/GeneralMills/pytrends) module.<br/>
<br>
NOTE: The to decrease the time to download the google trends data the binance data is collected first - the the latest date from the data for each coin is used as the latest date for the google trends data. May 1, 2020 was used as the earliest date.<br/>
<br>
The data was then transfered into a postgresql database a table for each coin (price info and trends info) and a single table for the list of coins and information. The outline of the database can be seen below. A dictionary for the data is found in the main directory: data-dictionary.html<br/>

![image info](./db.png)


### STRUCTURE

```
├── data                                                                                         
│   ├── coins                                                                                                        
│   │   ├── 0x.csv                                                                                                          
│   │   ├── Algorand.csv                                                                                                     
│   |   └── ...                                                                                       
│   ├── coins.csv
│   └── interest
│       ├── Basic-Attention-Token.csv
│       ├── Bitcoin.csv
│       └── ...
├── README.md
├── requirements.txt
├── data_dictionary.html
├── db.png
└── src
    ├── example_config.json
    ├── etl.py
    ├── get_data.py
    ├── collect_data.py
    ├── append_data.py
    ├── get_data.py
    ├── data_check.py
    ├── test_.py
    └── sql_queries.py

```

### SET UP

#### Requirements
* Python 3
* pandas
* pytrends
* python-binance
* datetime
* psycopg2
* requests

The configuration file should be edited. The example_config.json can be used for this.

If you all collecting data from scratch for the first time under the [data] section change trends_get/coins_get=append to trends_get/coins_get=collect.
If the you leave the "get" flags to  append then the files will search the .csv files for the last date collect and begin collection from there. Additionally only dates that have not been added to the postgres databases will be added.<br/>
<br>
For both appending data to .csv files and sending data to the database only coins with BOTH interest and price data will be added.

To re-download all the data (will take a few days) and then create databases - run the scripts the following way:
```
>> python3 check_.py # check to see if scripts can access postgres and config.json is set up.
>> python3 collect_data.py # collect all coin info, price and trends data
>> python3 etl.py # transform data and move to postgres tables
>> python3 data_check.py # perform data quality check
```
Otherwise to append data to the pre-made .csv files. Run the scripts in the following way:
```
>> python3 check_.py # check to see if scripts can access postgres and config.json is set up.
>> python3 append_data.py # append new data to the .csv files
>> python3 etl.py #transform data and move to postgres tables
>> python3 data_check.py # perform data quality check
```


### NOTES/DISCUSSION

###### ETL Process/Data Description:

The data acquisition and ETL is performed as follows by the above scripts:
* Coin geck API is queried and the resulting json response is parsed extracting the Cryptocurrency's: coingecko id, name, ticker, url and description of the coin. The data is save to a coins.csv file in the base_path directory (see config.json).
* Next, binance API is queried for hourly historical price data for each of the coins in the coins.csv file using the base currency "Tether" (USDT). A python list is recieved in response where each sub-list is the hourly data. The unix time, open, high, low, close, volume and number of trades are pulled for each hourly row and saved to a .csv file with the added ISO 8601 time as the first column right before the unix time. Theh file is Coinname.csv and saved to base_path/coins/ directory. If a coin is not supported it is saved to the fails.csv file in the same directory.
* Next, the google trends site is queried for hourly data on trends, the response is date/time in iso format, relative interest (normalize) and isPartial True/False data point that can be ignored. All rows are saved to a .csv file in the base_path/interest/ directory. The terms queried are the names of the coins or the file names in the base_path/coins/ directory excluding ".csv".
* The ETL process includes first checking for the set of coin names that are in both the interest/ and coins/ directory and generating a list of the names as well as postgres compatible table names from them.
* Next, the coins_info tables is creacted by importing the coins.csv file using pandasm excluding the coins not supported on Binance and saving all data to the SQL table.
* Next, the the .csv files from are imported with into a pandas data frame (2) for each coin - price data and interest data. These are joined using pandas by inner join on the their date/time columns to make sure they overlap before they are transfer to a postres table with pyscopg2. The isPartial row is dropped from the coin interest data.
* Next, a data check is performed.


###### Technologies/Data Model:

Postgres was chosen as the database because of its wide use, open source nature my already personal familiarity with pyscopg2. A SQL database provide convient and simple data storage and query options using sql query language. Pandas python library proved to be a useful data manipulation tool as well and was used frequently to manipulate and prepare .csv file contents.

The data base model is simple and allows for easy access to coin specific data for comparing prices and trends. A sql database allows for easy access to the data. The data is seperated into a table for each of the cryptocurrenies with primary key of the database is the time date + hour. This allows for queries comparing google trend and coin price comparisons to be easy made with one line queries such as the one below.

Sample SQL query:
```
db=# SELECT open_time_iso,open,relative_interest FROM _Bitcoin_ WHERE relative_interest > 20;
```

##### Use with Spark:
Use with Spark, an popular big-data analysis tool can be used to analysis the data easily since the data is store in a postgres databse. You could also use Spark to access the .csv directly.


##### Use with airflow:
For use with airflow the following DAG structure is recommended:
```
get_coin_info>>get_price_data>>get_trends_data>>etl_to_database
```

Data should be updated as frequently as new analysis needs to be accomplished based on coin price trends. If an interesting price or trend movement occurred and the instance needs to be investingated the data should be updated.<br/>
<br>

* If the data was increased by 100x, I would change little except for the interest data acquisition, the function gathering it would have to be changed. Currently, there is a loop which adds a wait period of a few minutes for every collection call which gets a week of data. However, it would take about about a year to collect 100x the data at the current rate.  Therefore, more clever way of collecting the data would have to be implimented, requiring a change to the pytrends api call function - maybe by pausing only when a 429 reponse is recieved and continuing to add time if the 429 is coninued to be recieved, then going back to zero wait time when it goes away. Also, right now the "append" and "collect" options are only for the .csv file. This is because the operation is fairly quick. However, with 100x more data an append option for the database would be warranted. 
* If the pipelines were run on a daily basis by 7am, some sort of script to automate the data acquisition would have to be implimented. This may be a good opportunity to imploy airflow. Otherwise a simple python script running on a server using a scheduling library like [schedule](https://pypi.org/project/schedule/) or Timer object from the built in threading module.
* If the database needed to be accessed by 100+ people and was 100x the size a move to a nosql database like MongoDB might be warranted.
### need more here
