# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 16:47:49 2022

Plot image 

@author: Fernanda

"""

import csv
#import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def main():
    '''later also insert the possibility of choosing which
    temperature to display from the program (not typing)'''
        
    get_pdf('tentativa_1.csv','Got_Thermography2.pdf', 'Temperature (°C)')
    
    
    
def get_pdf(csv_file_name, pdf_name, temperature_display):
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
    cbar.set_label(temperature_display, rotation=270, labelpad=15)
    
    plt.title(label='Thermography', fontdict=None, loc='center', pad=None)
    plt.xticks([])
    plt.yticks([])
    plt.savefig(pdf_name) 
    
    plt.show()
    # plt.xlabel("X axis label")
    # plt.ylabel("Y axis label")
    
    
if __name__ == "__main__":
    main()
    
    
     
    # reader = csv.reader(open("tentativa_1.csv", "r"), delimiter=" ")
    # rows = []
    
    # for row in reader:
    #     rows.append(row)
    
    # #print(rows)
    
    # plt.rcParams["figure.figsize"] = [7.00, 3.50]
    # plt.rcParams["figure.autolayout"] = True
    
    
    # #dataframe
    # df = pd.read_csv('tentativa_1.csv', delimiter=" ").astype(float)
    
    # im = plt.imshow(df, cmap="jet")
    
    # cbar = plt.colorbar(im)
    # cbar.set_label('Temperature (°C)', rotation=270, labelpad=15)
    
    # plt.title(label='Thermography', fontdict=None, loc='center', pad=None)
    # plt.xticks([])
    # plt.yticks([])
    # plt.savefig('Got_Thermography.pdf') 
    
    # plt.show()
    # # plt.xlabel("X axis label")
    # # plt.ylabel("Y axis label")
  

