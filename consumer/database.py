import os

import sqlalchemy

DATABASE_URL = os.environ["DATABASE_URL"]
TABLE_NAME = os.environ["TABLE_NAME"]

engine = sqlalchemy.create_engine(DATABASE_URL)

conn = engine.connect()
metadata = sqlalchemy.MetaData()


purchase_summmary = sqlalchemy.Table(
    TABLE_NAME,
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("country", sqlalchemy.String),
    sqlalchemy.Column("amount", sqlalchemy.Integer),
)


metadata.create_all(engine)
