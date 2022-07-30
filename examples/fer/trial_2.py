# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 13:06:38 2022

@author: Asus
"""

# class Struct():
#         """ Device Info """
#         def __init__(self, serialNumber):
#             self.model = int
#             self.serialNumber = str(13)
#             # self.modelNumber = str(17)
#             # self.manufactureDate = str(33)
#         def show(self):
#             print(self.serialNumber)
        
# a = Struct()

        
class Chatbot():
    def __init__(self, nome):
        self.nome = nome
    
    def fala(self):
        print ('oi, meu nome é ' + self.nome)
        
a = Chatbot('teteio')
a.fala()
