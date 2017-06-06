from generate_model import GenerateSchema

CON = {
    "database":"incidents", "host":"localhost",
    "user":"lloyd", "password":"Passw0rd"}
GM = GenerateSchema(CON)
# print(GM.get_schema())
RESOURCES = (GM.create_resources())


