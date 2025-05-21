import database

def book_train(username, train_name):
    database.book_train(username, train_name)

def get_history(username):
    return database.get_booking_history(username)

def cancel(username, train_name):
    database.cancel_booking(username, train_name)
