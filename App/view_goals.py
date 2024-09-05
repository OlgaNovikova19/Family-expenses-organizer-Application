import time
import flet as ft
import expenses_diary
import datetime
from dateutil.relativedelta import relativedelta

import identification_data
from identification_data import get_user
from fabrique_controls import create_sum_input_unit



def view_goals_create_layout(page: ft.Page):

    appbar_goals = ft.AppBar(leading=ft.Icon(ft.icons.SAVINGS), leading_width=60,
                             title=ft.Text("Family expenses organizer"), bgcolor=ft.colors.SURFACE_VARIANT,
                             actions=[ft.IconButton(icon=ft.icons.ARROW_RIGHT,
                                                    tooltip="Go to App without authentication",
                                                    on_click=lambda _: page.go('/authentication'))])
    text_goals_header = ft.Text("My spare goal", italic=True, weight=ft.FontWeight.BOLD,
                                font_family="Consolas", size=35)
    row_goals_header = ft.Row([text_goals_header], alignment=ft.MainAxisAlignment.CENTER)

    page.views[-1].controls.append(row_goals_header)


    def close_search_bar(e):
        text = f"{e.control.data}"
        print(text)
        search_bar_period_of_time.close_view(text)

    periods_of_time = ["1 week", "2 weeks", "3 weeks", "1 month", "2 months", "3 months", "6 months"]

    search_bar_period_of_time = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Select period of time",
        view_hint_text="Choose a period of time from the suggestions",
        width=500,
        controls=[
            ft.ListTile(title=ft.Text(f"{i}"), on_click=close_search_bar, data=f"{i}")
            for i in periods_of_time
        ]
    )

    column_search_bar = ft.Column([ft.OutlinedButton(
        "Open Search",
        on_click=lambda _: search_bar_period_of_time.open_view()), search_bar_period_of_time],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    sum_input_plus_textfield_min_row = create_sum_input_unit(page)
    text_field_input_sum = sum_input_plus_textfield_min_row.controls[1]
    page.views[-1].controls.append(sum_input_plus_textfield_min_row)
    page.update()

    def convert_to_date(time_str):
        if not time_str.split():
            page.open(
                ft.AlertDialog(title=ft.Text('For setting spare goal you should select period of time'), bgcolor=ft.colors.RED_100))
            column_search_bar.disabled=False
            page.update()
            return
        else:
            number, unit = time_str.split()
            number = int(number)

            if unit == "day" or unit == "days":
                delta = datetime.timedelta(days=number)
            elif unit == "week" or unit == "weeks":
                delta = datetime.timedelta(days=(number * 7))
            elif unit == "month" or unit == "months":
                delta = relativedelta(months=number)
            elif unit == "year" or unit == "years":
                delta = delta = relativedelta(years=number)  # Approximate years as 365 days
            else:
                raise ValueError(f"Unknown time unit: {unit}")

            future_date = datetime.date.today() + delta

            return future_date

    def save_sum_limit_button_clicked(e):
        if not search_bar_period_of_time.value or search_bar_period_of_time.value not in periods_of_time:
            page.open(
                ft.AlertDialog(title=ft.Text('For setting spare goal you should select period of time'),
                               bgcolor=ft.colors.RED_100))
            column_search_bar.disabled = False
            page.update()

        else:
            column_search_bar.disabled = True
            sum_input_plus_textfield_min_row.disabled = True

            check_response = expenses_diary.check_active_limits_for_user(get_user())
            if check_response:
                message_limit_already_exists = ft.Text(
                    "You have already another active limit installed. Do you want to update your active limit?",  italic=True, weight=ft.FontWeight.BOLD,
                                    font_family="Consolas", size=20)
                row_message = ft.Row([message_limit_already_exists], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START)
                page.views[-1].controls.append(row_message)
                page.update()
                questions_if_limit_already_exists()

            else:
                set_new_limit()

    def questions_if_limit_already_exists():
        def clicked_change_checkbox(e):
            if e.control == checkbox_1:
                checkbox_1.value = True
                checkbox_2.disabled = True
                if not check_limit_period_ended(get_user()):
                    # when replacing the last active limit with the new one if the end date of limit isn`t reached we won`t consider it for analysis.
                    # That`s why we use None for all parameters. history=1 is set automatically in make_limit_history_for_user function
                    expenses_diary.make_limit_history_for_user(None, None, get_user())
                page.views[-1].controls.append(
                    ft.Text("OK, your previous active limit is replaced with a new one."))
                page.update()
                set_new_limit()
                page.update()

            elif e.control == checkbox_2:
                checkbox_2.value = True
                checkbox_1.disabled = True
                page.update()
                page.views[-1].controls.append(
                    ft.Text("OK, setting of the new active limit is canceled. Your previous limit is active."))
                end_actions()
                page.update()



        checkbox_1 = ft.Checkbox(adaptive=True, label="Replace previous active limit with the new one", value=False, shape=ft.RoundedRectangleBorder(10), on_change=clicked_change_checkbox)
        checkbox_2 = ft.Checkbox(adaptive=True,
                                 label="Cancel setting of the new active limit. I want to use already existing limit",
                                 value=False,  shape=ft.RoundedRectangleBorder(10), on_change=clicked_change_checkbox)
        col_checkboxes_if_limit_already_exists = ft.Column([checkbox_1, checkbox_2])


        page.views[-1].controls.append(col_checkboxes_if_limit_already_exists)
        page.update()



   #########


    def ask_set_warning_sum():
        def clicked_yes_no_set_warning_sum(e):
            if e.control == checkbox_yes:
                checkbox_no.disabled = True
                input_warning_sum_row = create_sum_input_unit(page)
                text_field_input_warning_sum = input_warning_sum_row.controls[1]
                text_field_input_warning_sum.value = "Warning sum"
                text_field_input_warning_sum.label = "When your expenses reach this sum, you will see a warning"
                page.views[-1].controls.append(input_warning_sum_row)
                page.update()

                def confirmation_button_clicked(ev):
                    print(text_field_input_warning_sum.value, 'text_field_value')
                    print(text_field_input_sum.value, 'text_field_input_sum')
                    if text_field_input_warning_sum.value >= text_field_input_sum.value:
                        print('open condition')
                        actions_if_warning_sum_more_or_equal_than_limit(text_field_input_warning_sum)
                    else:
                        expenses_diary.set_warning_sum_in_active_limit_for_user(text_field_input_warning_sum.value, get_user())
                        page.views[-1].controls.append(ft.Text("The warning sum that will be used for warning creation is recorded"))
                        page.update()
                        #####here deleted about check
                    text_field_input_warning_sum.disabled = True
                    print(text_field_input_warning_sum.value, 'warning sum')
                    wsum = expenses_diary.get_warning_sum_from_active_limit_for_user(identification_data.identified_user)
                    print(wsum, 'wsum')
                page.views[-1].controls.append(ft.ElevatedButton("Confirmation", on_click=confirmation_button_clicked))
                page.update()
            else:
                end_actions()


        text_ask_warning_sum = ft.Text("Do you want to specify the sum left till the end of limit to create a warning?",  italic=True, weight=ft.FontWeight.BOLD,
                                font_family="Consolas", size=20)
        checkbox_yes = ft.Checkbox(adaptive=True, label="Yes", value=False,
                                 on_change=clicked_yes_no_set_warning_sum)
        checkbox_no = ft.Checkbox(adaptive=True,
                                 label="No, I want to see a warning during all the period of limit being enabled",
                                 value=False, on_change=clicked_yes_no_set_warning_sum)
        row_ask_warning_sum = ft.Row([checkbox_yes, checkbox_no])
        col_variants = ft.Column([text_ask_warning_sum, row_ask_warning_sum],
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER)


        page.views[-1].controls.append(col_variants)
        page.update()

    def actions_if_warning_sum_more_or_equal_than_limit(text_field_input_warning_sum):
        print('this')
        def clicked_yes_no_change_warning_sum(e):
            if e.control == checkbox_yes_change_warning_sum:
                checkbox_yes_change_warning_sum.value = True
                checkbox_no_change_warning_sum.disabled = True
                page.update()
                page.views[-1].controls.append(
                    ft.Text("OK, let`s change your warning sum. Type in the necessary sum once again."))
                text_field_input_warning_sum.disabled = False
                checkbox_yes_change_warning_sum.value = False
                checkbox_no_change_warning_sum.disabled = False
                page.close(dialog_modal)
                page.update()
                if text_field_input_warning_sum.disabled:
                    page.views[-1].controls.append(
                        ft.Text(f"OK, your warning sum is changed. Now it is {text_field_input_warning_sum.value}"))
                    page.update()

            elif e.control == checkbox_no_change_warning_sum:
                expenses_diary.set_warning_sum_in_active_limit_for_user(text_field_input_warning_sum.value, identified_user)
                checkbox_no_change_warning_sum.value = True
                checkbox_yes_change_warning_sum.disabled = True
                page.update()
                page.views[-1].controls.append(
                    ft.Text("OK, your warning sum won`t be changed and you will see the warning from this very moment"))
                text_field_input_warning_sum.disabled = True
                page.close(dialog_modal)
                show_warning_for_user_if_needed(get_user(), page)
                page.update()
                end_actions()

        checkbox_yes_change_warning_sum = ft.Checkbox(adaptive=True,
                                                          label="I want to change warning sum to make it lower than my set limit.",
                                                          value=False,
                                                          on_change=clicked_yes_no_change_warning_sum)
        checkbox_no_change_warning_sum = ft.Checkbox(adaptive=True,
                                                         label="No, I don`t want to change my warning sum. I want to see a warning right now",
                                                         value=False, on_change=clicked_yes_no_change_warning_sum)
        row_ask_change_warning_sum = ft.Row([checkbox_yes_change_warning_sum, checkbox_no_change_warning_sum])

        dialog_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("The warning sum you have set is more than the limit itself."),
                content=ft.Text("Do you want to change it? If not then the warning about reaching warning sum will "
                                                   "be created right now and will be shown from this time on"),
                actions=[row_ask_change_warning_sum],
                actions_alignment=ft.MainAxisAlignment.END
                )

        page.open(dialog_modal)
        page.update()

    ###########





    #######

    ##### text messages about success and lack of success
    """ def check_success_spare_goal():
            real_expenses_during_limit_time = expenses_diary.get_expenses_for_login_for_the_period(identified_user,
                                                                                               start_date_limit,
                                                                                               today_date)
            if limit_sum_for_user >= real_expenses_during_limit_time:
                success_spare_goal = f"Your spare goal {start_date_limit}-{end_date_limit} successfully reached!"
                results.append(success_spare_goal)
            else:
                unsuccessful_spare_goal = f"Your spare goal {start_date_limit}-{end_date_limit} wasn`t fulfilled. Difference is {limit_sum_for_user - real_expenses_during_limit_time}. Maybe next time better?!"
                results.append(unsuccessful_spare_goal)
            print(success_spare_goal, unsuccessful_spare_goal)"""
    #####

    def set_new_limit():
        today_date = datetime.datetime.today()
        limit_future_date = convert_to_date(search_bar_period_of_time.value)
        warning_sum = None
        print(text_field_input_sum.value, 'save')
        print(limit_future_date, 'save')
        print(search_bar_period_of_time.value)

        expenses_diary.add_active_limit(get_user(), today_date, limit_future_date, text_field_input_sum.value, warning_sum)
        #######
        create_warning(get_user())
        #####
        print(
            f"Your new spare goal was added. Your expenses limit for {search_bar_period_of_time.value} is set to {text_field_input_sum.value}")
        information_text = ft.Text(
            f"Your new spare goal was added. Your expenses limit for {search_bar_period_of_time.value} is set to {text_field_input_sum.value} rubbles")
        page.views[-1].controls.append(information_text)
        page.update()
        time.sleep(2)
        ask_set_warning_sum()
        page.update()

    img_obj_ = ft.Image(
        src=f"fragment_pic.png",
        fit=ft.ImageFit.COVER,
        width=90,
        height=90,
        expand=True
    )
    c = ft.Container(img_obj_, shape=ft.BoxShape.CIRCLE, border_radius=56, alignment=(ft.alignment.bottom_center))
    save_sum_limit_button = ft.ElevatedButton('ADD in EXPENSES DIARY', on_click=save_sum_limit_button_clicked)

    row_search_bar_and_input_sum = ft.Row([column_search_bar, sum_input_plus_textfield_min_row],
                                          alignment=ft.MainAxisAlignment.SPACE_AROUND, vertical_alignment=ft.CrossAxisAlignment.END)
    col_functional_goals_controls = ft.Column([row_search_bar_and_input_sum, save_sum_limit_button],
                                              horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def end_actions():
        def close_button_clicked(e):
            close_button.disabled = True
            cancel_button.disabled = True
            page.views.pop()
            page.update()

        def cancel_button_clicked(e):
            expenses_diary.delete_last_active_limit_for_user(identified_user)
            column_search_bar.disabled = False
            sum_input_plus_textfield_min_row.disabled = False
            page.views[-1].controls.clear()
            page.views[-1].controls.append(appbar_goals)
            page.views[-1].controls.append(row_goals_header)
            page.views[-1].controls.append(col_functional_goals_controls)
            page.update()

        close_button = ft.ElevatedButton('Close. Your set spare goal is applied', on_click=close_button_clicked)
        cancel_button = ft.ElevatedButton('Cancel your set goal and try once again', on_click=cancel_button_clicked)
        row_end_buttons = ft.Row([close_button, cancel_button], ft.MainAxisAlignment.SPACE_AROUND)
        page.views[-1].controls.append(row_end_buttons)
        page.update()

    controls_goals = [appbar_goals, row_goals_header, col_functional_goals_controls, c]


    return controls_goals

def check_limit_period_ended(identified_user):
    today = datetime.datetime.today()
    end_date_limit = expenses_diary.get_active_limit_end_date_for_user(identified_user)
    if today > datetime.datetime.strptime(end_date_limit, '%Y-%m-%d'):
        return True
    else:
        return False

def create_warning(identified_user):
    """
       1) get limit sum for the user who is signed in
       2) get warning sum for the user who is signed in. If warning sum is None than create a warning.
       3) count difference between limit sum and warning sum. This amount can be freely spent without generating warnings
       4) Compare today date and end date of the limit for this user. If today date is greater than end date of the limit, than delete the limit.
       5) Compare today date and end start of the limit for this user.
        If today date is greater than check all expenses made later than start date of the limit and earlier than today(there is opportunity to write expenses down for future dates!).
         Sum up these expenses.
       6) Count the difference between limit sum and sum already spent.
       7) Compare the 3) with 6). If 3) is greater, than no warning should be created.If 6) is equal or greater than create a warning.

    """
    print('here')
    warning_sum_for_user = expenses_diary.get_warning_sum_from_active_limit_for_user(identified_user)
    limit_sum_for_user = expenses_diary.get_active_limit_sum_for_user(identified_user)
    if limit_sum_for_user is None:
        return
    elif warning_sum_for_user is None:
        sum_to_spend_without_warnings=limit_sum_for_user
        #create a warning
    else:
        sum_to_spend_without_warnings = limit_sum_for_user - warning_sum_for_user
    print(warning_sum_for_user, '!')
    print(limit_sum_for_user, "!!")
    start_date_limit = expenses_diary.get_active_limit_start_date_for_user(identified_user)
    end_date_limit = expenses_diary.get_active_limit_end_date_for_user(identified_user)
    today_date = datetime.datetime.today()

    if check_limit_period_ended(identified_user):
        # make limit history (history assign 1, count general_success_rate and general_subjective_success_rate fot this limit period
        real_expenses_during_limit_time = expenses_diary.get_expenses_for_login_for_the_period(identified_user,
                                                                                                   start_date_limit,
                                                                                                   today_date)
        #diff_limit_all_real_expenses can be positive (positive general spare balance if positive when summed up with other values in this column) or negative (negative general spare balance).
        # General spare balance helps to support motivation for sparing money beyond time when limits and set,
        # it`s a link that connects periods with active spare goals and gives insights about general tendention
        diff_limit_all_real_expenses = limit_sum_for_user - real_expenses_during_limit_time
        general_subjective_success = expenses_diary.calculate_mean_subjective_success_rate(identified_user, start_date_limit, end_date_limit)
        expenses_diary.make_limit_history_for_user(diff_limit_all_real_expenses, general_subjective_success, identified_user)

    else:
        expenses_in_the_period = expenses_diary.get_sum_expenses_for_login_for_the_period(identified_user, start_date_limit, today_date)


        if sum_to_spend_without_warnings > expenses_in_the_period :
            return
        else:
            warning = f"WARNING! You approach your spending limit. The end date of your limit {end_date_limit} and you can spend {sum_to_spend_without_warnings - expenses_in_the_period} rubbles"
            print(warning)
            return warning

def show_warning_for_user_if_needed(identified_user_login, page:ft.Page):
    warning_for_user = create_warning(identified_user_login)
    if warning_for_user:
        page.open(ft.AlertDialog(title=ft.Text(f'{warning_for_user}'), bgcolor=ft.colors.RED_100))
    page.update()

