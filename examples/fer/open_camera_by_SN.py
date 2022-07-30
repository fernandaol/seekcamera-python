# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 10:40:36 2022

@author: Fernanda 
"""

#import ctypes
from enum import IntEnum
from threading import Condition ## https://docs.python.org/3/library/threading.html
#import cv2
import numpy as np
from seekcamera import (
    #SeekCameraIOType,
    #SeekCameraColorPalette,
    #SeekCameraManager,
    #SeekCameraManagerEvent,
    SeekCameraFrameFormat,
    SeekCamera,
    SeekFrame,
)


class SeekCameraManagerEvent(IntEnum):

    CONNECT = 0
    DISCONNECT = 1
    ERROR = 2
    READY_TO_PAIR = 3

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "SeekCameraManagerEvent({})".format(self.value)
       
class Renderer:
    def __init__(self):
        self.busy = False
        self.frame = SeekFrame()
        self.camera = SeekCamera()
        self.frame_condition = Condition()
        self.first_frame = True
        
  
    # def on_frame(_camera, camera_frame, renderer):
    #     """Async callback fired whenever a new frame is available.

    #     Parameters
    #     ----------
    #     _camera: SeekCamera
    #         Reference to the camera for which the new frame is available.
    #     camera_frame: SeekCameraFrame
    #         Reference to the class encapsulating the new frame (potentially
    #         in multiple formats).
    #     renderer: Renderer
    #         User defined data passed to the callback. This can be anything
    #         but in this case it is a reference to the renderer object.
    #     """
    #     with renderer.frame_condition:
    #         renderer.frame1 = camera_frame.thermography_float
    #         renderer.frame = camera_frame.color_argb8888
    #         renderer.frame_condition.notify()
            
    def on_frame(camera, camera_frame, file):
        """Async callback fired whenever a new frame is available.
    
        Parameters
        ----------
        camera: SeekCamera
            Reference to the camera for which the new frame is available.
        camera_frame: SeekCameraFrame
            Reference to the class encapsulating the new frame (potentially
            in multiple formats).
        file: TextIOWrapper
            # User defined data passed to the callback. This can be anything
            but in this case it is a reference to the open CSV file to which
            to log data.
        """
        frame = camera_frame.thermography_float
    
        print(
            "frame available: {cid} (size: {w}x{h})".format(
                cid=camera.chipid, w=frame.width, h=frame.height
                #cid=camera.serial_number, w=frame.width, h=frame.height
            )
        )
    
        # Append the frame to the CSV file.
        # np.savetxt(file, frame.data, fmt="%.1f")
        ''' "file" is defined under - line 82'''
        np.savetxt('test_self.csv', frame.data, fmt="%.1f")
            
        def on_event(camera, event_type, event_status, _user_data):
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
            _user_data: None
                User defined data passed to the callback. This can be anything
                but in this case it is None.
            """
            print("{}: {}".format(str(event_type), camera.chipid))
        
            if event_type == SeekCameraManagerEvent.CONNECT:
                # Open a new CSV file with the unique camera chip ID embedded.
                try:
                    file = open("Thermography-" + camera.chipid + ".csv", "w")
                except OSError as e:
                    print("Failed to open file: %s" % str(e))
                    return
        
                # Start streaming data and provide a custom callback to be called
                # every time a new frame is received.
                camera.register_frame_available_callback(on_frame, file)
                camera.capture_session_start(SeekCameraFrameFormat.THERMOGRAPHY_FLOAT)
        
            elif event_type == SeekCameraManagerEvent.DISCONNECT:
                camera.capture_session_stop()
        
            elif event_type == SeekCameraManagerEvent.ERROR:
                print("{}: {}".format(str(event_status), camera.chipid))
        
            elif event_type == SeekCameraManagerEvent.READY_TO_PAIR:
                return
