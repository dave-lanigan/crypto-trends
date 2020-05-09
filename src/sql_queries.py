

create_price_table="""CREATE TABLE price_{} ( open_table varchar PRIMARY KEY,
                                              open_time_unix bigint,
                                              open double precision,
                                              high double precision,
                                              low double precision,
                                              close double precision,
                                              volume bigint,
                                              close_time bigint,
                                              number_of_trades bigint
                                              );"""
                                              
create_interest_table=""" CREATE TABLE interest_{} ( date varchar PRIMARY KEY,
                                                    relative_interest int); """

create_coin_info_table=""" CREATE TABLE coin_info (symbol varchar(10) PRIMARY KEY,
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
                                           
insert_into_price_table="""INSERT INTO interest_{} (

                                                        )
                                            VALUES ()"""

insert_into_interest_table=""" """




delete_tables=[]
create_tables=[create_coin_info_table, create_price_table,create_interest_table]

