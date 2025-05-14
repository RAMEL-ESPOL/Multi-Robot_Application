import flet as ft
from funciones import obtain_model_list, add_model
from user_controls.modelo import Modelo
from user_controls.file_selector import FileSelector
from db.flet_pyrebase import PyrebaseWrapper

def ModeloView(page: ft.Page, myPyrebase: PyrebaseWrapper):
    title = 'Modelo'
    modelo_list = obtain_model_list()
    modelo_table = ft.ListView(
        expand=1, 
        spacing=10, 
        padding=20, 
        auto_scroll=False, 
        height=300, 
        width=300,)

    def construir_tabla(modelo_list: list):
        modelo_table.controls.clear()
        encabezado = ft.Container(
                content=ft.Text(
                    value="Nombre modelo",
                    style=ft.TextStyle(
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color=ft.colors.GREY_100)),
                bgcolor=ft.colors.GREY_600,
                padding=10,
                border_radius=ft.BorderRadius(5, 5, 5, 5),
                alignment=ft.alignment.center)
        modelo_table.controls.append(encabezado)
        for modelo in modelo_list:
            fila = ft.Container(
                        content=ft.Text(
                            value=modelo.nombre,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.NORMAL,
                                color=ft.colors.BLACK),
                            text_align=ft.TextAlign.CENTER),
                        bgcolor=ft.colors.GREY_300,
                        height=60,
                        width=250,
                        border_radius=ft.BorderRadius(5, 5, 5, 5),
                        alignment=ft.alignment.center)
            modelo_table.controls.append(fila)
        page.update()
    
    construir_tabla(modelo_list)
    
    nombre_input = ft.TextField(
        label="Nombre del Modelo",
        label_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        border_color=ft.colors.BLACK,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        bgcolor=ft.colors.BLUE_GREY_50,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK))
    urdf_input = ft.Text(
        value="Ruta URDF",
        style=ft.TextStyle(size=15, weight=ft.FontWeight.BOLD))
    urdf_picker = FileSelector()
    sdf_input = ft.Text(
        value="Ruta SDF",
        style=ft.TextStyle(size=15, weight=ft.FontWeight.BOLD))
    sdf_picker = FileSelector()
    nav_path_input = ft.Text(
        value="Ruta Navegacion",
        style=ft.TextStyle(size=15, weight=ft.FontWeight.BOLD))
    nav_picker = FileSelector()

    def save_model(e):
        nuevo_modelo = Modelo(
            nombre_input.value,
            urdf_picker.file_path_text,
            sdf_picker.file_path_text,
            nav_picker.file_path_text)
        add_model(nuevo_modelo)
        modelo_list = obtain_model_list()
        construir_tabla(modelo_list)
        nombre_input.value = ''
        urdf_picker.file_path_label.value = "Seleccionar archivos"
        urdf_picker.file_path_text = ""
        sdf_picker.file_path_label.value = "Seleccionar archivos"
        sdf_picker.file_path_text = ""
        nav_picker.file_path_label.value = "Seleccionar archivos"
        nav_picker.file_path_text = ""
        page.dialog.open = False
        page.update()

    def close_dialog(e):
        nombre_input.value = ''
        urdf_picker.file_path_label.value = "Seleccionar archivos"
        urdf_picker.file_path_text = ""
        sdf_picker.file_path_label.value = "Seleccionar archivos"
        sdf_picker.file_path_text = ""
        nav_picker.file_path_label.value = "Seleccionar archivos"
        nav_picker.file_path_text = ""
        page.dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Agregar Nuevo Modelo"),
        content=ft.Container(
            ft.Column(controls=[
                nombre_input,
                urdf_input,
                urdf_picker,
                sdf_input,
                sdf_picker,
                nav_path_input,
                nav_picker
            ],
            spacing=15),
            width=500,
            height=350
        ),
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
                    on_click=save_model,
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

    def show_add_model_dialog(e):
        page.dialog = dialog
        page.dialog.open = True
        page.update()

    def go_home(e):
        page.go('/home')
        page.update()

    def sign_out(e):
        myPyrebase.sign_out()
        page.go('/')
        page.update()

    button_add_model = ft.ElevatedButton(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        name=ft.icons.ADD_BOX, 
                        size=18),
                    ft.Text(
                        value="Agregar modelo", 
                        size=18)],
                alignment=ft.MainAxisAlignment.CENTER),
            alignment=ft.alignment.center), 
        on_click=show_add_model_dialog,
        width=220, 
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),  
            color={"": ft.colors.WHITE},  
            bgcolor={"": ft.colors.TEAL_ACCENT_700}))
    
    modelo_view = ft.SafeArea(
        content=ft.Column(
            spacing=40,
            controls=[
                ft.Container(
                    height=20),
                ft.Container(
                    content=button_add_model,
                    alignment=ft.alignment.center),
                ft.Container(
                    content=modelo_table,
                    alignment=ft.alignment.center)]
        )
    )

    def on_page_load():
        nonlocal modelo_list
        modelo_list = obtain_model_list()
        construir_tabla(modelo_list)
        page.appbar = ft.AppBar(
            toolbar_height=65,
            leading=ft.IconButton(
                icon=ft.icons.HOME,
                on_click=go_home,
                scale=1.2),
            leading_width=60,
            title=ft.Text(
                value="Modelos",
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
        "view": modelo_view,
        "title": title,
        "load": on_page_load
    }
