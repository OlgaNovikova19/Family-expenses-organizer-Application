"""import flet as ft

def create_app_bar(page:ft.Page):
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


    calendar_icon_button = ft.IconButton(ft.icons.CALENDAR_MONTH, tooltip="Calendar", on_click=lambda e: page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2023, month=10, day=1),
                    last_date=datetime.datetime(year=2025, month=10, day=1),
                    on_change=choose_date
                )))
    goals_icon_button = ft.IconButton(ft.icons.ADJUST, tooltip="Goals", on_click=open_pagelet_goals, data = 0)
    wallet_icon_button = ft.IconButton(ft.icons.HOME_REPAIR_SERVICE, tooltip="Sum you can still safely spend")
    warning_icon_button = ft.IconButton(ft.icons.REPORT, tooltip="Warnings")
    adjust_icon_button = ft.IconButton(ft.icons.ENGINEERING, tooltip="Settings")
    left_scroll_icon_button = ft.IconButton(ft.icons.ARROW_LEFT, tooltip="Left scroll",
                                                on_click=clicked_left_scroll_icon_in_appbar)
    right_scroll_icon_button = ft.IconButton(ft.icons.ARROW_RIGHT, tooltip="Right scroll", on_click=clicked_right_scroll_icon_in_appbar)
    date_str_appbar = 'Today, ' + datetime.datetime.now().strftime("%a") + ", " + datetime.datetime.now().strftime(
            "%d") + " " + datetime.datetime.now().strftime("%b")

    date_appbar = ft.Text(value=(date_str_appbar), size=20, data=0)
    scroll_appbar = ft.Row([left_scroll_icon_button, date_appbar, right_scroll_icon_button])
    page.appbar = ft.AppBar(leading=ft.Icon(ft.icons.SAVINGS), leading_width=60,
                                title=ft.Text("Family expenses organizer"), bgcolor=ft.colors.SURFACE_VARIANT,
                                actions=[scroll_appbar, calendar_icon_button, wallet_icon_button, warning_icon_button,
                                         goals_icon_button, adjust_icon_button])

    page.update()

    #create_app_bar()"""