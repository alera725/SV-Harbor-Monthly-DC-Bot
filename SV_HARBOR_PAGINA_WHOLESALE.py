# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 13:55:11 2020

@author: alejandro.gutierrez
"""

#PAGINA PRINCIPAL SUPER VALUE WHOLE SALE 

#from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait # Guardar en las paginas
from selenium.webdriver.support import expected_conditions as EC #Guardar en las paginas import unittest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class whole_sale_page():
    def __init__(self,my_driver):
        self.driver = my_driver
        self.wholesalee = (By.XPATH, '/html/body/div[1]/main/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/a') 
        
    def wholesale(self):
        try:
            
            button = WebDriverWait(self.driver,50).until(EC.element_to_be_clickable(self.wholesalee))
            button.click()
            
        except TimeoutException:
            print ("Loading -wholesale- took too much time!")


