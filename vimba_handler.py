import sys
import time
import cv2 as cv
import numpy as np
from typing import Optional
from vimba import Vimba, Camera, VimbaCameraError, VimbaFeatureError, intersect_pixel_formats, COLOR_PIXEL_FORMATS, MONO_PIXEL_FORMATS, PixelFormat, OPENCV_PIXEL_FORMATS

def abort(reason: str, return_code: int = 1):
    print(reason + '\n')
    sys.exit(return_code)

def get_camera(camera_id: str) -> Camera:
    with Vimba.get_instance() as vimba:
        try:
            return vimba.get_camera_by_id(camera_id)

        except VimbaCameraError:
            abort('Failed to access Camera \'{}\'. Abort.'.format(camera_id))

def get_camera_id_list():
    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()
        if not cams:
            return None
        return [cam.get_id() for cam in cams]

def setup_camera(cam: Camera,exposure=None):
    with cam:
        try:
            cam.ExposureAuto.set('Off')
        except (AttributeError, VimbaFeatureError):
            pass
        if exposure is not None:
            cam.ExposureTimeAbs.set(str(exposure))
        elif cam.get_id() == 'DEV_000F314F19EB':
            try:
                cam.ExposureTimeAbs.set('30000')
            except (AttributeError, VimbaFeatureError):
                pass
        elif cam.get_id() == 'DEV_000F314DA5E0':
            try:
                cam.ExposureTimeAbs.set('30000')
            except (AttributeError, VimbaFeatureError):
                pass
        elif cam.get_id() == 'DEV_000F314DE3E6':
            try:
                cam.ExposureTimeAbs.set('3000')
            except (AttributeError, VimbaFeatureError):
                pass
        else:
            raise Exception('Exposure and Camera ID provided are both invalid. Abort.')
        # Enable white balancing if camera supports it
        try:
            cam.BalanceWhiteAuto.set('Off')
        except (AttributeError, VimbaFeatureError):
            pass
        # Try to adjust GeV packet size. This Feature is only available for GigE - Cameras.
        try:
            cam.GVSPAdjustPacketSize.run()
            while not cam.GVSPAdjustPacketSize.is_done():
                pass
        except (AttributeError, VimbaFeatureError):
            pass
        # Query available, open_cv compatible pixel formats
        # prefer color formats over monochrome formats
        cv_fmts = intersect_pixel_formats(cam.get_pixel_formats(), OPENCV_PIXEL_FORMATS)
        color_fmts = intersect_pixel_formats(cv_fmts, COLOR_PIXEL_FORMATS)
        if color_fmts:
            cam.set_pixel_format(color_fmts[0])
        else:
            mono_fmts = intersect_pixel_formats(cv_fmts, MONO_PIXEL_FORMATS)
            if mono_fmts:
                cam.set_pixel_format(mono_fmts[0])
            else:
                abort('Camera does not support a OpenCV compatible format natively. Abort.')