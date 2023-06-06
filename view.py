import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
                             QPushButton, QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle('TAASView Controller')
        self.cam_buttons = {}
        
        self.init_cam_connect_widgets()
        self.init_cam_control_widgets()
        self.init_main_widgets()
        
    def init_cam_connect_widgets(self) -> None:
        self.cam_connect_layout = QVBoxLayout()
        self.label1 = QLabel("Accessible Cameras")
        self.label1.setFont(QFont("Segoe UI", 12))
        self.label1.setStyleSheet("QLabel { color: #333333; }")
        self.cam_connect_layout.addWidget(self.label1)

        self.camera_button_layout = QVBoxLayout()
        self.cam_connect_layout.addLayout(self.camera_button_layout)

        self.update_cams_button = QPushButton('Update Cameras')
        self.update_cams_button.setStyleSheet(
            "QPushButton { background-color: #f8f8f8; border: 1px solid #c0c0c0; padding: 10px; "
            "font-size: 14px; } "
            "QPushButton:pressed { background-color: #c0c0c0; }"
        )
        self.cam_connect_layout.addWidget(self.update_cams_button)

        self.cam_connect_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.cam_connect_layout.addStretch(1)
    
    def init_cam_control_widgets(self) -> None:
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
        
        self.cam_control_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        self.cam_control_layout.addStretch(1)
        
    def init_main_widgets(self) -> None:
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.cam_connect_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.cam_control_layout)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        self.main_layout_wrapper = QVBoxLayout()
        self.main_layout_wrapper.addWidget(self.main_widget)
        self.main_layout_wrapper.setContentsMargins(20, 20, 20, 20)

        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(self.main_layout_wrapper)

    
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())