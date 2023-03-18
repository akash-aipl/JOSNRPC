import httplib2,random, json

HOST = 'localhost'
PORT = 8069
DB = 'odoo16'
USER = 'odoo16'
PASS = 'odoo16'

odoo_url = "http://%s:%s/jsonrpc" % (HOST, PORT)

class OdooConnector:
    
    context = {}
    http = False
    cookies = '28693d646874bba7ec7600cb585d5f71da6c95be'
    
    def __init__(self):
        self.http = httplib2.Http()
        
    def get_session_info(self):
        url = '/web/session/get_session_info'
        requestData = self._create_params({})
        result =  self.requestJSON(url, requestData)
        res = result.get('result')
        return res
    
    def authenticate(self, username, password, db):
        url = '/web/session/authenticate'
        params = {
            "db": DB,
            "login": USER,
            "password": PASS,
            "context": {}
        }
        requestData = self._create_params(params)
        result = self.requestJSON(url, requestData)
        user = result.get('result')
        self.context = user.get('user_context')
        return user
    
    def write(self,model, data, record_id):
        url = "/web/dataset/call_kw"
        args = [(record_id), data]
        params = {
            "model": "sale.order",
            "method": "write",
            "args": args,
            "kwargs": {},
            "context": self.context
        }
        requestData = self._create_params(params)
        return self.requestJSON(url, requestData)
        
        
    def requestJSON(self, url, data):
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Connection': 'keep-alive'
        }        
        if self.cookies:
            headers['Cookie'] = self.cookies
        res, content = self.http.request(odoo_url + url, 'POST', headers=headers, body=json.dumps(data))
        self.cookies = res.get('set-cookie', '')
        return json.loads(content)

    def _create_params(self, params):
        data = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": params or {},
            "id": random.randint(0, 1000000000)
        }
        print(data)
        return data