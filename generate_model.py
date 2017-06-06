"""
"""

import psycopg2
import pymysql
import os
import ast
from jinja2 import Environment, FileSystemLoader

# cSpell:ignore pymysql, psycopg2

class GenerateSchema(object):
    """"""

    def __init__(self, connection, connection_type='mysql'):
        self.conn = connection
        self.conn_type = connection_type
        self.database = connection['database']
        self.PATH = os.path.dirname(os.path.abspath(__file__))
        self.TEMPLATE_ENVIRONMENT = Environment(
            autoescape=False,
            loader=FileSystemLoader(os.path.join(self.PATH)),
            trim_blocks=True)

    def render_template(self, template, context=''):
        return self.TEMPLATE_ENVIRONMENT.get_template(template).render(context)

    def connect(self):
        """create connection to the database"""
        conn = None
        if self.conn_type == 'mysql':
            conn = pymysql.connect(**self.conn)
        elif self.conn_type == 'postgres':
            conn = psycopg2.connect(**self.conn)
        return conn

    def get_schema(self):
        """ Retrieves the schema information"""
        resources = {}
        sql1 = 'USE '+ self.database
        if self.conn_type == 'mysql':
            conn = self.connect()
            with conn.cursor() as cur:
                cur.execute(sql1)
                cur.execute('SHOW TABLES')
                for rec in cur.fetchall():
                    resources[rec[0]] = '/'+rec[0]
        elif self.conn_type == 'postgres':
            pass
        return resources

    def create_resources(self):
        """creates the resources for the api"""
        resources = {'resources':self.get_schema()}
        py_name = 'resources.py'
        with open(py_name, 'w') as f:
            py_file = self.render_template('resource_template.py')
            f.write(py_file)
        for key in resources['resources'].items():
            context = {
                'ClassName':key[0],
                'db':self.conn['database'],
                'host': self.conn['host'],
                'user': self.conn['user'],
                'pass': self.conn['password'],
                'connection_type':self.conn_type,
                'table': key[0]
            }
            with open(py_name, 'a+') as f:
                py_file = self.render_template('class_template.py', context)
                f.write(py_file)
        return resources

        