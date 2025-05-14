import yaml
from funciones import gazebo_dir

def update_running_field(config_path: str):
    """
    Update the 'running' field in a YAML file to True.

    :param config_path: Path to the YAML configuration file.
    """
    try:
        # Leer el archivo YAML
        with open(config_path, 'r') as file:
            data = yaml.safe_load(file)
        
        # Verificar si el campo 'running' existe
        if 'running' in data:
            data['running'] = True
        else:
            print(f"El archivo YAML no contiene el campo 'running'. Añadiendo campo 'running'.")
            data['running'] = True

        # Escribir el archivo YAML actualizado
        with open(config_path, 'w') as file:
            yaml.safe_dump(data, file)

        print(f"El campo 'running' ha sido actualizado a True en {config_path}.")

    except Exception as e:
        print(f"Error al intentar actualizar el campo 'running': {e}")

# Ejemplo de uso
update_running_field(gazebo_dir + "/" + "prueba_1.yaml")


