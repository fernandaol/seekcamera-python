# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 11:15:22 2022

"""
import csv
import camera
import seekcamera_simple_fer
import seekcamera
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def main():
    '''later also insert the possibility of choosing which
    temperature to display from the program (not typing)'''
        
    unit_input = int(input("0 = CELSIUS, 1 = FAHRENHEIT, 2 = KELVIN\nWhich unit do you want?\n"))
    #unit_input = int(0)
    
    # use integer input to use the SeekCameraTemperatureUnit function
    # and change the format to string to be able to use 
    # and save the output at the "unit_input_name" variable

    unit_input_name=str(camera.SeekCameraTemperatureUnit(unit_input))
    print("You chose " + unit_input_name) #to chechk if reading correctly
    
    if unit_input_name == "CELSIUS":
        temperature_unit_wanted = "Temperature (°C)"

        
    elif unit_input_name == "FAHRENHEIT":
        temperature_unit_wanted = "Temperature (°F)"
    
        
    elif unit_input_name == "KELVIN":
        temperature_unit_wanted = "Temperature (K)"
    
    print(temperature_unit_wanted)

    generate_pdf('Thermography_1.csv','Got_Thermography2.pdf', temperature_unit_wanted)
    #generate_pdf('Thermography-DE0D2DEF2508.csv','Got_Thermography3.pdf', temperature_unit_wanted)
    

#   with open("Thermography-" + seekcamera.chipid + ".csv", 'r') as file_to_read:
#                file_to_read = file_to_read.read()
#               print(file_to_read)
    

def generate_pdf(csv_file_name, pdf_name, temperature_label_display):
    reader = csv.reader(open(csv_file_name, "r"), delimiter=" ")
    rows = []
    
    for row in reader:
        rows.append(row)
    
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
        
    #dataframe
    df = pd.read_csv(csv_file_name, delimiter=" ").astype(float)
    im = plt.imshow(df, cmap="jet")
    
    cbar = plt.colorbar(im)
    cbar.set_label(temperature_label_display, rotation=270, labelpad=15)
    
    plt.title(label='Thermography', fontdict=None, loc='center', pad=None)
    plt.xticks([])
    plt.yticks([])
    plt.savefig(pdf_name) 
    
    plt.show()

if __name__ == "__main__":
    main()
    
    
     
