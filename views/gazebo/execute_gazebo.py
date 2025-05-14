import flet as ft
from funciones import list_files_in_directory, launch_simulation, gazebo_dir
import threading
import logging
from db.flet_pyrebase import PyrebaseWrapper

logging.basicConfig(level=logging.DEBUG)

class GazeboRow(ft.UserControl):
    def __init__(self, name):
        super().__init__()
        self.name = ft.Text(value=name)
        self.play_button = ft.IconButton(icon=ft.icons.PLAY_ARROW_ROUNDED, on_click=self.play)
        self.stop_button = ft.IconButton(icon=ft.icons.STOP_CIRCLE_ROUNDED, on_click=self.stop)
        self.stop_event = threading.Event()
        self.gazebo_thread = None

    def play(self, e):
        self.stop_event.clear()
        path = gazebo_dir + '/' + self.name.value + ".yaml"
        logging.debug(f"Launching simulation with config: {path}")
        self.gazebo_thread = threading.Thread(target=launch_simulation, args=(path, self.stop_event))
        self.gazebo_thread.start()

    def stop(self, e):
        if self.gazebo_thread and self.gazebo_thread.is_alive():
            logging.debug("Stopping simulation")
            self.stop_event.set()
            self.gazebo_thread.join()
            logging.debug("Simulation stopped")

    def build(self):
        return ft.Row(
            controls=[
                self.name,
                ft.Row(
                    controls=[self.play_button, self.stop_button],
                    alignment=ft.MainAxisAlignment.END
                )
            ],
            width=500,
            height=100,
            alignment=ft.MainAxisAlignment.CENTER
        )

def ExecuteGazebo(page: ft.Page, myPyrebase: PyrebaseWrapper):
    title = "Entornos"
    list_gazebo_files = list_files_in_directory(gazebo_dir)

    def go_configure(e):
        page.go("/config_gz")
        page.update()

    add_gazebo = ft.ElevatedButton(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        name=ft.icons.ADD, 
                        size=18),
                    ft.Text(
                        value="Agregar entorno", 
                        size=18)],
                alignment=ft.MainAxisAlignment.CENTER),
            alignment=ft.alignment.center),
        on_click=go_configure,
        width=220, 
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),  
            color={"": ft.colors.WHITE},  
            bgcolor={"": ft.colors.TEAL_ACCENT_700}))

    def go_home(e):
        page.go("/home")
        page.update()

    gazebo_listview = ft.ListView(height=500, width=500)

    def build_table(gz_files):
        gazebo_listview.controls.clear()
        for file in gz_files:
            gazebo_listview.controls.append(GazeboRow(file))
        page.update()

    build_table(list_gazebo_files)

    gazebo = ft.SafeArea(
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=30,
            controls=[
                ft.Container(height=10),
                ft.Container(content=add_gazebo, alignment=ft.alignment.center),
                ft.Container(content=gazebo_listview, alignment=ft.alignment.center)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    def sign_out(e):
        myPyrebase.sign_out()
        page.go('/')
        page.update()

    def on_page_load():
        nonlocal list_gazebo_files
        list_gazebo_files = list_files_in_directory(gazebo_dir)
        build_table(list_gazebo_files)
        page.appbar = ft.AppBar(
            toolbar_height=65,
            leading=ft.IconButton(
                icon=ft.icons.HOME, 
                on_click=go_home,
                scale=1.2),
            leading_width=60,
            title=ft.Text(
                value="Entornos Gazebo", 
                style=ft.TextStyle(
                    size=40, 
                    weight=ft.FontWeight.BOLD)),
            center_title=True,
            bgcolor=ft.colors.GREY_300,
            actions=[
                ft.PopupMenuButton(
                    scale=1.2,
                    items=[
                        ft.PopupMenuItem(text=str(myPyrebase.email)),
                        ft.PopupMenuItem(text="Cerrar Sesion", icon=ft.icons.LOGOUT_ROUNDED, on_click=sign_out)
                    ]
                )
            ]
        )
        page.update()

    return {
        "view": gazebo,
        "title": title,
        "load": on_page_load
    }
