from time import sleep

import numpy as np
import pandas as pd

# from matplotlib import pyplot as plt

from seekcamera import (
    SeekCameraIOType,
    SeekCameraManager,
    SeekCameraManagerEvent,
    SeekCameraFrameFormat,
)


def on_frame(camera, camera_frame, file):

    frame = camera_frame.thermography_float
    print(frame)
    print("frame available: {cid} (size: {w}x{h})".format(cid=camera.chipid,
    w=frame.width, h=frame.height))

    np.savetxt('Thermography_1.csv', frame.data, fmt="%.1f")
    np.savetxt(file, frame.data, fmt="%.1f")

    '''trying to overwrite file'''
    '''
    my_file=open(file, "w")
    my_file.write(frame.data, fmt="%.1f")
    my_file.close()
    '''

    file.close()
    print(file.closed)
    
    df = frame.data
    print(df)
    #print(frame.data)
    print(" ", type(frame.data))
    print('The main data structure in NumPy is the ndarray, which is a shorthand name for N-dimensional array.')
    print('When working with NumPy, data in an ndarray is simply referred to as an array. It is a fixed-sized')
    print('array in memory that contains data of the same type, such as integers or floating point values.')
    print("No. of dimensions: ", frame.data.ndim)
    print("Shape of array: ", frame.data.shape)
    print("Size of array: ", frame.data.size)
    print("Array stores elements of type: ", frame.data.dtype)

    sleep(5.0)

    #try:
        
    #except ValueError:
    #    print ("Deine Code ist schlecht >:-( ")
        
# In Python, a callback is simply a function or a method passed to LocalSolver.
#  A callback takes two parameters: the LocalSolver object that triggers the event and
#  the type of the callback. It is possible to use the same callback method or object
#  for multiple events or multiple LocalSolver instances. The method can be a static 
# function or a method on a class.

def on_event(camera, event_type, event_status, _user_data):

    print("{}: {}".format(str(event_type), camera.chipid))
    print(event_type)
    print(str(event_type), str(event_status))

    if event_type == SeekCameraManagerEvent.CONNECT:
        try:
            file = open("Thermography-" + camera.chipid + ".csv", "w")
            
        except OSError as e:
            print("Failed to open file: %s" % str(e))
            return

        camera.register_frame_available_callback(on_frame, file)
        camera.capture_session_start(SeekCameraFrameFormat.THERMOGRAPHY_FLOAT)
        
    elif event_type == SeekCameraManagerEvent.DISCONNECT:
        camera.capture_session_stop()

    elif event_type == SeekCameraManagerEvent.ERROR:
        print("{}: {}".format(str(event_status), camera.chipid))

    elif event_type == SeekCameraManagerEvent.READY_TO_PAIR:
        return

def main():
    
    with SeekCameraManager(SeekCameraIOType.USB) as manager:
        manager.register_event_callback(on_event)
        sleep(2.0)
        manager.destroy()

        while True:
            sleep(1.0)

if __name__ == "__main__":
        main()
