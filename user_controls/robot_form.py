import flet as ft
from user_controls.robot import Robot

class RobotForm(ft.Row):
    def __init__(self, robot_list: list[Robot], num_robots: int):
        super().__init__()
        self.robot_list = robot_list
        self.num_robots = num_robots
        self.dropdown_robot_num = ft.Dropdown(options=[ft.dropdown.Option(f"Robot {n+1}") for n in range(num_robots)])
        self.dropdown_select_robot = ft.Dropdown(options=[ft.dropdown.Option(robot.name) for robot in robot_list])
        self.x_pose = ft.TextField(label="X pose")
        self.y_pose = ft.TextField(label="Y pose")
        self.z_pose = ft.TextField(label="Z pose")
        self.yaw = ft.TextField(label="Yaw")
        self.rviz_view = ft.Checkbox(label="Rviz view", value=False)
        self.controls = [
            self.dropdown_robot_num,
            self.dropdown_select_robot,
            self.x_pose,
            self.y_pose,
            self.z_pose,
            self.yaw,
            self.rviz_view]

    def build(self):
        return super().build()