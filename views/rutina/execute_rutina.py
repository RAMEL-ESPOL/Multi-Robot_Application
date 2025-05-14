import flet as ft
from funciones import list_files_in_directory, launch_rutina, rutina_dir
import threading
from db.flet_pyrebase import PyrebaseWrapper

class RutinaRow(ft.UserControl):
    def __init__(self, name):
        super().__init__()
        self.name = ft.Text(
            value=name)
        self.play_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW_ROUNDED,
            on_click=self.play)
        self.stop_button = ft.IconButton(
            icon=ft.icons.STOP_CIRCLE_ROUNDED)
        self.stop_event = threading.Event()
        self.rutina_thread = None

    def play(self, e):
        self.stop_event.clear()
        path = rutina_dir + '/' + self.name.value + ".yaml"
        self.rutina_thread = threading.Thread(target=launch_rutina, args=(path, self.stop_event))
        self.rutina_thread.start()

    def stop(self, e):
        if self.rutina_thread and self.rutina_thread.is_alive():
            self.stop_event.set()
            self.rutina_thread.join()

    def build(self):
        return ft.Row(
            controls=[
                self.name,
                ft.Row(
                    controls=[
                        self.play_button,
                        self.stop_button],
                    alignment=ft.MainAxisAlignment.END)
            ],
            width=300,
            height=100,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

def ExecuteRutina(page: ft.Page, myPyrebase: PyrebaseWrapper):
    title = 'Rutinas'
    
    list_rutina_files = list()
    
    def go_config_rutina(e):
        page.go("/config_rutina")
        page.update()

    add_rutina = ft.ElevatedButton(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        name=ft.icons.ADD, 
                        size=18),
                    ft.Text(
                        value="Agregar rutina", 
                        size=18)],
                alignment=ft.MainAxisAlignment.CENTER),
            alignment=ft.alignment.center),
        on_click=go_config_rutina,
        width=220, 
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),  
            color={"": ft.colors.WHITE},  
            bgcolor={"": ft.colors.TEAL_ACCENT_700}))
    
    def go_home(e):
        page.go("/home")
        page.update()

    def sign_out(e):
        myPyrebase.sign_out()
        page.go('/')
        page.update()
    
    rutina_listview = ft.ListView(
        height=500,
        width=700)
    
    def build_table(gz_files: list):
        rutina_listview.controls.clear()
        for file in gz_files:
            rutina_listview.controls.append(
                ft.Container(
                    content=RutinaRow(file),
                    alignment=ft.alignment.center))
        page.update()
    
    build_table(list_rutina_files)
    
    rutina_view = ft.SafeArea(
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=40,
            controls=[
                ft.Container(
                    height=10),
                ft.Container(
                    content=add_rutina,
                    alignment=ft.alignment.center),
                ft.Container(
                    content=rutina_listview,
                    alignment=ft.alignment.center)]
        ))

    def on_page_load():
        nonlocal list_rutina_files
        list_rutina_files = list_files_in_directory(rutina_dir)
        build_table(list_rutina_files)
        page.appbar = ft.AppBar(
            toolbar_height=65,
            leading=ft.IconButton(
                icon=ft.icons.HOME,
                on_click=go_home,
                scale=1.2),
            leading_width=60,
            title=ft.Text(
                value="Rutinas",
                style=ft.TextStyle(
                    size=30,
                    weight=ft.FontWeight.BOLD)),
            center_title=True,
            bgcolor=ft.colors.GREY_300,
            actions=[
                ft.PopupMenuButton(
                    scale=1.2,
                    items=[
                        ft.PopupMenuItem(
                            disabled=True,
                            text=str(myPyrebase.email)),
                        ft.PopupMenuItem(
                            text="Cerrar Sesion",
                            icon=ft.icons.LOGOUT_ROUNDED,
                            on_click=sign_out)])])
        page.update()

    return {
        "view": rutina_view,
        "title": title,
        "load": on_page_load
    }
