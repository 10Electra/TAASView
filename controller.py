import sys

from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QLabel, QMessageBox, QPushButton

import vimba_handler
from camera_view import CameraWindow
from runnables import CameraRunnable
from view import MainWindow


class Controller():
    """Main class for the TAASView app. Instantiates and provides functionality to
    all windows in TAASView.
    """
    def __init__(self) -> None:
        # Define instance variables
        self.main_window = MainWindow()
        self.main_window.show()
        
        self.pool = QThreadPool.globalInstance()
        
        self.accessible_cams = None
        self.cam_windows = {}
        self.cam_threads = {}
        
        # Connect buttons and other widgets
        self.main_window.update_cams_button.clicked.connect(self.update_cams)
        self.main_window.path_entry.returnPressed.connect(self.path_edit_clicked)
        self.main_window.path_edit_button.clicked.connect(self.path_edit_clicked)
        
        self.main_window.live_button.clicked.connect(self.all_toggle_live)
        self.main_window.close_button.clicked.connect(self.all_close)
        
        self.main_window.path_entry.setText('videos') # Default save path from the working directory (..\TAASView\videos\)
        
    def open_cam(self):
        """Instantiates a camera window and runnable for a camera. Makes the necessary
        GUI signal connections.
        """
        cam_id = self.main_window.cam_buttons[self.main_window.sender()]
        save_path = self.main_window.path_entry.text()
        if self.cam_windows.get(cam_id) is not None or self.cam_threads.get(cam_id) is not None:
            return
        self.cam_windows[cam_id] = CameraWindow()
        self.cam_threads[cam_id] = CameraRunnable(cam_id,save_path)
        
        self.cam_windows[cam_id].signals.closed.connect(self.cam_threads[cam_id].stop)
        self.cam_threads[cam_id].signals.release.connect(self.release_cam)
        self.cam_threads[cam_id].signals.frame.connect(self.cam_windows[cam_id].set_qimage)
        self.cam_threads[cam_id].signals.idle.connect(self.cam_windows[cam_id].set_splashscreen)
        self.pool.start(self.cam_threads[cam_id])
        
        self.cam_windows[cam_id].live_button.clicked.connect(self.cam_threads[cam_id].toggle_livestream)
        self.main_window.record_button.clicked.connect(self.cam_threads[cam_id].toggle_recording)
        
        self.cam_windows[cam_id].show()
    
    def all_toggle_live(self):
        for thread in self.cam_threads.values():
            thread.toggle_livestream()
            
    def all_close(self):
        for cam_id in self.cam_threads:
            self.cam_threads[cam_id].stop()
            self.release_cam(cam_id)
    
    def release_cam(self, cam_id: str):
        """Lets go of the cam window and thread references so they can be auto deleted.

        Args:
            cam_id (str): camera id string of the chosen camera to be released
        """
        assert(self.cam_windows.get(cam_id) is not None) # Check the cam_id has a window before release
        assert(self.cam_threads.get(cam_id) is not None) # Check the cam_id has a thread before release
        self.cam_windows[cam_id] = None
        self.cam_threads[cam_id] = None
    
    def path_edit_clicked(self) -> None:
        """Manages the video save path entry functionality.

        Raises:
            ValueError: If path_edit_button's text is something other than 'Edit' or 'Save'
        """
        if self.main_window.path_edit_button.text() == 'Edit':
            self.main_window.path_entry.setReadOnly(False)
            self.main_window.path_edit_button.setText('Save')
        elif self.main_window.path_edit_button.text() == 'Save':
            self.main_window.path_entry.setReadOnly(True)
            self.main_window.path_edit_button.setText('Edit')
            
            dlg = QMessageBox(self.main_window)
            dlg.setWindowTitle("Confirmation")
            dlg.setText("Are you sure you want to save this path?")
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dlg.setIcon(QMessageBox.Question)
            button = dlg.exec()

            if button == QMessageBox.Yes:
                self.save_path = self.main_window.path_entry.text()
        else:
            raise ValueError('Path edit button text is not set as expected')
    
    def update_camera_buttons(self) -> None:
        """Updates the camera buttons on the GUI to match the cameras available
        """
        while self.main_window.camera_button_layout.count() > 0:
            item = self.main_window.camera_button_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if self.accessible_cams is not None:
            self.main_window.cam_buttons = {}
            for cam_id in self.accessible_cams:
                button = QPushButton(cam_id)
                button.setStyleSheet(
                    "QPushButton { background-color: #f8f8f8; border: 1px solid #c0c0c0; padding: 10px; "
                    "font-size: 14px; } "
                    "QPushButton:pressed { background-color: #c0c0c0; }"
                )
                self.main_window.cam_buttons[button] = cam_id
                self.main_window.camera_button_layout.addWidget(button)
                button.clicked.connect(self.open_cam)
        else:
            self.main_window.camera_button_layout.addStretch(1)
            self.label2 = QLabel("No cameras found")
            self.label2.setFont(QFont("Segoe UI", 8))
            self.label2.setStyleSheet("QLabel { color: #333333; }")
            self.main_window.camera_button_layout.addWidget(self.label2)

    def update_cams(self) -> None:
        """Retrieves the IDs of the available cameras on the network.
        """
        self.accessible_cams = vimba_handler.get_camera_id_list()
        self.update_camera_buttons()

if __name__ == '__main__':
    app = QApplication([])
    c = Controller()
    sys.exit(app.exec_())