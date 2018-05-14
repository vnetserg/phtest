from collections import namedtuple

User = namedtuple("User", ["id", "name", "login", "attempts"])

def get_user_by_login(login):
    if login == "todd":
        return User(1, "Тоддов Василий Петрович", "todd", 1)

def get_user_by_id(uid):
    print(repr(uid))
    if uid == 1:
        return User("id", "Тоддов Василий Петрович", "todd", 1)
