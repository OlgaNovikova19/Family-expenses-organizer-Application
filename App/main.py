import random
import datetime
from collections import deque
import flet as ft
import expenses_diary
import calendar
import view_charts
import view_sign_in_sign_up_selection
from view_sign_in import view_sign_in_layout_creation
from view_goals import view_goals_create_layout, show_spare_balance
from identification_data import get_user, set_chosen_date, get_chosen_date
import view_goals
from fabrique_controls import date_picker_creation, create_individual_error_message
from expenses_input import basic_menu_creation
import view_charts
import logging


def main(page: ft.Page):
    page.adaptive = True
    page.padding = 30
    page.title = "Family expenses organizer"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed="green")
    page.scroll = ft.ScrollMode.ALWAYS

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),  # Log to a file
            logging.StreamHandler()  # Also print to console
        ]
    )

    #def create_app_bar():

    def clicked_left_scroll_icon_in_appbar(e):
        date_appbar.data -= 1
        change_date_appbar_value()

    def clicked_right_scroll_icon_in_appbar(e):
        date_appbar.data += 1
        change_date_appbar_value()

    def change_date_appbar_value():
        date_today_min_1day = datetime.datetime.now() + datetime.timedelta(days=date_appbar.data)
        date_appbar.value = date_today_min_1day.strftime("%a") + ", " + date_today_min_1day.strftime(
            "%d") + " " + date_today_min_1day.strftime("%b")
        page.update()

    def open_view_goals(e):
        page.views.append(ft.View(route='/goals', controls=view_goals_create_layout(page)))
        page.update()

    def date_picker_create() -> ft.Control:
        def choose_date_(e):
            str_selected_date = e.control.value.strftime('%Y-%m-%d')
            page.add(ft.Text(f"Date selected: {str_selected_date}"))
            page.add(ft.TextButton(f"{str_selected_date}"))
            set_chosen_date(str_selected_date)
            page.update()

        pick_date_in_calendar_ = ft.DatePicker(
            first_date=datetime.datetime(year=2023, month=10, day=1),
            last_date=datetime.datetime(year=2025, month=10, day=1),
            on_change=choose_date_
        )

        calendar_icon_button = ft.IconButton(ft.icons.CALENDAR_MONTH, tooltip="Calendar",
                                             on_click=lambda e: page.open(pick_date_in_calendar_))
        return calendar_icon_button

    calendar_icon_button = date_picker_create()

    def show_warning(e):
        view_goals.show_warning_for_user_if_needed(get_user(), page)

    def show_sum_left_before_warning_sum(e):
        name_user = get_user()
        information = ''
        if name_user is None:
            name_user = 'guest'
            information = 'please sign in to use this function.'
        else:
            if expenses_diary.check_active_limits_for_user(get_user()):
                warning_sum = expenses_diary.get_warning_sum_from_active_limit_for_user(get_user())
                start_date_active_limit = expenses_diary.get_active_limit_start_date_for_user(get_user())
                end_date_active_limit = expenses_diary.get_active_limit_end_date_for_user(get_user())
                sum_expenses = expenses_diary.get_sum_expenses_for_login_for_the_period(get_user(),
                                                                                        start_date_active_limit,
                                                                                        end_date_active_limit)
                sum_limit_user = expenses_diary.get_active_sum_limit_for_user(get_user())
                if warning_sum is None:
                    warning_sum = sum_limit_user

                sum_left_before_warning_sum = warning_sum - sum_expenses
                currency = expenses_diary.get_currency_for_user(name_user)
                if sum_left_before_warning_sum < 0:
                    page.open(
                        ft.AlertDialog(title=ft.Text(f'Dear {name_user}, you can`t spend money freely now.'),
                                       bgcolor=ft.colors.RED_100))
                    return
                else:
                    information = f'you can freely spend {sum_left_before_warning_sum} {currency}'

            else:
                information = (
                    'no active limits at the current moment, so you can now freely spend as much as you want...really :-)\n'
                    'However it will be wise to take into account your spare balance..It`s at the bottom of the page.')
        page.open(ft.AlertDialog(title=ft.Text(f'Dear {name_user}, {information}'), bgcolor=ft.colors.GREEN_200))

    goals_icon_button = ft.IconButton(ft.icons.ADJUST, tooltip="Goals", on_click=open_view_goals, data=0)
    wallet_icon_button = ft.IconButton(ft.icons.HOME_REPAIR_SERVICE, tooltip="Sum you can still safely spend",
                                       on_click=show_sum_left_before_warning_sum)
    warning_icon_button = ft.IconButton(ft.icons.REPORT, tooltip="Warnings", on_click=show_warning)

    def open_settings_click(e):
        def change_to_light_theme(ev):
            if page.theme_mode == ft.ThemeMode.DARK:
                page.theme_mode = ft.ThemeMode.LIGHT
                page.update()
            else:
                create_individual_error_message(page, 'Hmmm...but the light theme is already on...')

        def change_to_dark_theme(ev):
            if page.theme_mode == ft.ThemeMode.LIGHT:
                page.theme_mode = ft.ThemeMode.DARK
                page.update()
            else:
                create_individual_error_message(page, 'Hmmm...but the dark theme is already on...')

        def change_currency_to_rubbles(ev):
            login = get_user()
            if login is None:
                create_individual_error_message(page, "Dear guest, please sign in to save your choice")
            else:
                if expenses_diary.get_currency_for_user(login) == 'rubbles':
                    create_individual_error_message(page,
                                                    'Hmmm...but you have already set rubbles as your chosen currency...')
                else:
                    expenses_diary.set_currency_for_user("rubbles", login)

        def change_currency_to_euro(ev):
            login = get_user()
            if login is None:
                create_individual_error_message(page, "Dear guest, please sign in to save your choice")
            else:
                expenses_diary.set_currency_for_user("euro", login)

        def change_currency_to_dollars(ev):
            login = get_user()
            if login is None:
                create_individual_error_message(page, "Dear guest, please sign in to save your choice")
            else:
                expenses_diary.set_currency_for_user("dollars", login)

        dlg_modal_settings = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please choose your settings", text_align=ft.TextAlign.CENTER),
            content=ft.Text("And your choice is...", italic=True, weight=ft.FontWeight.W_600, size=20),
            actions=[ft.Column([
                ft.Row([
                    ft.ElevatedButton("Light theme", on_click=change_to_light_theme, bgcolor=ft.colors.AMBER_200,
                                      height=30),
                    ft.ElevatedButton("Dark theme", on_click=change_to_dark_theme, bgcolor=ft.colors.AMBER_200,
                                      height=30)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.ElevatedButton("Currency: rubbles", on_click=change_currency_to_rubbles,
                                      bgcolor=ft.colors.AMBER_300, height=30),
                    ft.ElevatedButton("Currency: euro", on_click=change_currency_to_euro, bgcolor=ft.colors.AMBER_300,
                                      height=30),
                    ft.ElevatedButton("Currency: dollars", on_click=change_currency_to_dollars,
                                      bgcolor=ft.colors.AMBER_300, height=30)], alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row([
                    ft.ElevatedButton("CLOSE SETTINGS", on_click=lambda _: page.close(dlg_modal_settings),
                                      bgcolor=ft.colors.RED_100, height=30)], alignment=ft.MainAxisAlignment.CENTER)
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN, shape=ft.RoundedRectangleBorder(radius=70.0),
            bgcolor=ft.colors.LIGHT_GREEN_ACCENT_100)

        page.open(dlg_modal_settings)

    adjust_icon_button = ft.IconButton(ft.icons.ENGINEERING, tooltip="Settings", on_click=open_settings_click)
    left_scroll_icon_button = ft.IconButton(ft.icons.ARROW_LEFT, tooltip="Left scroll",
                                            on_click=clicked_left_scroll_icon_in_appbar)
    right_scroll_icon_button = ft.IconButton(ft.icons.ARROW_RIGHT, tooltip="Right scroll",
                                             on_click=clicked_right_scroll_icon_in_appbar)
    date_str_appbar = 'Today, ' + datetime.datetime.now().strftime("%a") + ", " + datetime.datetime.now().strftime(
        "%d") + " " + datetime.datetime.now().strftime("%b")

    date_appbar = ft.Text(value=(date_str_appbar), size=20, data=0)
    scroll_appbar = ft.Row([left_scroll_icon_button, date_appbar, right_scroll_icon_button])
    page.appbar = ft.AppBar(leading=ft.Icon(ft.icons.SAVINGS), leading_width=60,
                            title=ft.Text("Family expenses organizer"), bgcolor=ft.colors.SURFACE_VARIANT,
                            actions=[scroll_appbar, calendar_icon_button, wallet_icon_button, warning_icon_button,
                                     goals_icon_button, adjust_icon_button])

    page.update()

    def clicked_balance_icon_button(e):
        show_spare_balance(get_user(), page)

    balance_icon_button = ft.IconButton(icon=ft.icons.SAVINGS, tooltip="Spare Balance",
                                        on_click=clicked_balance_icon_button)

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        page.views.append(
            ft.View(route='/', controls=view_sign_in_sign_up_selection.view_sign_in_sign_up(page))
        )

        if page.route == "/authentication":
            page.views.append(
                ft.View(route='/authentication',
                        controls=view_sign_in_layout_creation(page)))

        elif page.route == "/app":
            page.views.append(
                ft.View(route='/app', controls=[page.appbar, st,
                                                #main_category_selection_col,
                                                basic_menu_creation(page),
                                                ft.BottomAppBar(content=ft.Row(
                                                    controls=[ft.IconButton(icon=ft.icons.PIE_CHART, tooltip="Charts",
                                                                            on_click=lambda _: page.go('/third_page')),
                                                              ft.IconButton(icon=ft.icons.ARROW_LEFT,
                                                                            tooltip="Back to Authentication",
                                                                            on_click=lambda _: page.go('/')),
                                                              ft.IconButton(icon=ft.icons.ARROW_RIGHT,
                                                                            tooltip="Go to ThirdPage",
                                                                            on_click=lambda _: page.go('/third_page')),
                                                              balance_icon_button
                                                              ], alignment=ft.MainAxisAlignment.CENTER
                                                ))
                                                ]))

        elif page.route == "/third_page":
            page.views.append(
                ft.View(
                    route="/third_page",
                    controls=[
                        ft.AppBar(title=ft.Text("Charts"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Text("Select period of time you are interested in and press SHOW CHART button", italic=True,
                                weight=ft.FontWeight.W_600, size=18),
                        view_charts.create_charts_layout(page)
                    ]
                )
            )
        page.update()

    def view_pop(e: ft.ViewPopEvent):
        if len(page.views) > 1:
            page.views.pop()
        top_view: ft.View = page.views[-1]
        page.go(top_view.route)
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    page.update()

    img_obj = ft.Image(
        src=f"piggy-bank-with-stacks-coins.jpg",
        fit=ft.ImageFit.COVER,
        width=200,
        height=2000,
        expand=True
    )

    img = ft.Row(alignment=ft.MainAxisAlignment.CENTER, expand=True, controls=[img_obj])

    #def days_movable_row_creation():
    date_buttons_list = []
    max_visible_dates_in_row = 7
    dates_deque = deque([], maxlen=max_visible_dates_in_row)
    current_date = datetime.date.today()
    center_date = current_date

    start_calendar = datetime.date.today() - datetime.timedelta(days=30)
    end_calendar = datetime.date.today() + datetime.timedelta(days=30)

    def click_date_button(e):
        clicked_button = e.control
        upper_text = clicked_button.content.controls[0].value
        lower_text = clicked_button.content.controls[1].value
        chosen_row_date_str = upper_text + " " + lower_text + " " + "2024"
        chosen_row_date = datetime.datetime.strptime(chosen_row_date_str, "%B %d %Y")
        chosen_row_date_formatted_str = chosen_row_date.strftime("%Y-%m-%d")
        set_chosen_date(chosen_row_date_formatted_str)


    def generate_dates_around(center_date_):
        next_date = center_date_
        for i in range(-4, 4):
            next_date = center_date_ + datetime.timedelta(days=i)
            yield next_date
            dates_deque.append(next_date)

    def generate_buttons():
        nonlocal center_date
        current_date_ = start_calendar
        while current_date_ < end_calendar:
            text_upper = ft.Text(value=current_date_.strftime("%B"), size=20)
            text_lower = ft.Text(value=f"{current_date_.day}", size=15, text_align=ft.TextAlign.CENTER)
            current_date_ += datetime.timedelta(days=1)

            button_width = 150
            date_button = ft.ElevatedButton(
                content=ft.Column([text_upper,
                                   text_lower,
                                   ],
                                  alignment=ft.MainAxisAlignment.CENTER,
                                  spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                on_click=click_date_button,
                width=button_width
            )

            date_buttons_list.append(date_button)

    generate_dates_around(center_date)
    generate_buttons()

    movable_row = ft.Row(controls=date_buttons_list, alignment=ft.MainAxisAlignment.CENTER, spacing=50, wrap=False,
                         scroll=ft.ScrollMode.ALWAYS)

    days_movable_row = ft.Container(movable_row,
                                    bgcolor=ft.colors.GREEN_300,
                                    margin=40, padding=5, blend_mode=ft.BlendMode.MODULATE,
                                    border=ft.border.all(width=1, color=ft.colors.GREEN_200),
                                    border_radius=ft.border_radius.all(150), alignment=ft.alignment.top_left,
                                    width=1100, height=80)

    st = ft.Stack([img, days_movable_row], expand=True)
    page.add(st)

    page.update()


ft.app(target=main, assets_dir="assets")
