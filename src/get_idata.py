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
    
    pytrend = TrendReq( hl="en-US" , tz=300 )

    dt1 = datetime.strptime(fdate, '%Y-%m-%dT%H')
    dt2 = datetime.strptime(ldate, '%Y-%m-%dT%H')
    
    print("Begin saving csv...")
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
                                    sleep=0
                                    )

    fname="{}_{}_{}.csv".format( kw , fdate , ldate  )
    save_path=os.path.join(path,fname)
    df.to_csv(save_path)
    print("file saved to: {}".format(save_path))

if __name__ == "__main__":
    
    
    DATA_PATH="data/interest"
    #kw_list=["Bitcoin","Ether","Bytecoin","Bitcoin SV","Chainlink","BitShares","DigiByte","HedgeTrade",]
    
    date2,date1="2020-05-01T00","2015-05-01T00"
    
    get_idata(path=DATA_PATH,kw="Ethereum",fdate=date1,ldate=date2)
    
    
    
    
