import flet as ft
import expenses_diary
from identification_data import get_user
import random
from fabrique_controls import create_calendar_button, create_individual_error_message
import datetime

start_date_analysis = None
end_date_analysis = None
login = get_user()
current_statistics_data = {}

def set_current_statistics_data(login, data):
    global current_statistics_data
    current_statistics_data = data


def get_current_statistics_data(login):
    global current_statistics_data
    return current_statistics_data


def set_start_date_analysis(login, passed_start_date_analysis):
    global start_date_analysis
    start_date_analysis = passed_start_date_analysis


def get_start_date_analysis(login):
    global start_date_analysis
    return start_date_analysis


def set_end_date_analysis(login, passed_end_date_analysis):
    global end_date_analysis
    end_date_analysis = passed_end_date_analysis


def get_end_date_analysis(login):
    global end_date_analysis
    return end_date_analysis


def create_charts_layout(page: ft.Page):
    def make_chart():
        normal_radius = 100
        hover_radius = 150
        normal_title_style = ft.TextStyle(
            size=20, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD
        )
        hover_title_style = ft.TextStyle(
            size=30,
            color=ft.colors.WHITE,
            weight=ft.FontWeight.BOLD,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),

        )

        def on_chart_event(e: ft.PieChartEvent):
            for idx, section in enumerate(chart.sections):
                if idx == e.section_index:
                    section.radius = hover_radius
                    section.title_style = hover_title_style
                else:
                    section.radius = normal_radius
                    section.title_style = normal_title_style

            chart.update()

        chart = ft.PieChart(
            sections=[],
            sections_space=0,
            center_space_radius=30,
            on_chart_event=on_chart_event,
            expand=True
        )

        colors = [ft.colors.RED, ft.colors.GREEN, ft.colors.ORANGE, ft.colors.PURPLE, ft.colors.YELLOW,
                  ft.colors.LIME_800, ft.colors.BROWN, ft.colors.LIGHT_GREEN, ft.colors.INDIGO, ft.colors.PINK,
                  ft.colors.LIGHT_BLUE_50, ft.colors.CYAN, ft.colors.DEEP_PURPLE_900]
        print("on_chart_event")
        print(expenses_diary.check_expenses_for_user(get_user()))
        start_date = get_start_date_analysis(get_user())
        end_date = get_end_date_analysis(get_user())
        statistics_data = expenses_diary.categories_procent_for_period_for_chart(get_user(), start_date, end_date)
        if statistics_data:
            print(statistics_data)
            set_current_statistics_data(get_user(), statistics_data)
            for key, val in statistics_data.items():
                random_color = random.choice(colors)
                chart.sections.append(
                    ft.PieChartSection(val, title=f"{int(val)}%", title_style=normal_title_style, color=random_color,
                                       radius=normal_radius))


        #page.views[-1].controls.append(chart)
        return chart

    def button_show_chart_clicked(ev):
        print(get_user(), 'get_user() in chart show function')
        login_name = get_user()
        if login_name is None:
            create_individual_error_message(page, "Dear guest, please sign in to use this function")
            login_name = "guest"
            page.update()
            return
        if get_start_date_analysis(get_user()) is None:
            create_individual_error_message(page,
                                            f"Dear {login_name}, please select start date to create a chart for the period")
            return
        elif get_end_date_analysis(get_user()) is None:
            create_individual_error_message(page, f"Dear {login_name}, please select end date to create a chart for the period")
            return
        if not expenses_diary.get_expenses_for_login_for_the_period(get_user(), get_start_date_analysis(get_user()), get_end_date_analysis(get_user())):
            create_individual_error_message(page,f"What a nice task, there is no real work to do."
                                                 f"\n Absolutely no expenses in this period from {get_start_date_analysis(get_user())} till {get_end_date_analysis(get_user())}.")
            return
        else:
            def close_chart_clicked(e):
                page.close(dialog_modal_chart)
            created_chart = make_chart()
            button_close_chart = ft.ElevatedButton('Close chart', on_click=close_chart_clicked)

            chart_data = get_current_statistics_data(get_user())
            print(chart_data, 'chart data')
            text_chart = ""
            if chart_data is not None:
                for key, value in chart_data.items():
                    text_chart += f"{key} : {int(value)}%\n"
                    print(text_chart, 'text_chart')
            dialog_modal_chart = ft.AlertDialog(
                modal=True,
                title=ft.Text(f"Chart: period {get_start_date_analysis(get_user())} - {get_end_date_analysis(get_user)}\n\n{text_chart}"),
                content=created_chart,
                actions=[button_close_chart],
                actions_alignment=ft.MainAxisAlignment.END
            )

            page.open(dialog_modal_chart)
            page.update()

            """page.views[-1].controls.append(make_chart())
            page.update()"""

    button_show_chart = ft.ElevatedButton("Show chart", bgcolor=ft.colors.AMBER_200, on_click=button_show_chart_clicked)

    def create_start_date_button() -> ft.Control:
        def setting_start_date(ev):
            set_start_date_analysis(get_user(), ev.control.value.strftime('%Y-%m-%d'))
            print('start_date_analysis', get_start_date_analysis(get_user()))

        pick_start_date_in_calendar = ft.DatePicker(
            first_date=datetime.datetime(year=2023, month=10, day=1),
            last_date=datetime.datetime(year=2025, month=10, day=1),
            on_change=setting_start_date
        )

        button_start_date_for_chart = ft.ElevatedButton(
            "Select START date",
            icon=ft.icons.CALENDAR_MONTH,
            tooltip="Select start date for period to create a chart",
            bgcolor=ft.colors.AMBER_200,
            on_click=lambda e: page.open(
                pick_start_date_in_calendar
            )
        )

        return button_start_date_for_chart

    def create_end_date_button() -> ft.Control:
        def setting_end_date(ev):
            end_date_for_analysis = ev.control.value
            print("ev.control.value end_date_for_analysis", end_date_for_analysis)
            start_date_str = get_start_date_analysis(get_user())
            print(start_date_str, "start_date_str")
            print(type(start_date_str), 'type start_date_str')
            if start_date_str is not None:
                start_date_for_analysis = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
                if start_date_for_analysis > end_date_for_analysis:
                    create_individual_error_message(page,
                                                    "End date is earlier than start date!\n Select dates once again.\n"
                                                    "Otherwise we will use later date as the end date and earlier date as the start date!\n")
                    set_start_date_analysis(get_user(), end_date_for_analysis.strftime('%Y-%m-%d'))
                    set_end_date_analysis(get_user(), start_date_for_analysis)
                else:
                    print(end_date_for_analysis.strftime('%Y-%m-%d'), 'end_date_for_analysis.strftime')
                    print(get_user(), 'get_user')
                    set_end_date_analysis(get_user(), end_date_for_analysis.strftime('%Y-%m-%d'))
                    print('end_date_analysis else in if', get_end_date_analysis(get_user()))
            else:
                create_individual_error_message(page,
                                                "Select start date! Otherwise start date will be the day 7 days before!")
                date_1_week_ago = end_date_for_analysis + datetime.timedelta(-7)
                set_start_date_analysis(get_user(), date_1_week_ago.strftime('%Y-%m-%d'))
            print('end_date_analysis', get_end_date_analysis(get_user()))

        pick_end_date_in_calendar = ft.DatePicker(
            first_date=datetime.datetime(year=2023, month=10, day=1),
            last_date=datetime.datetime(year=2025, month=10, day=1),
            on_change=setting_end_date
        )

        button_end_date_for_chart = ft.ElevatedButton(
            "Select END date",
            icon=ft.icons.CALENDAR_MONTH,
            tooltip="Select end date for period to create a chart",
            bgcolor=ft.colors.AMBER_200,
            on_click=lambda e: page.open(
                pick_end_date_in_calendar
            )
        )

        return button_end_date_for_chart

    button_start_date_for_chart = create_start_date_button()

    button_end_date_for_chart = create_end_date_button()

    column_input_dates = ft.Column([button_start_date_for_chart, button_end_date_for_chart])
    row_show_chart = ft.Row([column_input_dates, button_show_chart])
    page.views[-1].controls.append(row_show_chart)
    page.update()
    return row_show_chart
