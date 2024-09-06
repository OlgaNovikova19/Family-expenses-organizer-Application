import random
import datetime
from collections import deque
import flet as ft
import expenses_diary
import calendar
import view_sign_in_sign_up_selection
from view_sign_in import view_sign_in_layout_creation
from view_goals import view_goals_create_layout
from identification_data import get_user
import view_goals
import view_sign_up
import app_bar
import time
from fabrique_controls import date_picker_creation
from expenses_input import basic_menu_creation


def main(page: ft.Page):
    page.adaptive = True
    page.padding = 30
    page.title = "Family expenses organizer"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed="green")
    page.scroll = ft.ScrollMode.ALWAYS

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

    def choose_date(e):
        str_selected_date = e.control.value.strftime('%Y-%m-%d')
        page.add(ft.Text(f"Date selected: {str_selected_date}"))
        page.add(ft.TextButton(f"{str_selected_date}"))


    calendar_icon_button = ft.IconButton(ft.icons.CALENDAR_MONTH, tooltip="Calendar", on_click=lambda e: page.open(
        date_picker_creation(page)))

    def show_warning(e):
        view_goals.show_warning_for_user_if_needed(get_user(), page)

    def show_sum_left_before_warning_sum(e):
        name_user = get_user()
        information = ''
        if name_user is None:
            name_user = 'guest'
            information = 'please sign in to use this function.'
        if expenses_diary.check_active_limits_for_user(get_user()):
            sum_left_before_warning_sum = expenses_diary.get_sum_left_to_spend_without_warning_for_user(get_user())
            if sum_left_before_warning_sum is None:
                information = 'you have set no warning sum.'
        page.open(ft.AlertDialog(title=ft.Text(f'Dear {name_user}, {information}'), bgcolor=ft.colors.GREEN_200))

    goals_icon_button = ft.IconButton(ft.icons.ADJUST, tooltip="Goals", on_click=open_view_goals, data=0)
    wallet_icon_button = ft.IconButton(ft.icons.HOME_REPAIR_SERVICE, tooltip="Sum you can still safely spend", on_click=show_sum_left_before_warning_sum)
    warning_icon_button = ft.IconButton(ft.icons.REPORT, tooltip="Warnings", on_click=show_warning)
    adjust_icon_button = ft.IconButton(ft.icons.ENGINEERING, tooltip="Settings")
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

    #create_app_bar()

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        page.views.append(
            ft.View(route='/', controls=view_sign_in_sign_up_selection.view_sign_in_sign_up(page))
        )

        if page.route == "/authentication":
            '''page.views.append(
                ft.View(route='/authentication',
                        controls=[ft.AppBar(leading=ft.Icon(ft.icons.SAVINGS), leading_width=60,
                            title=ft.Text("Family expenses organizer"), bgcolor=ft.colors.SURFACE_VARIANT,
                            actions=[ft.IconButton(icon=ft.icons.ARROW_LEFT, tooltip="Go to Sign In/Sign Up",on_click=lambda _: page.go('/')),
                                    ft.IconButton(icon=ft.icons.ARROW_RIGHT, tooltip="Go to App without authentication",on_click=lambda _: page.go('/app'))]),
                                ft.Text("Type in your authentication data"),
                                ft.TextField("Name")
                                ]))'''

            page.views.append(
                ft.View(route='/authentication',
                        controls=view_sign_in_layout_creation(page)))

        elif page.route == "/app":
            page.views.append(
                ft.View(route='/app', controls=[page.appbar, st,
                    #main_category_selection_col,
                                    basic_menu_creation(page),
                    ft.BottomAppBar(content=ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.ARROW_LEFT, tooltip="Back to Authentication", on_click=lambda _: page.go('/')),
                ft.IconButton(icon=ft.icons.ARROW_RIGHT, tooltip="Go to ThirdPage",on_click=lambda _: page.go('/third_page'))
            ], alignment=ft.MainAxisAlignment.CENTER
                    ))
                        ]))

        elif page.route == "/third_page":
            page.views.append(
                ft.View(
                    route="/third_page",
                    controls=[
                        ft.AppBar(title=ft.Text("Third Page"), bgcolor=ft.colors.AMBER_900),
                        ft.Text("This is the third page"),
                        ft.ElevatedButton("Back to App", on_click=lambda _: page.go('/app')),
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
    print(page.views, "VIEWS")

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
    regulator = 1

    start_calendar = datetime.date.today() - datetime.timedelta(days=366)
    end_calendar = datetime.date.today() + datetime.timedelta(days=366)

    def click_date_button(e):
        clicked_button = e.control
        upper_text = clicked_button.content.controls[0].value
        lower_text = clicked_button.content.controls[1].value
        #print(f"Clicked Date: {upper_text} {lower_text} 2024")

    def generate_dates_around(center_date):
        next_date = center_date
        print(next_date, 'next_date')
        for i in range(-3, 4):
            next_date = center_date + datetime.timedelta(days=i)
            print(i, next_date)
            yield next_date
            dates_deque.append(next_date)
            print(dates_deque)

    def func_reverse_scroll_dates():
        print('rev')
        #shifted_backwards_center_date = dates_deque[0] - datetime.timedelta(days=1)
        #dates_deque.appendleft(shifted_backwards_center_date)
        #print(dates_deque, 'backw')
        #generate_buttons()

    def func_forward_scroll_dates():
        print('forw')
        #nonlocal center_date
        #shifted_forward_center_date = dates_deque[-1] + datetime.timedelta(days=1)
        #center_date = dates_deque[-1] + datetime.timedelta(days=4)
        #generate_dates_around(center_date)
        #dates_deque.append(shifted_forward_center_date)
        #print(dates_deque, 'forward')
        #generate_buttons()

    def check_on_scroll_direction(e: ft.OnScrollEvent):
        nonlocal regulator
        print(e.scroll_delta, 'delta')
        if e.scroll_delta:
            if e.scroll_delta > 0:
                print(e.scroll_delta, 'positive')
                regulator = 1

            elif e.scroll_delta < 0:
                print(e.scroll_delta, 'negative')
                regulator = -1

    movable_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=50, wrap=False, scroll=ft.ScrollMode.ALWAYS,
                         on_scroll=check_on_scroll_direction)

    def generate_buttons():
        nonlocal center_date
        print(center_date, 'center_date')
        while start_calendar < center_date < end_calendar:
            for date in generate_dates_around(center_date):
                print(date, 'date')
                text_upper = ft.Text(value=date.strftime("%B"), size=20)
                #print('text_upper', text_upper)
                text_lower = ft.Text(value=f"{date.day}", size=15, text_align=ft.TextAlign.CENTER)
                #print('text_lower', text_lower
                center_date += datetime.timedelta(days=regulator)

                date_button = ft.ElevatedButton(
                    content=ft.Column([text_upper,
                                       text_lower,
                                       ],
                                      alignment=ft.MainAxisAlignment.CENTER,
                                      spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    on_click=click_date_button
                )

                date_buttons_list.append(date_button)
                movable_row.controls.append(date_button)
            page.update()

    generate_dates_around(center_date)
    generate_buttons()

    days_movable_row = ft.Container(movable_row,
                                    bgcolor=ft.colors.GREEN_300,
                                    margin=40, padding=5, blend_mode=ft.BlendMode.MODULATE,
                                    border=ft.border.all(width=1, color=ft.colors.GREEN_200),
                                    border_radius=ft.border_radius.all(150), alignment=ft.alignment.top_left,
                                    width=1100, height=80)

    st = ft.Stack([img, days_movable_row], expand=True)
    page.add(st)

    #days_movable_row_creation()

    ####choose_date func
"""
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

    #def create_calendar():
    print(calendar.month(2024, 8))


    def cheer_up_before_asking_sum():
        text1 = "Expenses are an essential part of life, chin up!"
        text2 = "All work and no play makes Jack a dull boy...you need sometimes to spend money not only to spare, right?"
        text3 = "It`s impossible only to spare money"
        text4 = "Well, what`s done, is done"
        text_list = [text1, text2, text3, text4]
        chosen_random_cheer_up_message = random.choice(text_list)

        cheer_up_text = ft.Text(chosen_random_cheer_up_message, italic=True, weight=ft.FontWeight.BOLD,
                                    font_family="Consolas", size=20)

        page.views[-1].controls.append(cheer_up_text)
        page.update()


    def on_click_sum_input(e):
        cheer_up_before_asking_sum()

        def focus_change_sum_money_text_field(e):
            sum_money_text_field.value = ""
            sum_money_text_field.prefix_text = ""
            sum_money_text_field.suffix_text = ''
            sum_money_text_field.hint_text = "0.00"
            page.update()

        def change_sum_money_text_field(e):
            #sum_money_text_field.value = ""
            sum_money_text_field.prefix_text = "We have spent..."
            sum_money_text_field.suffix_text = 'rubbles'
            sum_money_text_field.hint_text = ''
            page.update()

        def submit_sum_money_text_field(e):
            sum_money_text_field.disabled = True
            page.update()

        sum_money_text_field = ft.TextField(label="Sum of money spent",
                                            width=400,
                                            hint_text="0.00",
                                            helper_text="The sum spent should be positive decimal number",
                                            value="Type in the sum of money spent",
                                            on_focus=focus_change_sum_money_text_field,
                                            on_change=change_sum_money_text_field,
                                            on_submit=submit_sum_money_text_field)
        not_spent_icon = ft.Icon(name=ft.icons.MONETIZATION_ON, color=ft.colors.PINK, size=35)
        spent_icon = ft.Icon(name=ft.icons.MONEY_OFF, color=ft.colors.PINK, size=35)

        row_sum_input = ft.Row(controls=[not_spent_icon, sum_money_text_field, not_spent_icon])
        page.add(row_sum_input)
        page.views[-1].controls.append(row_sum_input)


        def add_expense_to_db():
            expense_date = pick_date_in_calendar.value
            print(expense_date, 'expense_date')
            if not expense_date:
                expense_date = datetime.datetime.today().strftime('%Y-%m-%d')
                print(expense_date, "transformed")
            else:
                expense_date = pick_date_in_calendar.value.strftime('%Y-%m-%d')
            sum_expense = sum_money_text_field.value
            ####
            #e.control.value.strftime
            print(pick_date_in_calendar.value)
            ###
            expense_category = main_category_selection.value
            expense_subcategory = None
            subjective_success_rate = None

            identified_user = get_user()
            expenses_diary.add_expense(identified_user, expense_date, sum_expense, expense_category,
                                       expense_subcategory, subjective_success_rate)
            view_goals.show_warning_for_user_if_needed(get_user(), page)



        def add_button_clicked(e):
            nonlocal row_sum_input
            row_sum_input.clean()
            row_sum_input = ft.Row(controls=[spent_icon, sum_money_text_field, spent_icon])
            page.add(row_sum_input)
            page.views[-1].controls.append(row_sum_input)
            row_sum_input.visible = False
            text_thanks_information_added = ft.Text("Thanks. Information about expenses added.")
            row_expense_added_information = ft.Row([spent_icon, text_thanks_information_added, spent_icon])
            #page.add(text_thanks_information_added )
            page.add(row_expense_added_information)
            #page.views[-1].controls.append(text_thanks_information_added)
            page.views[-1].controls.append(row_expense_added_information)
            page.update()

            add_expense_to_db()

            text_before_slider = ft.Text("Please select the level of your certainty that you are go_ing to fulfill your spare goals",
                                     size=20, weight=ft.FontWeight.BOLD)
            page.add(text_before_slider)
            page.views[-1].controls.append(text_before_slider)


        add_button = ft.ElevatedButton('ADD in EXPENSES DIARY', on_click=add_button_clicked)

        page.add(add_button)
                #if sum_money_text_field.value is not float and float(sum_money_text_field.value) >= 0:
                #page.add(ft.Column(controls=[ft.Text()]))

        page.views[-1].controls.append(add_button)
        slider = ft.RangeSlider(min=0,
                                max=100,
                                start_value=0,
                                divisions=100,
                                end_value=20,
                                inactive_color=ft.colors.GREEN_300,
                                active_color=ft.colors.GREEN_700,
                                overlay_color=ft.colors.GREEN_100,
                                label="{value}%",
                                )
        page.add(slider)
        page.views[-1].controls.append(slider)
        page.update()
        return add_button

    def click_category_expenses(e):
        extra_category_entertainment = ft.Dropdown(label="Subcategory of Entertainment",
                                                       hint_text="Select subcategory of expenses for entertainment",
                                                       options=[ft.dropdown.Option("Cinema"),
                                                                ft.dropdown.Option("Netflix"),
                                                                ft.dropdown.Option("Videogames")
                                                                ],
                                                       on_click=on_click_sum_input
                                                       )
        page.add(ft.Column(controls=[extra_category_entertainment]))
        page.views[-1].controls.append(extra_category_entertainment)
        page.update()

    def click_category_purchases(e):
        extra_category_purchases = ft.Dropdown(label="Subcategory of Purchases",
                                                   hint_text="Select subcategory of expenses for purchases",
                                                   options=[ft.dropdown.Option("Clothes"),
                                                            ft.dropdown.Option("Shoes"),
                                                            ft.dropdown.Option("Books, magazines"),
                                                            ft.dropdown.Option("Home items"),
                                                            ft.dropdown.Option("Other")
                                                            ],
                                                   on_click=on_click_sum_input
                                                   )
        page.add(ft.Column(controls=[extra_category_purchases]))
        page.views[-1].controls.append(extra_category_purchases)



            #cheer_up_text_column, row_sum_input,
        #add_button, slider

    main_category_selection = ft.Dropdown(label="Category of expenses", hint_text="Select category of expenses",
                                              options=[ft.dropdown.Option("Products"),
                                                       ft.dropdown.Option("Transportation", on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Taxes", on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Utilities", on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Household repairments",
                                                                          on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Insurances", on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Healthcare expenses above insurance",
                                                                          on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Cell phone bills", on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Dining out", on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Gifts", on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Travelling", on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Entertainment",
                                                                          on_click=click_category_expenses),
                                                       ft.dropdown.Option("Purchases", on_click=click_category_purchases),
                                                       ft.dropdown.Option("Other", on_click=on_click_sum_input)
                                                       ]
                                              )


    main_category_selection_col = ft.Column(controls=[main_category_selection])
    r = ft.Row([calendar_elev_button, main_category_selection_col, ft.ElevatedButton("addd")])
    #page.add(main_category_selection_col)
    page.add(r)
    #page.views[-1].controls.append(r)
    page.update()"""


ft.app(target=main, assets_dir="assets")
