import yaml
import os
import subprocess
import threading
from ament_index_python import get_package_share_path
from user_controls.modelo import Modelo
from user_controls.robot import Robot
from user_controls.world import World
import time
import logging
import signal

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("flet").setLevel(logging.WARNING)

home_dir = os.path.expanduser('~')
robots_path = os.path.join(home_dir,'robotmap-data', "data",'robots_register.yaml')
models_path = os.path.join(home_dir,'robotmap-data', "data",'models_register.yaml')
worlds_path = os.path.join(home_dir,'robotmap-data', "data",'worlds_register.yaml')
gazebo_dir = os.path.join(home_dir,'robotmap-data','gazebo')
rutina_dir = os.path.join(home_dir,'robotmap-data','rutinas')

def configure_package():
    try:
        package_share_path = get_package_share_path('multi_robot_bringup')
        config_path = package_share_path / 'config'
        return str(config_path)
    except ValueError as e:
        print(f"Error al obtener la ruta del paquete: {e}")
        return None

def configure_rutina_path():
    try:
        package_share_path = get_package_share_path('multi_robot_master_slave')
        config_path = package_share_path / 'config'
        return str(config_path)
    except ValueError as e:
        print(f"Error al obtener la ruta del paquete: {e}")
        return None

def obtain_model_list() -> list:
    model_list = list()
    path = models_path
    # Verificar si el archivo existe
    if not os.path.exists(path):
        # Crear el archivo vacío
        with open(path, 'w') as file:
            data = {'models': list()}
            yaml.dump(data, file)
            return model_list
    with open(path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            if data is None or "models" not in data.keys():
                return []
            else:
                if data["models"]:
                    for modelo in data["models"]:
                        model_list.append(Modelo(modelo["name"], modelo["rutaURDF"], modelo["rutaSDF"], modelo['nav_path']))
                    return model_list
                else:
                    return model_list
        except yaml.YAMLError as e:
            print(f"Error en la lectura: {e}")
            return []
        
def model_to_yaml(modelo: Modelo) -> dict:
    return {
        'name': modelo.nombre,
        'rutaURDF': modelo.rutaURDF,
        'rutaSDF': modelo.rutaSDF,
        'nav_path': modelo.nav_path
    }

def add_model(modelo: Modelo):
    path = models_path
    modelos_old = list()
    with open(path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            modelos_old = data['models']
        except yaml.YAMLError as e:
            print(f"Error en la actualizacion: {e}")
    modelos_old.append(model_to_yaml(modelo))
    with open(path, 'w') as file:
            datos = {'models': modelos_old}
            yaml.dump(datos, file)

def obtain_robot_list() -> list:
    robot_list = list()
    path = robots_path
    # Verificar si el archivo existe
    if not os.path.exists(path):
        # Crear el archivo vacío
        with open(path, 'w') as file:
            data = {'robots': list()}
            yaml.dump(data, file)
            return robot_list
    with open(path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            if data is None or "robots" not in data.keys():
                return []
            else:
                if data["robots"]:
                    for robot in data["robots"]:
                        modelo_robot = Modelo(robot["model_name"], robot["model_urdf_path"], robot["model_sdf_path"], robot['model_nav_path'])
                        robot_list.append(Robot(robot["name"], modelo_robot, robot["control_type"], robot["has_camera"]))
                    return robot_list
                else:
                    return robot_list
        except yaml.YAMLError as e:
            print(f"Error en la lectura: {e}")
            return []

def robot_to_yaml(robot: Robot) -> dict:
    return {
        'name': robot.name,
        'control_type': robot.control_type,
        'has_camera': robot.has_camera,
        'model_name': robot.modelo.nombre,
        'model_urdf_path': robot.modelo.rutaURDF,
        'model_sdf_path': robot.modelo.rutaSDF,
        'model_nav_path': robot.modelo.nav_path
    }

def add_robot(robot: Robot):
    path = robots_path
    robots_old = list()
    with open(path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            robots_old = data['robots']
        except yaml.YAMLError as e:
            print(f"Error en la actualizacion: {e}")
    robots_old.append(robot_to_yaml(robot))
    with open(path, 'w') as file:
            datos = {'robots': robots_old}
            yaml.dump(datos, file)

def obtain_world_list() -> list:
    world_list = list()
    path = worlds_path
    if not os.path.exists(path):
        with open(path, 'w') as file:
            data = {'worlds': world_list}
            yaml.dump(data, file)
            return world_list
    with open(path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            if data is None or "worlds" not in data.keys():
                return []
            else:
                if data['worlds']:
                    for world in data['worlds']:
                        world_item = World(world['name'], world['world_path'], world['map_path'])
                        world_list.append(world_item)
                    return world_list
                else:
                    return world_list
        except yaml.YAMLError as e:
            print(f"Error en la lectura: {e}")
            return []

def add_world(world: World):
    path = worlds_path
    worlds_old = list()
    with open(path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            worlds_old = data['worlds']
        except yaml.YAMLError as e:
            print(f"Error en la actualizacion: {e}")
    worlds_old.append(world.to_yaml())
    with open(path, 'w') as file:
            datos = {'worlds': worlds_old}
            yaml.dump(datos, file)

def list_files_in_directory(directory_path: str) -> list:
    """
    List all .yaml or .yml files in the given directory.

    :param directory_path: Path to the directory.
    :return: List of .yaml or .yml file names in the directory.
    """
    try:
        # Verificar si el path proporcionado es un directorio
        response = list()
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"El path proporcionado no es un directorio: {directory_path}")
        
        # Obtener la lista de archivos .yaml en el directorio
        yaml_files = [
            f for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f)) and (f.endswith('.yaml'))
        ]
        for yaml in yaml_files:
            response.append(yaml.split(".")[0])
        return response
    except Exception as e:
        print(f"Error al listar archivos en el directorio: {e}")
        return []

def activate_running_field(config_path: str):
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

    except Exception as e:
        print(f"Error al intentar actualizar el campo 'running': {e}")

def disable_running_field(config_path: str):
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
            data['running'] = False
        else:
            print(f"El archivo YAML no contiene el campo 'running'. Añadiendo campo 'running'.")
            data['running'] = False

        # Escribir el archivo YAML actualizado
        with open(config_path, 'w') as file:
            yaml.safe_dump(data, file)

    except Exception as e:
        print(f"Error al intentar actualizar el campo 'running': {e}")

def launch_rutina(config_path: str, stop_event: threading.Event):
    """
    Launch a routine with the given configuration file.

    :param config_path: Path to the configuration file.
    :param stop_event: Event to signal when to stop the simulation.
    """
    try:
        # Construir el comando a ejecutar
        command = [
            "ros2", "run", "multi_robot_master_slave", "nav_master_slave.py",
            f"{config_path}"
        ]
        print("Corri la rutina")
        # Ejecutar el comando
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Esperar hasta que el evento de stop se establezca
        while not stop_event.is_set():
            if process.poll() is not None:  # Verificar si el proceso ha terminado
                break
        
        # Terminar el proceso si aún está corriendo
        if process.poll() is None:
            process.terminate()
            process.wait()

    except Exception as e:
        print(f"Error al intentar lanzar la simulación: {e}")

def obtain_robots_to_gz(name: str):
    path = gazebo_dir + "/" + name + ".yaml"
    robots = list()
    with open(path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            robots = data['robots']
            return robots
        except yaml.YAMLError as e:
            return []

def robots_to_analyze():
    robots = list()
    try:
        gz_files = list_files_in_directory(gazebo_dir)
        for file in gz_files:
            path = gazebo_dir + '/' + file + '.yaml'
            with open(path, 'r') as archivo:
                try:
                    data = yaml.safe_load(archivo)
                    running = data['running']
                    if running:
                        robots = data['robots']
                except yaml.YAMLError as e:
                    print(f"Error al obtener datos: {e}")
    except Exception as e:
        print(f'Error al obtener los robots: {e}')
    return robots

def launch_simulation(config_path: str, stop_event: threading.Event):
    """
    Launch a ROS2 simulation with the given configuration file.

    :param config_path: Path to the configuration file.
    :param stop_event: Event to signal when to stop the simulation.
    """
    process = None
    additional_pids = []

    try:
        # Comando para cargar el entorno de Gazebo
        gazebo_setup = "/usr/share/gazebo/setup.bash"
        source_command = f"source {gazebo_setup} && export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/path/to/your/packages"
        
        # Construir el comando a ejecutar
        command = f"{source_command} && ros2 launch multi_robot_bringup multi_robot_simulation.launch.py sim_param_file:={config_path} navigation:=true"
        
        logging.debug(f"Launching simulation with command: {command}")

        # Ejecutar el comando en un entorno bash
        process = subprocess.Popen(f"bash -c '{command}'", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        
        # Función para leer y registrar la salida del proceso
        def log_process_output(pipe, level):
            for line in iter(pipe.readline, ''):
                logging.log(level, line.strip())
                # Captura de PIDs adicionales de los servicios ROS2
                if 'node created' in line:
                    try:
                        pid = int(line.split('[')[-1].split(']')[0])
                        additional_pids.append(pid)
                    except ValueError:
                        logging.warning(f"Failed to parse PID from line: {line}")
            pipe.close()

        # Crear hilos para leer stdout y stderr
        stdout_thread = threading.Thread(target=log_process_output, args=(process.stdout, logging.INFO))
        stderr_thread = threading.Thread(target=log_process_output, args=(process.stderr, logging.ERROR))

        stdout_thread.start()
        stderr_thread.start()
        
        logging.info("Gazebo simulation started.")
        activate_running_field(config_path)

        # Esperar hasta que el evento de stop se establezca
        while not stop_event.is_set():
            if process.poll() is not None:  # Verificar si el proceso ha terminado
                logging.warning("Simulation process terminated unexpectedly.")
                break
            time.sleep(1)  # Añadir un pequeño retraso para evitar un bucle de espera ocupada

        # Comandos para detener gzclient y gzserver
        command_kill_gzclient = ["pkill", "gzclient"]
        command_kill_gzserver = ["pkill", "gzserver"]

        # Ejecutar los comandos de kill
        logging.debug("Killing gzclient and gzserver.")
        subprocess.run(command_kill_gzclient, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        subprocess.run(command_kill_gzserver, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        logging.info("Gazebo simulation stopped.")
        disable_running_field(config_path)
        
        # Terminar el proceso si aún está corriendo
        if process.poll() is None:
            logging.debug("Terminating simulation process.")
            process.terminate()
            process.wait()

        # Terminar los procesos adicionales
        for pid in additional_pids:
            try:
                logging.debug(f"Terminating additional process with PID: {pid}")
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                logging.warning(f"Process with PID: {pid} not found.")
            except Exception as e:
                logging.error(f"Error terminating additional process with PID: {pid}: {e}")

    except Exception as e:
        logging.error(f"Error while trying to launch the simulation: {e}")

    finally:
        # Asegurarse de limpiar recursos
        if process and process.poll() is None:
            logging.debug("Cleaning up simulation process.")
            process.terminate()
            process.wait()

        # Asegurarse de terminar los procesos adicionales
        for pid in additional_pids:
            try:
                logging.debug(f"Cleaning up additional process with PID: {pid}")
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                logging.warning(f"Process with PID: {pid} not found.")
            except Exception as e:
                logging.error(f"Error terminating additional process with PID: {pid}: {e}")

def get_namespaces():
    namespaces = list()
    robots_info = robots_to_analyze()
    for robot in robots_info:
        namespaces.append(robot['name'])
    return namespaces    

def get_topic_list():
    try:
        result = subprocess.run(['ros2', 'topic', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            topics = result.stdout.splitlines()
            return topics
        else:
            print("Error al obtener la lista de tópicos.")
            print("Error:", result.stderr)
            return []
    except Exception as e:
        print(f"Error al intentar obtener la lista de tópicos: {e}")
        return []
    
def get_odom_topics():
    odom_topics = []
    topics = get_topic_list()
    for topic in topics:
        if "odom" in topic:
            odom_topics.append(topic)
    return odom_topics

def get_camera_topics():
    camera_topics = []
    topics = get_topic_list()
    for topic in topics:
        if "image" in topic:
            camera_topics.append(topic)
    return camera_topics

def run_ros2_echo(topic: str, output_list: list, duration: int):
    # Crear un proceso de ros2 topic echo
    process = subprocess.Popen(['ros2', 'topic', 'echo', topic], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Leer la salida del proceso en un hilo separado
    def read_output():
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                output_list.append(output)
    # Iniciar el hilo para leer la salida
    read_thread = threading.Thread(target=read_output)
    read_thread.start()
    # Esperar durante la duración deseada
    time.sleep(duration)
    # Terminar el proceso y esperar a que el hilo termine
    process.terminate()
    read_thread.join()
    # Obtener la salida capturada
    output = ''.join(output_list)
    return output

def get_odom(topic: str, duration: int = 2):
    position = dict()
    position['x'] = 'N/A'
    position['y'] = 'N/A'
    position['z'] = 'N/A'
    try:
        output_list = []
        output = run_ros2_echo(topic, output_list, duration)
        new_position = extract_position_data(str(output))
        if new_position:
            return new_position
        else:
            return position
    except Exception as e:
        print(f"Error al intentar obtener la salida del tópico: {e}")
        return position
    
def extract_position_data(text: str):
    position = dict()
    found_position = False
    data = text.split('---')[0].split('\n')
    for line in data:
        if 'position:' in line.strip():
            found_position = True
            continue
        if found_position:
            if 'x:' in line:
                position['x'] = f"{float(line.split('x:')[1].strip()):.3f}"
            elif 'y:' in line:
                position['y'] = f"{float(line.split('y:')[1].strip()):.3f}"
            elif 'z:' in line:
                position['z'] = f"{float(line.split('z:')[1].strip()):.3f}"
                break  # Se han extraído todos los datos necesarios
    return position