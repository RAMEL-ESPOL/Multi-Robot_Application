import flet as ft
from db.flet_pyrebase import PyrebaseWrapper
import rclpy
from rclpy.node import Node
import subprocess
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import io
import base64
from PIL import Image as PILImage
import threading
from funciones import robots_to_analyze, get_odom_topics, get_camera_topics, get_odom
import time

class ImageSubscriber(Node):
    def __init__(self, topic_name, callback):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(
            Image,
            topic_name,
            self.listener_callback,
            10)
        self.bridge = CvBridge()
        self.callback = callback

    def listener_callback(self, msg):
        try:
            if msg.encoding == "32FC1":
                cv_image = self.bridge.imgmsg_to_cv2(msg, "passthrough")
                cv_image = np.uint8(cv_image * 255)
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2BGR)
            else:
                cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            self.get_logger().error(f"Could not convert image: {e}")
            return
        
        pil_image = PILImage.fromarray(cv_image)
        buffered = io.BytesIO()
        pil_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        self.callback(img_str)

def start_subscriber(node_class, *args):
    if not rclpy.ok():
        rclpy.init()
    node = node_class(*args)
    rclpy.spin(node)
    node.destroy_node()

def stop_subscriber():
    rclpy.shutdown()

def MonitorView(page: ft.Page, myPyrebase: PyrebaseWrapper):
    title = "Monitoreo de tareas"

    camera_topics = list()
    robots = list()
    odom_timers = list()
    odom_topics = list()
    robot_positions = dict()

    table_thread = None

    image_process = ft.Image(
        src=f"/images/no_image.jpeg",
        fit=ft.ImageFit.FILL,
        width=300,
        height=300,
        expand=1)

    def update_image(base64_str):
        if image_process.page is not None:
            image_process.src_base64 = base64_str
            image_process.update()

    def actualize_image(e):
        topic_name = dropdown_camera.value
        if topic_name:
            if hasattr(page, 'image_thread') and page.image_thread.is_alive():
                page.image_thread.do_run = False
                stop_subscriber()
                page.image_thread.join()
            
            def thread_target():
                start_subscriber(ImageSubscriber, topic_name, update_image)
            
            page.image_thread = threading.Thread(target=thread_target)
            page.image_thread.start()

    dropdown_camera = ft.Dropdown(
        label="Elige un tópico",
        label_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK,
        ),
        border_color=ft.colors.BLACK,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        hint_text="No seleccionado",
        text_style=ft.TextStyle(
            size=16,
            color=ft.colors.BLACK),
        width=500,
        options=[ft.dropdown.Option(topic) for topic in camera_topics],
        on_change=actualize_image
    )

    robot_listview = ft.ListView(
        spacing=10,
        padding=20,
        auto_scroll=False,
        height=250,
        width=600)
    
    def update_position():
        nonlocal robot_positions, odom_topics,robots
        for odom_topic in odom_topics:
            namespace = odom_topic.split('/')[1]
            for robot in robots:
                name = robot['name']
                if name == namespace:
                    robot_positions[name] = get_odom(odom_topic)

    def build_table():
        nonlocal robot_listview, robots, robot_positions
        actualize = True
        update_position()
        for robot in robots:
            x = robot_positions[robot['name']]['x']
            y = robot_positions[robot['name']]['y']
            if x == 'N/A' or y == 'N/A':
                actualize = False
        if actualize:
            robot_listview.controls.clear()
            encabezado = ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            value="Robot", 
                            expand=1,
                            text_align=ft.TextAlign.CENTER,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_500,
                                color=ft.colors.GREY_100)),
                        bgcolor=ft.colors.GREY_600,
                        padding=10,
                        border_radius=ft.BorderRadius(5, 5, 5, 5),
                        expand=2,
                        alignment=ft.alignment.center),
                    ft.Container(
                        content=ft.Text(
                            value="Pos X",
                            expand=1,
                            text_align=ft.TextAlign.CENTER,
                            style=ft.TextStyle(
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=ft.colors.GREY_100)),
                        padding=10,
                        expand=1,
                        alignment=ft.alignment.center,
                        border_radius=ft.BorderRadius(5, 5, 5, 5),
                        bgcolor=ft.colors.GREY_600),
                    ft.Container(
                        content=ft.Text(
                            value="Pos Y",
                            expand=1,
                            text_align=ft.TextAlign.CENTER,
                            style=ft.TextStyle(
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=ft.colors.GREY_100)),
                        padding=10,
                        expand=1,
                        bgcolor=ft.colors.GREY_600,
                        border_radius=ft.BorderRadius(5, 5, 5, 5),
                        alignment=ft.alignment.center)],
                height=45,
                width=700,
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER)
            robot_listview.controls.append(encabezado)
            for robot in robots:
                namespace = robot['name']
                pos_x = robot_positions[namespace]['x']
                pos_y = robot_positions[namespace]['y']
                fila = ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            value=namespace, 
                            expand=1,
                            text_align=ft.TextAlign.CENTER,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.NORMAL,
                                color=ft.colors.BLACK)),
                        bgcolor=ft.colors.GREY_300,
                        padding=10,
                        expand=2,
                        border_radius=ft.BorderRadius(5, 5, 5, 5),
                        alignment=ft.alignment.center),
                    ft.Container(
                        content=ft.Text(
                            value=str(pos_x),
                            expand=1,
                            text_align=ft.TextAlign.CENTER,
                            style=ft.TextStyle(
                                size=14,
                                weight=ft.FontWeight.NORMAL,
                                color=ft.colors.BLACK)),
                        padding=10,
                        expand=1,
                        alignment=ft.alignment.center,
                        border_radius=ft.BorderRadius(5, 5, 5, 5),
                        bgcolor=ft.colors.GREY_300),
                    ft.Container(
                        content=ft.Text(
                            value=str(pos_y),
                            expand=1,
                            text_align=ft.TextAlign.CENTER,
                            style=ft.TextStyle(
                                size=14,
                                weight=ft.FontWeight.NORMAL,
                                color=ft.colors.BLACK)),
                        padding=10,
                        expand=1,
                        bgcolor=ft.colors.GREY_300,
                        border_radius=ft.BorderRadius(5, 5, 5, 5),
                        alignment=ft.alignment.center)],
                height=45,
                width=700,
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER)
                robot_listview.controls.append(fila)
            robot_listview.update()
        threading.Timer(10, build_table).start()

    def cleanup_threads():
        nonlocal table_thread
        if hasattr(page, 'image_thread') and page.image_thread.is_alive():
            page.image_thread.do_run = False
            stop_subscriber()
            page.image_thread.join()
        for timer in odom_timers:
            timer.cancel()
        odom_timers.clear()

    def return_home(e):
        cleanup_threads()
        page.go("/home")
        page.update()

    def sign_out(e):
        cleanup_threads()
        myPyrebase.sign_out()
        page.go("/")
        page.update()

    def on_page_load():
        nonlocal robots, camera_topics, image_process, dropdown_camera, odom_topics, odom_timers, robot_positions, table_thread
        dropdown_camera.value = None
        image_process.src = f"/images/no_image.jpeg"
        camera_topics = get_camera_topics()
        robots = robots_to_analyze()
        odom_topics = get_odom_topics()
        dropdown_camera.options = [ft.dropdown.Option(topic) for topic in camera_topics]

        for robot in robots:
            robot_positions[robot['name']] = dict()
            robot_positions[robot['name']]['x'] = 'N/A'
            robot_positions[robot['name']]['y'] = 'N/A'
            
        threading.Timer(10, build_table).start()

        page.appbar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.icons.HOME, 
                on_click=return_home),
            toolbar_height=60,
            title=ft.Text(
                value="Monitoreo de datos",
                style=ft.TextStyle(
                    size=40,
                    weight=ft.FontWeight.BOLD)),
            center_title=True,
            bgcolor=ft.colors.GREY_200,
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text=str(myPyrebase.email)),
                        ft.PopupMenuItem(
                            text="Cerrar Sesión",
                            icon=ft.icons.LOGOUT_ROUNDED,
                            on_click=sign_out)])])
        build_table()
        page.update()

    monitor_view = ft.SafeArea(
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=40,
            controls=[
                ft.Container(
                    content=dropdown_camera,
                    alignment=ft.alignment.center),
                ft.Container(
                    content=image_process,
                    alignment=ft.alignment.center),
                ft.Container(
                    content=robot_listview,
                    alignment=ft.alignment.center)
            ]
        )
    )

    return {
        "view": monitor_view,
        "title": title,
        "load": on_page_load
    }
