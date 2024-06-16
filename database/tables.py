from sqlalchemy import Table, MetaData, Column, BigInteger, String, Integer

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("telegram_id", BigInteger, primary_key=True),  # 0
    Column("first_name", String),  # 1
    Column("last_name", String),  # 2
    Column("address", String),  # 3
    Column("mnemonics", String),  # 4
    Column("purchase", Integer),  # 5
    Column("purchase_sum", Integer),  # 6
    Column("referrals", Integer),  # 7
    Column("invited", Integer),  # 8
    Column("page", Integer),  # 9
    Column("status", String)  # 10
)

catalogue = Table(
    "catalogue",
    metadata,
    Column("index", Integer, primary_key=True),  # 0
    Column("category", String),  # 1
    Column("name", String),  # 2
    Column("description", String),  # 3
    Column("image", String),  # 4
    Column("self_price", BigInteger),  # 5
    Column("sell_price", BigInteger),  # 6
    Column("count", Integer)  # 7
)

income = Table(
    "income",
    metadata,
    Column("index", Integer, primary_key=True),  # 0
    Column("admin_id", BigInteger),  # 1
    Column("date_and_time", String), # 2
    Column("item_index", Integer), # 3
    Column("category", String),  # 4
    Column("name", String),  # 5
    Column("count", Integer),  # 6
    Column("income_sellprice", BigInteger),  # 7
    Column("income_selfprice", BigInteger),  # 8
)

process = Table(
    "process",
    metadata,
    Column("index", Integer, primary_key=True),  # 0
    Column("user_id", BigInteger),  # 1
    Column("delivery_address", String),  # 2
    Column("date_and_time", String),  # 3
    Column("item_index", Integer),  # 4
    Column("category", String),  # 5
    Column("name", String),  # 6
    Column("count", Integer),  # 7
    Column("income", BigInteger),  # 8
    Column("pure_income", BigInteger)  # 9
)

outcome = Table(
    "outcome",
    metadata,
    Column("index", Integer, primary_key=True),  # 0
    Column("user_id", BigInteger),  # 1
    Column("date_and_time", String),  # 2
    Column("item_index", Integer),  # 3
    Column("category", String),  # 4
    Column("name", String),  # 5
    Column("count", Integer),  # 6
    Column("outcome_sellprice", BigInteger),  # 7
    Column("outcome_selfprice", BigInteger),  # 8
)

edited = Table(
    "edited",
    metadata,
    Column("index", Integer, primary_key=True),  # 0
    Column("admin_id", BigInteger),  # 1
    Column("date_and_time", String),  # 2
    Column("item_index", Integer),  # 3
    Column("category", String),  # 4
    Column("name", String),  # 5
    Column("commit", String),  # 6
)