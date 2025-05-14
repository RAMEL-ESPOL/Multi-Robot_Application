import flet as ft
import yaml
from user_controls.robot import Robot
from user_controls.world import World
from funciones import list_files_in_directory, obtain_robots_to_gz, rutina_dir, gazebo_dir
from db.flet_pyrebase import PyrebaseWrapper

def ConfigureRutina(page: ft.Page, myPyrebase: PyrebaseWrapper):
    title = "Configurar rutina"

    num_poses = 0
    entornos_files = []
    robot_list = []
    current_robot = dict()
    robot_info = dict()
    
    def actualize_robots(e):
        nonlocal robot_list
        robot_list.clear()
        robot_list = obtain_robots_to_gz(str(dropdown_entorno.value))
        dropdown_robot.options = [ft.dropdown.Option(robot["name"]) for robot in robot_list]
        dropdown_master.options = [ft.dropdown.Option(robot["name"]) for robot in robot_list]
        for robot in robot_list:
            if not robot["name"] in robot_info.keys():
                robot_info[robot["name"]] = dict()
                robot_info[robot["name"]]['poses'] = list()
        dropdown_robot.update()
        dropdown_master.update()

    def actualize_robot_current(e):
        nonlocal current_robot
        check_camera.disabled = False
        for robot in robot_list:
            if robot["name"] == dropdown_robot.value:
                current_robot = robot
        if not current_robot["has_camera"]:
            check_camera.disabled = True
            check_camera.value = False
        check_camera.update()
    
    dropdown_entorno = ft.Dropdown(
        label="Selecciona Entorno",
        label_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        border_color=ft.colors.BLACK,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        bgcolor=ft.colors.BLUE_GREY_50,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        hint_text='No Seleccionado',
        width=300,
        on_change=actualize_robots)
    
    dropdown_robot = ft.Dropdown(
        label="Elige un Robot",
        label_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        border_color=ft.colors.BLACK,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        bgcolor=ft.colors.BLUE_GREY_50,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        hint_text='No Seleccionado',
        width=300,
        on_change=actualize_robot_current)
    
    dropdown_master = ft.Dropdown(
        label="Nombre Master",
        label_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        border_color=ft.colors.BLACK,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        bgcolor=ft.colors.BLUE_GREY_50,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        hint_text="No Seleccionado",
        width=300,
        disabled=False)
    
    def change_master(e):
        if check_master.value:
            dropdown_master.disabled = True
            dropdown_master.value = None
            check_hierarchy.disabled = False
            check_max_time.disabled = True
            add_num_pose_button.disabled = True
            remove_num_pose_button.disabled = True
            add_pose.disabled = True
        else:
            check_hierarchy.value = True
            dropdown_master.disabled = False
            check_hierarchy.disabled = True
            check_max_time.disabled = False
            add_num_pose_button.disabled = False
            remove_num_pose_button.disabled = False
            add_pose.disabled = False
        dropdown_master.update()
        check_hierarchy.update()
        check_max_time.update()
        add_num_pose_button.update()
        remove_num_pose_button.update()
        add_pose.update()

    check_master = ft.Checkbox(
        label="Es master?",
        shape=ft.BeveledRectangleBorder(radius=8),
        active_color=ft.colors.GREEN_400,
        value=False,
        on_change=change_master)
    
    def change_max_time(e):
        duration_time.disabled = True
        duration_time.value = 0
        if check_max_time.value:
            duration_time.disabled = False
        duration_time.update()

    def update_poses(value: int):
        nonlocal num_poses
        num_poses = value
        pose_goals_field.value = str(value)
        pose_goals_field.update()

    def add_num_poses(e):
        value = int(pose_goals_field.value) + 1
        update_poses(value)

    def remove_num_poses(e):
        value = int(pose_goals_field.value) - 1
        if not value < 0:
            update_poses(value)

    check_camera = ft.Checkbox(
        label="Usa camara",
        shape=ft.BeveledRectangleBorder(radius=8),
        active_color=ft.colors.GREEN_400,
        value=False)
    
    check_max_time = ft.Checkbox(
        label="Usa tiempo max",
        shape=ft.BeveledRectangleBorder(radius=8),
        active_color=ft.colors.GREEN_400,
        value=False,
        on_change=change_max_time)
    
    check_hierarchy = ft.Checkbox(
        label="Hereda tiempo",
        shape=ft.BeveledRectangleBorder(radius=8),
        active_color=ft.colors.GREEN_400,
        value=True,
        disabled=True)
    
    duration_time = ft.TextField(
        label="Duracion (min)",
        text_align="center",
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        border_color=ft.colors.BLACK,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        value="0",
        width=100,
        disabled=True)
    
    pose_goals_field = ft.TextField(
        label="Poses goals",
        width=80,
        height=60,
        text_align="center",
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        border_color=ft.colors.BLACK,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        value="0",
        disabled=True)
    
    add_num_pose_button = ft.IconButton(
        icon=ft.icons.ADD_CIRCLE,
        style=ft.ButtonStyle(
            color={"": ft.colors.GREEN}),
        scale=1.2,
        on_click=add_num_poses)
    
    remove_num_pose_button = ft.IconButton(
        icon=ft.icons.REMOVE_CIRCLE,
        scale=1.2,
        style=ft.ButtonStyle(
            color={"": ft.colors.RED}),
        on_click=remove_num_poses)
    
    pose_table = ft.Column(
        width=500,
        height=200,
        alignment=ft.MainAxisAlignment.CENTER)
    
    x_pose = ft.TextField(
        label="Pose X",
        text_align="center",
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        border_color=ft.colors.BLACK,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        width=80)
    
    y_pose = ft.TextField(
        label="Pose Y",
        text_align="center",
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        border_color=ft.colors.BLACK,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        width=80)
    
    z_pose = ft.TextField(
        label="Pose Z",
        text_align="center",
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        border_color=ft.colors.BLACK,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        width=80)
    
    yaw = ft.TextField(
        label="Yaw",
        text_align="center",
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        border_color=ft.colors.BLACK,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        width=80)

    def configure_pose(e):
        page.dialog = ft.AlertDialog(
            modal=True,
            elevation=20,
            title=ft.Text("Agregar pose"),
            title_padding=15,
            content=ft.Container(
                width=400,
                height=200,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                x_pose,
                                y_pose,
                                z_pose]),
                        yaw])),
            actions=[
                ft.TextButton("Guardar", on_click=save_pose),
                ft.TextButton("Cancelar", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END)
        page.dialog.open = True
        page.update()

    def build_table_pose():
        nonlocal current_robot, robot_info
        pose_table.controls.clear()
        poses = robot_info[current_robot["name"]]['poses']
        for pose in poses:
            id_pose = str(pose["id"])
            pose_table.controls.append(
                ft.Text(
                    value=f"Pose {id_pose}"))
        pose_table.update()

    def save_pose(e):
        nonlocal robot_info, current_robot
        id_pose = len(robot_info[current_robot["name"]]['poses']) + 1
        pose = {
            "id": id_pose,
            "x": float(x_pose.value),
            "y": float(y_pose.value),
            "z": float(z_pose.value),
            "yaw": float(yaw.value)}
        robot_info[current_robot["name"]]['poses'].append(pose)
        build_table_pose()
        x_pose.value = None
        y_pose.value = None
        z_pose.value = None
        yaw.value = None
        page.dialog.open = False
        page.update()

    def close_dialog(e):
        x_pose.value = None
        y_pose.value = None
        z_pose.value = None
        yaw.value = None
        page.dialog.open = False
        page.update()
    
    add_pose = ft.IconButton(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        name=ft.icons.ADD,
                        size=11),
                    ft.Text(
                        value="Agregar pose",
                        size=12,
                        style=ft.TextStyle(
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE))],
                alignment=ft.MainAxisAlignment.CENTER),
            alignment=ft.alignment.center),
        width=130,
        height=35,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),  
            color={"": ft.colors.WHITE},  
            bgcolor={"": ft.colors.BLUE_ACCENT_400}),
        on_click=configure_pose)
    
    def save_configuration_robot(e):
        nonlocal current_robot, robot_info, num_poses
        robot_info[current_robot["name"]]["is_master"] = check_master.value
        robot_info[current_robot["name"]]["has_camera"] = current_robot["has_camera"]
        robot_info[current_robot["name"]]["same_time_task"] = check_hierarchy.value
        if not check_master.value:
            robot_info[current_robot["name"]]["name_master"] = dropdown_master.value
            robot_info[current_robot["name"]]["has_max_time"] = check_max_time.value
            robot_info[current_robot["name"]]["duration_max_time"] = float(duration_time.value)
            robot_info[current_robot["name"]]["use_camera"] = check_camera.value
        check_camera.value = False
        check_master.value = False
        dropdown_master.value = None
        check_max_time.value = False
        duration_time.value = 0
        pose_goals_field.value = 0
        num_poses = 0
        dropdown_robot.value = None
        add_num_pose_button.disabled = False
        add_pose.disabled = False
        remove_num_pose_button.disabled = False
        print(robot_info)
        page.update()

    file_name_rutina = ft.TextField(
        label="Nombre del archivo")

    def write_rutina(e):
        nonlocal robot_info
        path = rutina_dir + '/' + file_name_rutina.value + '.yaml'
        data = []
        for robot_name in robot_info.keys():
            robot_data = dict()
            robot_data['name'] = robot_name
            robot_data['is_master'] = robot_info[robot_name]['is_master']
            robot_data['has_camera'] = robot_info[robot_name]['has_camera']
            if not robot_info[robot_name]['is_master']:
                robot_data['name_master'] = robot_info[robot_name]['name_master']
                robot_data['has_max_time'] = robot_info[robot_name]['has_max_time']
                robot_data['duration_max_time'] = robot_info[robot_name]['duration_max_time']
                robot_data['use_camera'] = robot_info[robot_name]['use_camera']
                for pose in robot_info[robot_name]['poses']:
                    name = "pose_goal_" + str(pose['id'])
                    robot_data[name] = dict()
                    robot_data[name]['x'] = pose['x']
                    robot_data[name]['y'] = pose['y']
                    robot_data[name]['z'] = pose['z']
                    robot_data[name]['yaw'] = pose['yaw']
            else:
                robot_data['same_time_task'] = robot_info[robot_name]['same_time_task']
            data.append(robot_data)
        with open(path, 'w') as file:
            datos = {'robots': data}
            yaml.dump(datos, file)
        
    def finish_configuration(e):
        page.dialog = ft.AlertDialog(
            modal=True,
            elevation=20,
            title=ft.Text("Guardar rutina"),
            title_padding=15,
            content=ft.Container(
                width=400,
                height=200,
                content=file_name_rutina),
            actions=[
                ft.TextButton("Guardar", on_click=write_rutina),
                ft.TextButton("Cancelar", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END)
        page.dialog.open = True
        page.update()
    
    save_button = ft.TextButton(
        text="Guardar",
        on_click=save_configuration_robot)
    
    finish_button = ft.TextButton(
        text="Finalizar",
        on_click=finish_configuration)
    
    def go_list_rutinas(e):
        page.go("/rutina")
        page.update()

    def sign_out(e):
        myPyrebase.sign_out()
        page.go('/')
        page.update()

    def on_page_load():
        page.window_min_width, page.window_max_width = 400, 400
        page.window_min_height, page.window_max_height = 400, 400
        nonlocal entornos_files
        entornos_files = list_files_in_directory(gazebo_dir)
        dropdown_entorno.options = [ft.dropdown.Option(name) for name in entornos_files]
        page.appbar = ft.AppBar(
            toolbar_height=65,
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK_ROUNDED,
                on_click=go_list_rutinas,
                scale=1.2),
            leading_width=60,
            title=ft.Text(
                value="Configurar rutina",
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
                            text=str(myPyrebase.email)),
                        ft.PopupMenuItem(
                            text="Cerrar Sesion",
                            icon=ft.icons.LOGOUT_ROUNDED,
                            on_click=sign_out)])])
        page.update()
    
    rutina_view = ft.SafeArea(
        expand=True,
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Container(
                    height=10),
                ft.Container(
                    content=dropdown_entorno,
                    alignment=ft.alignment.center_left),
                ft.Row(
                    spacing=30,
                    controls=[
                        dropdown_robot,
                        ft.Container(
                            content=check_camera,
                            alignment=ft.alignment.center)
                    ]),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=30,
                    controls=[
                        check_master,
                        dropdown_master,
                        check_hierarchy]),
                ft.Row(
                    controls=[
                        check_max_time,
                        duration_time],
                    alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=add_num_pose_button,
                            alignment=ft.alignment.center),
                        ft.Container(
                            content=pose_goals_field,
                            alignment=ft.alignment.center),
                        ft.Container(
                            content=remove_num_pose_button,
                            alignment=ft.alignment.center)],
                    alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        pose_table,
                        ft.Container(
                            alignment=ft.alignment.center,
                            content=add_pose)]),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        save_button,
                        finish_button])
            ]))

    return {
        "view": rutina_view,
        "title": title,
        "load": on_page_load
    }
