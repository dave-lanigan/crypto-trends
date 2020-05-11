

drop_coin_info_table="""DROP TABLE IF EXISTS coin_info"""
drop_price_tables=""" DROP TABLE IF EXISTS price_%s"""
drop_interest tables=""""DROP TABLE IF EXISTS interest_%s"""


create_price_tables="""CREATE TABLE IF NOT EXISTS price_%s (open_time_iso varchar PRIMARY KEY,
                                              open_time_unix bigint,
                                              open double precision,
                                              high double precision,
                                              low double precision,
                                              close double precision,
                                              volume bigint,
                                              close_time bigint,
                                              number_of_trades bigint
                                              );"""
                                              
create_interest_tables=""" CREATE TABLE IF NOT EXISTS interest_%s (
                                                    date varchar PRIMARY KEY,
                                                    relative_interest int); """

create_coin_info_table=""" CREATE TABLE IF NOT EXISTS coin_info (
                                             symbol varchar(10) PRIMARY KEY,
                                             name varchar(30),
                                             market_cap_rank int,
                                             links varchar,
                                             description text
                                             );"""
                                             
                                             


insert_into_coin_info_table=""" INSERT INTO coin_info (symbol,
                                                       name,
                                                       market_cap_rank,
                                                       links,
                                                       description) 
                                        
                                           VALUES (%s,%s,%s,%s,%s)"""
                                           
insert_into_price_table="""INSERT INTO price_%s ( open_table,
                                              open_time_unix,
                                              open,
                                              high,
                                              low,
                                              close,
                                              volume,
                                              close_time,
                                              number_of_trades)
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

insert_into_interest_table="""INSERT INTO interest_%s (date,relative_interest)
                                        VALUES (%s,%s)"""




delete_tables=[]
create_tables=[create_coin_info_table, create_price_table,create_interest_table]

