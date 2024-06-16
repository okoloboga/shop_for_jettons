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
    # INSERT INTO catalogue (index, category, name, description, image, self_price, sell_price, count)
    # VALUES (0, 'Mushroom', 'Amanita Muscaria', 'He will punish u', 'https://m.media-amazon.com/images/I/61jQXEFqzPL._SL1500_.jpg', 1500, 850, 10);
)