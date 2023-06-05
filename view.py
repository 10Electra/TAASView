import sys
from PyQt5 import QtGui

import cv2 as cv
from PyQt5.QtCore import Qt, QThreadPool, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
                             QPushButton, QVBoxLayout, QWidget)

import vimba_handler
from camera_view import CameraWindow
from runnables import CameraRunnable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TAASView Controller')

        self.pool = QThreadPool.globalInstance()
        self.accessible_cams = None
        self.cam_buttons = {}
        self.cam_windows = {}
        self.cam_threads = {}

        self.cam_connect_layout = QVBoxLayout()
        self.label1 = QLabel("Accessible Cameras")
        self.label1.setFont(QFont("Segoe UI", 12))
        self.label1.setStyleSheet("QLabel { color: #333333; }")
        self.cam_connect_layout.addWidget(self.label1)

        self.camera_button_layout = QVBoxLayout()  # New layout for camera buttons
        self.cam_connect_layout.addLayout(self.camera_button_layout)  # Add camera button layout to main layout

        # self.cam_connect_layout.addStretch(1)  # Add stretchable space before the button

        self.update_cams_button = QPushButton('Update Cameras')
        self.update_cams_button.setStyleSheet(
            "QPushButton { background-color: #f8f8f8; border: 1px solid #c0c0c0; padding: 10px; "
            "font-size: 14px; } "
            "QPushButton:pressed { background-color: #c0c0c0; }"
        )
        self.cam_connect_layout.addWidget(self.update_cams_button)

        self.cam_connect_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.cam_connect_layout.addStretch(1)  # Add additional stretchable space after the button
        
        self.cam_control_layout = QVBoxLayout()

        self.label2 = QLabel("All-Camera Control")
        self.label2.setFont(QFont("Segoe UI", 12))
        self.label2.setStyleSheet("QLabel { color: #333333; }")
        self.cam_control_layout.addWidget(self.label2)
        
        self.cam_control_layout.addStretch(1)
        
        self.record_button = QPushButton('Record Video')
        self.record_button.setStyleSheet(
            "QPushButton { background-color: #f8f8f8; border: 1px solid #c0c0c0; padding: 10px; "
            "font-size: 14px; } "
            "QPushButton:pressed { background-color: #c0c0c0; }"
        )
        self.cam_control_layout.addWidget(self.record_button)
        
        self.cam_connect_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        self.cam_control_layout.addStretch(1)
        
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.cam_connect_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.cam_control_layout)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        # Set padding around the main widget
        self.main_layout_wrapper = QVBoxLayout()
        self.main_layout_wrapper.addWidget(self.main_widget)
        self.main_layout_wrapper.setContentsMargins(20, 20, 20, 20)  # Padding: left, top, right, bottom

        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(self.main_layout_wrapper)

        self.update_cams_button.clicked.connect(self.update_cams)  # Connect update_cams_button to update_cams method

    def update_camera_buttons(self):
        # Clear existing buttons
        while self.camera_button_layout.count() > 0:
            item = self.camera_button_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if self.accessible_cams is not None:
            self.cam_buttons = {}
            for cam_id in self.accessible_cams:
                button = QPushButton(cam_id)
                button.setStyleSheet(
                    "QPushButton { background-color: #f8f8f8; border: 1px solid #c0c0c0; padding: 10px; "
                    "font-size: 14px; } "
                    "QPushButton:pressed { background-color: #c0c0c0; }"
                )
                self.cam_buttons[button] = cam_id
                self.camera_button_layout.addWidget(button)  # Add buttons to the camera button layout
                button.clicked.connect(self.open_cam)
        else:
            self.label2 = QLabel("No cameras found")
            self.label2.setFont(QFont("Segoe UI", 8))
            self.label2.setStyleSheet("QLabel { color: #333333; }")
            self.camera_button_layout.addWidget(self.label2)  # Add label to the camera button layout

    def update_cams(self):
        self.accessible_cams = vimba_handler.get_camera_id_list()
        self.update_camera_buttons()

    @pyqtSlot()
    def open_cam(self):
        cam_id = self.cam_buttons[self.sender()]
        if self.cam_windows.get(cam_id) is None:
            self.cam_windows[cam_id] = CameraWindow()
            self.cam_threads[cam_id] = CameraRunnable(cam_id)
            self.cam_threads[cam_id].signals.frame.connect(self.cam_windows[cam_id].set_qimage)
            self.pool.start(self.cam_threads[cam_id])
            
            self.cam_windows[cam_id].live_video.clicked.connect(self.cam_threads[cam_id].livestream_toggle)
            
            self.cam_windows[cam_id].show()

        else:
            self.cam_windows[cam_id] = None
            self.cam_threads[cam_id] = None
    
    def resizeEvent(self, a0) -> None:
        print([self.size().height(),self.size().width()])
        return super().resizeEvent(a0)
    
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
