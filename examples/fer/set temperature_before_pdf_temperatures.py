# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 11:15:22 2022
TRYING TO CONVERT DATA FRAME TEMPERATURES

"""
import csv
import seekcamera
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def main():
    '''later also insert the possibility of choosing which
    temperature to display from the program (not typing)'''
        
    unit_input = int(input("0 = CELSIUS, 1 = FAHRENHEIT, 2 = KELVIN\nWhich unit do you want?\n"))
    #unit_input=int(0)
    #unit_input=int(1)
    #unit_input=int(2)

    # use integer input to use the SeekCameraTemperatureUnit function
    # and change the format to string to be able to use 
    # and save the output at the "unit_input_name" variable

    unit_input_name=str(seekcamera.SeekCameraTemperatureUnit(unit_input))
    print("You chose " + unit_input_name) #to chechk if reading correctly
         
    #csv_file_name = 'Thermography_1.csv'
    csv_file_name = "Thermography-DE0D2DEF2508.csv"

    if unit_input_name == "CELSIUS":
        temperature_unit_wanted = "Temperature (°C)"

        pdf_name = 'Got_Thermography_C.pdf'
        generate_pdf("Thermography_1.csv",pdf_name, temperature_unit_wanted)

        
    elif unit_input_name == "FAHRENHEIT":
        temperature_unit_wanted = "Temperature (°F)"

        temperature_change(unit_input, csv_file_name, "Thermography_in_Fahrenheit.csv")
        pdf_name = 'Got_Thermography_F.pdf'
        generate_pdf("Thermography_in_Fahrenheit.csv",pdf_name, temperature_unit_wanted)

    elif unit_input_name == "KELVIN":
        temperature_unit_wanted = "Temperature (K)"

        temperature_change(unit_input, csv_file_name, "Thermography_in_Kelvin.csv")
        pdf_name = 'Got_Thermography_K.pdf'
        generate_pdf("Thermography_in_Kelvin.csv",pdf_name, temperature_unit_wanted)
    
    print(temperature_unit_wanted)

    #generate_pdf('Thermography-DE0D2DEF2508.csv','Got_Thermography3.pdf', temperature_unit_wanted)

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

def temperature_change(unit_input, csv_file_name, csv_output_file):

    rows = []
    dff = pd.read_csv(csv_file_name, header=None, delimiter=" ").astype(float)
    #print(dff)

    for row in dff:
        rows.append(row)

        #Fahrenheit
        if unit_input == int(1):
            temp_fahrenheit = dff*1.8 + 32
            temp_fahrenheit.to_csv(csv_output_file, float_format='%.2f', index=False, header=False, sep=' ')
            #print(temp_fahrenheit)
        
        #Kelvin
        elif unit_input == int(2):
            temp_kelvin = dff + 273.5
            temp_kelvin.to_csv(csv_output_file, index=False, header=False, sep=' ')
            #print(temp_kelvin)
           
        elif unit_input == int(0):
            pass

if __name__ == "__main__":
    main()
    
    
     
