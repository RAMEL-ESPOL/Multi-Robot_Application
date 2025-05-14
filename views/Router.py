import flet as ft
import os

from db.flet_pyrebase import PyrebaseWrapper

# views
from views.login.login_view import LoginView
from views.register.register_view import RegisterView
from views.home.home_view import HomeView
from views.modelo.modelo_view import ModeloView
from views.worlds.worlds_view import WorldsView
from views.gazebo.configure_world_view import ConfigureWorld
from views.gazebo.execute_gazebo import ExecuteGazebo
from views.rutina.configure_rutina import ConfigureRutina
from views.rutina.execute_rutina import ExecuteRutina
from views.dashboard.monitor_view import MonitorView

home_dir = os.path.expanduser('~')
robotmap_data_dir = os.path.join(home_dir, "robotmap-data")
data_dir = os.path.join(robotmap_data_dir, "data")
gazebo_dir = os.path.join(robotmap_data_dir, "gazebo")
rutina_dir = os.path.join(robotmap_data_dir, "rutinas")

if not os.path.exists(robotmap_data_dir):
    os.makedirs(robotmap_data_dir)

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if not os.path.exists(gazebo_dir):
    os.makedirs(gazebo_dir)

if not os.path.exists(rutina_dir):
    os.makedirs(rutina_dir)

class Router:

    def __init__(self, page: ft.Page, myPyrebase: PyrebaseWrapper):
        self.page = page
        self.routes = {
            "/": LoginView(page, myPyrebase),
            "/home": HomeView(page, myPyrebase),
            "/add_model": ModeloView(page, myPyrebase),
            "/register": RegisterView(page, myPyrebase),
            "/worlds": WorldsView(page, myPyrebase),
            "/environments": ExecuteGazebo(page, myPyrebase),
            "/config_gz": ConfigureWorld(page, myPyrebase),
            "/rutina": ExecuteRutina(page, myPyrebase),
            "/config_rutina": ConfigureRutina(page, myPyrebase),
            "/monitor": MonitorView(page, myPyrebase)
        }
        self.body = ft.Container(content=self.routes['/']["view"])

    def route_change(self, route):
        self.body.content = self.routes[route.route].get("view")
        self.page.title = self.routes[route.route].get("title")
        if self.routes[route.route].get("load"):
            self.routes[route.route].get("load")()
        self.page.update()
        