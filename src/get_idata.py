from pytrends.request import TrendReq
from datetime import datetime
import os
import pandas as pd
import time
from get_data import convert_date

"""This script offers the main function for google interest data collection. Running it alone collects interest data for a specific coin."""

def get_trend_data(get_flag="",path="",kw="",start_date="",end_date="",tfunc=convert_date):
    
    """Collects google trends data based on keyword and saves a .csv file.
    Arguments:
        get_flag {str}: Flag either "append" or "collect" - si defined in the config file
        kw {str}: Search term.
        path {str}: where .csv will be saved.
        fdate {str}: Date in the ISO 8601 format *with hour* YYYY-MM-DDT01
        ldate {str}:Date in the ISO 8601 format *with hour* YYYY-MM-DDT01
        
    Returns:
        Nothing.
    
    
    Pre-set parameters: geo="",timezone=eastern
    """
    
    pytrend = TrendReq( hl="en-US" , tz=300)

    if get_flag=="collect":

        CDATA_PATH=os.path.join(BASE_PATH)
        df=pd.read_csv( os.path.join( CDATA_PATH,filename) )

        

        
        dt1 = datetime.strptime(start_date, '%Y-%m-%dT%H')
        dt2 = datetime.strptime(end_date, '%Y-%m-%dT%H')
    
    

    print("Begin saving {} data csv...".format(kw))

    if get_flag=="collect":
        df=pytrend.get_historical_interest([kw],
                                        year_start=dt1.year,
                                        month_start=dt1.month, 
                                        day_start=dt1.day, 
                                        hour_start=dt1.hour, 
                                        year_end=dt2.year, 
                                        month_end=dt2.month,
                                        day_end=dt2.day, 
                                        hour_end=dt2.hour, 
                                        cat=0, 
                                        geo='', 
                                        gprop='', 
                                        sleep=120
                                        )
        fname="{}.csv".format( kw.replace(" ","-") )
        save_path=os.path.join(path,fname)
        df.to_csv(save_path)
        print("file saved to: {}".format(save_path))
    

        with open(,"a+") as f:

if __name__ == "__main__":
    
    jfile=open("config.json")
    config=json.load(jfile)
    jfile.close()

    GET_FLAG=cofig["data"]["trends_get"]
    BASE_PATH=config["data"]["base_path"]

    IDATA_PATH=os.path.join(BASE_PATH,"interest")
    name="Bitcoin"

    get_idata(get_flag=GET_FLAG,path=IDATA_PATH,kw=name,fdate=date1,ldate="2020-05-01T00")
    

df=pd.read_csv( os.path.join( CDATA_PATH,filename) )
name=filename[:filename.find(".")].replace("-"," ")
print(name)
if name not in ["Basic Attention Token","Bitcoin","Ethereum", 
                "Lisk", "Theta Network","0x","EOS","Monero","FTX Token"]:
    print(name)
    date1=df["open_time_iso"].values[0].replace(" ","T")[:-6]

    get_idata(path=IDATA_PATH,kw=name,fdate=date1,ldate="2020-05-01T00")