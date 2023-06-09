import cv2 as cv
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage
from vimba import Frame


def vimba2nparray(image: Frame):
    """Converts a Vimba Frame to a numpy array.

    Args:
        image (Frame): Input image

    Returns:
        array (np.ndarray): Output image
    """
    array = cv.cvtColor(image.as_opencv_image(),cv.COLOR_GRAY2RGB) # PyQt uses RGB but OpenCV uses BGR
    return array
    
def nparray2QImage(array: np.ndarray):
    """Converts a numpy array to a PyQt QImage.

    Args:
        array (np.ndarray): Input image

    Returns:
        image (QImage): Output image
    """
    hres, vres = len(array[0]), len(array)
    h, w, ch = array.shape
    bytesPerLine = ch * w
    convertToQtFormat = QImage(array.data, w, h, bytesPerLine, QImage.Format_RGB888)
    return convertToQtFormat.scaled(hres, vres, Qt.KeepAspectRatio)