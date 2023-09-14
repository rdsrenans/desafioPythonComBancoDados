from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer, String, DECIMAL
from sqlalchemy import insert

engine = create_engine("sqlite+pysqlite:///sqlite.db", echo=True)
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

# Usar metodo metada para popular banco ou mudar para declarative base
josias_client = insert(client_table).values(name='Josias Afam', cpf='02548974556',
                                            address='Rua Ingá, 80 - Canoas/RS')
josias_account = insert(account_table).values(type='Conta Corrente', agency=1001,
                                              number=100203, balance=300.00, client_id=1)
malaquias_client = insert(client_table).values(name='Malaquias Kron', cpf='02358654721',
                                               address='Rua Logo Ali, 9990 - Longe/RS')
malaquias_account = insert(account_table).values(type='Conta Corrente', agency=1001,
                                                 number=100201, balance=548.54, client_id=1)

with engine.connect() as conn:
    result = conn.execute(josias_client)
    print(result)
    result = conn.execute(josias_account)
    print(result)
    result = conn.execute(malaquias_client)
    print(result)
    result = conn.execute(malaquias_account)
    print(result)
    conn.commit()
