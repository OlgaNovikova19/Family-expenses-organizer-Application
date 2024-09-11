import datetime
identified_user = None
chosen_date = None


def set_user(user_name):
    global identified_user
    identified_user = user_name


def get_user():
    global identified_user
    return identified_user

def set_chosen_date(passed_date):
    global chosen_date
    chosen_date = passed_date



def get_chosen_date():
    global chosen_date
    return chosen_date


