import random
import time

import cv2 as cv
import numpy as np
from PyQt5.QtCore import QObject, QRunnable, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage
from vimba import (COLOR_PIXEL_FORMATS, MONO_PIXEL_FORMATS,
                   OPENCV_PIXEL_FORMATS, Camera, PixelFormat, Vimba,
                   VimbaCameraError, VimbaFeatureError,
                   intersect_pixel_formats)

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
    buttons_disabled = pyqtSignal(bool)
    set_status = pyqtSignal(str)
    
class CameraRunnable(QRunnable):
    
    def __init__(self, camID):
        super().__init__()
        self.signals = RunnableSignals()
        self.camID = camID
        self.is_stopped = False
        self.is_idle = True
        self.livestream_switch = False
        self.framegrab_switch = False
        self.exposure_value = 60000 # Maybe make a default settings dictionary to pipe in?
    
    @pyqtSlot()
    def run(self):
        # while not self.is_stopped:
        #     while self.livestream_switch:
        #         self.is_idle = False
        #         self.signals.frame.emit(vimba2QImage(cv.imread('foil_image.png')))
        #         time.sleep(random.randrange(2, 17, 1)/10)
        #     if self.framegrab_switch:
        #         self.is_idle = False
        #         self.signals.frame.emit(vimba2QImage(cv.imread('foil_image.png')))
        #         print('tried to emit image after framegrab')
        #         self.framegrab_switch = False
        #         if not self.is_idle:
        #             self.signals.frame.emit(vimba2QImage(cv.imread('splashscreen.png')))
        #             self.is_idle = True
        #     time.sleep(0.5)
        with Vimba.get_instance():
            with vimba_handler.get_camera(self.camID) as cam:
                vimba_handler.setup_camera(cam,self.exposure_value)
                
                while not self.is_stopped:
                    if self.livestream_switch:
                        
                        for frame in cam.get_frame_generator(limit=None):
                            frame = vimba2QImage(frame)
                            self.signals.frame.emit(frame)
                            if not self.livestream_switch:
                                break
                        
                    
                    elif self.framegrab_switch:
                        
                        frame = cam.get_frame()
                        self.signals.frame.emit(vimba2QImage(frame))
                        
                    time.sleep(0.5)
    
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

    @property
    def framegrab_switch(self):
        return self._framegrab_switch
    
    @framegrab_switch.setter
    def framegrab_switch(self, setting:bool):
        if isinstance(setting,bool):
            self._framegrab_switch = setting
        else:
            print('Framegrab instruction was not a boolean.')
    
    @property
    def exposure_value(self):
        return self._exposure
    
    @exposure_value.setter
    def exposure_value(self, value:int):
        if isinstance(value,int):
            if value > 10 and value < 120000:
                self._exposure = value
            else:
                print('Exposure value not in a sensible range.')
        else:
            print('Exposure value not an integer.')
    