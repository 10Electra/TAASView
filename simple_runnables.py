import time

import cv2 as cv
import numpy as np
from PyQt5.QtCore import QObject, QRunnable, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage
from vimba import PixelFormat, Vimba

import vimba_handler


def vimba2QImage(array, resolution=(656,492)):
    array.convert_pixel_format(PixelFormat.Mono8) # Not sure if this needs to be done
    array = cv.cvtColor(array.as_opencv_image(),cv.COLOR_GRAY2RGB) # PyQt uses RGB but OpenCV uses BGR
    if not isinstance(array, np.ndarray):
        raise Exception('Unable to get frame from camera')
    hres, vres = resolution
    h, w, ch = array.shape
    bytesPerLine = ch * w
    convertToQtFormat = QImage(array.data, w, h, bytesPerLine, QImage.Format_RGB888)
    return convertToQtFormat.scaled(hres, vres, Qt.KeepAspectRatio)

class RunnableSignals(QObject):
    frame = pyqtSignal(QImage)
    
class CameraRunnable(QRunnable):
    
    def __init__(self, camID):
        super().__init__()
        self.signals = RunnableSignals()
        self.camID = camID
        self.is_stopped = False
        self.is_idle = True
        self.livestream_switch = False
    
    @pyqtSlot()
    def run(self):
        with Vimba.get_instance():
            with vimba_handler.get_camera(self.camID) as cam:
                vimba_handler.setup_camera(cam)
                
                while not self.is_stopped:
                    if self.livestream_switch:
                        
                        for frame in cam.get_frame_generator(limit=None):
                            frame = vimba2QImage(frame)
                            self.signals.frame.emit(frame)
                            if not self.livestream_switch:
                                break
                    # time.sleep(0.2)
    
    @property
    def is_stopped(self):
        return self._stop
    
    @is_stopped.setter
    def is_stopped(self, setting:bool):
        if isinstance(setting,bool):
            self._stop = setting
        else:
            print('Stop instruction was not a boolean.')
    
    @property
    def livestream_switch(self):
        return self._livestream
    
    @livestream_switch.setter
    def livestream_switch(self, setting:bool):
        if isinstance(setting,bool):
            self._livestream = setting
        else:
            print('Livestream instruction was not a boolean.')