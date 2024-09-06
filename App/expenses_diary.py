import sqlite3
from identification_data import identified_user, users, set_user, get_user

#class ExpensesDiary??

balance: float = 0


def create_db_finance():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute(
        "create table if not exists limits (id INTEGER PRIMARY KEY, login TEXT, limit_start_date TEXT,"
        "limit_end_date TEXT, sum_limit REAL, warning_sum REAL DEFAULT NULL,"
        " history INTEGER CHECK(history IN (0, 1)) DEFAULT 0,"
        "diff_limit_real_expenses REAL DEFAULT 0, general_subjective_success_rate REAL CHECK(general_subjective_success_rate >= 0 AND general_subjective_success_rate <= 100) DEFAULT NULL)")

    c.execute(
        "create table if not exists expenses (id INTEGER PRIMARY KEY, login TEXT, expense_date TEXT, sum_expense REAL,"
        " expense_category TEXT, expense_subcategory TEXT DEFAULT NULL, subjective_success_rate REAL CHECK(subjective_success_rate >= 0 AND subjective_success_rate <= 100) DEFAULT NULL)")

    c.execute(
        "create table if not exists users (id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT NOT NULL, password TEXT NOT NULL    , spare_balance REAL DEFAULT NULL,"
        " sum_left_to_spend_without_warning REAL DEFAULT NULL)")

    conn.commit()
    conn.close()


def add_active_limit(login, limit_start_date, limit_end_date, sum_limit, warning_sum, history=0,
                     diff_limit_real_expenses=None, general_subjective_success_rate=None):
    create_db_finance()
    conn_ = sqlite3.connect('finance.db')
    c_ = conn_.cursor()
    c_.execute(
        "INSERT INTO limits (login, limit_start_date, limit_end_date, sum_limit, warning_sum, history, diff_limit_real_expenses, general_subjective_success_rate) VALUES (?,?,?,?,?,?,?,?)",
        (login, limit_start_date, limit_end_date, sum_limit, warning_sum, history, diff_limit_real_expenses,
         general_subjective_success_rate))
    conn_.commit()
    conn_.close()


def add_expense(login, expense_date, sum_expense, expense_category, expense_subcategory, subjective_success_rate=None):
    create_db_finance()
    conn_2 = sqlite3.connect('finance.db')
    c_2 = conn_2.cursor()
    c_2.execute(
        "INSERT INTO expenses (login, expense_date, sum_expense, expense_category, expense_subcategory, subjective_success_rate) VALUES (?,?,?,?,?,?)",
        (login, expense_date, sum_expense, expense_category, expense_subcategory, subjective_success_rate))
    conn_2.commit()
    conn_2.close()


def check_expenses_for_user(identified_user):
    create_db_finance()
    conn1 = sqlite3.connect('finance.db')
    c1 = conn1.cursor()
    c1.execute("SELECT * FROM expenses WHERE login = ?", (identified_user,))
    expenses_data = c1.fetchone()
    print(expenses_data, 'exp.data')
    conn1.close()
    if expenses_data:
        return True
    else:
        return False


def get_expenses_for_login_for_the_period(identified_user, start_date, end_date):
    response_check_expenses_data = check_expenses_for_user(identified_user)
    if response_check_expenses_data:
        conn2 = sqlite3.connect('finance.db')
        c2 = conn2.cursor()
        c2.execute("SELECT sum_expense FROM expenses WHERE login = ? AND expense_date >= ? AND expense_date <= ?",
                   (identified_user, start_date, end_date))
        expenses_data_in_the_period = c2.fetchall()
        conn2.close()
        return expenses_data_in_the_period
    return


def get_sum_expenses_for_login_for_the_period(identified_user, start_date, end_date):
    response_check_expenses_data = check_expenses_for_user(identified_user)
    if response_check_expenses_data:
        conn2 = sqlite3.connect('finance.db')
        c2 = conn2.cursor()
        start_date = start_date.split()[0]
        c2.execute("SELECT SUM(sum_expense) FROM expenses WHERE login = ? AND expense_date >= ? AND expense_date <= ?",
                   (identified_user, start_date, end_date))
        sum_all_expenses_for_the_period = c2.fetchone()
        print(sum_all_expenses_for_the_period, 'tuple?')
        conn2.close()
        return sum_all_expenses_for_the_period[0] if sum_all_expenses_for_the_period is not None else 0
    return 0


def check_active_limits_for_user(identified_user):
    create_db_finance()
    conn1 = sqlite3.connect('finance.db')
    c1 = conn1.cursor()
    c1.execute("SELECT * FROM limits WHERE login = ? AND history = 0 ORDER BY limit_start_date DESC LIMIT 1",
               (identified_user,))
    limit_start_data = c1.fetchone()
    print(limit_start_data, 'fetchone')
    conn1.close()
    if limit_start_data:
        return True
    else:
        return False


def delete_last_active_limit_for_user(identified_user):
    check_response = check_active_limits_for_user(identified_user)
    if check_response:
        conn1 = sqlite3.connect('finance.db')
        c1 = conn1.cursor()
        c1.execute("DELETE FROM limits WHERE login = ?", (identified_user,))
        conn1.commit()
        conn1.close()
    return


def set_warning_sum_in_active_limit_for_user(new_warning_sum, identified_user):
    check_response = check_active_limits_for_user(identified_user)
    print('func is called', check_response)
    if check_response:
        conn1 = sqlite3.connect('finance.db')
        c1 = conn1.cursor()
        c1.execute(
            "SELECT id FROM limits WHERE login = ? AND history = 0 ORDER BY limit_start_date DESC LIMIT 1",
            (identified_user,)
        )
        result = c1.fetchone()
        if result:
            limit_id = result[0]
            c1.execute(
                "UPDATE limits SET warning_sum = ? WHERE id = ?",
                (new_warning_sum, limit_id)
            )

        print(c1.rowcount, 'rowcount')
        conn1.commit()
        conn1.close()


def get_warning_sum_from_active_limit_for_user(identified_user):
    check_response = check_active_limits_for_user(identified_user)
    if check_response:
        conn1 = sqlite3.connect('finance.db')
        c1 = conn1.cursor()
        c1.execute(
            "SELECT warning_sum FROM limits WHERE login = ? AND history = 0 ORDER BY limit_start_date DESC LIMIT 1",
            (identified_user,)
        )
        warning_sum = c1.fetchone()
        conn1.close()
        return warning_sum[0]
    return


def get_active_limit_sum_for_user(identified_user):
    check_response = check_active_limits_for_user(identified_user)
    if check_response:
        conn1 = sqlite3.connect('finance.db')
        c1 = conn1.cursor()
        c1.execute(
            "SELECT sum_limit FROM limits WHERE login = ? AND history = 0 ORDER BY limit_start_date DESC LIMIT 1",
            (identified_user,)
        )
        sum_limit = c1.fetchone()
        conn1.close()
        return sum_limit[0]
    return


def get_active_limit_start_date_for_user(identified_user):
    check_response = check_active_limits_for_user(identified_user)
    if check_response:
        conn1 = sqlite3.connect('finance.db')
        c1 = conn1.cursor()
        c1.execute(
            "SELECT limit_start_date FROM limits WHERE login = ? AND history = 0 ORDER BY limit_start_date DESC LIMIT 1",
            (identified_user,)
        )
        limit_start = c1.fetchone()
        conn1.close()
        print(limit_start, 'limit_start')
        return limit_start[0]
    return


def get_active_limit_end_date_for_user(identified_user):
    check_response = check_active_limits_for_user(identified_user)
    if check_response:
        conn1 = sqlite3.connect('finance.db')
        c1 = conn1.cursor()
        c1.execute(
            "SELECT limit_end_date FROM limits WHERE login = ? AND history = 0 ORDER BY limit_start_date DESC LIMIT 1",
            (identified_user,)
        )
        limit_end = c1.fetchone()
        conn1.close()
        return limit_end[0]
    return


def make_limit_history_for_user(diff_limit_all_real_expenses, general_subjective_success, identified_user):
    check_response = check_active_limits_for_user(identified_user)
    if check_response:
        conn1 = sqlite3.connect('finance.db')
        c1 = conn1.cursor()
        c1.execute(
            "UPDATE limits SET history = 1 diff_limit_real_expenses=?, general_subjective_success_rate=None  WHERE login = ? AND history = 0 ORDER BY limit_start_date DESC LIMIT 1",
            (diff_limit_all_real_expenses, general_subjective_success, identified_user)
        )
        conn1.commit()
        conn1.close()

        def update_balance():
            set_balance_for_user(identified_user)

        update_balance()
    return


def calculate_mean_subjective_success_rate(login, start_date, end_date):
    create_db_finance()
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute(
        """SELECT AVG(subjective_success_rate) 
           FROM expenses 
           WHERE login = ? AND expense_date BETWEEN ? AND ?""",
        (login, start_date, end_date)
    )

    mean_subjective_success_rate = c.fetchone()[0]  # returns a tuple
    conn.close()
    return mean_subjective_success_rate


def add_active_limit(login, limit_start_date, limit_end_date, sum_limit, warning_sum, history=0,
                     diff_limit_real_expenses=None, general_subjective_success_rate=None):
    create_db_finance()
    conn_ = sqlite3.connect('finance.db')
    c_ = conn_.cursor()
    c_.execute(
        "INSERT INTO limits (login, limit_start_date, limit_end_date, sum_limit, warning_sum, history, diff_limit_real_expenses, general_subjective_success_rate) VALUES (?,?,?,?,?,?,?,?)",
        (login, limit_start_date, limit_end_date, sum_limit, warning_sum, history, diff_limit_real_expenses,
         general_subjective_success_rate))
    conn_.commit()
    conn_.close()


def add_expense(login, expense_date, sum_expense, expense_category, expense_subcategory, subjective_success_rate=None):
    create_db_finance()
    conn_2 = sqlite3.connect('finance.db')
    c_2 = conn_2.cursor()
    c_2.execute(
        "INSERT INTO expenses (login, expense_date, sum_expense, expense_category, expense_subcategory, subjective_success_rate) VALUES (?,?,?,?,?,?)",
        (login, expense_date, sum_expense, expense_category, expense_subcategory, subjective_success_rate))
    conn_2.commit()
    conn_2.close()


def check_expenses_for_user(identified_user):
    create_db_finance()
    conn1 = sqlite3.connect('finance.db')
    c1 = conn1.cursor()
    c1.execute("SELECT * FROM expenses WHERE login = ?", (identified_user,))
    expenses_data = c1.fetchone()
    print(expenses_data, 'exp.data')
    conn1.close()
    if expenses_data:
        return True
    else:
        return False


def get_expenses_for_login_for_the_period(identified_user, start_date, end_date):
    response_check_expenses_data = check_expenses_for_user(identified_user)
    if response_check_expenses_data:
        conn2 = sqlite3.connect('finance.db')
        c2 = conn2.cursor()
        c2.execute("SELECT sum_expense FROM expenses WHERE login = ? AND expense_date >= ? AND expense_date <= ?",
                   (identified_user, start_date, end_date))
        expenses_data_in_the_period = c2.fetchall()
        conn2.close()
        return expenses_data_in_the_period
    return


def get_sum_expenses_for_login_for_the_period(identified_user, start_date, end_date):
    response_check_expenses_data = check_expenses_for_user(identified_user)
    if response_check_expenses_data:
        conn2 = sqlite3.connect('finance.db')
        c2 = conn2.cursor()
        start_date = start_date.split()[0]
        c2.execute("SELECT SUM(sum_expense) FROM expenses WHERE login = ? AND expense_date >= ? AND expense_date <= ?",
                   (identified_user, start_date, end_date))
        sum_all_expenses_for_the_period = c2.fetchone()
        print(sum_all_expenses_for_the_period, 'tuple?')
        conn2.close()
        return sum_all_expenses_for_the_period[0] if sum_all_expenses_for_the_period is not None else 0
    return 0


def check_active_limits_for_user(identified_user):
    create_db_finance()
    conn1 = sqlite3.connect('finance.db')
    c1 = conn1.cursor()
    c1.execute("SELECT * FROM limits WHERE login = ? AND history = 0 ORDER BY limit_start_date DESC LIMIT 1",
               (identified_user,))
    limit_start_data = c1.fetchone()
    print(limit_start_data, 'limit_start_data when checking active limits for user. If user has had no active limits before - for example new user, or, older limits are history now - than None')
    conn1.close()
    if limit_start_data:
        return True
    else:
        return False


def delete_last_active_limit_for_user(identified_user):
    check_response = check_active_limits_for_user(identified_user)
    if check_response:
        conn1 = sqlite3.connect('finance.db')
        c1 = conn1.cursor()
        c1.execute("DELETE FROM limits WHERE login = ?", (identified_user,))
        conn1.commit()
        conn1.close()
    return


def set_warning_sum_in_active_limit_for_user(new_warning_sum, identified_user):
    check_response = check_active_limits_for_user(identified_user)
    print('func set_warning_sum_in_active_limit_for_user is called', check_response, ' False or True  - is`s about checking active limits for user. Is user is new or his limits are already history than False')
    if check_response:
        conn1 = sqlite3.connect('finance.db')
        c1 = conn1.cursor()
        c1.execute(
            "SELECT id FROM limits WHERE login = ? AND history = 0 ORDER BY limit_start_date DESC LIMIT 1",
            (identified_user,)
        )
        result = c1.fetchone()
        if result:
            limit_id = result[0]
            c1.execute(
                "UPDATE limits SET warning_sum = ? WHERE id = ?",
                (new_warning_sum, limit_id)
            )

        print(c1.rowcount, 'rowcount')
        conn1.commit()
        conn1.close()


def get_warning_sum_from_active_limit_for_user(identified_user):
    check_response = check_active_limits_for_user(identified_user)
    if check_response:
        conn1 = sqlite3.connect('finance.db')
        c1 = conn1.cursor()
        c1.execute(
            "SELECT warning_sum FROM limits WHERE login = ? AND history = 0 ORDER BY limit_start_date DESC LIMIT 1",
            (identified_user,)
        )
        warning_sum = c1.fetchone()
        conn1.close()
        return warning_sum[0]
    return


def get_active_limit_sum_for_user(identified_user):
    check_response = check_active_limits_for_user(identified_user)
    if check_response:
        conn1 = sqlite3.connect('finance.db')
        c1 = conn1.cursor()
        c1.execute(
            "SELECT sum_limit FROM limits WHERE login = ? AND history = 0 ORDER BY limit_start_date DESC LIMIT 1",
            (identified_user,)
        )
        sum_limit = c1.fetchone()
        conn1.close()
        return sum_limit[0]
    return


def get_active_limit_start_date_for_user(identified_user):
    check_response = check_active_limits_for_user(identified_user)
    if check_response:
        conn1 = sqlite3.connect('finance.db')
        c1 = conn1.cursor()
        c1.execute(
            "SELECT limit_start_date FROM limits WHERE login = ? AND history = 0 ORDER BY limit_start_date DESC LIMIT 1",
            (identified_user,)
        )
        limit_start = c1.fetchone()
        conn1.close()
        print(limit_start, 'limit_start')
        return limit_start[0]
    return

def get_active_sum_limit_for_user(identified_user):
    check_response = check_active_limits_for_user(identified_user)
    if check_response:
        conn1 = sqlite3.connect('finance.db')
        c1 = conn1.cursor()
        c1.execute(
            "SELECT sum_limit FROM limits WHERE login = ? AND history = 0 ORDER BY limit_start_date DESC LIMIT 1",
            (identified_user,)
        )
        received_sum_limit = c1.fetchone()[0]
        conn1.close()
        print(received_sum_limit, 'sum_limit')
        return received_sum_limit
    return


def get_active_limit_end_date_for_user(identified_user):
    check_response = check_active_limits_for_user(identified_user)
    if check_response:
        conn1 = sqlite3.connect('finance.db')
        c1 = conn1.cursor()
        c1.execute(
            "SELECT limit_end_date FROM limits WHERE login = ? AND history = 0 ORDER BY limit_start_date DESC LIMIT 1",
            (identified_user,)
        )
        limit_end = c1.fetchone()
        conn1.close()
        return limit_end[0]
    return

def update_balance_for_user(diff_limit_all_real_expenses, login_identified_user):
    if check_user_for_login(login_identified_user):
        balance_now = get_balance_for_user(login_identified_user)
        balance_now += diff_limit_all_real_expenses
        set_balance_for_user(balance_now, login_identified_user)
        global balance
        balance = balance_now



def make_limit_history_for_user(diff_limit_all_real_expenses, general_subjective_success, identified_user):
    check_response = check_active_limits_for_user(identified_user)
    if check_response:
        conn1 = sqlite3.connect('finance.db')
        c1 = conn1.cursor()
        c1.execute(
            """UPDATE limits 
               SET history = 1, diff_limit_real_expenses = ?, general_subjective_success_rate = ? 
               WHERE id = (SELECT id FROM limits WHERE login = ? AND history = 0 ORDER BY limit_start_date DESC LIMIT 1)""",
            (diff_limit_all_real_expenses, general_subjective_success, identified_user)
        )
        conn1.commit()
        conn1.close()

        update_balance_for_user(diff_limit_all_real_expenses, identified_user)

    return


def check_user_for_login(passed_login):
    create_db_finance()
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute(
        """SELECT *
           FROM users 
           WHERE login = ?""",
        (passed_login,)
    )
    user_data = c.fetchall()
    conn.close()
    if user_data:
        return True
    else:
        return False

def check_password_for_login(passed_login, passed_password):
    create_db_finance()
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute(
        """SELECT *
           FROM users 
           WHERE login = ? AND password = ?""",
        (passed_login, passed_password)
    )
    user_data = c.fetchall()
    conn.close()
    if user_data:
        return True
    else:
        return False


def set_balance_for_user(new_balance, login):
    if check_user_for_login(login):
        conn = sqlite3.connect('finance.db')
        c = conn.cursor()
        c.execute(
            """"UPDATE users SET spare_balance = ? WHERE login = ?""",
            (new_balance, login)
        )
        conn.commit()
        conn.close()
    return

def set_subjective_success_rate_for_user(subjective_success_rate_value, login):
    if check_user_for_login(login):
        conn = sqlite3.connect('finance.db')
        c = conn.cursor()
        c.execute(
            """UPDATE expenses SET subjective_success_rate = ? WHERE id = (SELECT id FROM expenses WHERE login = ?
            ORDER BY id DESC LIMIT 1)""",
            (subjective_success_rate_value, login)
        )
        conn.commit()
        conn.close()
    return

def get_subjective_success_rate_for_user(login):
    if check_user_for_login(login):
        conn = sqlite3.connect('finance.db')
        c = conn.cursor()
        c.execute(
            """SELECT subjective_success_rate FROM expenses WHERE login = ? ORDER BY id DESC LIMIT 1""",
            (login,)
        )
        received_subjective_success_rate_for_user = c.fetchone()[0]
        conn.commit()
        conn.close()
        return received_subjective_success_rate_for_user
    return


def get_balance_for_user(login):
    if check_user_for_login(login):
        conn = sqlite3.connect('finance.db')
        c = conn.cursor()
        c.execute(
            """SELECT spare_balance 
               FROM users 
               WHERE login = ?""",
            (login,)
        )
        user_balance = c.fetchone()[0]
        conn.close()
        return user_balance if user_balance is not None else 0
    return


def get_sum_left_to_spend_without_warning_for_user(login):
    if check_user_for_login(login):
        conn = sqlite3.connect('finance.db')
        c = conn.cursor()
        c.execute(
            """SELECT sum_left_to_spend_without_warning  
               FROM users 
               WHERE login = ?""",
            (login,)
        )
        user_balance = c.fetchone()[0]
        conn.close()
        return user_balance if user_balance is not None else 0
    return


def sign_up_set_new_user(login, password, spare_balance=0, sum_left_to_spend_without_warning=0):
    check_user_with_this_login = check_user_for_login(login)
    if not check_user_with_this_login:
        create_db_finance()
        conn = sqlite3.connect('finance.db')
        c = conn.cursor()
        c.execute(
            """INSERT INTO users
            (login, password, spare_balance, sum_left_to_spend_without_warning) VALUES (?,?,?,?)""",
            (login, password, spare_balance, sum_left_to_spend_without_warning))
        conn.commit()
        conn.close()
        print('Created')
        return True
    else:
        return False


def sign_in_user(passed_login, passed_password):
    create_db_finance()
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute(
        """SELECT login
         FROM users
         WHERE login = ? AND password = ?""",
        (passed_login, passed_password))
    result_finding_user_sign_in = c.fetchone()
    conn.close()
    # global identified_user
    # identified_user = passed_login
    if result_finding_user_sign_in:
        print(f"Sign in user login {passed_login}, password{passed_password}: success.")
        set_user(passed_login)
    print('Found')
