from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy import text
from faker import Faker

engine = create_engine("sqlite+pysqlite:///sqlite.db", echo=True)
Base = declarative_base()
fake = Faker(["pt_BR"])


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    cpf = Column(String(11), unique=True)
    address = Column(String(50), unique=True)


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    agency = Column(Integer)
    number = Column(Integer)
    balance = Column(DECIMAL)
    client_id = Column(ForeignKey("clients.id"), nullable=False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

with Session.begin() as session:
    for i in range(1000):
        session.add(Client(name=fake.name(), cpf=fake.cpf(), address=fake.address()))
        session.add(Account(type='Conta Corrente', agency=1001, number=str(fake.aba()), balance=0.0, client_id=i))

with Session.begin() as session:
    stmt = text('SELECT * FROM clients c INNER JOIN accounts a ON a.client_id = c.id')
    clients = session.execute(stmt)

for client_list in clients:
    address = client_list[3].replace("\n", " - ")
    print(f'Nome: {client_list[1]} - CPF: {client_list[2]} - Endereço: {address}'
          f' - Tipo de conta: {client_list[5]} - Banco: {client_list[6]} - Número da conta: {client_list[7]}'
          f' - Saldo: R$ {client_list[8]}')
