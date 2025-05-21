import database

def get_trains():
    return database.get_trains()

def add_train(name, time, origin, destination):
    database.add_train(name, time, origin, destination)