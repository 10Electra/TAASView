import sys

from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QApplication

from simple_runnables import CameraRunnable
from simple_view import CameraWindow


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

    window = CameraWindow()
    controller = CameraController(window, 'DEV_000F314DA5E0') #Tech Workshop: DEV_000F314DA5E0, Subin's camera:DEV_000F314DE3E6
    window.show()
    app.exec()