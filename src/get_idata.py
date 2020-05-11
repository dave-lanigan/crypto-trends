from pytrends.request import TrendReq
from datetime import datetime
import os
import pandas as pd





def get_idata(path="",kw="",fdate="",ldate=""):
    
    """Collects google trends data based on keyword and saves a .csv file.
    Arguments:
        kw {strs}: Search term.
        path {str}: where .csv will be saved.
        fdate {str}: Date in the ISO 8601 format *with hour* YYYY-MM-DDT01
        ldate {str}:Date in the ISO 8601 format *with hour* YYYY-MM-DDT01
        
    Returns:
        Nothing.
    
    
    Pre-set parameters: geo="",timezone=eastern
    """
    
    pytrend = TrendReq( hl="en-US" , tz=300)

    dt1 = datetime.strptime(fdate, '%Y-%m-%dT%H')
    dt2 = datetime.strptime(ldate, '%Y-%m-%dT%H')
    
    print("Begin saving {} data csv...".format(kw))
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

if __name__ == "__main__":
    
    CDATA_PATH="../data/coins"
    IDATA_PATH="../data/interest"
    
    sleep_time=720
    for filename in os.listdir(CDATA_PATH):
        df=pd.read_csv( os.path.join( CDATA_PATH,filename) )
        name=filename[:filename.find(".")].replace("-"," ")
        
        date1=df["open_time_iso"].values[0].replace(" ","T")[:-6]

        get_idata(path=IDATA_PATH,kw=name,fdate=date1,ldate="2020-05-01T00")
        
        
        time.sleep(sleep_time)
        sleep_time=sleep_time+60
        
    print("ALL FILES SAVED")
    
    
    
