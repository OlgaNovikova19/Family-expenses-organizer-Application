import flet as ft
import datetime
from identification_data import get_chosen_date, set_chosen_date

def create_sum_input_unit(page:ft.Page):
    def focus_text_field_input_sum(e):
        text_field_input_sum.value = ""
        text_field_input_sum.prefix_text = ""
        text_field_input_sum.suffix_text = ""
        text_field_input_sum.hint_text = "0.00"
        text_field_input_sum.error_text = ""
        page.update()


    def change_text_field_input_sum(e):
        if validate_sum_input():
            text_field_input_sum.prefix_text = 'Limit I want to set...'
            text_field_input_sum.suffix_text = 'rubbles'
            text_field_input_sum.hint_text = ""
            text_field_input_sum.error_text = ""
            print(text_field_input_sum.value)
            page.update()
        else:
            text_field_input_sum.error_text = ""
            text_field_input_sum.error_text = "Warning:illegal input"
            page.update()



    def submit_text_field_input_sum(e):
        print(text_field_input_sum.value)
        if validate_sum_input():
            text_field_input_sum.disabled = True
            page.update()
        else:
            text_field_input_sum.disabled = False
            text_field_input_sum.value = 0.00
            page.update()

    text_field_input_sum = ft.TextField(label="Sum you don`t want to exceed", value="Limit of spending",
                                            hint_text="0.00", helper_text="Type in here sum of money",
                                            on_focus=focus_text_field_input_sum,
                                            on_change=change_text_field_input_sum, on_submit=submit_text_field_input_sum,
                                            data=0.00)

    def validate_sum_input():
        if text_field_input_sum.value == 'Limit of spending' or text_field_input_sum.value == "":
            return True
        elif text_field_input_sum.value == '-':
            return False

        else:
            try:
                float_sum_input = float(text_field_input_sum.value)
                if float(text_field_input_sum.value) < 0:
                    text_field_input_sum.error_text = "Sum should be a positive number"
                    page.open(
                        ft.AlertDialog(title=ft.Text('Sum should be a positive number'), bgcolor=ft.colors.RED_100))
                    page.update()
                    return False
            except:
                return False

        return True


    def add_one(e):
        if validate_sum_input():
            text_field_input_sum.error_text = ""
            text_field_input_sum.value = float(text_field_input_sum.value) + 1
            page.update()
        else:
            raise ValueError('Check validate_sum_input function')


    def subtract_one(e):
        validate_sum_input()
        if float(text_field_input_sum.value) < 1.00:
            text_field_input_sum.error_text = "For subtraction sum should be 1 or more"
            page.open(ft.AlertDialog(title=ft.Text('For subtraction sum should be 1 or more'), bgcolor=ft.colors.RED_100))
            page.update()


        else:
            text_field_input_sum.value = float(text_field_input_sum.value) - 1
            text_field_input_sum.data = text_field_input_sum.value
            page.update()


    icon_plus = ft.IconButton(icon=ft.icons.ADD,
                              icon_color="green",
                              icon_size=20,
                              tooltip="Plus", on_click=add_one)
    icon_minus = ft.IconButton(icon=ft.icons.MINIMIZE,
                               icon_color="red",
                               icon_size=20,
                               tooltip="Minus", on_click=subtract_one)

    sum_input_unit = ft.Row([icon_minus, text_field_input_sum, icon_plus], alignment=ft.alignment.bottom_right)

    return sum_input_unit

def date_picker_creation(page:ft.Page)->ft.Control:
    selected_date = None

    def choose_date(e):
        nonlocal selected_date
        str_selected_date = e.control.value.strftime('%Y-%m-%d')
        page.add(ft.Text(f"Date selected: {str_selected_date}"))
        page.add(ft.TextButton(f"{str_selected_date}"))
        print(str_selected_date, 'str_selected_date')
        print(e.control.data, 'data..')
        e.control.data = str_selected_date
        selected_date = str_selected_date
        page.update()


    pick_date_in_calendar = ft.DatePicker(
        first_date=datetime.datetime(year=2023, month=10, day=1),
        last_date=datetime.datetime(year=2025, month=10, day=1),
        data = selected_date,
        on_change=choose_date
        )
    print (selected_date, 'sel.date')
    return pick_date_in_calendar

def create_error_message(page:ft.Page)->None:
    alert_dialog = ft.AlertDialog(title=ft.Text('Something went wrong...Try once again'), bgcolor=ft.colors.RED_100)
    page.open(alert_dialog)
    page.update()

def create_individual_error_message(page:ft.Page, message:str)->None:
    page.open(ft.AlertDialog(title=ft.Text(message, text_align=ft.TextAlign.CENTER), bgcolor=ft.colors.RED_100))
    page.update()

def create_calendar_button(page:ft.Page) -> ft.Control:
    def choose_date(e):
            str_selected_date = e.control.value.strftime('%Y-%m-%d')
            page.add(ft.Text(f"Date selected: {str_selected_date}"))
            page.add(ft.TextButton(f"{str_selected_date}"))
            print(str_selected_date, 'str_selected_date')
            print(e.control.data, 'data..')
            set_chosen_date(str_selected_date)
            print(get_chosen_date(), 'ch.date')
            page.update()

    pick_date_in_calendar = ft.DatePicker(
            first_date=datetime.datetime(year=2023, month=10, day=1),
            last_date=datetime.datetime(year=2025, month=10, day=1),
            on_change=choose_date
        )

    calendar_elev_button = ft.ElevatedButton(
            "Select date",
            icon=ft.icons.CALENDAR_MONTH,
            bgcolor=ft.colors.AMBER_200,
            on_click=lambda e: page.open(
                pick_date_in_calendar
            )
        )
    page.add(calendar_elev_button)
    return calendar_elev_button



