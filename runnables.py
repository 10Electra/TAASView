import time

import cv2 as cv
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage
from vimba import Vimba

import utils
import vimba_handler


class RunnableSignals(QObject):
    frame = pyqtSignal(QImage)
    
class CameraRunnable(QRunnable):
    
    def __init__(self, camID:str, save_path:str):
        super().__init__()
        self.signals = RunnableSignals()
        self.camID = camID
        self.save_path = save_path
        self.is_livestreaming = False
        self.is_recording = False
        self.is_stopped = False
    
    @pyqtSlot()
    def run(self):
        with Vimba.get_instance():
            with vimba_handler.get_camera(self.camID) as cam:
                vimba_handler.setup_camera(cam)
                
                while not self.is_stopped:
                    if self.is_livestreaming:
                        frame_timings = []
                        tstart = time.time()
                        for frame in cam.get_frame_generator(limit=None):
                            
                            window = 10 # seconds
                            t = time.time()
                            frame_timings.append(t)
                            for timing in frame_timings:
                                if timing < t - window:
                                    frame_timings.remove(timing)
                                else:
                                    break
                            if t - tstart > window:
                                print('{} fps over last {} secs'.format(round(len(frame_timings)/window,3),window))
                            
                            array = utils.vimba2nparray(frame)
                            
                            # ratio = 1
                            # dim = (int(array.shape[1]*ratio),int(array.shape[0]*ratio))
                            # array = cv.resize(array, dim, interpolation=cv.INTER_AREA)
                            qimage = utils.nparray2QImage(array)
                            self.signals.frame.emit(qimage)
                            if not self.is_livestreaming or self.is_stopped:
                                break
    
    def toggle_recording(self):
        if self.is_recording:
            self.is_recording = False
        else:
            self.is_recording = True
    
    def livestream_toggle(self):
        if self.is_livestreaming:
            self.is_livestreaming = False
        else:
            self.is_livestreaming = True
    
    def stop(self):
        self.is_stopped = True