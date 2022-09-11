from time import sleep
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv

import seekcamera
from seekcamera import (
    SeekCameraIOType,
    SeekCameraManager,
    SeekCameraManagerEvent,
    SeekCameraFrameFormat, SeekCameraFrameHeader, SeekCamera,
)

values_x = []
min_temp = []
max_temp = []
mean_temp = []

fieldnames = ["x_value", "minimum_value", "maximum_value", "meantemp_value"]

def animation(self):

    x = range(len(min_temp))
    y1 = min_temp
    y2 = mean_temp
    y3 = max_temp
    plt.style.use('fivethirtyeight')

    fig, axs = plt.subplots(3, sharex=True)
    axs[0].plot(x, y1, label='Min')
    axs[0].set_title('MIN Temperature over Time')
    axs[1].plot(x, y2, 'tab:orange', label='Average')
    axs[1].set_title('AVERAGE of Temperatures over Time')
    axs[2].plot(x, y3, 'tab:green', label='Max')
    axs[2].set_title('MAX Temperature over Time')

    # plt.show()

"""    # format plot min temperature values
    plt.cla()
    plt.tight_layout()
    plt.plot(x, y1)
    plt.subplot(1, 2, 1)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('MIN Temperature over Time')
    plt.xlabel('Frames')
    plt.ylabel('Temperature')

    # format plot average temp values

    plt.plot(x, y2)
    plt.subplot(1, 2, 2)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('AVERAGE of Temperatures over Time')
    plt.xlabel('Frames')
    plt.ylabel('Temperature')

    plt.plot(x, y3)
    plt.subplot(1, 2, 3)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('MAX Temperature over Time')
    plt.xlabel('Frames')
    plt.ylabel('Temperature')

    plt.show()
    """

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

    file.close()
    print(file.closed)

    df = frame.data
    print(df)

    print("\n")
    print("Min:", df.min().min(), "Max:", df.max().max(), "Mean:", np.mean(df))


    # with open('data.csv', 'w') as csv_file:
    #     csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #     csv_writer.writeheader()


    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)



        x_value = len(min_temp)
        # print(x_value)
        # values_x.append(x_value+1)
        # print(values_x)

        minimum_value = df.min().min()
        min_temp.append(minimum_value)
        print(minimum_value)
        # print(len(min_temp))

        maximum_value = df.max().max()
        # max_temp.append(maximum_value)
        # print(max_temp)
        # print(len(max_temp))

        meantemp_value = np.mean(df)
        # mean_temp.append(meantemp_value)
        # print(np.mean(df))
        # print("Mean:", mean_temp)

        info = {
            "x_value": x_value,
            "minimum_value": minimum_value,
            "maximum_value": maximum_value,
            "meantemp_value": meantemp_value
        }
        csv_writer.writerow(info)
        print(x_value, minimum_value, meantemp_value, maximum_value)

        # time.sleep(1)

      #  header_camera = SeekCameraFrameHeader(SeekCamera)
        #time_stamp = property(SeekCameraFrameHeader.timestamp_utc_ns)
      # print(SeekCamera.timestamp_utc_ns)
        #print("Here is the time >>", time_stamp)


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

        with open('data.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()


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
    # anim = FuncAnimation(plt.gcf(), animation, interval=1000)
    # plt.tight_layout()
    # plt.show()
    with SeekCameraManager(SeekCameraIOType.USB) as manager:
        #temperature_wanted = int(input("0 = CELSIUS, 1 = FAHRENHEIT, 2 = KELVIN\nWhich unit do you want?\n"))
        temperature_wanted = int(0)

        # Start listening for events.
        manager.register_event_callback(on_event, temperature_wanted)
        sleep(30)

    generate_pdf("Thermography.csv", "Thermography.pdf")

if __name__ == "__main__":
    main()

#anim = FuncAnimation(plt.gcf(), animation)
#plt.tight_layout()
#plt.show()
#



