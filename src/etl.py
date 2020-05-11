import configparser
import psycopg2
import pandas as pd
import os
from sql_queries import *


def get_coin_names(base_path):
    ipath,cpath=base_path+"interest",base_path+"coins"
    
    cnames=[]
    for filename in os.listdir(cpath):
        idx=filename.find("_")
        cnames.append(filename[:idx])
    inames=[]
    for filename in os.listdir(ipath):
        idx=filename.find("_")
        inames.append(filename[:idx])
    
    inames_set,cnames_set=set(inames),set(cnames)
    
    return list(inames_set.intersection(cnames_set) )

def drop_tables(cur, coin_names):
    cur.execute(drop_coin_info_table)
    cur.commit()
    
    for name in coin_names:
        cur.execute( drop_price_tables,(name,) )
        cur.execute( drop_interest_tables,(name,) )
    cur.commit()
    
def create_tables(cur, coin_names):
    cur.execute(create_coin_info_table)
    cur.commit()
    
    for name in coin_names:
        cur.execute( create_price_tables, (name,) )
        cur.execute( create_interest_tables, (name,) )
    cur.commit()

def insert_coin_info(cur,base_path):
    
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
    
    

def insert_ci_data(cur,base_path,coin_names):
    CDATA,IDATA="interest","coins"
    
    for name in coin_names:
        coindf=pd.read_csv("coins/{}.csv".format(name))
        interestdf=pd.read_csv("interest/{}.csv".format(name))
        
        df.merge(interestdf,coindf,left_on="date",right_on="open_time_iso",how="innder")
        out=df.values
        
        cur.execute(insert_into_price_table
    


def main():
    BASE_PATH="./data/"

    config=configparser.ConfigParser()
    config.read("pgdb.cfg")
    conn=psycopg2.connect(
    "host={} dbname={} user={}".format( config["DB"]["HOST"],
                                        config["DB"]["DB_NAME"],
                                        config["DB"]["DB_USER"] ))

    cur = conn.cursor()
    
    coin_names=get_coin_names(BASE_PATH)
    drop_tables(cur, coin_names)
    create_tables(cur, coin_names)
    insert_data(cur, coin_names, BASE_PATH)
    
    
    #insert_data()
    
    conn.close()



if __name__ == "__main__":
    main()


