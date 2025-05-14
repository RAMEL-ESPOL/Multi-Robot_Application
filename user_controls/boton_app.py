from flet_core.types import OptionalEventCallable
import flet as ft
from typing import Optional

class Boton(ft.ElevatedButton):
    def __init__(self, text: str, on_click: OptionalEventCallable = None, icon: Optional[str] = None):
        super().__init__()
        self.bgcolor = ft.colors.ON_PRIMARY_CONTAINER
        self.color = ft.colors.WHITE70
        self.height = 50
        self.width = 180
        self.elevation = 10
        self.text = text
        self.scale = 1
        self.on_click = on_click
        self.icon = icon
        
def main(page: ft.Page):
    def ok_clicked(e):
        print("OK clicked")
    
    page.add(
        Boton(
            text="Prueba",
            on_click=ok_clicked))

ft.app(target=main)