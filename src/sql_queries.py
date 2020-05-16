

drop_coin_info_table="DROP TABLE IF EXISTS coin_info"
drop_coin_tables="DROP TABLE IF EXISTS _{}_data"


create_coin_tables="""CREATE TABLE IF NOT EXISTS _{}_ (open_time_iso varchar PRIMARY KEY,
                                              open_time_unix bigint,
                                              "open" double precision,
                                              "high" double precision,
                                              "low" double precision,
                                              "close" double precision,
                                              "volume" bigint,
                                              close_time bigint,
                                              number_of_trades bigint,
                                              relative_interest int
                                              );"""

create_coin_info_table=""" CREATE TABLE IF NOT EXISTS coin_info (
                                             "symbol" varchar(10) PRIMARY KEY,
                                             "name" varchar(100),
                                             market_cap_rank int,
                                             links varchar,
                                             "description" text
                                             );"""

insert_into_coin_info_tables=""" INSERT INTO coin_info ("symbol",
                                                       "name",
                                                       market_cap_rank,
                                                       links,
                                                       "description"
                                                                ) 
                                            VALUES (%s,%s,%s,%s,%s)
                                            ON CONFLICT 
                                            DO NOTHING;"""
                                           
insert_into_coin_table="""INSERT INTO _{}_ ( open_time_iso,
                                                    open_time_unix,
                                                    "open",
                                                    "high",
                                                    "low",
                                                    "close",
                                                    "volume",
                                                    close_time,
                                                    number_of_trades,
                                                    relative_interest)
                                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                            ON CONFLICT 
                                            DO NOTHING;"""
