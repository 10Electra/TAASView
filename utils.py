import cv2 as cv
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage
from vimba import Frame


def vimba2nparray(image: Frame):
    array = cv.cvtColor(image.as_opencv_image(),cv.COLOR_GRAY2RGB) # PyQt uses RGB but OpenCV uses BGR
    return array
    
def nparray2QImage(array: np.ndarray): # resolution=(656,492), new one: resolution=(1936,1216)
    hres, vres = len(array[0]), len(array)
    h, w, ch = array.shape
    bytesPerLine = ch * w
    convertToQtFormat = QImage(array.data, w, h, bytesPerLine, QImage.Format_RGB888)
    return convertToQtFormat.scaled(hres, vres, Qt.KeepAspectRatio)