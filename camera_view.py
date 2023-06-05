import sys
from PyQt5 import QtGui

import cv2 as cv
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QObject
from PyQt5.QtGui import QImage, QPixmap, QCloseEvent
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
                             QVBoxLayout, QWidget)

import utils

class Signals(QObject):
    closed = pyqtSignal()
    
class CameraWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.signals = Signals()

        self.live_video = QPushButton("Live Video")
        self.live_video.setMinimumHeight(38)
        self.live_video.setCheckable(True)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.live_video)
        main_layout.addWidget(self.image_label)

        self.setLayout(main_layout)

        self.splashscreen = cv.imread('splashscreen.png')
        self.qsplashscreen = utils.nparray2QImage(self.splashscreen)
        self.set_qimage(self.qsplashscreen)

        self.setMinimumSize(200, 200)
                
    @pyqtSlot(QImage)
    def set_qimage(self, image: QImage):
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)
    
    def closeEvent(self, a0: QCloseEvent) -> None:
        self.signals.closed.emit()
        return super().closeEvent(a0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraWindow()
    window.show()
    app.exec()