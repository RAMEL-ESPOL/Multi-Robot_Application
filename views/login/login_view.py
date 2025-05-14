import flet as ft
from db.flet_pyrebase import PyrebaseWrapper

def LoginView(page: ft.Page, myPyrebase: PyrebaseWrapper):
    title = "Login"

    def on_page_load():
        page.platform = ft.PagePlatform.LINUX
        # page.window_maximized = True
        page.appbar = None
        if myPyrebase.check_token():
            page.go('/home')
            page.update()

    def handle_sign_in(e):
        try:
            myPyrebase.sign_in(
                email=email.value, 
                password=password.value)
            email.value = ""
            password.value = ""
            page.go('/home')
            page.update()
        except:
            handle_sign_in_error()
            page.update()

    def handle_sign_in_error():
        page.snack_bar = ft.SnackBar(
            content=ft.Text(
                value="Credenciales incorrectas. Intente de nuevo.", 
                color=ft.colors.WHITE, 
                weight=ft.FontWeight.BOLD),
            bgcolor=ft.colors.RED)
        page.snack_bar.open = True
        page.update()

    def handle_register(e):
        page.go("/register")
        page.update()

    def highlight_link(e):
        e.control.style.color = ft.colors.BLUE
        e.control.update()

    def unhighlight_link(e):
        e.control.style.color = None
        e.control.update()

    # Componentes del view
    imagen = ft.Image(
        src=f"/images/Login.png", 
        fit=ft.ImageFit.FILL, 
        width=500, 
        height=500, 
        expand=1)
    encabezado = ft.Text(
        value="Bienvenido", 
        style=ft.TextStyle(weight=ft.FontWeight.W_600, size=24), 
        text_align=ft.TextAlign.CENTER, 
        expand=1)
    email = ft.TextField(
        label="Email", 
        autofocus=True, 
        width=300, 
        expand=1)
    login_button = ft.ElevatedButton(
        text="Entrar", 
        scale=1.5, 
        on_click=handle_sign_in, 
        expand=1)
    password = ft.TextField(
        label="Password", 
        password=True, 
        can_reveal_password=True, 
        width=300, 
        expand=1,
        on_submit=handle_sign_in)
    text_register = ft.Text(
        disabled=False,
        expand=1,
        spans=[
            ft.TextSpan("¿No tienes una cuenta? "),
            ft.TextSpan(
                "¡Registrate!",
                style=ft.TextStyle(
                    italic=True, 
                    color=ft.colors.BLUE),
                on_enter=highlight_link,
                on_exit=unhighlight_link,
                on_click=handle_register
            )
        ]
    )

    # Making the layout responsive and centered
    myPage = ft.SafeArea(
        ft.ResponsiveRow(
            [
                ft.Container(
                    content=imagen, 
                    expand=1, 
                    alignment=ft.alignment.center, 
                    col=6),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=encabezado, 
                                alignment=ft.alignment.center),
                            ft.Container(
                                content=email, 
                                alignment=ft.alignment.center),
                            ft.Container(
                                content=password, 
                                alignment=ft.alignment.center),
                            ft.Container(
                                content=login_button, 
                                alignment=ft.alignment.center),
                            ft.Container(
                                content=text_register, 
                                alignment=ft.alignment.center)
                        ],
                        spacing=30,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    expand=1,
                    col=6,
                    padding=ft.Padding(
                        bottom=20.0, 
                        left=20.0, 
                        right=20.0, 
                        top=30.0),
                    alignment=ft.alignment.center
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        expand=True,
        adaptive=True
    )

    return {
        "view": myPage,
        "title": title,
        "load": on_page_load
    }


