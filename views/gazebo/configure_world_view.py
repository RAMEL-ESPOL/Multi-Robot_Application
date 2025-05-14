import flet as ft
from funciones import obtain_world_list, obtain_robot_list, gazebo_dir
from user_controls.world import World
from user_controls.robot import Robot
import yaml
from db.flet_pyrebase import PyrebaseWrapper

def ConfigureWorld(page: ft.Page, myPyrebase: PyrebaseWrapper):
    title = "Configurar mundos"

    world_list: list[World] = list()
    robot_list: list[Robot] = list()
    robot_configure_list: list = list()
    num_robots = 0
    widget_robots = ft.Column(
        controls=[ft.Text(value="No hay robots agregados")])

    def update_num_robots_input(value):
        nonlocal num_robots
        num_robots_input.value = str(value)
        num_robots = value
        num_robots_input.update()
        on_num_robots_input_change()

    def add_value_number(e):
        value = int(num_robots_input.value) + 1
        update_num_robots_input(value)

    def reduce_value_number(e):
        value = int(num_robots_input.value) - 1
        if value >= 0:
            update_num_robots_input(value)

    def close_dialog(e):
        page.dialog.open = False
        page.update()

    def build_table_robot(collection_robot):
        widget_robots.controls.clear()
        if collection_robot:
            for robot in collection_robot:
                widget_robots.controls.append(ft.Text(value=robot['name']))
        else:
            widget_robots.controls.append(ft.Text(value="No hay robots agregados"))
        widget_robots.update()

    def save_robot(e):
        robot = find_robot_by_name(robot_combobox.value, robot_list)
        info = robot.yaml_configure()
        info['x_pose'] = float(x_pose.value)
        info['y_pose'] = float(y_pose.value)
        info['z_pose'] = float(z_pose.value)
        info['yaw'] = float(yaw.value)
        info['rviz_view'] = str(rviz_view.value).lower()
        robot_configure_list.append(info)
        build_table_robot(robot_configure_list)
        page.dialog.open = False
        x_pose.value = ''
        robot_combobox.value = None
        y_pose.value = ''
        z_pose.value = ''
        yaw.value = ''
        rviz_view.value = False
        page.update()

    def write_gazebo_world(world: World, robots: list):
        path = gazebo_dir + '/' + save_path.value + '.yaml'
        print(path)
        with open(path, 'w') as file:
            datos = {'world': world.to_yaml(),
                     'robots': robots,
                     'running': False}
            yaml.dump(datos, file)

    def save_file(e):
        nonlocal robot_configure_list
        world = find_world_by_name(world_combobox.value, world_list)
        write_gazebo_world(world, robot_configure_list)
        robot_configure_list = []
        build_table_robot(robot_configure_list)
        update_num_robots_input(0)
        world_combobox.value = None
        page.dialog.open = False
        page.update()

    def find_robot_by_name(name: str, robots: list[Robot]) -> Robot:
        for robot in robots:
            if robot.name == name:
                return robot
    
    def find_world_by_name(name: str, worlds: list[World]) -> World:
        for world in worlds:
            if world.name == name:
                return world

    def save_configuration(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Guardar configuracion"),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        save_path
                    ]),
                width=300,
                height=200),
            actions=[
                ft.TextButton("Guardar", on_click=save_file),
                ft.TextButton("Cancelar", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog.open = True
        page.update()

    def on_num_robots_input_change():
        check_add_robot_button()
    
    def check_add_robot_button():
        if len(robot_configure_list) >= int(num_robots_input.value):
            add_robot_button.disabled = True
        else:
            add_robot_button.disabled = False
        add_robot_button.update()

    world_combobox = ft.Dropdown(
        label="Seleccionar Mundo",
        label_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        width=300,
        border_color=ft.colors.BLACK,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        bgcolor=ft.colors.BLUE_GREY_50,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK))
    label_num_robots = ft.Text(
        value="Numero de robots",
        style=ft.TextStyle(
            size=20,
            weight=ft.FontWeight.BOLD))
    num_robots_input = ft.TextField(
        value="0",
        text_align="center",
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        border_color=ft.colors.BLACK,
        disabled=True,
        text_style=ft.TextStyle(
            size=25,
            color=ft.colors.BLACK),
        on_change=lambda e: on_num_robots_input_change(),
        width=70)
    add_value = ft.IconButton(
        style=ft.ButtonStyle(
            color={"": ft.colors.GREEN}),
        scale=1.2,
        icon=ft.icons.ADD_CIRCLE,
        on_click=add_value_number)
    reduce_value = ft.IconButton(
        scale=1.2,
        style=ft.ButtonStyle(
            color={"": ft.colors.RED}),
        icon=ft.icons.REMOVE_CIRCLE,
        on_click=reduce_value_number)
    save_button = ft.ElevatedButton(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        name=ft.icons.SAVE,
                        size=18),
                    ft.Text(
                        value="Guardar",
                        size=18)],
                alignment=ft.MainAxisAlignment.CENTER),
            alignment=ft.alignment.center),
        on_click=save_configuration,
        width=200,
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),  
            color={"": ft.colors.WHITE},  
            bgcolor={"": ft.colors.BLUE_ACCENT_400}))
    robot_combobox = ft.Dropdown(
        label="Seleccionar Robot",
        label_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK,
        ),
        border_color=ft.colors.BLACK,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        bgcolor=ft.colors.BLUE_GREY_50,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        width=290,
        options=[ft.dropdown.Option(robot.name) for robot in robot_list])
    x_pose = ft.TextField(
        label="Pose X",
        label_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        border_color=ft.colors.BLACK,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        bgcolor=ft.colors.BLUE_GREY_50,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        width=90)
    y_pose = ft.TextField(
        label="Pose Y",
        label_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        border_color=ft.colors.BLACK,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        bgcolor=ft.colors.BLUE_GREY_50,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        width=90)
    z_pose = ft.TextField(
        label="Pose Z",
        label_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        border_color=ft.colors.BLACK,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        bgcolor=ft.colors.BLUE_GREY_50,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        width=90)
    yaw = ft.TextField(
        label="Yaw",
        label_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        border_color=ft.colors.BLACK,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        bgcolor=ft.colors.BLUE_GREY_50,
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        width=90)
    rviz_view = ft.Checkbox(
        label="Vista en RViz",
        shape=ft.BeveledRectangleBorder(radius=8),
        active_color=ft.colors.GREEN_400,
        value=False)
    save_path = ft.TextField(
        label="Nombre archivo configuracion")

    def add_robot(e):
        if len(robot_configure_list) < int(num_robots_input.value):
            page.dialog = ft.AlertDialog(
                title=ft.Text("Agregar robot"),
                content=ft.Container(
                    ft.Column(
                        controls=[
                            robot_combobox,
                            ft.Row(
                                controls=[
                                    x_pose,
                                    y_pose,
                                    z_pose,
                                ]
                            ),
                            yaw,
                            rviz_view
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
                        width=150,
                        height=40,
                        on_click=save_robot,
                        style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),  
                        color={"": ft.colors.BLACK},  
                        bgcolor={"": ft.colors.GREEN_ACCENT_400})),
                    ft.TextButton(
                        on_click=close_dialog,
                        content=ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Text("Cancelar", size=18)],
                                alignment=ft.MainAxisAlignment.CENTER),
                        alignment=ft.alignment.center), 
                        width=150,
                        height=40,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),  
                            color={"": ft.colors.BLACK},  
                            bgcolor={"": ft.colors.BLUE_GREY_200}))
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            page.dialog.open = True
            page.update()
        check_add_robot_button()
    
    add_robot_button = ft.ElevatedButton(
        on_click=add_robot,
        content=ft.Container(
            content=ft.Text(
                value="Agregar Robots",
                size=15),
            alignment=ft.alignment.center),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),  
            color={"": ft.colors.WHITE},  
            bgcolor={"": ft.colors.CYAN_ACCENT_700}),
        width=160)
    
    def go_gz_list(e):
        page.go("/environments")
        page.update()

    configure_view = ft.SafeArea(
        content=ft.Column(
            controls=[
                ft.Container(
                    height=10),
                ft.Container(
                    content=world_combobox,
                    alignment=ft.alignment.center),
                ft.Container(
                    content=label_num_robots,
                    alignment=ft.alignment.center),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            num_robots_input,
                            add_value,
                            reduce_value
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    alignment=ft.alignment.center),
                ft.Container(
                    content=widget_robots,
                    alignment=ft.alignment.center),  
                ft.Container(
                    content=add_robot_button,
                    alignment=ft.alignment.center),
                ft.Container(
                    height=30),
                ft.Container(
                    content=save_button,
                    alignment=ft.alignment.center)
            ],
            spacing=20
        )
    )

    def sign_out(e):
        myPyrebase.sign_out()
        page.go('/')
        page.update()

    def on_page_load():
        nonlocal robot_configure_list, num_robots, world_list, robot_list, num_robots_input
        robot_configure_list = []
        num_robots = 0
        num_robots_input.value = "0"
        widget_robots.controls.clear()
        world_combobox.value = None
        robot_combobox.value = None
        world_list = obtain_world_list()
        world_combobox.options = [ft.dropdown.Option(world.name) for world in world_list]
        robot_list = obtain_robot_list()
        robot_combobox.options = [ft.dropdown.Option(robot.name) for robot in robot_list]
        page.appbar = ft.AppBar(
            toolbar_height=65,
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK_ROUNDED,
                on_click=go_gz_list,
                scale=1.2),
            leading_width=60,
            title=ft.Text(
                value="Configurar Gazebo",
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
        "view": configure_view,
        "title": title,
        "load": on_page_load
    }
