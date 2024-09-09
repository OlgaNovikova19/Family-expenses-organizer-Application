import flet as ft
import random
import datetime
import expenses_diary
import calendar
import view_sign_in_sign_up_selection
from view_sign_in import view_sign_in_layout_creation
from view_goals import view_goals_create_layout
from identification_data import get_user, set_chosen_date, get_chosen_date
import view_goals
import view_sign_up
import time
from fabrique_controls import create_error_message, create_calendar_button



def basic_menu_creation(page: ft.Page):

    def cheer_up_after_asking_sum() -> ft.Control:
        text1 = "Expenses are an essential part of life, chin up!"
        text2 = "All work and no play makes Jack a dull boy...you need sometimes to spend money not only to spare, right?"
        text3 = "It`s impossible only to spare money"
        text4 = "Well, what`s done, is done"
        text_list = [text1, text2, text3, text4]
        chosen_random_cheer_up_message = random.choice(text_list)

        cheer_up_text = ft.Text(chosen_random_cheer_up_message, italic=True, weight=ft.FontWeight.BOLD,
                                font_family="Consolas", size=20)
        cheer_up_text_row=ft.Row([cheer_up_text], alignment=ft.MainAxisAlignment.CENTER)

        page.views[-1].controls.append(cheer_up_text_row)
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
            add_button.disabled = False
            page.update()

        def submit_sum_money_text_field(e):
            sum_money_text_field.disabled = True
            add_button.disabled = False
            #cheer_up_after_asking_sum()
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
            expense_date = get_chosen_date()

            if not expense_date:
                expense_date = datetime.datetime.today().strftime('%Y-%m-%d')
                print(expense_date, "exp")



            sum_expense = sum_money_text_field.value
            ####
            # e.control.value.strftime

            ###
            expense_category = main_category_selection.value
            expense_subcategory = None
            subjective_success_rate = None

            identified_user = get_user()
            expenses_diary.add_expense(identified_user, expense_date, sum_expense, expense_category,
                                       expense_subcategory, subjective_success_rate)
            view_goals.show_warning_for_user_if_needed(get_user(), page)
            history_limit_sum = expenses_diary.get_limit_sum_for_date_for_user_if_history(identified_user, expense_date)
            print(history_limit_sum, "history_limit_sum")
            if history_limit_sum is not None:
                diff_limit_expense = history_limit_sum - float(sum_expense)
                expenses_diary.update_balance_for_user(diff_limit_expense, identified_user)
                print(diff_limit_expense, 'diff_limit_expense')

        def add_button_clicked(e):
            row_sum_input.clean()
            page.update()
            row_sum_input.controls = [spent_icon, sum_money_text_field, spent_icon]
            page.update()

            row_text_thanks_information_added = ft.Row([ft.Text("Thanks. Information about expenses added.")], alignment=ft.MainAxisAlignment.CENTER)

            page.views[-1].controls.append(row_text_thanks_information_added)

            print(row_text_thanks_information_added)
            print(page.views[-1].controls)
            page.update()
            calendar_elev_button.visible = False
            row_sum_input.visible = False
            main_category_selection.visible = False
            add_button.visible = False
            page.update()
            cheer_up_text = cheer_up_after_asking_sum()
            page.update()
            time.sleep(4)
            row_text_thanks_information_added.visible=False
            cheer_up_text.visible=False

            add_expense_to_db()
            view_goals.create_warning(get_user())

            def yes_button_clicked(e):
                row_text1_information.visible = False
                row_text2_question.visible = False
                page.update()
                create_text_before_slider()
                create_slider_subjective_estimation_expense()
                page.update()


            def no_button_clicked(e):
                row_text1_information.visible = False
                row_text2_question.visible = False
                page.update()
                page.open(ft.AlertDialog(title=ft.Text("More expenses?..Here we go!", text_align=ft.TextAlign.CENTER),
                                         bgcolor=ft.colors.GREEN_200))
                time.sleep(3)
                page.go('/')
                page.go('/app')
                page.update()

            yes_button = ft.ElevatedButton("Yes", bgcolor=ft.colors.AMBER_200, on_click=yes_button_clicked)
            no_button = ft.ElevatedButton("No", bgcolor=ft.colors.AMBER_200, on_click=no_button_clicked)
            row_text1_information = ft.Row([ft.Text(
                "To get further valuable insights about your habitual spending patterns leave your subjective estimation of your recent expense.", italic=True, size=20, weight=ft.FontWeight.W_400)],
                alignment=ft.MainAxisAlignment.CENTER)
            row_text2_question = ft.Row([yes_button, ft.Text("Would you like to participate?", italic=True, size=20, weight=ft.FontWeight.BOLD), no_button], alignment=ft.MainAxisAlignment.CENTER)

            page.views[-1].controls.append(row_text1_information)
            page.views[-1].controls.append(row_text2_question)
            page.update()



        add_button = ft.ElevatedButton('ADD in EXPENSES DIARY', on_click=add_button_clicked, disabled=True)
        page.add(add_button)
        return add_button

    def create_text_before_slider() -> ft.Control:
        instruct_before_slider = ft.Text(
            "Please select the level of your certainty whether you are going to fulfill your spare goals", italic=True,
            size=20, weight=ft.FontWeight.W_500)
        row_instruct_before_slider = ft.Row([instruct_before_slider], alignment=ft.MainAxisAlignment.CENTER)
        page.views[-1].controls.append(row_instruct_before_slider)
        page.update()
        return row_instruct_before_slider

    row_instruct_before_slider = create_text_before_slider()

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
        def save_button_clicked(e):
            print(slider.end_value)
            print(type(slider.end_value))
            if get_user() is None:
                page.open(
                    ft.AlertDialog(title=ft.Text('Dear guest, please, sign in to save results'), bgcolor=ft.colors.RED_100))
                page.update()
            else:
                print(get_user())
                expenses_diary.set_subjective_success_rate_for_user(slider.end_value, get_user())
                if expenses_diary.get_subjective_success_rate_for_user(get_user()) is None or expenses_diary.get_subjective_success_rate_for_user(get_user()) != slider.end_value:
                    create_error_message(page)
                else:
                    row_estimation_saved = ft.Row([ft.Text("Your estimation is added", italic=True, size=20, weight=ft.FontWeight.W_500)],
                                                  alignment=ft.MainAxisAlignment.CENTER)
                    page.views[-1].controls.append(row_estimation_saved)
                    save_slider_value_button.disabled = True
                    page.update()
                    time.sleep(5)
                    """print('route')
                    page.go('/')
                    page.go('/app')"""
                    page.update()
                    page.update()
                    page.open(ft.AlertDialog(title=ft.Text("More expenses?..Here we go!", text_align=ft.TextAlign.CENTER),
                                             bgcolor=ft.colors.GREEN_200))
                    time.sleep(3)
                    page.go('/')
                    page.go('/app')
                    page.update()

        save_slider_value_button = ft.ElevatedButton("SAVE", bgcolor=ft.colors.AMBER_200, on_click=save_button_clicked)
        row_save_slider_value_button = ft.Row([save_slider_value_button], alignment = ft.MainAxisAlignment.CENTER)
        page.views[-1].controls.append(slider)
        page.update()
        page.views[-1].controls.append(row_save_slider_value_button)
        page.update()
        return slider


    def if_more_expenses_input():
       """
        text.visible = False
        slider_control.visible = False
        page.update()
        create_calendar_button()
        create_sum_money_text_field()
        create_add_button()
        page.update()"""


    def create_main_category_selection() -> ft.Control:
        count_click_extra_category = 0
        a = None
        def on_click_sum_input(e):
            if e.control.key is not None and a is not None:
                a.disabled = True
                print(a.disabled)
                print(a.value,'a.value a not None, e.control.key not None')
                print(e.control.key, 'e.control.key not None, a not None')
            print(e.control.key, 'e.control.key')
            print(a, 'a')
            page.update()



        def click_category_entertainment(e):
            nonlocal count_click_extra_category

            extra_category_entertainment = ft.Dropdown(label="Subcategory of Entertainment",
                                                       hint_text="Select subcategory of expenses for entertainment",
                                                       options=[ft.dropdown.Option("Cinema"),
                                                                ft.dropdown.Option("Netflix"),
                                                                ft.dropdown.Option("Videogames")
                                                                ],

                                                  on_click=on_click_sum_input)
            nonlocal a
            a = extra_category_entertainment
            if count_click_extra_category >=1:
                page.views[-1].controls.pop()
                count_click_extra_category = 0


            #c = ft.Column(controls=[extra_category_entertainment])
            #page.add(ft.Column(controls=[extra_category_entertainment]))
            current_subcategory_dropdown = extra_category_entertainment
            #page.add(c)
            #page.views[-1].controls.append(extra_category_entertainment)
            page.views[-1].controls.append(extra_category_entertainment)
            count_click_extra_category += 1
            page.update()

        def click_category_purchases(e):
            nonlocal count_click_extra_category
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
            if count_click_extra_category >=1:
                page.views[-1].controls.pop()
                count_click_extra_category = 0
                page.update()
                return


            #page.add(ft.Column(controls=[extra_category_purchases]))
            page.views[-1].controls.append(extra_category_purchases)
            count_click_extra_category += 1
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


    main_category_selection = create_main_category_selection()
    add_button = create_add_button()
    calendar_elev_button = create_calendar_button(page)

    main_category_selection_col = ft.Column(controls=[main_category_selection])
    row_basic_menu = ft.Row([calendar_elev_button, main_category_selection_col, row_sum_input, add_button],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND)

    page.views[-1].controls.append(row_basic_menu)
    page.update()
    return row_basic_menu
