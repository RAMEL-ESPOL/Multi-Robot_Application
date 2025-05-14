import flet as ft
from funciones import *
from user_controls.robot import Robot
from db.flet_pyrebase import PyrebaseWrapper

def HomeView(page: ft.Page, myPyrebase: PyrebaseWrapper):
    title = "Home"

    modelos = []
    all_robots = obtain_robot_list()
    control_types = ["Diferencial", "Omnidireccional", "Aerial"]

    def show_add_robot(e):
        modelos = obtain_model_list()
        combobox_model.options = [ft.dropdown.Option(modelo.nombre) for modelo in modelos]
        page.dialog = ft.AlertDialog(
            modal=True,
            elevation=1,
            title=ft.Container(
                content=ft.Text("Agregar Robot")),
            title_padding=15,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        name_input,
                        combobox_model,
                        combobox_control_type,
                        has_camera]),
                width=500,
                height=300),
            actions=[
                ft.TextButton(
                    content=ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text("Guardar", size=18),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        alignment=ft.alignment.center,
                    ), 
                    width=150,
                    height=40,
                    on_click=save_robot,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),  
                        color={"": ft.colors.BLACK},  
                        bgcolor={"": ft.colors.GREEN_ACCENT_400},
                    )
                ),
                ft.TextButton(
                    content=ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text("Cancelar", size=18),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        alignment=ft.alignment.center,
                    ), 
                    width=150,
                    height=40,
                    on_click=close_dialog,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),  
                        color={"": ft.colors.BLACK},  
                        bgcolor={"": ft.colors.BLUE_GREY_200},
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog.open = True
        page.update()

    def add_model_robot(e):
        page.go("/add_model")
        page.update()

    robot_list_view = ft.ListView(
        expand=1, 
        spacing=10, 
        padding=20, 
        auto_scroll=False, 
        height=250, 
        width=700)

    def build_robot_list(robot_list: list[Robot]):
        robot_list_view.controls.clear()
        encabezado = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(
                        value="Nombre", 
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                        style=ft.TextStyle(
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=ft.colors.GREY_100,
                        )
                    ),
                    padding=10,
                    expand=2,
                    bgcolor=ft.colors.GREY_600,
                    alignment=ft.alignment.center,
                    border_radius=ft.BorderRadius(5, 5, 5, 5),
                ),
                ft.Container(
                    content=ft.Text(
                        value="Modelo",
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                        style=ft.TextStyle(
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=ft.colors.GREY_100,
                        )
                    ),
                    padding=10,
                    expand=2,
                    bgcolor=ft.colors.GREY_600,
                    alignment=ft.alignment.center,
                    border_radius=ft.BorderRadius(5, 5, 5, 5),
                ),
                ft.Container(
                    content=ft.Text(
                        value="Tipo control",
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                        style=ft.TextStyle(
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=ft.colors.GREY_100,
                        )
                    ),
                    padding=10,
                    expand=2,
                    bgcolor=ft.colors.GREY_600,
                    alignment=ft.alignment.center,
                    border_radius=ft.BorderRadius(5, 5, 5, 5),
                ),
            ],
            height=45,
            width=700,
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        )
        robot_list_view.controls.append(encabezado)
        for robot in robot_list:
            fila = robot.build()
            robot_list_view.controls.append(fila)
        page.update()

    def go_worlds(e):
        page.go("/worlds")
        page.update()

    def go_environments(e):
        page.go("/environments")
        page.update()

    def go_configure_rutina(e):
        page.go('/rutina')
        page.update()
    
    def go_monitoreo(e):
        page.go('/monitor')
        page.update()

    def sign_out(e):
        myPyrebase.sign_out()
        page.go('/')
        page.update()

    add_robots_button = ft.ElevatedButton(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.ADD_BOX, size=18),
                    ft.Text("Robots", size=18),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        ),
        on_click=show_add_robot,
        width=200, 
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),  
            color={"": ft.colors.WHITE},  
            bgcolor={"": ft.colors.TEAL_ACCENT_700},
        )
    )
    add_models_button = ft.ElevatedButton(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.CALENDAR_VIEW_MONTH_ROUNDED, size=18),
                    ft.Text("Modelos", size=18),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        ),
        on_click=add_model_robot,
        width=200,
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),  
            color={"": ft.colors.WHITE},  
            bgcolor={"": ft.colors.TEAL_ACCENT_700}, 
        )
    )
    add_world_button = ft.ElevatedButton(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.ASSURED_WORKLOAD_ROUNDED, size=18),
                    ft.Text("Mundos", size=18),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        ),
        on_click=go_worlds,
        width=200,
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),  
            color={"": ft.colors.WHITE},  
            bgcolor={"": ft.colors.TEAL_ACCENT_700}, 
        )
    )
    add_configure_button = ft.ElevatedButton(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.APARTMENT_ROUNDED, size=18),
                    ft.Text("Entornos", size=18),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        ),
        on_click=go_environments,
        width=200,
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),  
            color={"": ft.colors.WHITE},  
            bgcolor={"": ft.colors.CYAN_ACCENT_700}, 
        )
    )
    configure_rutina = ft.ElevatedButton(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.BOOK_OUTLINED, size=18),
                    ft.Text("Rutinas", size=18),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        ),
        on_click=go_configure_rutina,
        width=200,
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),  
            color={"": ft.colors.WHITE},  
            bgcolor={"": ft.colors.CYAN_ACCENT_700}, 
        )
    )
    monitoreo_rutina = ft.ElevatedButton(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.DATA_EXPLORATION_OUTLINED, size=18),
                    ft.Text("Monitoreo", size=18),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        ),
        on_click=go_monitoreo,
        width=200,
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),  
            color={"": ft.colors.WHITE},  
            bgcolor={"": ft.colors.CYAN_ACCENT_700}, 
        )
    )

    build_robot_list(all_robots)

    name_input = ft.TextField(
        label="Nombre del Robot",
        label_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        border_color=ft.colors.BLACK,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        bgcolor=ft.colors.BLUE_GREY_50,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK))
    combobox_model = ft.Dropdown(
        label="Seleccionar Modelo",
        label_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK,
        ),
        border_color=ft.colors.BLACK,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        bgcolor=ft.colors.BLUE_GREY_50,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK,
        ))
    combobox_control_type= ft.Dropdown(
        options=[ft.dropdown.Option(control_type) for control_type in control_types],
        label="Seleccionar Tipo de Control",
        label_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK,
        ),
        border_color=ft.colors.BLACK,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        bgcolor=ft.colors.BLUE_GREY_50,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK,
        ),
    )
    has_camera = ft.Switch(
        label="Camara",
        value=False,
        label_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK,
        ),
        active_color=ft.colors.ORANGE_ACCENT_400,
        inactive_thumb_color=ft.colors.GREY_400,
        inactive_track_color=ft.colors.GREY_200,
    )

    def find_model_by_name(name: str, models: list[Modelo]) -> Modelo:
        for modelo in models:
            if modelo.nombre == name:
                return modelo

    def save_robot(e):
        modelo = find_model_by_name(combobox_model.value, modelos)
        new_robot = Robot(
            name_input.value,
            modelo,
            combobox_control_type.value,
            has_camera.value)
        add_robot(new_robot)
        all_robots = obtain_robot_list()
        build_robot_list(all_robots)
        page.dialog.open = False
        combobox_control_type.value = ""
        combobox_model.value = ""
        combobox_model.options = []
        name_input.value = ""
        has_camera.value = False
        page.update()

    def close_dialog(e):
        combobox_control_type.value = ""
        combobox_model.value = ""
        combobox_model.options = []
        name_input.value = ""
        has_camera.value = False
        page.dialog.open = False
        page.update()

    myPage = ft.SafeArea(
        expand=True,
        content=ft.Column(
            spacing=40,
            controls=[
                ft.Container(
                    height=10),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        add_models_button,
                        add_robots_button,
                        add_world_button]),
                ft.Container(
                    robot_list_view,
                    alignment=ft.alignment.center),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        add_configure_button,
                        configure_rutina,
                        monitoreo_rutina]),],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        
    )

    def on_page_load():
        nonlocal modelos, all_robots
        modelos = obtain_model_list()
        all_robots = obtain_robot_list()
        build_robot_list(all_robots)
        page.window_maximized = False
        page.appbar = ft.AppBar(
            toolbar_height=65,
            leading=ft.IconButton(
                icon=ft.icons.ROCKET_LAUNCH,
                scale=1.2),
            leading_width=60,
            title=ft.Text(
                value="Robots Disponibles",
                style=ft.TextStyle(
                    size=40,
                    weight=ft.FontWeight.BOLD)),
            center_title=True,
            bgcolor=ft.colors.GREY_300,
            actions=[
                ft.PopupMenuButton(
                    scale=1.2,
                    items=[
                        ft.PopupMenuItem(
                            text=str(myPyrebase.email)),
                        ft.PopupMenuItem(
                            text="Cerrar Sesion",
                            icon=ft.icons.LOGOUT_ROUNDED,
                            on_click=sign_out)])])
        page.update()

    return {
        "view":myPage,
        "title": title,
        "load": on_page_load
    }
