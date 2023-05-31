import time

import cv2 as cv
from PyQt5.QtCore import QObject, QRunnable, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage


def nparray2QImage(array):
    h, w, ch = array.shape
    bytesPerLine = ch * w
    convertToQtFormat = QImage(array.data, w, h, bytesPerLine, QImage.Format_RGB888)
    return convertToQtFormat.scaled(656, 492, Qt.KeepAspectRatio)

class RunnableSignals(QObject):
    changePixmap = pyqtSignal(QImage)
    buttons_disabled = pyqtSignal(bool)
    set_status = pyqtSignal(str)
    set_last_reading = pyqtSignal(str)
    
class CameraRunnable(QRunnable):
    
    def __init__(self, camID):
        super().__init__()
        self.signal = RunnableSignals()
    
    @pyqtSlot
    def run(self):
        for i in range(10):
            print('running; {}s in'.format(i))
            time.sleep(1)
    
    def livestream(self, setting:bool):
        if isinstance(setting,bool):
            self.livestream = setting
        else:
            print('Livestream instruction was not a boolean.')