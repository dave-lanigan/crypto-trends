import json
from psycopg2 import sql
import psycopg2
import pandas as pd
import os
from sql_queries import *


def get_names_set(base_path,type="all",form="sql"):
    """
    EXAMPLE
    Imports data from an S3 bucket to a Redshift database table given the table name
    
    Arguments:
        table {str}: table name
        redshift_conn_id {str}: airflow connection id for redshift
        aws_credentials_id {str}: airflow connection id for aws
        s3_bucket {str}: S3 bucket name.
        s3_key {str}:
        iam {str}:
        region {str}: Region that the s3 bucket is from.
        json {str}:
        **kwargs: Pass in key-value pairs of dates in the format "year"="2018","month"="11"} to import only part of data
                    otherwise all data will be imported.
    Return:
        No return.
    """
    ipath,cpath=base_path+"interest",base_path+"coins"
    
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
    cur.execute(drop_coin_info_table)
    conn.commit()
    for name in table_names:
        pquery=sql.SQL(drop_price_tables).format( sql.SQL( name ) ) 
        iquery=sql.SQL(drop_interest_tables).format( sql.SQL(name) )
        cur.execute(pquery)
        cur.execute(iquery)
    conn.commit()
    
def create_tables(cur, conn, table_names):
    cur.execute(create_coin_info_table)
    conn.commit()
    
    for name in table_names:
        pquery=sql.SQL(create_price_tables).format( sql.SQL( name ) ) 
        iquery=sql.SQL(create_interest_tables).format( sql.SQL(name) )
        cur.execute(pquery)
        cur.execute(iquery)
    conn.commit()

def insert_coin_info(cur,conn,base_path,table_names,coin_names):
    df=pd.read_csv( base_path+"coins.csv" )
    A=df[ (df.name).isin(coin_names) ].values

    for coin_row in A:
        cur.execute(insert_into_coin_info_table , coin_row[1:] )
    conn.commit()
    
def insert_cidata(cur,conn,base_path,table_names,coin_names):
    CDATA,IDATA="interest","coins"
    
    for i,name in enumerate(table_names):
        coindf=pd.read_csv(base_path+"coins/{}.csv".format(coin_names[i]))
        interestdf=pd.read_csv(base_path+"interest/{}.csv".format(coin_names[i]))
        coinA,interstA=coindf.values,interestdf.values
        # df.merge(interestdf,coindf,left_on="date",right_on="open_time_iso",how="inner")
        # out=df.values
        for row in coinA:
            pquery=sql.SQL(insert_into_price_table).format(sql.SQL(name))
            cur.execute(pquery,row)
        conn.commit()
        
        for row in interstA:
            iquery=sql.SQL(insert_into_interest_table).format(sql.SQL(name))
            cur.execute(iquery,row[:-1])
        conn.commit()

def main():
    jfile=open("config.json")
    config=json.load(jfile)
    jfile.close()
    conn=psycopg2.connect(
    "host={} dbname={} user={}".format( config["postgres"]["host"],
                                        config["postgres"]["db_name"],
                                        config["postgres"]["db_user"] ))

    cur = conn.cursor()
    
    table_names=get_names_set(BASE_PATH,form="sql")
    coin_names=get_names_set(BASE_PATH,form="basic")
    drop_tables(cur, conn, table_names)
    create_tables(cur, conn, table_names)
    insert_coin_info(cur,conn,BASE_PATH,table_names,coin_names)
    insert_cidata(cur,conn,BASE_PATH,table_names,coin_names)

    cur.execute("SELECT * FROM coin_info LIMIT 5")
    print(cur.fetchone())

    cur.execute("SELECT * FROM price_bitcoin LIMIT 5")
    print(cur.fetchone())

    cur.execute("SELECT * FROM interest_bitcoin LIMIT 5")
    print(cur.fetchone())
    
    conn.close()


if __name__ == "__main__":
    main()


