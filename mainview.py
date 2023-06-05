import sys

import cv2 as cv
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
                             QVBoxLayout, QWidget)

import utils
import vimba_handler


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TAASView Controller')
        
        self.update_cams()
        
        self.main_layout = QVBoxLayout()
        self.label1 = QLabel("Accessible Cameras")
        self.main_layout.addWidget(self.label1)
        
        if self.accessible_cams is not None:
            
            self.cam_buttons = []
            for cam_id in self.accessible_cams:
                button = QPushButton(cam_id)
                self.cam_buttons.append(button)
                self.main_layout.addWidget(button)
            
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.setMinimumSize(200, 200)
        
    def update_cams(self):
        self.accessible_cams = vimba_handler.get_camera_id_list()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
