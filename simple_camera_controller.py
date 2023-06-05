import os
import sys

import cv2 as cv
from numpy import ndarray
from PyQt5.QtCore import QObject, QThreadPool, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication

from simple_runnables import CameraRunnable
from simple_view import MainWindow


class CameraController:
    def __init__(self, window, camera_id: str):
        self.pool = QThreadPool.globalInstance()
        self.camera_thread = CameraRunnable(camera_id)
        self.camera_thread.signals.frame.connect(window.set_qimage)
        self.pool.start(self.camera_thread)
        
        window.live_video.clicked.connect(self.manage_livestream)
    
    def manage_livestream(self, toggled_on):
        self.camera_thread.livestream_switch = toggled_on

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    controller = CameraController(window, 'DEV_000F314DE3E6') #DEV_000F314DA5E0
    window.show()
    app.exec()