import configparser
import psycopg2
import pandas as pd
import os
from sql_queries import *




def dnc_tables():
    pass
    

def insert_data(cur,base_path):
    
    def insert_coin_data(pair):
        pass
        
        
    
    BASE_COIN="USDT"
    
    #check failed list (both) then delete the lists
    with (base_path + "failed.csv","r") as f:
        failed=f.readline().split()
    #coin_info
    path=os.path.join(base_path,"coins.csv")
    coin_df=read_csv(path)
    coinl=coin_df[ ~coin_df.isin(failed) ].values
    
    #coin info insert
    for row in coinl:
        cur.execute(insert_into_coin_info_table,tuple(row))
    cur.commit()
    
    
    #coin data insert
    #for 



def main():

    config=configparser.ConfigParser()
    config.read("pgdb.cfg")

    conn=psycopg2.connect("host={} dbname={} user={}".format( config["DB"]["HOST"],
                                                              config["DB"]["DB_NAME"],
                                                              config["DB"]["DB_USER"] ))

    cur = conn.cursor()
    
    #insert_data()
    
    conn.close()




if __name__ == "__main__":
    main()


