import time
import flet as ft
import expenses_diary
import datetime
from dateutil.relativedelta import relativedelta
from identification_data import get_user, get_chosen_date, set_chosen_date
from fabrique_controls import create_sum_input_unit, create_calendar_button, create_individual_error_message
import logging


def view_goals_create_layout(page: ft.Page):
    def route_to_main_page_from_goals(e):
        page.go('/')
        page.go('/app')
        page.update()

    appbar_goals = ft.AppBar(leading=ft.Icon(ft.icons.SAVINGS), leading_width=60,
                             title=ft.Text("Family expenses organizer"), bgcolor=ft.colors.SURFACE_VARIANT,
                             actions=[ft.IconButton(icon=ft.icons.ARROW_LEFT,
                                                    tooltip="Go to MAIN PAGE",
                                                    on_click=route_to_main_page_from_goals),
                                 ft.IconButton(icon=ft.icons.ARROW_RIGHT,
                                                    tooltip="Go to SIGN IN",
                                                    on_click=lambda _: page.go('/authentication'))])
    text_goals_header = ft.Text("My spare goal", italic=True, weight=ft.FontWeight.BOLD,
                                font_family="Consolas", size=35)
    row_goals_header = ft.Row([text_goals_header], alignment=ft.MainAxisAlignment.CENTER)

    page.views[-1].controls.append(row_goals_header)

    def close_search_bar(e):
        text = f"{e.control.data}"
        search_bar_period_of_time.close_view(text)

    periods_of_time = ["1 week", "2 weeks", "3 weeks", "1 month", "2 months", "3 months", "6 months"]

    search_bar_period_of_time = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Select period of time",
        view_hint_text="Choose a period of time from the suggestions",
        width=400,
        controls=[
            ft.ListTile(title=ft.Text(f"{i}"), on_click=close_search_bar, data=f"{i}")
            for i in periods_of_time
        ]
    )

    column_search_bar = ft.Column([ft.OutlinedButton(
        "Open Search",
        on_click=lambda _: search_bar_period_of_time.open_view()), search_bar_period_of_time],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    calendar_button_goals = create_calendar_button(page)
    calendar_button_goals.width = 400

    sum_input_plus_textfield_min_row = create_sum_input_unit(page)
    text_field_input_sum = sum_input_plus_textfield_min_row.controls[1]
    text_field_input_sum.width = 250
    page.views[-1].controls.append(sum_input_plus_textfield_min_row)
    page.update()

    def convert_to_date(time_str):
        logging.info('function called: convert_to_date(time_str)')
        if not time_str.split():
            page.open(
                ft.AlertDialog(title=ft.Text('For setting spare goal you should select period of time'),
                               bgcolor=ft.colors.RED_100))
            column_search_bar.disabled = False
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

        date_selected_as_start_of_limit = datetime.datetime.strptime(get_chosen_date(), '%Y-%m-%d')

        if date_selected_as_start_of_limit is None:
            date_selected_as_start_of_limit = datetime.date.today()
        future_date = date_selected_as_start_of_limit + delta
        return future_date

    def save_sum_limit_button_clicked(e):
        logging.info('function called: save_sum_limit_button_clicked(e)')
        if not search_bar_period_of_time.value or search_bar_period_of_time.value not in periods_of_time:
            page.open(
                ft.AlertDialog(title=ft.Text('For setting spare goal you should select period of time'),
                               bgcolor=ft.colors.RED_100))
            column_search_bar.disabled = False
            page.update()

        else:
            column_search_bar.disabled = True
            sum_input_plus_textfield_min_row.disabled = True
            set_new_limit()

    def questions_if_limit_already_exists():
        logging.info('function called: questions_if_limit_already_exists()')
        def clicked_change_checkbox(e):
            logging.info('function called: clicked_change_checkbox(e)')
            logging.info(f'e.control: {e.control}')
            if e.control == checkbox_1:
                checkbox_1.value = True
                checkbox_2.disabled = True
                logging.info(f'function as check condition called: check_limit_period_ended(get_user())')
                logging.info(f'get_user(): {get_user()}')
                if not check_limit_period_ended(get_user()):
                    # when replacing the last active limit with the new one if the end date of limit isn`t reached we won`t consider it for analysis.
                    # That`s why we use None for all parameters. history=1 is set automatically in make_limit_history_for_user function
                    expenses_diary.make_limit_history_for_user(get_user(), None, None, None, None)
                    logging.info(f'function called expenses_diary.make_limit_history_for_user(get_user(), None, None, None, None)')
                else:
                    chosen_start_day_limit_ = get_chosen_date()
                    logging.info(f'chosen_start_day_limit_: {chosen_start_day_limit_}')
                    limit_end_date_ = convert_to_date(search_bar_period_of_time.value)
                    limit_end_date_ = limit_end_date_.strftime('%Y-%m-%d')
                    logging.info(f'limit_end_date_ after formatting %Y-%m-%d: {limit_end_date_}')
                    exp_dates = expenses_diary.get_expenses_for_login_for_the_period(get_user(), chosen_start_day_limit_, limit_end_date_)
                    logging.info(f'exp_dates: {exp_dates}')
                    if exp_dates is not None:
                        for date in exp_dates:
                            for i in date:
                                expenses_diary.update_not_active_limit_for_user_when_expense(get_user(), i)
                                logging.info('function called expenses_diary.update_not_active_limit_for_user_when_expense(get_user(), i)')

                    else:
                        expenses_diary.make_limit_history_for_user(get_user(), 0, 0, 0, 0)
                        logging.info(
                            'function called expenses_diary.make_limit_history_for_user(get_user(), 0, 0, 0, 0)')

                page.views[-1].controls.append(
                    ft.Text("OK, your previous active limit is replaced with a new one."))
                logging.info('output: "OK, your previous active limit is replaced with a new one."')
                page.update()
                set_new_limit()
                logging.info(
                    'function called: set_new_limit()')
                logging.info(
                    'function called: end_actions()')
                page.update()

            elif e.control == checkbox_2:
                checkbox_2.value = True
                checkbox_1.disabled = True
                page.update()
                page.views[-1].controls.append(
                    ft.Text("OK, setting of the new active limit is canceled. Your previous limit is active."))
                logging.info('output: "OK, setting of the new active limit is canceled. Your previous limit is active."')
                end_actions_variant_cancel_setting_new_limit()
                logging.info(f'function called: end_actions_variant_cancel_setting_new_limit()')
                page.update()

        checkbox_1 = ft.Checkbox(adaptive=True, label="Replace previous active limit with the new one", value=False,
                                 shape=ft.RoundedRectangleBorder(10), on_change=clicked_change_checkbox)
        checkbox_2 = ft.Checkbox(adaptive=True,
                                 label="Cancel setting of the new active limit. I want to use already existing limit",
                                 value=False, shape=ft.RoundedRectangleBorder(10), on_change=clicked_change_checkbox)
        col_checkboxes_if_limit_already_exists = ft.Column([checkbox_1, checkbox_2])

        page.views[-1].controls.append(col_checkboxes_if_limit_already_exists)
        page.update()



    def ask_set_warning_sum():
        logging.info('function called ask_set_warning_sum()')
        def clicked_yes_no_set_warning_sum(e):
            logging.info('function called clicked_yes_no_set_warning_sum(e)')
            logging.info(f'e.control: {e.control}')
            if e.control == checkbox_yes:
                checkbox_no.disabled = True
                checkbox_yes.disabled = True
                input_warning_sum_row = create_sum_input_unit(page)
                text_field_input_warning_sum = input_warning_sum_row.controls[1]
                text_field_input_warning_sum.value = "Warning sum"
                text_field_input_warning_sum.label = "When your expenses reach this sum, you will see a warning"
                page.views[-1].controls.append(input_warning_sum_row)
                page.update()

                def confirmation_button_clicked(ev):
                    logging.info('function called confirmation_button_clicked(ev)')
                    logging.info(f'text_field_input_warning_sum.value: {text_field_input_warning_sum.value}')
                    logging.info(f"text_field_input_sum.value: {text_field_input_sum.value}")
                    if text_field_input_warning_sum.value >= text_field_input_sum.value:
                        actions_if_warning_sum_more_or_equal_than_limit(text_field_input_warning_sum)
                        logging.info('function called: actions_if_warning_sum_more_or_equal_than_limit(text_field_input_warning_sum)')
                    else:
                        expenses_diary.set_warning_sum_in_active_limit_for_user(text_field_input_warning_sum.value,
                                                                                get_user())
                        logging.info(
                            'function called: expenses_diary.set_warning_sum_in_active_limit_for_user(text_field_input_warning_sum.value, get_user())')
                        page.views[-1].controls.append(
                            ft.Text("The warning sum that will be used for warning creation is recorded"))
                        page.update()
                        end_actions()
                        logging.info(
                            'function called: end_actions()')
                        checkbox_yes.disabled = True
                        checkbox_no.disabled = True
                    text_field_input_warning_sum.disabled = True

                confirm_button = ft.ElevatedButton("Confirmation", on_click=confirmation_button_clicked)
                page.views[-1].controls.append(confirm_button)
                page.update()
            else:
                end_actions()
                logging.info(
                    'function called: end_actions()')
                checkbox_yes.disabled = True
                checkbox_no.disabled = True
                show_warning_for_user_if_needed(get_user(), page)
                logging.info(
                    'function called: show_warning_for_user_if_needed(get_user(), page)')

        text_ask_warning_sum = ft.Text("Do you want to specify the sum left till the end of limit to create a warning?",
                                       italic=True, weight=ft.FontWeight.BOLD,
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
        logging.info(
            'function called: actions_if_warning_sum_more_or_equal_than_limit(text_field_input_warning_sum)')

        def clicked_yes_no_change_warning_sum(e):
            logging.info(
                'function called: clicked_yes_no_change_warning_sum(e)')
            logging.info(
                f'e.control: {e.control})')
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
                logging.info(
                    f'text_field_input_warning_sum.value: {text_field_input_warning_sum.value}')
                logging.info(
                    f'get_user(): {get_user()}')
                expenses_diary.set_warning_sum_in_active_limit_for_user(text_field_input_warning_sum.value, get_user())
                logging.info(
                    'function called: expenses_diary.set_warning_sum_in_active_limit_for_user(text_field_input_warning_sum.value, get_user())')
                checkbox_no_change_warning_sum.value = True
                checkbox_yes_change_warning_sum.disabled = True
                page.update()
                page.views[-1].controls.append(
                    ft.Text("OK, your warning sum won`t be changed and you will see the warning from this very moment"))
                text_field_input_warning_sum.disabled = True
                page.close(dialog_modal)
                show_warning_for_user_if_needed(get_user(), page)
                logging.info(
                    'function called: show_warning_for_user_if_needed(get_user(), page)')

                page.update()
                end_actions()
                logging.info(
                    'function called: end_actions()')

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



    def set_new_limit():
        logging.info(
            'function called: set_new_limit()')
        current_date = datetime.datetime.today().strftime('%Y-%m-%d')
        logging.info(
            f'get_user(): {get_user()}')
        if get_user() is None:
            create_individual_error_message(page, 'Dear guest, please sign in to save your limit')
        else:
            chosen_start_day_limit = get_chosen_date()
            logging.info(
                f'get_chosen_date(): {get_chosen_date()}')
            if chosen_start_day_limit is None:
                chosen_start_day_limit = current_date
            logging.info(
                f'chosen_start_day_limit: {chosen_start_day_limit}')
            limit_future_date = convert_to_date(search_bar_period_of_time.value)
            limit_future_date = limit_future_date.strftime('%Y-%m-%d')
            start_dates_all_limits = expenses_diary.get_all_limits_start_dates_for_user(get_user()) or []
            logging.info(
                f'function called expenses_diary.get_all_limits_start_dates_for_user(get_user()) and returned start_dates_all_limits: {start_dates_all_limits}')
            end_dates_all_limits = expenses_diary.get_all_limits_end_dates_for_user(get_user()) or []
            logging.info(
                f'function called expenses_diary.get_all_limits_end_dates_for_user(get_user()) and returned end_dates_all_limits: {end_dates_all_limits}')
            # check if limit with such dates already exists
            if (chosen_start_day_limit,) in start_dates_all_limits and (limit_future_date,) in end_dates_all_limits:
                column_search_bar.disabled = False
                sum_input_plus_textfield_min_row.disabled = False
                create_individual_error_message(page,
                                                "Limit with such dates already exists. It won`t be saved once again.")

                return
            # check if active limit already exists. Active limit is the latest limit with history = 0.
            check_response = expenses_diary.check_active_limits_for_user(get_user())
            logging.info(
                f'function called expenses_diary.check_active_limits_for_user(get_user()) and returned check_response: {check_response}')
            history = 0
            if check_response:
                # check if limit user wants to set is in the past time. If so not to ask about wish to replace previous limit
                logging.info(f'limit_future_date: {limit_future_date}, current_date:{current_date}')
                if limit_future_date >= current_date:
                    message_limit_already_exists = ft.Text(
                        "You have already another active limit installed. Do you want to update your active limit?",
                        italic=True, weight=ft.FontWeight.BOLD,
                        font_family="Consolas", size=20)
                    row_message = ft.Row([message_limit_already_exists], alignment=ft.MainAxisAlignment.CENTER,
                                         vertical_alignment=ft.CrossAxisAlignment.START)
                    page.views[-1].controls.append(row_message)
                    page.update()
                    questions_if_limit_already_exists()
                    logging.info(f'function called: questions_if_limit_already_exists()')
                    return

                else:
                    history = 1
                    message_limit_already_exists_add_history_limit = ft.Text(
                        "You have already another active limit installed.\n"
                        "Limit you want to set now can`t be an active one, as its period has already passed by.\n"
                        "It will be added as non-active limit. You can still add expenses and get statistical insights for your newly set period.",
                        text_align=ft.TextAlign.CENTER,
                        italic=True, weight=ft.FontWeight.BOLD,
                        font_family="Consolas", size=20)
                    row_message_add_history_limit = ft.Row([message_limit_already_exists_add_history_limit],
                                                           alignment=ft.MainAxisAlignment.CENTER,
                                                           vertical_alignment=ft.CrossAxisAlignment.START)
                    page.views[-1].controls.append(row_message_add_history_limit)
                    page.update()



            warning_sum = None
            currency = expenses_diary.get_currency_for_user(get_user())

            expenses_diary.add_active_limit(get_user(), chosen_start_day_limit, limit_future_date,
                                            text_field_input_sum.value, warning_sum, history)

            logging.info(
                f'get_user(): {get_user()}, chosen_start_day_limit: {chosen_start_day_limit}, limit_future_date: {limit_future_date}, '
                f'text_field_input_sum.value: {text_field_input_sum.value}, warning_sum: {warning_sum}')
            logging.info(
                f'function called: expenses_diary.add_active_limit(get_user(),'
                f' chosen_start_day_limit, limit_future_date, text_field_input_sum.value, warning_sum, history)')

            create_warning(get_user())
            logging.info(
                f'function called: create_warning(get_user())')

            information_text = ft.Text(
                f"Your new spare goal was added. Your expenses limit for {search_bar_period_of_time.value} from {chosen_start_day_limit} is set to {text_field_input_sum.value} {currency}")
            page.views[-1].controls.append(information_text)
            page.update()
            time.sleep(2)
            # If the limit period is in the past the app won`t ask about setting warning sum, but in other cases it will:
            if limit_future_date < current_date:
                end_actions()
                logging.info('function called: end_actions()')
                return
            ask_set_warning_sum()
            logging.info('function called: ask_set_warning_sum()')
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

    row_search_bar_and_input_sum = ft.Row([calendar_button_goals, column_search_bar, sum_input_plus_textfield_min_row],
                                          alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                          vertical_alignment=ft.CrossAxisAlignment.END)
    col_functional_goals_controls = ft.Column([row_search_bar_and_input_sum, save_sum_limit_button],
                                              horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def end_actions():
        logging.info('function called: end_actions()')
        def close_button_clicked(e):
            logging.info('function called: close_button_clicked(e)')
            close_button.disabled = True
            cancel_button.disabled = True
            page.views.pop()
            page.update()

        def cancel_button_clicked(e):
            logging.info('function called: cancel_button_clicked(e)')
            expenses_diary.delete_last_active_limit_for_user(get_user())
            logging.info('function called: expenses_diary.delete_last_active_limit_for_user(get_user())')
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

    def end_actions_variant_cancel_setting_new_limit():
        logging.info('function called: end_actions_variant_cancel_setting_new_limit()')
        def close_button_clicked_(e):
            logging.info('function called: close_button_clicked_(e)')
            close_button_cancel_var.disabled = True
            page.views.pop()
            page.update()

        close_button_cancel_var = ft.ElevatedButton('Close and return to main page', on_click=close_button_clicked_)

        row_end_buttons = ft.Row([close_button_cancel_var], ft.MainAxisAlignment.SPACE_AROUND)
        page.views[-1].controls.append(row_end_buttons)
        page.update()

    controls_goals = [appbar_goals, row_goals_header, col_functional_goals_controls, c]

    return controls_goals


def check_limit_period_ended(identified_user):
    logging.info('function called: check_limit_period_ended(identified_user)')
    today = datetime.datetime.today()
    end_date_limit = expenses_diary.get_active_limit_end_date_for_user(identified_user)
    end_date_limit = end_date_limit.split(" ")[0]
    logging.info(f'end_date_limit: {end_date_limit}')
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
    logging.info('function called: create_warning(identified_user)')
    warning_sum_for_user = expenses_diary.get_warning_sum_from_active_limit_for_user(identified_user)
    logging.info(f'function called: expenses_diary.get_warning_sum_from_active_limit_for_user(identified_user),'
                 f' returned: warning_sum_for_user: {warning_sum_for_user}')
    limit_sum_for_user = expenses_diary.get_active_limit_sum_for_user(identified_user)
    logging.info(f'function called: expenses_diary.get_active_limit_sum_for_user(identified_user),'
                 f' returned: limit_sum_for_user: {limit_sum_for_user}')
    if limit_sum_for_user is None:
        return
    else:
        if warning_sum_for_user is None:
            sum_to_spend_beyond_warning = limit_sum_for_user
            warning_sum_for_user = limit_sum_for_user
            #create a warning
        else:
            if warning_sum_for_user > limit_sum_for_user:
                sum_to_spend_beyond_warning = limit_sum_for_user
            else:
                sum_to_spend_beyond_warning = limit_sum_for_user - warning_sum_for_user

    start_date_limit = expenses_diary.get_active_limit_start_date_for_user(identified_user)
    end_date_limit = expenses_diary.get_active_limit_end_date_for_user(identified_user)
    end_date_limit = end_date_limit.split(" ")[0]
    today_date = datetime.datetime.today()

    logging.info(f'start_date_limit: {start_date_limit}')
    logging.info(f'end_date_limit after formatting: {end_date_limit}')

    real_expenses_during_limit_time = expenses_diary.get_sum_expenses_for_login_for_the_period(identified_user,
                                                                                               start_date_limit,
                                                                                               end_date_limit)

    logging.info(f'function called: expenses_diary.get_sum_expenses_for_login_for_the_period(identified_user, start_date_limit, end_date_limit), '
                 'returned: real_expenses_during_limit_time: {real_expenses_during_limit_time}')

    if real_expenses_during_limit_time is None:
        real_expenses_during_limit_time = 0
    elif real_expenses_during_limit_time < warning_sum_for_user:
        return
    diff_limit_all_real_expenses = limit_sum_for_user - real_expenses_during_limit_time
    logging.info(f'diff_limit_all_real_expenses: {diff_limit_all_real_expenses}')
    logging.info(f'function as condition called: check_limit_period_ended(identified_user), returned:{check_limit_period_ended(identified_user)}')
    if check_limit_period_ended(identified_user):
        # make limit history (history assign 1, count general_success_rate and general_subjective_success_rate fot this limit period

        #diff_limit_all_real_expenses can be positive (positive general spare balance if positive when summed up with other values in this column) or negative (negative general spare balance).
        # General spare balance helps to support motivation for sparing money beyond time when limits are set,
        # it`s a link that connects periods with active spare goals and gives insights about general tendention

        """if expenses_diary.check_real_success_for_user(get_user()) is None:
            real_success_rate = None"""
        "else:"""
        if diff_limit_all_real_expenses >= 0:
            real_success_rate = 100 * diff_limit_all_real_expenses / limit_sum_for_user
        else:
            real_success_rate = 100 * (diff_limit_all_real_expenses - limit_sum_for_user) / limit_sum_for_user

        logging.info(f"diff_limit_all_real_expenses, {diff_limit_all_real_expenses}")
        logging.info(f"real_success_rate, {real_success_rate}")

        general_subjective_success = expenses_diary.calculate_mean_subjective_success_rate(identified_user,
                                                                                               start_date_limit,
                                                                                               end_date_limit)
        logging.info(f"function called: expenses_diary.calculate_mean_subjective_success_rate(identified_user, start_date_limit, end_date_limit),"
                     f"returned: general_subjective_success {general_subjective_success}")

        expenses_diary.make_limit_history_for_user(identified_user, real_expenses_during_limit_time, diff_limit_all_real_expenses,
                                                       general_subjective_success, real_success_rate)
        logging.info(f"function called:  expenses_diary.make_limit_history_for_user(identified_user, real_expenses_during_limit_time,"
                     f" diff_limit_all_real_expenses, general_subjective_success, real_success_rate)")

    else:
        if diff_limit_all_real_expenses == 0:
            text_warning = "you have just reached your limit, you can`t spend anymore at all according to your spare goal. You see this message as you have reached your warning sum"
        elif diff_limit_all_real_expenses < 0:
            text_warning = (
                f"you have exceeded your set limit. You are beyond your set limit sum as much as {-(diff_limit_all_real_expenses)}."
                f" This means that you have spent more than you have planned. What a pity...next time better!")
        else:
            currency_selected = expenses_diary.get_currency_for_user(get_user())
            text_warning1 = "You see this message as you have reached your warning sum."
            text_warning2 = (
                f" You can still spend {sum_to_spend_beyond_warning} {currency_selected} before reaching the limit."
                f"The end date of your limit is {end_date_limit}. You still have chance to fulfill your spare goal.")
            if warning_sum_for_user is None:
                text_warning = text_warning2
            else:
                text_warning = text_warning1 + text_warning2

        warning = f"WARNING! {text_warning}"
        logging.info(f'warning: {warning}')
        return warning


def show_warning_for_user_if_needed(identified_user_login, page: ft.Page):
    logging.info(f'function called: show_warning_for_user_if_needed(identified_user_login, page: ft.Page)')
    warning_for_user = create_warning(identified_user_login)
    logging.info(f'function called: create_warning(identified_user_login), returned: warning_for_user: {warning_for_user}')
    information = ''
    logging.info(f'identified_user_login:{identified_user_login}')
    if identified_user_login is None:
        information = 'please sign in to follow warnings.'
        identified_user_login = 'guest'
    else:
        if warning_for_user:
            information = warning_for_user
        else:
            information = 'no warnings for you.'
            page.open(
                ft.AlertDialog(
                    title=ft.Text(f'Dear {identified_user_login}, {information}', text_align=ft.TextAlign.CENTER),
                    bgcolor=ft.colors.GREEN_200))
            page.update()
            return
    page.open(
        ft.AlertDialog(title=ft.Text(f'Dear {identified_user_login}, {information}', text_align=ft.TextAlign.CENTER),
                       bgcolor=ft.colors.RED_100))

    page.update()


def show_spare_balance(identified_user_login, page: ft.Page):
    logging.info('function called: show_spare_balance(identified_user_login, page: ft.Page)')
    login = identified_user_login
    logging.info(f'login:{login}')
    information_balance = ''

    if login is None:
        login = "guest"
        information_balance = "please sign in to use this function"
    else:
        balance = expenses_diary.get_balance_for_user(login)
        logging.info(f'function called: expenses_diary.get_balance_for_user(login), returned: balance: {balance}')
        currency = expenses_diary.get_currency_for_user(login)
        logging.info(f'function called: expenses_diary.get_currency_for_user(login), returned: currency: {currency}')
        if balance is None:
            information_balance = "now no data about your balance"
        else:
            information_balance = (f"your spare balance is {balance} {currency}.\n"
                                   f"This means that in general considering all your previous spare goals results up to this moment your spare progress looks like that...")
    page.open(
        ft.AlertDialog(title=ft.Text(f'Dear {login}, {information_balance}', text_align=ft.TextAlign.CENTER),
                       bgcolor=ft.colors.GREEN_200))
    page.update()
