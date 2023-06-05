import sys
import cv2 as cv
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
                             QVBoxLayout, QWidget)

import utils
import vimba_handler


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TAASView Controller')

        self.accessible_cams = None
        self.cam_buttons = []

        self.main_layout = QVBoxLayout()
        self.label1 = QLabel("Accessible Cameras")
        self.label1.setFont(QFont("Segoe UI", 12))
        self.label1.setStyleSheet("QLabel { color: #333333; }")
        self.main_layout.addWidget(self.label1)

        self.camera_button_layout = QVBoxLayout()  # New layout for camera buttons
        self.main_layout.addLayout(self.camera_button_layout)  # Add camera button layout to main layout

        self.main_layout.addStretch(1)  # Add stretchable space before the button

        self.update_cams_button = QPushButton('Update Cameras')
        self.update_cams_button.setStyleSheet(
            "QPushButton { background-color: #f8f8f8; border: 1px solid #c0c0c0; padding: 10px; "
            "font-size: 14px; } "
            "QPushButton:pressed { background-color: #c0c0c0; }"
        )
        self.main_layout.addWidget(self.update_cams_button)

        self.main_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.main_layout.addStretch(1)  # Add additional stretchable space after the button

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        # Set padding around the main widget
        self.main_layout_wrapper = QVBoxLayout()
        self.main_layout_wrapper.addWidget(self.main_widget)
        self.main_layout_wrapper.setContentsMargins(20, 20, 20, 20)  # Padding: left, top, right, bottom

        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(self.main_layout_wrapper)

        self.update_cams_button.clicked.connect(self.update_cams)  # Connect update_cams_button to update_cams method

        self.setFixedSize(200, 200)  # Initial fixed size

    def update_camera_buttons(self):
        # Clear existing buttons
        while self.camera_button_layout.count() > 0:
            item = self.camera_button_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if self.accessible_cams is not None:
            self.cam_buttons = []
            for cam_id in self.accessible_cams:
                button = QPushButton(cam_id)
                button.setStyleSheet(
                    "QPushButton { background-color: #f8f8f8; border: 1px solid #c0c0c0; padding: 10px; "
                    "font-size: 14px; } "
                    "QPushButton:pressed { background-color: #c0c0c0; }"
                )
                self.cam_buttons.append(button)
                self.camera_button_layout.addWidget(button)  # Add buttons to the camera button layout
                button.clicked.connect(self.myfun)
        else:
            self.label2 = QLabel("No cameras found")
            self.label2.setFont(QFont("Segoe UI", 8))
            self.label2.setStyleSheet("QLabel { color: #333333; }")
            self.camera_button_layout.addWidget(self.label2)  # Add label to the camera button layout

        self.update_window_size()  # Update the window size

    def update_cams(self):
        self.accessible_cams = vimba_handler.get_camera_id_list()
        self.update_camera_buttons()

    def update_window_size(self):
        num_cam_buttons = len(self.cam_buttons)
        button_height = 50
        padding = 20

        window_width = 200 + (2 * padding)
        window_height = 100 + (num_cam_buttons * button_height) + (2 * padding)

        self.setFixedSize(window_width, window_height)

    @pyqtSlot()
    def myfun(self):
        button = self.sender()
        print('Button clicked:', button.text())


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
