import sys

import cv2 as cv
from PyQt5.QtCore import QObject, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QCloseEvent, QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout,
                             QWidget)

import utils


class Signals(QObject):
    closed = pyqtSignal()
    
class CameraWindow(QWidget):
    """This class is the camera view window. It is instantiated for each
    open camera. The relevant camera displays its frames here.
    """
    def __init__(self):
        super().__init__()
        self.signals = Signals()
        
        # Add live video button
        self.live_button = QPushButton("Live Video")
        self.live_button.setStyleSheet(
            "QPushButton { background-color: #f8f8f8; border: 1px solid #c0c0c0; padding: 10px; "
            "font-size: 14px; } "
            "QPushButton:pressed { background-color: #c0c0c0; }"
        )
        self.live_button.setMinimumHeight(38)
        
        # Add image display area
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        
        # Put both into a main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.live_button)
        main_layout.addWidget(self.image_label)

        self.setLayout(main_layout)
        
        # Read, store and load the splashscreen image
        self.splashscreen = cv.imread('splashscreen.png')
        self.qsplashscreen = utils.nparray2QImage(self.splashscreen)
        self.set_splashscreen()

        self.setMinimumSize(200, 200)
                
    def set_splashscreen(self) -> None:
        self.set_qimage(self.qsplashscreen)
                
    @pyqtSlot(QImage)
    def set_qimage(self, image: QImage):
        """Displays the given image in the window's display area

        Args:
            image (QImage): image or frame to be displayed
        """
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)
    
    def closeEvent(self, a0: QCloseEvent) -> None:
        self.signals.closed.emit()
        return super().closeEvent(a0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraWindow()
    window.show()
    app.exec()
