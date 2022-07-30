
import csv
import pandas as pd

rows = []
df = pd.read_csv("Thermography_1.csv", header=None, delimiter=" ").astype(float)
print(df)

for row in df:
    rows.append(row)

choose_temp = input("which temperature?\n1 = kelvin, 2=fahrenheit\n")

if choose_temp == "1":
    #Kelvin
    temp_kelvin = df + 273.5
    temp_kelvin.to_csv('Thermography_changed_K.csv', index=False, header=False, sep=' ')
    print(temp_kelvin)

elif choose_temp == "2":
    temp_fahrenheit = df*1.8 + 32
    temp_fahrenheit.to_csv('Thermography_changed_F.csv', float_format='%.2f', index=False, header=False, sep=' ')
    print(temp_fahrenheit)

#Fahrenheit
#rows = []
#dff = pd.read_csv("Thermography_1.csv", header=None, delimiter=" ").astype(float)
#print(dff)
#for row in dff:
#    rows.append(row)
#temp_fahrenheit = df*1.8 + 32
#temp_fahrenheit.to_csv('Thermography_changed_F.csv', float_format='%.2f', index=False, header=False, sep=' ')
#print(temp_fahrenheit)


""" 
#csv_writer = csv.writer(open("output_file.csv", "w"), delimiter=" ")

#df = pd.read_csv("Thermography_1.csv")
#print(df)

for line in csv_reader:
    csv_writer.writerow(line)
    
""" 
