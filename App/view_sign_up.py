import flet as ft
import time
from identification_data import set_user, get_user
import expenses_diary




def view_sign_up_controls(page: ft.Page):
    def validate_new_login(login: str):
        if isinstance(login, str) and 0 < len(login) < 10:
            if login not in users:
                return True
            else:
                raise Exception('Select another login. This login is already used')
        raise Exception('Type in another login. Login should be at least 1 symbol long and less than 10 symbols')


    def validate_new_password(password: str):
        if isinstance(password, str) and 0 < len(password) < 10:
            return True

        raise Exception('Type in another login. Login should be at least 1 symbol long and less than 10 symbols')

    def validate_repeat_new_password(password: str):
        if repeat_password_text_field.value == new_password_text_field.value:
            return True
        raise Exception('Try one more time. It does`t match the password you`ve typed in previously')

    def after_validation_actions(e):
        #global identified_user


        if expenses_diary.sign_up_set_new_user(new_login_text_field.value, new_password_text_field.value):
            set_user(new_login_text_field.value)
            #identified_user = new_login_text_field.value
            print(get_user(), "identified_user")
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
            page.open(
                ft.AlertDialog(title=ft.Text('User with such login already exists'), bgcolor=ft.colors.RED_100))
            new_login_text_field.value = ''
            new_password_text_field.value = ''
            repeat_password_text_field = ''
            page.update()



    def validation_new_password_login(control: ft.control, user_input_str: str):
        if control == new_login_text_field:
            valid_val_login = validate_new_login(user_input_str)
            if valid_val_login:
                control.data = 1
                return True
        elif control == new_password_text_field:
            if new_login_text_field.data == 1:
                valid_val_password = validate_new_password(user_input_str)
                if valid_val_password:
                    new_password_text_field.data = 1
                    return True
                return False
            return False
        elif control == repeat_password_text_field:
            if new_password_text_field.data == 1:
                valid_val_repeat_password = validate_repeat_new_password(user_input_str)
                if valid_val_repeat_password:
                    print("lllllll")
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



