import sys
import socket
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
    QFrame, QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer
import pygame

class PrototypeSoftware(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title and dimensions
        self.setWindowTitle('Prototype Software For Hydra')
        self.resize(1200, 800)
        self.setStyleSheet("""
            QWidget {
                background-color: #222831;
                color: #EEEEEE;
                font-family: Arial;
            }
            QLabel {
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #393E46;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                border: 2px solid transparent;
            }
            QPushButton:hover {
                background-color: #00ADB5;
                border: 2px solid white;
            }
            QPushButton:pressed {
                background-color: #007A85;
            }
            QFrame {
                background-color: #393E46;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout()

        # Heading
        heading = QLabel("Prototype Software For Hydra", self)
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setStyleSheet("font-size: 24px; font-weight: bold; color: #00ADB5;")
        main_layout.addWidget(heading)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #EEEEEE; height: 2px;")
        main_layout.addWidget(line)

        main_layout.addSpacing(20)

        # Video & 3D Image Sections
        horizontal_section = QHBoxLayout()

        left_section = QVBoxLayout()
        label_3d_image = QLabel("Video Captured From Raspberry Pi", self)
        label_3d_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_3d_image.setStyleSheet("border: 2px solid #00ADB5; border-radius: 10px;")
        label_3d_image.setFixedSize(500, 400)
        left_section.addWidget(label_3d_image)

        right_section = QVBoxLayout()
        label_camera = QLabel("3D Image Of The Video We Got", self)
        label_camera.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_camera.setStyleSheet("border: 2px solid #00ADB5; border-radius: 10px;")
        label_camera.setFixedSize(500, 400)
        right_section.addWidget(label_camera)

        horizontal_section.addLayout(left_section)
        horizontal_section.addLayout(right_section)
        main_layout.addLayout(horizontal_section)

        main_layout.addSpacing(20)

        # Controls Sections
        controls_section = QHBoxLayout()

        # Robotic Arm Controls
        robotics_arm_section = QVBoxLayout()
        robotics_arm_label = QLabel("Robotic Arm Controls", self)
        robotics_arm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        robotics_arm_layout = QGridLayout()
        self.joystick_up = QPushButton("Up", self)
        self.joystick_down = QPushButton("Down", self)
        self.joystick_left = QPushButton("Left", self)
        self.joystick_right = QPushButton("Right", self)

        robotics_arm_layout.addWidget(self.joystick_up, 0, 1)
        robotics_arm_layout.addWidget(self.joystick_left, 1, 0)
        robotics_arm_layout.addWidget(robotics_arm_label, 1, 1)
        robotics_arm_layout.addWidget(self.joystick_right, 1, 2)
        robotics_arm_layout.addWidget(self.joystick_down, 2, 1)

        robotics_arm_section.addLayout(robotics_arm_layout)

        # Thruster Controls
        thrusters_section = QVBoxLayout()
        thruster_label = QLabel("Thrusters Control", self)
        thruster_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        thrusters_layout = QGridLayout()
        self.thruster_up = QPushButton("Up", self)
        self.thruster_down = QPushButton("Down", self)
        self.thruster_left = QPushButton("Left", self)
        self.thruster_right = QPushButton("Right", self)

        thrusters_layout.addWidget(self.thruster_up, 0, 1)
        thrusters_layout.addWidget(self.thruster_left, 1, 0)
        thrusters_layout.addWidget(thruster_label, 1, 1)
        thrusters_layout.addWidget(self.thruster_right, 1, 2)
        thrusters_layout.addWidget(self.thruster_down, 2, 1)

        thrusters_section.addLayout(thrusters_layout)

        controls_section.addLayout(robotics_arm_section)
        controls_section.addLayout(thrusters_section)
        main_layout.addLayout(controls_section)

        # Grip Button
        grip_button_layout = QHBoxLayout()
        self.grip_button = QPushButton("Grip Open/Close", self)
        self.grip_button.setFixedSize(150, 50)
        grip_button_layout.addStretch(1)
        grip_button_layout.addWidget(self.grip_button)
        grip_button_layout.addStretch(1)
        main_layout.addLayout(grip_button_layout)

        self.setLayout(main_layout)

        # Initialize Pygame Joystick
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Joystick connected: {self.joystick.get_name()}")
        else:
            self.joystick = None
            print("No joystick detected")

        # Initialize socket connection to ESP32
        self.esp32_ip = '192.168.166.80'  # Replace with ESP32 IP
        self.esp32_port = 8080
        self.esp32_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_esp32()

        # Timer to poll joystick
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll_joystick)
        self.timer.start(100)

    def connect_to_esp32(self):
        try:
            self.esp32_socket.connect((self.esp32_ip, self.esp32_port))
            print("Connected to ESP32")
        except Exception as e:
            print(f"ESP32 Connection error: {e}")


    def send_command(self, command):
        try:
            # Send command to Raspberry Pi
            self.socket.sendall(command.encode('utf-8'))
            print(f"Command sent to Raspberry Pi: {command}")
        except Exception as e:
            print(f"Error sending command to Raspberry Pi: {e}")

        try:
            # Send command to ESP32
            self.esp32_socket.sendall(command.encode('utf-8'))
            print(f"Command sent to ESP32: {command}")
        except Exception as e:
            print(f"Error sending command to ESP32: {e}")


    def poll_joystick(self):
        if self.joystick:
            pygame.event.pump()  # Process events

            # Get joystick axes and buttons
            axes = [self.joystick.get_axis(i) for i in range(self.joystick.get_numaxes())]
            buttons = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]

            # Log buttons and axes for debugging
            print(f"Axes: {axes}")
            print(f"Buttons: {buttons}")

            # Axis-based control for Up/Down (axis 1) and Left/Right (axis 0)
            if axes[1] < -0.5:  # Move Up if axis 1 is less than -0.5
                print("Axis moved: Moving Up")
                self.send_command('a')
                self.joystick_up.setStyleSheet("background-color: yellow")
                QTimer.singleShot(100, lambda: self.joystick_right.setStyleSheet(""))   

                
            elif axes[1] > 0.5:  # Move Down if axis 1 is greater than 0.5
                print("Axis moved: Moving Down")
                self.send_command('b')
                self.joystick_down.setStyleSheet("background-color: yellow")
                QTimer.singleShot(100, lambda: self.joystick_right.setStyleSheet(""))   

            else:
                self.joystick_up.setStyleSheet("")
                self.joystick_down.setStyleSheet("")

            if axes[0] < -0.5:  # Move Left if axis 0 is less than -0.5
                print("Axis moved: Moving Left")
                self.send_command('c')
                self.joystick_right.setStyleSheet("background-color: yellow")
                QTimer.singleShot(100, lambda: self.joystick_right.setStyleSheet(""))   

            elif axes[0] > 0.5:
                print("Axis moved: Moving Right")
                self.send_command('d')
                self.joystick_right.setStyleSheet("background-color: yellow")
                QTimer.singleShot(100, lambda: self.joystick_right.setStyleSheet(""))   

            else:
                self.joystick_left.setStyleSheet("")
                self.joystick_right.setStyleSheet("")

            # Grip Control
            if buttons[6]:
                print("Grip Open!")
                self.send_command('x')
                self.grip_button.setStyleSheet("background-color: yellow")
            else:
                self.grip_button.setStyleSheet("")

            # Grip Control
            if buttons[7]:
                print("Grip close!")
                self.send_command('y')
                self.grip_button.setStyleSheet("background-color: yellow")
            else:
                self.grip_button.setStyleSheet("")

            # 360 Rotation Start
            if buttons[4]:
                print("Quit Command Pressed")
                self.send_command('q')
                self.grip_button.setStyleSheet("background-color: yellow")
            else:
                self.grip_button.setStyleSheet("")

# Main function to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create an instance of the window
    window = PrototypeSoftware()
    window.show()

    # Execute the application's main loop
    sys.exit(app.exec())