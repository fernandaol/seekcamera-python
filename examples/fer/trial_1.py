# -*- coding: utf-8 -*-
"""
@author: Fernanda
"""

#import os
#import time
#import sys
# import ctypes
# from enum import IntEnum
# import numpy as np
from enum import IntEnum
from seekcamera import (
    SeekCameraIOType,
    SeekCameraColorPalette,
    SeekCameraManager,
    SeekCameraManagerEvent,
    SeekCameraFrameFormat,
    SeekCamera,
    SeekFrame,
    _clib #Means that it is part of the C library
)

from seekcamera.error import (
    is_error,
    error_from_status,
    SeekCameraInvalidParameterError,
)


from threading import Condition ## https://docs.python.org/3/library/threading.html

import cv2

class Renderer:
    """Contains camera and image data required to render images to the screen."""

    def __init__(self):
        self.busy = False
        self.frame = SeekFrame()
        self.camera = SeekCamera()
        self.frame_condition = Condition()
        self.first_frame = True


def on_frame(_camera, camera_frame, renderer):
    """Async callback fired whenever a new frame is available.

    Parameters
    ----------
    _camera: SeekCamera
        Reference to the camera for which the new frame is available.
    camera_frame: SeekCameraFrame
        Reference to the class encapsulating the new frame (potentially
        in multiple formats).
    renderer: Renderer
        User defined data passed to the callback. This can be anything
        but in this case it is a reference to the renderer object.
    """

    # Acquire the condition variable and notify the main thread
    # that a new frame is ready to render. This is required since
    # all rendering done by OpenCV needs to happen on the main thread.
    with renderer.frame_condition:
        renderer.frame = camera_frame.color_argb8888
        renderer.frame_condition.notify()



def on_event(camera, event_type, event_status, renderer):
    """Async callback fired whenever a camera event occurs.

    Parameters
    ----------
    camera: SeekCamera
        Reference to the camera on which an event occurred.
    event_type: SeekCameraManagerEvent
        Enumerated type indicating the type of event that occurred.
    event_status: Optional[SeekCameraError]
        Optional exception type. It will be a non-None derived instance of
        SeekCameraError if the event_type is SeekCameraManagerEvent.ERROR.
    renderer: Renderer
        User defined data passed to the callback. This can be anything
        but in this case it is a reference to the Renderer object.
    """
    print("{}: {}".format(str(event_type), camera.chipid))
    print("The Camera SN {} Status is {}".format(str(camera.serial_number),event_type))
    

    if event_type == SeekCameraManagerEvent.CONNECT:
        if renderer.busy:
            return

        # Claim the renderer.
        # This is required in case of multiple cameras.
        renderer.busy = True
        renderer.camera = camera

        # Indicate the first frame has not come in yet.
        # This is required to properly resize the rendering window.
        renderer.first_frame = True

        # Set a custom color palette.
        # Other options can set in a similar fashion.
        camera.color_palette = SeekCameraColorPalette.TYRIAN

        # Start imaging and provide a custom callback to be called
        # every time a new frame is received.
        camera.register_frame_available_callback(on_frame, renderer)
        camera.capture_session_start(SeekCameraFrameFormat.COLOR_ARGB8888)
        class SingleSeekCamera(object):
            
                def scene_emissivity(self):
                    emissivity, status = _clib.cseekcamera_get_scene_emissivity(self._camera)
                    print(float(emissivity))
                    
                    if is_error(status):
                        raise error_from_status(status)
                        
                        return emissivity.value
                    
                    print("The Emissivity is: {}".format(float(emissivity.value)))

    elif event_type == SeekCameraManagerEvent.DISCONNECT:
        # Check that the camera disconnecting is one actually associated with
        # the renderer. This is required in case of multiple cameras.
        if renderer.camera == camera:
            # Stop imaging and reset all the renderer state.
            camera.capture_session_stop()
            renderer.camera = None
            renderer.frame = None
            renderer.busy = False

    elif event_type == SeekCameraManagerEvent.ERROR:
        print("{}: {}".format(str(event_status), camera.chipid))
        print("The Camera SN {} Status is {}".format(str(camera.serial_number),event_type))

    elif event_type == SeekCameraManagerEvent.READY_TO_PAIR:
        return
    
# class SingleSeekCamera(object):
    
#         def scene_emissivity(self):
#             emissivity, status = _clib.cseekcamera_get_scene_emissivity(self._camera)
#             print(float(emissivity))
            
#             if is_error(status):
#                 raise error_from_status(status)
                
#                 return emissivity.value
            
#             print("The Emissivity is: {}".format(float(emissivity.value)))


def main():
    window_name = "Seek Thermal - Python OpenCV Sample"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # Create a context structure responsible for managing all connected USB cameras.
    # Cameras with other IO types can be managed by using a bitwise or of the
    # SeekCameraIOType enum cases.
    with SeekCameraManager(SeekCameraIOType.USB) as manager:
        # Start listening for events.
        renderer = Renderer()
        manager.register_event_callback(on_event, renderer)

        while True:
            # Wait a maximum of 150ms for each frame to be received.
            # A condition variable is used to synchronize the access to the renderer;
            # it will be notified by the user defined frame available callback thread.
            with renderer.frame_condition:
                if renderer.frame_condition.wait(150.0 / 1000.0):
                    img = renderer.frame.data

                    # Resize the rendering window.
                    if renderer.first_frame:
                        (height, width, _) = img.shape
                        cv2.resizeWindow(window_name, width * 2, height * 2)
                        renderer.first_frame = False

                    # Render the image to the window.
                    cv2.imshow(window_name, img)

            # Process key events.
            key = cv2.waitKey(1)
            if key == ord("q"):
                break

            # Check if the window has been closed manually.
            if not cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE):
                break

    cv2.destroyWindow(window_name)
  
if __name__ == "__main__":
    main()


class SeekCameraUSBIOProperties(object):
    """IO properties of USB cameras. ## IO input/output

    Attributes
    ----------
    bus_number: int
        USB bus number on which the camera is connected.
    port_numbers: Optional[list[int]]
        USB port numbers on which the camera is connected. Valid port numbers are
        indicated by a value strictly greater than zero.
    """

    def __init__(self, bus_number=0, port_numbers=None):
        if port_numbers is None:
            port_numbers = [0] * 8
        self.bus_number = bus_number
        self.port_numbers = port_numbers

    def __repr__(self):
        return "SeekCameraUSBIOProperties({}, {})".format(
            self.bus_number, self.port_numbers
        )


class SeekCameraIOProperties(object):
    """Generic IO properties of cameras.

    Attributes
    ----------
    type:
        IO type of the camera.
    usb: Optional[SeekCameraUSBIOProperties]
        Contains properties of USB cameras.
    spi: Optional[SeekCameraSPIIOProperties]
        Contains properties of SPI cameras.
    """

    def __init__(self, type_, usb=None, spi=None):
        if usb is None:
            usb = SeekCameraUSBIOProperties()

        self.type = type_
        self.usb = usb

    def __repr__(self):
        return "SeekCameraIOProperties({}, {}, {})".format(
            self.type, self.usb, self.spi
        )
    
class SeekCameraSPIIOProperties(object):
    """IO properties of SPI cameras.

    Attributes
    ----------
    bus_number: int
        SPI bus number on which the camera is connected. This field corresponds to the
        bus number set in the SPI configuration file.
    cs_number: int
        SPI chip select number on which the camera is connected. This field corresponds
        to the chip select (cs) number set in the SPI configuration file.
    """

    def __init__(self, bus_number=0, cs_number=0):
        self.bus_number = bus_number
        self.cs_number = cs_number

    def __repr__(self):
        return "SeekCameraSPIIoProperties({}, {})".format(
            self.bus_number, self.cs_number
        )


def __init__(self, camera=None):
    """Creates a new SeekCamera.

    Parameters
    ----------
    camera: Optional[CSeekCamera]
        Optional reference to the camera object type used by the C bindings.

    Raises
    ------
    SeekCameraInvalidParameterError
        If camera is specified and is not an instance of CSeekCamera.
    """
    if camera is None:
        camera = _clib.CSeekCamera(None)
    elif not isinstance(camera, _clib.CSeekCamera):
        raise SeekCameraInvalidParameterError

    self._camera = camera
    self._user_data = None
    self._frame_available_callback = None
    self._frame_available_callback_ctypes = None
    
    def __eq__(self, other):
        return self._camera == other._camera
    
    def __repr__(self):
        return "SeekCamera({})".format(self._camera)
    
    @property
    def io_type(self):
        
        io_type, status = _clib.cseekcamera_get_io_type(self._camera)
        if is_error(status):
            raise error_from_status(status)
    
        return SeekCameraIOType(io_type.value)
    
    @property
    def io_properties(self):
        
        properties, status = _clib.cseekcamera_get_io_properties(self._camera)
        if is_error(status):
            raise error_from_status(status)
    
        if properties.type == SeekCameraIOType.SPI:
            spi = SeekCameraSPIIOProperties(
                properties.properties.spi.bus_number,
                properties.properties.spi.cs_number,
            )
    
            return SeekCameraIOProperties(SeekCameraIOType.SPI, spi=spi)
    
        elif properties.type == SeekCameraIOType.USB:
            usb = SeekCameraUSBIOProperties(
                properties.properties.usb.bus_number,
                properties.properties.usb.port_numbers[:],
            )
    
            return SeekCameraIOProperties(SeekCameraIOType.USB, usb=usb)    
    
    # dir = "C:\Program Files\Seek Thermal\SeekSimpleViewer\SeekSimpleViewer.exe"
    # os.startfile("C:\Users\Asus\Desktop\JOB\SeekSimpleViewer")
    # os.system("SeekSimpleViewer")
    # os.startfile(dir)
    # os.system(dir)
    
    #time.sleep(3) # Sleep for 3 seconds
    
    #os._exit(1)
    #sys.exit(1)
    
    def __init__(self, discovery_mode):
        
        self._discovery_mode = discovery_mode
        self._user_data = None
        self._event_callback = None
        self._event_callback_ctypes = None
        self._cameras = []
    
        _clib.configure_dll()
    
        self._manager, status = _clib.cseekcamera_manager_create(discovery_mode)
        if is_error(status):
            raise error_from_status(status)

