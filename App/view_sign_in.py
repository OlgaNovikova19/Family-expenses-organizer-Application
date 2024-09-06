import flet as ft
import time
from identification_data import get_user, set_user
import expenses_diary
from view_goals import create_warning, show_warning_for_user_if_needed
from fabrique_controls import create_individual_error_message

def view_sign_in_layout_creation(page: ft.Page):


    appbar_sign_in = ft.AppBar(leading=ft.Icon(ft.icons.SAVINGS), leading_width=60,
                               title=ft.Text("Family expenses organizer"), bgcolor=ft.colors.SURFACE_VARIANT,
                               actions=[ft.IconButton(icon=ft.icons.ARROW_LEFT, tooltip="Go to Sign In/Sign Up",
                                                      on_click=lambda _: page.go('/')),
                                        ft.IconButton(icon=ft.icons.ARROW_RIGHT,
                                                      tooltip="Go to App without authentication",
                                                      on_click=lambda _: page.go('/app'))])

    def validate_login(login:str):
        if expenses_diary.check_user_for_login(login):
            print(expenses_diary.check_user_for_login(login), 'expenses_diary.check_user_for_login(login)')
            return True
        return False


    def validate_password(login:str, password:str):
        if expenses_diary.check_password_for_login(login, password):
            return True
        return False


    def actions_after_sign_in_validation(e):
        print('before condition')
        if validate_login(login_text_field.value):
            print('1 condition')

            if validate_password(login_text_field.value, password_text_field.value):
                login_text_field.disabled = True
                password_text_field.disabled = True
                print("Sign in - validation")
                set_user(login_text_field.value)
                expenses_diary.sign_in_user(login_text_field.value, password_text_field.value)
                page.views[-1].controls.append(
                    ft.Row([ft.Text(f"Greetings, {login_text_field.value}!", italic=True, weight=ft.FontWeight.BOLD,
                                    font_family="Consolas", size=35, color=ft.colors.AMBER)],
                           alignment=ft.MainAxisAlignment.CENTER))
                page.update()
                time.sleep(2)
                page.go('/app')
                show_warning_for_user_if_needed(get_user(), page)
            else:
                create_individual_error_message(page, "Incorrect password")
        else:
            create_individual_error_message(page, "Incorrect login")


    def validation_password_login(control:ft.control, user_input_str:str):
        if control == login_text_field:
            valid_val_login = validate_login(user_input_str)
            if valid_val_login:
                password_text_field.disabled = False
                control.data = 1
                print(control.data)
                return True
            else:
                password_text_field.disabled = True
                return False
        elif control == password_text_field:
            if login_text_field.data == 1:
                valid_val_password = validate_password(login_text_field.value, user_input_str)
                if valid_val_password:
                    login_text_field.data = 0
                    return True
                return False
            return False
        else:
            raise ValueError()



    def password_or_login_changed(e):
        e.control.hint_text = ''
        page.update()


    def password_or_login_submit(e):
        validation_response = validation_password_login(e.control, e.control.value)
        if validation_response == True:
            e.control.disabled=True
            page.views[-1].controls.append(ft.Text(f"Successful. Correct {e.control.label}"))
            page.update()
        else:
            page.views[-1].controls.append(ft.Text(f"Unsuccessful input. Incorrect {e.control.label}. Try again"))
            e.control.value = ''
            page.update()



    def password_or_login_field_on_focus(e):
        e.control.value = ''
        page.update()


    login_text_field = ft.TextField(label="Login", value="Your login", hint_text="Type in here your login", on_focus= password_or_login_field_on_focus, on_change = password_or_login_changed, on_submit=password_or_login_submit)
    password_text_field = ft.TextField(label="Password", value="Your password", hint_text="Type in here your password", on_focus= password_or_login_field_on_focus, password=True, can_reveal_password=True,
                                     on_change = password_or_login_changed, on_submit=password_or_login_submit)

    sign_in_button = ft.ElevatedButton('SIGN IN', on_click=actions_after_sign_in_validation)

    column_login_password_input_t_fields = ft.Column([login_text_field, password_text_field, sign_in_button], spacing=50, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    view_sign_in_controls = [appbar_sign_in, column_login_password_input_t_fields]
    return view_sign_in_controls