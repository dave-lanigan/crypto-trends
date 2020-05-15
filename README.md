# Crypto Data Trends Project

### INTRO
This purpose of this project is to download, consolidate, transform and prepare cryptocurrency price, volume and google trend data for analysis and exploration.<br/>
<br>
To accomplish this a list data was acquired from (3) different sources. The first was [coingecko API](https://www.coingecko.com/en/api) where a list of viable coin candidate were pulled along with information about each coin. hose coins ranked in the top ~50 by market cap that were supported on Binance. Binance was chosen for its ubiquity as a cryptocurrency exchange, strong API and fairly low trading fees. The historical data was then pulled from binance API with a [python wrapper](https://github.com/sammchardy/python-binance) using [USDT](https://tether.to/) as the base currency. The google trends data was pulled from google (a very time consuming process because google is very unfreindly to those who need their trends data) using a [pytrends](https://github.com/GeneralMills/pytrends) module.<br/>
<br>
NOTE: The to decrease the time to download the google trends data the binance data is collected first - the the latest date from the data for each coin is used as the latest date for the google trends data. May 1, 2020 was used as the earliest date.<br/>
<br>
The data was then transfered into a postgresql database a table for each coin (price info and trends info) and a single table for the list of coins and information. The outline of the database can be seen below.<br/>
<br>



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
└── src
    ├── dwh.cfg
    ├── etl.py
    ├── get_cdata.py
    ├── get_idata.py
    ├── get_info.py
    ├── get_data.py
    └── sql_queries.py

```
#### Requirements
* Python 3
* pandas
* pytrends
* python-binance
* datetime
* psycopg2

A the configuration file should be edited.

For data acquisition operate in the following way:
```
>> python3 get_data.py
>> python3 etl.py
```
If you all collecting data from scratch for the first time under the [DATA] section change get=append to get=collect.
If the you leave the get=append flag on then the get_data.py file will search the .csv files for the last date collect and begin collection from there. Additionally only dates that have not been added to the postgres databases will be added.



### NOTES/DISCUSSION



-what queries do i wan to run?
-How would spark or airflow be incorporated?

##### Use with Spark:
Spark, an popular big-data analysis tool can be used to analysis the data easily in the following way:
```

```


##### Use with airflow:
```


```

-why did i choose the model?
-Clearly state the rationale for the choice of tools and technologies for the project.
-Propose how often the data should be updated and why.

Data should be updated as frequently as new analysis needs to be accomplished based on coin price trends. If an interesting price or trend movement occurred and the instance needs to be investingated the data should be updated.

Include a description of how you would approach the problem differently under the following scenarios:
    If the data was increased by 100x.
    If the pipelines were run on a daily basis by 7am.
    If the database needed to be accessed by 100+ people
