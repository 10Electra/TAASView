import sys
import cv2 as cv
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage
from vimba import Vimba

import utils
import vimba_handler


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
                            array = utils.vimba2nparray(frame)
                            ratio = 1
                            dim = (int(array.shape[1]*ratio),int(array.shape[0]*ratio))
                            resized = cv.resize(array, dim, interpolation=cv.INTER_AREA)
                            qimage = utils.nparray2QImage(resized)
                            self.signals.frame.emit(qimage)
                            if not self.livestream_switch:
                                break
    
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
    
    def livestream_toggle(self):
        if not self.livestream_switch:
            self.livestream_switch = True
        else:
            self.livestream_switch = False