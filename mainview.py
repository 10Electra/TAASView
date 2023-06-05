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

        self.update_cams()

        self.main_layout = QVBoxLayout()
        self.label1 = QLabel("Accessible Cameras")
        self.label1.setFont(QFont("Segoe UI", 12))
        self.label1.setStyleSheet("QLabel { color: #333333; }")
        self.main_layout.addWidget(self.label1)

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
                self.main_layout.addWidget(button)
                button.clicked.connect(self.myfun)

        self.main_layout.addStretch(1)
        self.main_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.setFixedSize(200, 200)

    def update_cams(self):
        self.accessible_cams = vimba_handler.get_camera_id_list()

    @pyqtSlot()
    def myfun(self):
        button = self.sender()
        print('Button clicked:', button.text())


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
