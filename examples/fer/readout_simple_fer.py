from time import sleep

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import csv

import seekcamera
from seekcamera import (
    SeekCameraIOType,
    SeekCameraManager,
    SeekCameraManagerEvent,
    SeekCameraFrameFormat,
)


def generate_pdf(csv_file_name, pdf_name, temperature_label_display=None):
    reader = csv.reader(open(csv_file_name, "r"), delimiter=" ")
    rows = []

    for row in reader:
        rows.append(row)

    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    # dataframe
    df = pd.read_csv(csv_file_name, delimiter=" ").astype(float)
    im = plt.imshow(df, cmap="jet")

    cbar = plt.colorbar(im)
    if temperature_label_display is not None:
        cbar.set_label(temperature_label_display, rotation=270, labelpad=15)

    plt.title(label='Thermography', fontdict=None, loc='center', pad=None)
    plt.xticks([])
    plt.yticks([])
    plt.savefig(pdf_name)

    plt.show()


def on_frame(camera, camera_frame, file_name):
    """Async callback fired whenever a new frame is available.

    Parameters
    ----------
    camera: SeekCamera
        Reference to the camera for which the new frame is available.
    camera_frame: SeekCameraFrame
        Reference to the class encapsulating the new frame (potentially
        in multiple formats).
    file_name: string
        User defined data passed to the callback. This can be anything
        but in this case it is a reference to the open CSV file to which
        to log data.
    """
    # Open a new CSV file with the unique camera chip ID embedded.
    try:
        file = open(file_name, "w")

    except OSError as e:
        print("Failed to open file: %s" % str(e))
        return

    frame = camera_frame.thermography_float
    print(frame)
    print("frame available: {cid} (size: {w}x{h})".format(cid=camera.chipid,
                                                          w=frame.width, h=frame.height))

    # np.savetxt('Thermography_1.csv', frame.data, fmt="%.1f")
    # would be better to overwrite file every time here instead of opening and closing it at every iteration
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
    # print(frame.data)
    print(" ", type(frame.data))
    print('The main data structure in NumPy is the ndarray, which is a shorthand name for N-dimensional array.')
    print('When working with NumPy, data in an ndarray is simply referred to as an array. It is a fixed-sized')
    print('array in memory that contains data of the same type, such as integers or floating point values.')
    print("No. of dimensions: ", frame.data.ndim)
    print("Shape of array: ", frame.data.shape)
    print("Size of array: ", frame.data.size)
    print("Array stores elements of type: ", frame.data.dtype)

    # sleep(5.0)

    # try:

    # except ValueError:
    #    print ("Deine Code ist schlecht >:-( ")


# In Python, a callback is simply a function or a method passed to LocalSolver.
#  A callback takes two parameters: the LocalSolver object that triggers the event and
#  the type of the callback. It is possible to use the same callback method or object
#  for multiple events or multiple LocalSolver instances. The method can be a static 
# function or a method on a class.

def on_event(camera, event_type, event_status, temperature_wanted):
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
    print(event_type)
    print(str(event_type), str(event_status))

    if event_type == SeekCameraManagerEvent.CONNECT:
        # file_name = "Thermography-" + camera.chipid + ".csv"
        file_name = "Thermography.csv"

        # Start streaming data and provide a custom callback to be called
        # every time a new frame is received.
        camera.temperature_unit = seekcamera.SeekCameraTemperatureUnit(temperature_wanted)
        camera.register_frame_available_callback(on_frame, file_name)
        camera.capture_session_start(SeekCameraFrameFormat.THERMOGRAPHY_FLOAT)

    elif event_type == SeekCameraManagerEvent.DISCONNECT:
        camera.capture_session_stop()

    elif event_type == SeekCameraManagerEvent.ERROR:
        print("{}: {}".format(str(event_status), camera.chipid))

    elif event_type == SeekCameraManagerEvent.READY_TO_PAIR:
        return


def main():
    # Create a context structure responsible for managing all connected USB cameras.
    # Cameras with other IO types can be managed by using a bitwise or of the
    # SeekCameraIOType enum cases.
    with SeekCameraManager(SeekCameraIOType.USB) as manager:
        temperature_wanted = int(input("0 = CELSIUS, 1 = FAHRENHEIT, 2 = KELVIN\nWhich unit do you want?\n"))

        # Start listening for events.
        manager.register_event_callback(on_event, temperature_wanted)
        sleep(2.0)

    generate_pdf("Thermography.csv", "Thermography.pdf")

if __name__ == "__main__":
    main()
