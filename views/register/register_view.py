import flet as ft
from db.flet_pyrebase import PyrebaseWrapper

def RegisterView(page: ft.Page, myPyrebase: PyrebaseWrapper):
    title = "Register"

    def on_load():
        pass

    def handle_register(e):
        try:
            myPyrebase.register_user(name.value, email.value, password.value)
            name.value = ""
            email.value = ""
            password.value = ""
            page.go("/home")
        except:
            handle_register_error()
            page.update()

    def go_to_login(e):
        page.go("/")   

    def handle_register_error():
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Campos no cumplen los requerimentos. Intente de nuevo.", color=ft.colors.WHITE),
            bgcolor=ft.colors.RED
        )
        page.snack_bar.open = True
        page.update()

    def highlight_link(e):
        e.control.style.color = ft.colors.BLUE
        e.control.update()

    def unhighlight_link(e):
        e.control.style.color = None
        e.control.update()

    # Componentes del view
    imagen = ft.Container(content=ft.Image(src=f"/images/register.png", width=500, height=500), expand= 1)
    encabezado = ft.Text("Registrate", style=ft.TextStyle(weight=ft.FontWeight.W_600, size=24), text_align=ft.TextAlign.CENTER, expand=1)
    name = ft.TextField(label="Nombre", autofocus=True, width=300)
    email = ft.TextField(label="Email", autofocus=True, width=300)
    register_button = ft.ElevatedButton(text="Registrate", scale=1.2, on_click=handle_register)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
    text_login = ft.Text(
        disabled= False,
        spans= [
            ft.TextSpan("¿Ya tienes una cuenta? "),
            ft.TextSpan(
                "Inicia sesion",
                style=ft.TextStyle(italic=True),
                on_enter=highlight_link,
                on_exit=unhighlight_link,
                on_click=go_to_login
            )
        ]
    )

    register_view = ft.SafeArea(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(encabezado, alignment=ft.alignment.center),
                            ft.Container(name, alignment=ft.alignment.center),
                            ft.Container(email, alignment=ft.alignment.center),
                            ft.Container(password, alignment=ft.alignment.center),
                            ft.Container(register_button, alignment=ft.alignment.center),
                            ft.Container(text_login, alignment=ft.alignment.center),
                        ], 
                        spacing= 27
                    ),
                    expand=1
                ),
                imagen
            ]
        )
    )
    return {
        "view": register_view,
        "title": title,
        "on_load": on_load
    }