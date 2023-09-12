from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer, String, DECIMAL


engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
metadata_obj = MetaData()

client_table = Table(
                "clients",
                metadata_obj,
                Column("id", Integer, primary_key=True, autoincrement=True),
                Column("name", String(30)),
                Column("cpf", String(11), unique=True),
                Column("address", String(50), unique=True)
            )

account_table = Table(
    "address",
    metadata_obj,
    Column("id", primary_key=True, autoincrement=True),
    Column("type", String),
    Column("agency", Integer),
    Column("number", Integer),
    Column("balance", DECIMAL),
    Column("client_id", ForeignKey("clients.id"), nullable=False)
)
