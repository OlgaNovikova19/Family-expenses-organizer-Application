import pydantic

identified_user = None
users = {}


def set_user(user_name):
    global identified_user
    identified_user = user_name


def get_user():
    global identified_user
    return identified_user
