import flet as ft
import time
from identification_data import set_user, get_user
import expenses_diary
from fabrique_controls import create_individual_error_message
import logging




def view_sign_up_controls(page: ft.Page):
    def validate_new_login(login: str):
        logging.info("function called: validate_new_login(login: str)")
        logging.info(f"login: {login}")
        logging.info(f"len(login): {len(login)}")
        if isinstance(login, str) and 0 < len(login) < 10:
            if login != "Your login":
                if not expenses_diary.check_user_for_login(login):
                    return True
                else:
                    create_individual_error_message(page, 'Select another login. This login is already used')
                    return False
            else:
                create_individual_error_message(page, 'Type in your login. The field for login should not be empty')
                return False
        else:
            create_individual_error_message(page, 'Login should be at least 1 symbol long and less than 10 symbols long')
            return False


    def validate_new_password(password: str):
        logging.info("function called: validate_new_password(password: str)")
        logging.info(f"password: {password}")
        logging.info(f"len(password): {len(password)}")
        if isinstance(password, str) and 0 < len(password) < 10:
            if password != "Your password":
                return True
            else:
                create_individual_error_message(page,
                                                'Type in your password. The field for password should not be empty')
                return False
        else:
            create_individual_error_message(page,
                                            'Type in another password. Password should be at least 1 symbol long and less than 10 symbols long')
            return False

    def validate_repeat_new_password(password: str):
        logging.info("function called: validate_repeat_new_password(password: str)")
        if repeat_password_text_field.value == new_password_text_field.value:
            return True
        create_individual_error_message(page,'Try one more time. It does`t match the password you`ve typed in previously')
        return False

    def after_validation_actions(e):
        logging.info("function called: after_validation_actions(e)")
        check_valid_response_login = validation_new_password_login(new_login_text_field,new_login_text_field.value)
        check_valid_response_password = validation_new_password_login(new_password_text_field, new_password_text_field.value)
        check_valid_response_repeat_password = validation_new_password_login(repeat_password_text_field, repeat_password_text_field.value)
        logging.info(f"check_valid_response_login: {check_valid_response_login}, check_valid_response_password: {check_valid_response_password},"
                     f" check_valid_response_repeat_password: {check_valid_response_repeat_password}")
        if check_valid_response_login and check_valid_response_password and check_valid_response_repeat_password:
            expenses_diary.sign_up_set_new_user(new_login_text_field.value, new_password_text_field.value)
            logging.info("function called: expenses_diary.sign_up_set_new_user(new_login_text_field.value, new_password_text_field.value)")
            page.views[-1].controls.append(ft.Row(
                [ft.Text(f"Welcome, {new_login_text_field.value}!", italic=True, weight=ft.FontWeight.BOLD,
                         font_family="Consolas", size=35, color=ft.colors.AMBER)],
                alignment=ft.MainAxisAlignment.CENTER))
            page.update()
            time.sleep(3)
            page.views[-1].controls.append(ft.Row([ft.Text("One more formality...", italic=True, weight=ft.FontWeight.BOLD,
                                                           font_family="Consolas", size=35, color=ft.colors.AMBER)],
                                                  alignment=ft.MainAxisAlignment.CENTER))
            page.update()
            time.sleep(3)
            page.go('/authentication')
        else:
            new_login_text_field.value = ''
            new_password_text_field.value = ''
            repeat_password_text_field.value = ''
            page.update()



    def validation_new_password_login(control: ft.control, user_input_str: str):
        logging.info("function called: validation_new_password_login(control: ft.control, user_input_str: str)")
        logging.info(f"control: {control}")
        if control == new_login_text_field:
            valid_val_login = validate_new_login(user_input_str)
            logging.info(f"function called: validate_new_login(user_input_str), returned: valid_val_login: {valid_val_login}")
            if valid_val_login:
                control.data = 1
                return True
        elif control == new_password_text_field:
            if new_login_text_field.data == 1:
                valid_val_password = validate_new_password(user_input_str)
                logging.info(
                    f"function called: validate_new_password(user_input_str), returned: valid_val_password: {valid_val_password}")
                if valid_val_password:
                    new_password_text_field.data = 1
                    return True
                return False
            return False
        elif control == repeat_password_text_field:
            if new_password_text_field.data == 1:
                valid_val_repeat_password = validate_repeat_new_password(user_input_str)
                logging.info(
                    f"function called: validate_repeat_new_password(user_input_str), returned: valid_val_repeat_password: {valid_val_repeat_password}")
                if valid_val_repeat_password:
                    new_login_text_field.data = 0
                    new_password_text_field.data = 0
                    return True

                return False
            return False
        else:
            raise ValueError()

    def new_password_or_login_changed(e):
        e.control.hint_text = ''
        page.update()

    def new_password_or_login_submit(e):
        logging.info("function called: new_password_or_login_submit(e)")
        validation_response = validation_new_password_login(e.control, e.control.value)
        if validation_response:
            e.control.disabled = True
            page.views[-1].controls.append(ft.Text(f"Successful. Correct {e.control.label}"))
            page.update()

        else:
            page.views[-1].controls.append(ft.Text(f"Unsuccessful input. Incorrect {e.control.label}. Try again"))
            e.control.value = ''
            page.update()

    def new_password_or_login_field_on_focus(e):
        e.control.value = ''
        page.update()

    appbar_sign_up = ft.AppBar(leading=ft.Icon(ft.icons.SAVINGS), leading_width=60,
                               title=ft.Text("Family expenses organizer"), bgcolor=ft.colors.SURFACE_VARIANT,
                               actions=[ft.IconButton(icon=ft.icons.ARROW_LEFT, tooltip="Go to Sign In/Sign Up",
                                                      on_click=lambda _: page.go('')),
                                        ft.IconButton(icon=ft.icons.ARROW_RIGHT,
                                                      tooltip="Go to App without authentication",
                                                      on_click=lambda _: page.go('/app'))])

    new_login_text_field = ft.TextField(label="Login", value="Your login", hint_text="Type in here your login",
                                        helper_text='Login should be less than 10 symbols',
                                        on_focus=new_password_or_login_field_on_focus,
                                        on_change=new_password_or_login_changed, on_submit=new_password_or_login_submit)
    new_password_text_field = ft.TextField(label="Password", value="Your password",
                                           hint_text="Type in here your password",
                                           helper_text='Password should be less than 10 symbols',
                                           on_focus=new_password_or_login_field_on_focus, password=True,
                                           can_reveal_password=True,
                                           on_change=new_password_or_login_changed,
                                           on_submit=new_password_or_login_submit)
    repeat_password_text_field = ft.TextField(label="Repeat password", value="Your password",
                                              hint_text="Type in here your password one more time",
                                              on_focus=new_password_or_login_field_on_focus, password=True,
                                              can_reveal_password=True,
                                              on_change=new_password_or_login_changed,
                                              on_submit=new_password_or_login_submit)

    sign_up_button = ft.ElevatedButton('SIGN UP', on_click=after_validation_actions)

    column_new_login_password_input_t_fields = ft.Column(
        [new_login_text_field, new_password_text_field, repeat_password_text_field, sign_up_button], spacing=50,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    view_sign_up_controls = [appbar_sign_up, column_new_login_password_input_t_fields]
    return view_sign_up_controls



