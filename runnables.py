import os
import time

import cv2 as cv
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage
from vimba import Vimba

import utils
import vimba_handler


class RunnableSignals(QObject):
    frame = pyqtSignal(QImage)
    release = pyqtSignal(str)
    idle = pyqtSignal()
    
class CameraRunnable(QRunnable):
    """A runnable that acts as a camera controller. It connects to
    and sets up its corresponding camera and sends its frames to the
    relevant camera window.
    """
    def __init__(self, camID:str, save_path:str):
        super().__init__()
        self.signals = RunnableSignals()
        self.cam_id = camID
        self.save_path = save_path
        self.video_file = None
        self.is_livestreaming = False
        self.is_recording = False
        self.is_idle = True
        self.is_stopped = False
    
    @pyqtSlot()
    def run(self):
        with Vimba.get_instance():
            with vimba_handler.get_camera(self.cam_id) as cam:
                vimba_handler.setup_camera(cam)
                
                while not self.is_stopped:
                    
                    if self.is_livestreaming:
                        nframes = 0
                        tstart = time.time()
                            
                        for frame in cam.get_frame_generator(limit=None):
                            nframes += 1
                            
                            array = utils.vimba2nparray(frame)
                            
                            if self.is_recording:
                                self.video_file.write(array)

                            qimage = utils.nparray2QImage(array)
                            self.signals.frame.emit(qimage)
                            if not self.is_livestreaming or self.is_stopped:
                                break
                        print('Camera {} had an average fps rate of {}'.format(self.cam_id,round(nframes/(time.time()-tstart),2)))
                        
                        if self.is_recording and self.video_file.isOpened():
                            self.video_file.release()
                            
                    elif not self.is_idle:
                        self.signals.idle.emit()
                        self.is_idle = True
        self.signals.release.emit(self.cam_id)
    
    def get_filename(self) -> str:
        for i in range(30):
            path = f'{self.save_path}\\{self.cam_id}_{i}.mp4'
            if not os.path.exists(path):
                return path
        raise FileExistsError("Searched many possible video paths in the given save_path - none available.")
    
    def toggle_recording(self):
        if self.is_recording:
            self.is_recording = False
            
            self.video_file.release()
        else:
            self.is_idle = False
            self.is_livestreaming = True
            self.is_recording = True
            
            width = 656
            height = 492
            frame_rate = 18
            fourcc = cv.VideoWriter_fourcc(*'mp4v')
            output_file = self.get_filename()
            self.video_file = cv.VideoWriter(output_file, fourcc, frame_rate, (width, height))
    
    def toggle_livestream(self):
        if self.is_livestreaming:
            self.is_livestreaming = False
        else:
            self.is_idle = False
            self.is_livestreaming = True
    
    def stop(self):
        self.is_stopped = True