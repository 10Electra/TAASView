import os
import sys

import cv2 as cv
from numpy import ndarray
from PyQt5.QtCore import (QCoreApplication, QObject, QThreadPool, pyqtSignal,
                          pyqtSlot)
from PyQt5.QtGui import QImage, QPixmap, QPixmapCache
from PyQt5.QtWidgets import QApplication

from runnables import CameraRunnable
from view import MainWindow


class ControllerSignals(QObject):
    show_frame = pyqtSignal(QImage)

class CameraController:
    def __init__(self, camera_id: str):
        self.pool = QThreadPool.globalInstance()
        self.camera_thread = CameraRunnable(camera_id)
        self.camera_thread.signals.frame.connect(window.set_qimage)
        self.camera_thread.signals.set_status.connect(window.status_label.setText)
        self.pool.start(self.camera_thread)
        
        # self.signals = ControllerSignals()
        # self.signals.show_frame.connect(window.set_image)
        
        window.live_video.clicked.connect(self.manage_livestream)
        window.cap_image.clicked.connect(self.capture_frame)
    
    def manage_livestream(self, toggled_on):
        self.camera_thread.livestream_switch = toggled_on
    
    def capture_frame(self):
        self.camera_thread.framegrab_switch = True
    
    # def frame_manager(self, frame):
    #     print('[frame_manager] Received a signal.')

    #     print('[set_image_pixmap] Pixmap set successfully.')


app = QApplication(sys.argv)

window = MainWindow()
controller = CameraController('DEV_000F314DA5E0')
window.show()
app.exec()