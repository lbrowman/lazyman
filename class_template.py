
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
            results = []
            conn = pymysql.connect(**self.conn)
            params = req.get_param('describe')
            if params:
                sql = 'describe '+self.table
            else:
                sql = 'Select * from '+self.table
            with conn.cursor() as cur:
                cur.execute(sql)
                cols = cur.description
                results = [{cols[x][0]: col for x, col in enumerate(val)} for val in cur.fetchall()]
            RESP['msg'][self.table] = []
            RESP['msg'][self.table] = results
            resp.status = falcon.HTTP_200
            resp.content_type = CONTENT_TYPE
        except Exception as identifier:
            resp.status = falcon.HTTP_500
            resp.content_type = CONTENT_TYPE
            RESP['msg'] = str(identifier)
        finally:
            resp.body = json.dumps(RESP, sort_keys=True, indent=4)

