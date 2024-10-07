from sqlalchemy import (Table, MetaData, Column, BigInteger, 
                        String, Float, TIMESTAMP)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("telegram_id", BigInteger, primary_key=True),  # 0
    Column("first_name", String),  # 1
    Column("last_name", String),  # 2
    Column("eth_address", String),  # 3
    # Column("sol_address", String),  
    Column("trx_address", String),  # 4
    Column("last_get", TIMESTAMP)  # 5
)

