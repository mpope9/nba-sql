from peewee import *
from settings import Settings

# peewee database proxy, because we have multiple configurable databases.
database_proxy = DatabaseProxy()

class BaseModel(Model):
    class Meta:
        database = database_proxy

if __name__ == '__main__':
    pass
