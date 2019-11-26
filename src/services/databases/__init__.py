
def init_databases(app):

    from .mongodb import init_mongodb
    init_mongodb(app)
