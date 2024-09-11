import flet as ft
from view_sign_up import view_sign_up_controls


def view_sign_in_sign_up(page: ft.Page):
    def create_go_view_sign_up(page):
        page.views.append(
                ft.View(route='/sign_up',
                        controls=view_sign_up_controls(page)))
        page.update()


    img_auth_under_appbar = ft.Image(
        src=f"financial_planning.png",
        fit=ft.ImageFit.COVER,
        width=100,
        height=700,
        expand=True
    )
    img_row_sign_in_sign_up = ft.Row(alignment=ft.MainAxisAlignment.CENTER, expand=True,
                                     controls=[img_auth_under_appbar])

    appbar_sign_in_sign_up = ft.AppBar(leading=ft.Icon(ft.icons.SAVINGS), leading_width=60,
                                       title=ft.Text("Family expenses organizer"), bgcolor=ft.colors.SURFACE_VARIANT,
                                       actions=[ft.IconButton(icon=ft.icons.ARROW_RIGHT,
                                                              tooltip="Go to App without authentication",
                                                              on_click=lambda _: page.go('/app'))])

    row_sing_in_sign_up_elev_buttons = ft.Row(
        [ft.ElevatedButton("Sign In", bgcolor=ft.colors.AMBER_200, on_click=lambda _: page.go('/authentication')),
         ft.ElevatedButton("Sign Up", bgcolor=ft.colors.AMBER_200, on_click=lambda _:create_go_view_sign_up(page))],
        spacing=50, alignment=ft.MainAxisAlignment.CENTER)
    row_text_before_sign_in_sign_up_elev_buttons = ft.Row(
        [ft.Text("Select between Sign In and Sign Up", italic=True, weight=ft.FontWeight.BOLD,
                 font_family="Consolas", size=20)], alignment=ft.MainAxisAlignment.CENTER)
    column_text_elev_buttons_sign_in_sign_up = ft.Column([row_text_before_sign_in_sign_up_elev_buttons,
                                                          row_sing_in_sign_up_elev_buttons], spacing=50)

    row_bottom_app_bar_sign_in_sign_up = ft.Row(
        [ft.IconButton(icon=ft.icons.ARROW_RIGHT, tooltip="Go to Authentication",
                       on_click=lambda _: page.go('/authentication')),
         ft.IconButton(icon=ft.icons.ARROW_RIGHT, tooltip="Go to App without authentication",
                       on_click=lambda _: page.go('/app'))], alignment=ft.MainAxisAlignment.CENTER)

    bottom_app_bar_sign_in_sign_up = ft.BottomAppBar(content=row_bottom_app_bar_sign_in_sign_up)

    controls_view_sign_in_sign_up = [appbar_sign_in_sign_up, column_text_elev_buttons_sign_in_sign_up,
                                     img_row_sign_in_sign_up, bottom_app_bar_sign_in_sign_up]
    return controls_view_sign_in_sign_up
