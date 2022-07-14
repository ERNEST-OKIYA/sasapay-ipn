""" this is a db class. for all script files """

from django.db import connection
from django.conf import settings
import os,sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mpesa.settings')
django.setup()



class Db:
    """ this is here handy incase you need custom queries """

    def __init__(self):
        self.cursor=connection.cursor()


    def dictfetchall(self):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in self.cursor.description]
        return [
            dict(zip(columns, row))
            for row in self.cursor.fetchall()
        ]

    def dictfetchone(self):
        "Return one row from a cursor as a dict"
        return dict(zip([col[0] for col in self.cursor.description], self.cursor.fetchone()))


    def run_query(self,query):
        return self.cursor.execute(query)

    def get_one(self,): #ppull one row, or single result from query that returns one result
        return self.dictfetchone()
    def get_many(self,):#for query that returns many.
        return self.dictfetchall()









