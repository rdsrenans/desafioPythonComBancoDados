import pprint
import random
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from faker import Faker


ca = certifi.where()
uri = "mongodb+srv://dasafiodio:desafiodio@cluster0.bjwf4vb.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, tlsCAFile=ca, server_api=ServerApi('1'))

db = client["bank"]
collection = db.bank

fake = Faker(["pt_BR"])

data_insert = []
for i in range(100):
    data_insert.append({
        'name': fake.name(),
        'cpf': fake.cpf(),
        'address': str(fake.address()).replace('\n', ' - '),
        'type': 'Conta Corrente',
        'agency': 1001,
        'number': fake.aba(),
        'balance': random.uniform(0, 500.00)
    })

collection.insert_many(data_insert)

for post in collection.find({'balance': {'$gt': 250}}):
    pprint.pprint(post)

VALUE = 250
print(f"\nQuantidade de contas com valor maior que R$ {VALUE}"
      f" é: {collection.count_documents({'balance': {'$gt': VALUE}})}")

client.close()
