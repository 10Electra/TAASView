import sys
from typing import Optional

import cv2 as cv
import numpy as np
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor, QImage, QPalette, QPixmap
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
                             QPushButton, QSlider, QVBoxLayout, QWidget)


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Python FoilCV")

        exposure_label = QLabel()
        exposure_label.setAlignment(Qt.AlignBottom)
        exposure_label.setText('Above Camera Exposure')
        
        self.exposure_val = QLabel()
        self.exposure_val.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.exposure_sldr = QSlider(Qt.Horizontal)
        self.exposure_sldr.setRange(70000,120000)
        self.exposure_sldr.setValue(70000)
        self.exposure_val.setText(str(70000))
        self.exposure_sldr.valueChanged.connect(self.update_exposure_val)
        self.exposure_sldr.setTickPosition(QSlider.TicksBelow)
        self.exposure_sldr.setTickInterval(10000)
        
        exposure_sldr_hbox = QHBoxLayout()
        exposure_sldr_hbox.setSpacing(10)
        exposure_sldr_hbox.addWidget(self.exposure_sldr)
        exposure_sldr_hbox.addWidget(self.exposure_val)
        
        exposure = QVBoxLayout()
        exposure.setSpacing(2)
        exposure.addWidget(exposure_label)
        exposure.addLayout(exposure_sldr_hbox)
        
        button_width = 130
        button_height = 38
        
        self.record_button = QPushButton("Record Video")
        self.record_button.setMinimumSize(button_width,button_height)
        
        self.cap_image = QPushButton("Save Image")
        self.cap_image.setMinimumSize(button_width,button_height)
        
        self.live_video = QPushButton("Live Video")
        self.live_video.setMinimumSize(button_width,button_height)
        self.live_video.setCheckable(True)
        
        self.buttons = [self.record_button,
                        self.cap_image,
                        self.live_video]
        
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.record_button)
        button_layout.addWidget(self.cap_image)
        button_layout.addWidget(self.live_video)
        button_layout.setSpacing(10)
        # Use button_layout.addStretch()?
        
        self.image = QLabel()
        
        self.status_label = QLabel()
        self.status_label.setText('Status: Idle')
        
        image_layout = QVBoxLayout()
        image_layout.addWidget(self.status_label)
        image_layout.addWidget(self.image)
        image_layout.setSpacing(5)
        
        self.splashscreen = cv.imread('splashscreen.png')
        self.set_image(self.splashscreen)
        
        main_layout = QHBoxLayout()
        control_layout = QVBoxLayout()
        control_layout.setSpacing(10)
        
        control_layout.addLayout(exposure)
        control_layout.addLayout(button_layout)

        main_layout.addLayout(control_layout)
        main_layout.addLayout(image_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        # widget.setMaximumSize(800,500)
        self.setCentralWidget(widget)
    
    def set_image(self, array: np.ndarray)->QPixmap:
        qimage = QImage(array, array.shape[1],array.shape[0], array.shape[1]*3,QImage.Format_RGB888)
        self.image.setPixmap(QPixmap(qimage))
        
    @pyqtSlot(QImage)
    def set_qimage(self, image: QImage):
        self.image.setPixmap(QPixmap.fromImage(image))
    
    def update_exposure_val(self,v):
        self.exposure_val.setText(str(v))
    
    def text_changed(self,s):
        print(s)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()