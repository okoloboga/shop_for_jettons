from sqlalchemy import Table, MetaData, Column, BigInteger, String, Integer

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("telegram_id", BigInteger, primary_key=True), # 0
    Column("first_name", String), # 1
    Column("last_name", String), # 2
    Column("address", String), # 3
    Column("mnemonics", String), # 4
    Column("purchase", Integer), # 5
    Column("purchase_sum", Integer), # 6
    Column("referrals", Integer), # 7
    Column("invited", Integer), # 8
    Column("page", Integer) # 9
)

catalogue = Table(
    "catalogue",
    metadata,
    Column("index", Integer, primary_key=True), # 0
    Column("name", String), # 1
    Column("address", String), # 2
    Column("description", String), # 3
    Column("marketplace", String), # 4
    Column("image", String), # 5
    Column("collection", String), # 6
    Column("owner", String) # 7
)