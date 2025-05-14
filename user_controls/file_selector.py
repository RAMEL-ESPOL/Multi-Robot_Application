import flet as ft
import subprocess

def open_file_explorer() -> str:
    try:
        result = subprocess.run(['zenity', '--file-selection'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            file_path = result.stdout.decode('utf-8').strip()
            return file_path
        else:
            return ""
    except Exception as e:
        return ""

class FileSelector(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.file_path_text = str()
        self.file_path_label = ft.Text(
            value="Seleccionar Archivo", 
            expand=2)
        self.select_button = ft.IconButton(icon=ft.icons.ARROW_CIRCLE_RIGHT_OUTLINED, on_click=self.select_file, expand=1, scale=1.2)

    def select_file(self, e):
        file_path = open_file_explorer()
        self.file_path_text = file_path
        self.file_path_label.value = "Ruta seleccionada correctamente"
        self.file_path_label.update()

    def build(self):
        return ft.Row(
            controls=[
                self.file_path_label,
                self.select_button],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    
    def reset(self):
        self.file_path_text = str()
        self.file_path_label.value = "Seleccionar Archivo"
        self.file_path_label.update()