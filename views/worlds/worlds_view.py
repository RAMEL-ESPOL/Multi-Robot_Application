import flet as ft
from funciones import obtain_world_list, add_world
from user_controls.world import World
from user_controls.file_selector import FileSelector
from db.flet_pyrebase import PyrebaseWrapper

def WorldsView(page: ft.Page, myPyrebase: PyrebaseWrapper):
    title = "Worlds"
    world_list = obtain_world_list()

    world_listview = ft.ListView(
        spacing=10, 
        padding=20, 
        auto_scroll=False,
        height=300, 
        width=300)
    name_input = ft.TextField(
        label="Nombre del Mundo",
        label_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        border_color=ft.colors.BLACK,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        bgcolor=ft.colors.BLUE_GREY_50,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK))
    world_path_label = ft.Text(
        value="Ruta del Mundo",
        style=ft.TextStyle(size=15, weight=ft.FontWeight.BOLD))
    map_label = ft.Text(
        value="Ruta del Mapa",
        style=ft.TextStyle(size=15, weight=ft.FontWeight.BOLD))
    world_path_picker = FileSelector()
    map_path = FileSelector()

    def construir_tabla(world_list: list[World]):
        world_listview.controls.clear()
        encabezado = ft.Container(
            content=ft.Text(
                value="Nombre mundos",
                style=ft.TextStyle(
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color=ft.colors.GREY_100)),
            bgcolor=ft.colors.GREY_600,
            padding=10,
            border_radius=ft.BorderRadius(5, 5, 5, 5),
            alignment=ft.alignment.center)
        world_listview.controls.append(encabezado)
        for world in world_list:
            fila = ft.Container(
                content=ft.Text(
                    value=world.name,
                    style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.NORMAL,
                                color=ft.colors.BLACK),
                            text_align=ft.TextAlign.CENTER),
                alignment=ft.alignment.center,
                border_radius=ft.BorderRadius(5, 5, 5, 5),
                height=60,
                bgcolor=ft.colors.GREY_300)
            world_listview.controls.append(fila)
        page.update()

    construir_tabla(world_list)

    def save_world(e):
        new_world = World(
            name_input.value,
            world_path_picker.file_path_text,
            map_path.file_path_text
        )
        add_world(new_world)
        world_list = obtain_world_list()
        construir_tabla(world_list)
        name_input.value = ''
        world_path_picker.reset()
        map_path.reset()
        page.dialog.open = False
        page.update()

    def close_dialog(e):
        name_input.value = ""
        world_path_picker.reset()
        map_path.reset()
        page.dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        title=ft.Text('Agregar mundo'),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    name_input,
                    world_path_label,
                    world_path_picker,
                    map_label,
                    map_path
                ]),
            width=350,
            height=300),
        actions=[
            ft.TextButton(
                content=ft.Container(
                    content=ft.Row(
                            controls=[
                                ft.Text("Guardar", size=18)],
                            alignment=ft.MainAxisAlignment.CENTER),
                        alignment=ft.alignment.center), 
                on_click=save_world,
                width=150,
                height=40,
                style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),  
                        color={"": ft.colors.BLACK},  
                        bgcolor={"": ft.colors.GREEN_ACCENT_400})),
            ft.TextButton(
                content=ft.Container(
                    content=ft.Row(
                            controls=[
                                ft.Text("Cancelar", size=18)],
                            alignment=ft.MainAxisAlignment.CENTER),
                        alignment=ft.alignment.center), 
                on_click=close_dialog,
                width=150,
                height=40,
                style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),  
                        color={"": ft.colors.BLACK},  
                        bgcolor={"": ft.colors.BLUE_GREY_200}))
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def show_add_world(e):
        page.dialog = dialog
        page.dialog.open = True
        page.update()

    add_world_button = ft.ElevatedButton(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        name=ft.icons.ADD_BOX, 
                        size=18),
                    ft.Text(
                        value="Agregar mundo", 
                        size=18)],
                alignment=ft.MainAxisAlignment.CENTER),
            alignment=ft.alignment.center),
        on_click=show_add_world,
        width=220, 
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),  
            color={"": ft.colors.WHITE},  
            bgcolor={"": ft.colors.TEAL_ACCENT_700}))
    
    def go_home(e):
        page.go('/home')
        page.update()

    def sign_out(e):
        myPyrebase.sign_out()
        page.go('/')
        page.update() 

    def on_page_load():
        nonlocal world_list
        world_list = obtain_world_list()
        construir_tabla(world_list)
        page.appbar = ft.AppBar(
            toolbar_height=65,
            leading=ft.IconButton(
                icon=ft.icons.HOME,
                on_click=go_home,
                scale=1.2),
            leading_width=60,
            title=ft.Text(
                value="Mundos Disponibles",
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

    world_view = ft.SafeArea(
        expand=True,
        content=ft.Column(
            spacing=40,
            controls=[
                ft.Container(
                    height=20),
                ft.Container(
                    content=add_world_button,
                    alignment=ft.alignment.center),
                ft.Container(
                    content=world_listview,
                    alignment=ft.alignment.center),
            ]
        )
    )

    return {
        "view":world_view,
        "title": title,
        "load": on_page_load
    }
