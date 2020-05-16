import json
from psycopg2 import sql
import psycopg2
import pandas as pd
import os
from sql_queries import *


def get_names_set(base_path="../data",form="sql"):
    """
    Returns a list of coin names and table names that are in BOTH interest/ and coins/
    
    Arguments:
        base_path {str}: table name
        form {str}:
            "sql": returns sql tables compatible names
            "basic": returns coins names. 
    Return:
        tables_names {list}
        coin_names {list}
    """
    ipath,cpath=os.path.join(base_path,"interest/"),os.path.join(base_path,"coins/")
    
    cnames=[]
    for filename in os.listdir(cpath):
        idx=filename.find(".")
        cnames.append(filename[:idx])
    inames=[]
    for filename in os.listdir(ipath):
        idx=filename.find(".")
        inames.append(filename[:idx])
    

    inames_set,cnames_set=set(inames),set(cnames)

    coin_names=list(inames_set.intersection(cnames_set) )

    if form=="basic":
        return coin_names

    elif form=="sql":
        table_names=[name.replace("-","_").lower() for name in coin_names]
        return table_names


def drop_tables(cur, conn, table_names):
    """drops the tables"""
    cur.execute(drop_coin_info_table)
    conn.commit()
    for name in table_names:
        pquery=sql.SQL(drop_coin_tables).format( sql.SQL( name ) ) 
        cur.execute(pquery)
    conn.commit()
    
def create_tables(cur, conn, table_names):
    """creates the tables"""
    cur.execute(create_coin_info_table)
    conn.commit()
    
    for name in table_names:
        pquery=sql.SQL(create_coin_tables).format( sql.SQL( name ) ) 
        cur.execute(pquery)
    conn.commit()

def insert_coin_info(cur,conn,base_path,table_names,coin_names):
    """
    Performs an insert of the coin info.
    """
    df=pd.read_csv( os.path.join( base_path,"coins.csv" ) )
    A=df[ (df.name).isin(coin_names) ].values

    for coin_row in A:
        cur.execute(insert_into_coin_info_tables , coin_row[1:] )
    conn.commit()
    
def insert_cidata(cur,conn,base_path,table_names,coin_names):

    """
    Performs sql table inserts for each coin
    
    Arguments:
        cur {obj}: pyscopg2 curser
        conn {obj}: pyscopg2 connection
        base_path {str}: path
        table_names {list}
        coin_names {list}
    Return:
        Nothing.
    """
    
    for i,name in enumerate(table_names):
        coin_name=coin_names[i]
        coindf=pd.read_csv(os.path.join(base_path,"coins/{}.csv".format(coin_name) ) )
        interestdf=pd.read_csv(os.path.join(base_path,"interest/{}.csv".format(coin_name) ) )
        joindf=pd.merge( coindf,interestdf,left_on="open_time_iso",right_on="date",how="inner")
        joindf=joindf.drop(["date","isPartial"],axis=1)
        A=joindf.values
        for row in A:
            pquery=sql.SQL(insert_into_coin_table).format(sql.SQL(name))
            cur.execute(pquery,row)
        conn.commit()
        

def main():
    """Runs functions to perform etl"""
    jfile=open("config.json")
    config=json.load(jfile)
    jfile.close()
    BASE_PATH=config["data"]["base_path"]
    SQL_FLAG=config["data"]["sql_flag"]
    conn=psycopg2.connect(
    "host={} dbname={} user={}".format( config["postgres"]["host"],
                                        config["postgres"]["db_name"],
                                        config["postgres"]["db_user"] ))

    cur = conn.cursor()
    
    table_names=get_names_set(BASE_PATH,form="sql")
    coin_names=get_names_set(BASE_PATH,form="basic")

    if SQL_FLAG=="collect":
        drop_tables(cur, conn, table_names)
        create_tables(cur, conn, table_names)
    
    insert_coin_info(cur,conn,BASE_PATH,table_names,coin_names)
    insert_cidata(cur,conn,BASE_PATH,table_names,coin_names)

    cur.execute("SELECT * FROM _bitcoin_ LIMIT 5")
    print(cur.fetchone())

    conn.close()


if __name__ == "__main__":
    main()


