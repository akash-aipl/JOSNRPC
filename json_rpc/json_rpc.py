import json
import random
import urllib.request

HOST = 'localhost'
PORT = 8069
DB = 'odoo16'
USER = 'odoo16'
PASS = 'odoo16'

def json_rpc(url, method, params):
    # data = {
    #     "jsonrpc": "2.0",
    #     "method": method,
    #     "params": params,
    #     "id": random.randint(0, 1000000000),
    # }
    data = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": "sale.order",
            "method": "create",
            "args":  "/home/akash/Desktop/json_rpc/sample.json"
        },
        "id": 28
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type":"application/json",
    })
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]

def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})

# log in the given database
url = "http://%s:%s/jsonrpc" % (HOST, PORT)
uid = call(url, "common", "login", DB, USER, PASS)

# *** push operation ***
# args = {
#     'name': 'S00025'
# }

with open('/home/akash/Desktop/json_rpc/push_sample.json') as f:
    args = json.load(f)
    print(args)
    push = call(url, "object", "execute", DB, uid, PASS, 'sale.order', 'create', args)
    print("Push Operation")


# *** pull operation ***
# pull = call(url, "object", "execute", DB, uid, PASS, 'sale.order', 'read')
# print("Data Pulled : ", pull)
# json_object = json.dumps(pull, indent=1)
# with open('/home/akash/Desktop/json_rpc/pull_sample.json', "w") as outfile:
#     outfile.write(json_object)