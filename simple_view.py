import sys
from typing import Optional

import cv2 as cv
import numpy as np
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
                             QMainWindow, QPushButton, QScrollArea,
                             QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("TAASView ")

        button_width = 130
        button_height = 38

        self.live_video = QPushButton("Live Video")
        self.live_video.setMinimumHeight(38)
        # self.live_video.setMinimumSize(button_width, button_height)  # Remove this line

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)  # Center align the image within the label

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.live_video)
        main_layout.addWidget(self.image_label)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        self.splashscreen = cv.imread('splashscreen.png')
        self.set_image(self.splashscreen)

        self.setMinimumSize(200, 200)  # Set a minimum size for the window

    def set_image(self, array: np.ndarray):
        qimage = QImage(array, array.shape[1], array.shape[0], array.shape[1] * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        super(MainWindow, self).resizeEvent(event)
        self.set_image(self.splashscreen)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()




        
    # @pyqtSlot(QImage)
    # def set_qimage(self, image: QImage):
    #     self.image.setPixmap(QPixmap.fromImage(image))

    # def resizeEvent(self, event):
    #     self._image_size = [self.image.width(), self.image.height()]
    #     self.event_size = [event.size().width(), event.size().height()]
    #     print('Compare {} and {}.'.format(self._image_size,self.event_size))