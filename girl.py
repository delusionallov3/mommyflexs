from mommyflexs import Client

client = Client()

# Sans login
users = client.users.list()
user = client.users.get_by_username("V")
results = client.users.search("ric")
print(users)
print(user)
print(results)
