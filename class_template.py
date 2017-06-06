
class {{ClassName}}(object):
    def __init__(self):
        self.conn = {
            'database': '{{db}}',
            'host': '{{host}}',
            'user': '{{user}}',
            'password': '{{pass}}'
        }
        self.conn_type = '{{connection_type}}'
        self.table = '{{table}}'

    def on_get(self, req, resp):
        try:
            resp.status = falcon.HTTP_200
            resp.content_type = CONTENT_TYPE
        except Exception as identifier:
            resp.status = falcon.HTTP_500
            resp.content_type = CONTENT_TYPE
            RESP['msg'] = identifier
        finally:
            resp.data = json.dumps(RESP)

