import sys

from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QFont

import vimba_handler
from camera_view import CameraWindow
from runnables import CameraRunnable
from view import MainWindow


class Controller():
    def __init__(self) -> None:
        self.main_window = MainWindow()
        self.main_window.show()
        
        self.pool = QThreadPool.globalInstance()
        
        self.accessible_cams = None
        self.cam_windows = {}
        self.cam_threads = {}
        
        self.main_window.update_cams_button.clicked.connect(self.update_cams)
        self.main_window.path_entry.returnPressed.connect(self.path_edit_clicked)
        self.main_window.path_edit_button.clicked.connect(self.path_edit_clicked)

    def open_cam(self):
        cam_id = self.main_window.cam_buttons[self.main_window.sender()]
        if self.cam_windows.get(cam_id) is None:
            self.cam_windows[cam_id] = CameraWindow()
            self.cam_threads[cam_id] = CameraRunnable(cam_id)
            self.cam_threads[cam_id].signals.frame.connect(self.cam_windows[cam_id].set_qimage)
            self.pool.start(self.cam_threads[cam_id])
            
            self.cam_windows[cam_id].live_video.clicked.connect(self.cam_threads[cam_id].livestream_toggle)
            
            self.cam_windows[cam_id].show()

        else:
            self.cam_windows[cam_id] = None
            self.cam_threads[cam_id] = None
    
    def path_edit_clicked(self) -> None:
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
                print('Path of {} has been saved.'.format(self.main_window.path_entry.text()))
        else:
            raise ValueError('Path edit button text is not set as expected')
    
    def update_camera_buttons(self) -> None:
        while self.main_window.camera_button_layout.count() > 0:
            item = self.main_window.camera_button_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if self.accessible_cams is not None:
            self.main_window.cam_buttons = {}
            for cam_id in self.accessible_cams:
                print('now connecting cam id {}'.format(cam_id))
                button = QPushButton(cam_id)
                button.setStyleSheet(
                    "QPushButton { background-color: #f8f8f8; border: 1px solid #c0c0c0; padding: 10px; "
                    "font-size: 14px; } "
                    "QPushButton:pressed { background-color: #c0c0c0; }"
                )
                self.main_window.cam_buttons[button] = cam_id
                self.main_window.camera_button_layout.addWidget(button)
                print('self.main_window.cam_buttons = {}'.format(self.main_window.cam_buttons))
                button.clicked.connect(self.open_cam)
        else:
            self.main_window.camera_button_layout.addStretch(1)
            self.label2 = QLabel("No cameras found")
            self.label2.setFont(QFont("Segoe UI", 8))
            self.label2.setStyleSheet("QLabel { color: #333333; }")
            self.main_window.camera_button_layout.addWidget(self.label2)

    def update_cams(self) -> None:
        self.accessible_cams = vimba_handler.get_camera_id_list()
        self.update_camera_buttons()

if __name__ == '__main__':
    app = QApplication([])
    c = Controller()
    sys.exit(app.exec_())