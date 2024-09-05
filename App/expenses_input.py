import flet as ft
import random
import datetime
import expenses_diary
import calendar
import view_sign_in_sign_up_selection
from view_sign_in import view_sign_in_layout_creation
from view_goals import view_goals_create_layout
from identification_data import get_user
import view_goals
import view_sign_up
import time
from fabrique_controls import date_picker_creation


def basic_menu_creation(page: ft.Page):
    def create_calendar_button() -> ft.Control:

        calendar_elev_button = ft.ElevatedButton(
            "Select date",
            icon=ft.icons.CALENDAR_MONTH,
            bgcolor=ft.colors.AMBER_200,
            on_click=lambda e: page.open(
                date_picker_creation(page)
            )
        )
        page.add(calendar_elev_button)
        return calendar_elev_button

    def cheer_up_after_asking_sum() -> ft.Control:
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
        return cheer_up_text

    def create_sum_money_text_field() -> ft.Control:
        def focus_change_sum_money_text_field(e):
            sum_money_text_field.value = ""
            sum_money_text_field.prefix_text = ""
            sum_money_text_field.suffix_text = ''
            sum_money_text_field.hint_text = "0.00"
            page.update()

        def change_sum_money_text_field(e):
            # sum_money_text_field.value = ""
            sum_money_text_field.prefix_text = "We have spent..."
            sum_money_text_field.suffix_text = 'rubbles'
            sum_money_text_field.hint_text = ''
            page.update()

        def submit_sum_money_text_field(e):
            sum_money_text_field.disabled = True
            cheer_up_after_asking_sum()
            page.update()

        sum_money_text_field = ft.TextField(label="Sum of money spent",
                                            width=400,
                                            hint_text="0.00",
                                            helper_text="The sum spent should be positive decimal number",
                                            value="Type in the sum of money spent",
                                            on_focus=focus_change_sum_money_text_field,
                                            on_change=change_sum_money_text_field,
                                            on_submit=submit_sum_money_text_field)

        return sum_money_text_field

    sum_money_text_field = create_sum_money_text_field()
    not_spent_icon = ft.Icon(name=ft.icons.MONETIZATION_ON, color=ft.colors.PINK, size=35)
    spent_icon = ft.Icon(name=ft.icons.MONEY_OFF, color=ft.colors.PINK, size=35)

    row_sum_input = ft.Row(controls=[not_spent_icon, sum_money_text_field, not_spent_icon])
    page.add(row_sum_input)
    page.views[-1].controls.append(row_sum_input)

    def create_add_button() -> ft.Control:
        def add_expense_to_db():
            expense_date = date_picker_creation(page).value
            print(expense_date, 'expense_date')
            if not expense_date:
                expense_date = datetime.datetime.today().strftime('%Y-%m-%d')
                print(expense_date, "transformed")
            else:
                expense_date = date_picker_creation(page).value.strftime('%Y-%m-%d')
            sum_expense = sum_money_text_field.value
            ####
            # e.control.value.strftime
            print(date_picker_creation(page).value)
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
            # row_sum_input.visible = False
            text_thanks_information_added = ft.Text("Thanks. Information about expenses added.")
            row_expense_added_information = ft.Row([spent_icon, text_thanks_information_added, spent_icon])
            # page.add(text_thanks_information_added )
            page.add(row_expense_added_information)
            # page.views[-1].controls.append(text_thanks_information_added)
            page.views[-1].controls.append(row_expense_added_information)
            page.update()

            add_expense_to_db()

        add_button = ft.ElevatedButton('ADD in EXPENSES DIARY', on_click=add_button_clicked)
        page.add(add_button)
        return add_button

    def create_text_before_slider() -> ft.Control:
        text_before_slider = ft.Text(
            "Please select the level of your certainty that you are go_ing to fulfill your spare goals",
            size=20, weight=ft.FontWeight.BOLD)
        page.add(text_before_slider)
        page.views[-1].controls.append(text_before_slider)
        page.update()
        return text_before_slider

    def create_slider_subjective_estimation_expense() -> ft.Control:
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
        return slider

    def create_main_category_selection() -> ft.Control:
        count = 0
        def on_click_sum_input(e):
            print(main_category_selection.value)

            nonlocal count
            print(count)
            if e.control.key is None:
                count += 1
                if count >= 1:
                    e.control.visible = False
            page.update()

        def click_category_entertainment(e):

            extra_category_entertainment = ft.Dropdown(label="Subcategory of Entertainment",
                                                       hint_text="Select subcategory of expenses for entertainment",
                                                       options=[ft.dropdown.Option("Cinema"),
                                                                ft.dropdown.Option("Netflix"),
                                                                ft.dropdown.Option("Videogames")
                                                                ],
                                                       on_click=on_click_sum_input)

            c = ft.Column(controls=[extra_category_entertainment])
            #page.add(ft.Column(controls=[extra_category_entertainment]))
            page.add(c)
            #page.views[-1].controls.append(extra_category_entertainment)
            page.views[-1].controls.append(c)

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

            page.update()

        main_category_selection = ft.Dropdown(label="Category of expenses", hint_text="Select category of expenses",
                                              options=[ft.dropdown.Option("Products"),
                                                       ft.dropdown.Option("Transportation",
                                                                          on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Taxes", on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Utilities", on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Household repairments",
                                                                          on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Insurances", on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Healthcare expenses above insurance",
                                                                          on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Cell phone bills",
                                                                          on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Dining out", on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Gifts", on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Travelling", on_click=on_click_sum_input),
                                                       ft.dropdown.Option("Entertainment",
                                                                          on_click=click_category_entertainment),
                                                       ft.dropdown.Option("Purchases",
                                                                          on_click=click_category_purchases),
                                                       ft.dropdown.Option("Other", on_click=on_click_sum_input)
                                                       ]
                                              )
        return main_category_selection

    calendar_elev_button = create_calendar_button()
    main_category_selection = create_main_category_selection()
    add_button = create_add_button()

    main_category_selection_col = ft.Column(controls=[main_category_selection])
    row_basic_menu = ft.Row([calendar_elev_button, main_category_selection_col, row_sum_input, add_button],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND)
    page.add(row_basic_menu)
    page.views[-1].controls.append(row_basic_menu)
    return row_basic_menu
