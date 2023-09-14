from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer, String, DECIMAL
from sqlalchemy import insert
from faker import Faker

engine = create_engine("sqlite+pysqlite:///sqlite.db", echo=True)
metadata_obj = MetaData()
fake = Faker(["pt_BR"])

client_table = Table(
    "clients",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(30)),
    Column("cpf", String(11), unique=True),
    Column("address", String(50), unique=True)
)

account_table = Table(
    "account",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("type", String),
    Column("agency", Integer),
    Column("number", Integer),
    Column("balance", DECIMAL),
    Column("client_id", ForeignKey("clients.id"), nullable=False)
)

with engine.begin() as conn:
    metadata_obj.create_all(conn)


with engine.connect() as conn:

    for i in range(30):
        client = insert(client_table).values(name=fake.name(), cpf=fake.cpf(),
                                             address=fake.address())
        result = conn.execute(client)

        account = insert(account_table).values(type='Conta Corrente', agency=1001,
                                               number=str(fake.aba()), balance=0.0, client_id=i)
        result = conn.execute(account)

        conn.commit()
