# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 12:51:58 2020

@author: alejandro.gutierrez
"""

#Importar paqueterias
import os
import shutil
os.chdir('C:\\Users\\SET UP WORKING DIRECTORY PATH') # relative path: scripts dir is under Lab

import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # Guardar en las paginas
from datetime import date, timedelta
import time 
import datetime
import calendar

#Import the .py files
from SV_HARBOR_PAGINA_INICIO import initial_page
from SV_HARBOR_PAGINA_WHOLESALE import whole_sale_page
from SV_HARBOR_PAGINA_PROCESO import process_page


class Download_SuperValue_Data(unittest.TestCase):
    
    def setUp(self):
        #option = Options()
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory' : 'C:\\Users\\SET UP DOWNLOAD PATH'}
        chrome_options.add_experimental_option('prefs', prefs)
      #  chrome_options.add_argument('--headless')
        chromedriver_path = 'C:\\Users\\SET UP Chromedriver PATH'
        url = 'https://myhome.svharbor.com/siteminderagent/forms/svhlogin.fcc?TYPE=33554433&REALMOID=06-000d8ea6-308c-1c8b-8ca7-651f0aaa0000&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=$SM$DhN8BKiYjPa0wXV87nLVLAJXPtPpXtU8fiDQXhR7CAJ%2b1sh1reaPfFF%2f99NIqOJy&TARGET=$SM$https%3a%2f%2fmyhome%2esvharbor%2ecom%2fcontent%2fsvhb%2fhome%2ehtml' #Main URL
        self.driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
        self.driver.get(url)
        self.WebDriverWait = WebDriverWait
        #self.driver.implicity_wait(7)
        self.PageInitial = initial_page(self.driver)
        self.PageWholesale = whole_sale_page(self.driver)
        self.PageProcess = process_page(self.driver)
        self.dir_download = 'C:\\Users\\SET UP DOWNLOAD PATH again'
        self.driver.maximize_window()
    
    
    #@unittest.skip('Not need now') #AQUI INICIA EL TEST PARA MONTHLY DC, BAJA EL ARCHIVO DESDE EL 1RO DEL MES HASTA EL ULTIMO SABADO (A PARTIR DE LA FECHA DE EJECUCION)
    def test_Descarga_archivos_MONTLHY_DC(self):
        before = os.listdir(self.dir_download) 

        #Cargamos los datos del inicio de sesion
        email = 'XXXX'  
        pswd = 'XXXX' 
        
        #Seleccionamos el retailer deseado
        retailers = ' Montlhy DC' # SELECT FAV REPORT OR 'all'
        
        #Fecha de hoy
        today = date.today()
        today_dayname = calendar.day_name[today.weekday()] #EX. 'Wednesday'
        
        # format dd/mm/YY and we get a STR value 
        d1 = today.strftime("%d/%m/%Y")
        day = d1[0:2]
        month = d1[3:5]
        year = d1[6:11]
        
        #Encontrar el utlimo dia sabado
        idx = (today.weekday() + 1) % 7
        sat = today - datetime.timedelta(7+idx-6)  
        
        d1 = sat.strftime("%d/%m/%Y") #Last Saturday complete date
        days_month = d1[0:2]
        
        sun = sat - datetime.timedelta(days=6)
        d2 = sun.strftime("%d/%m/%Y") #Previous Sunday before of that Saturday 
        days_month_initial = d2[0:2]
            
        #Ingresar el rango de fechas que se busca descargar dd/mm/yyyy ultimo mes
        fecha_inicio = month + '/' + str(days_month_initial) + '/' + year[0:2] #'08/01/20'
        fecha_fin = month + '/' + str(days_month) + '/' + year[0:2]  #'08/31/20'
        
        
        #REVISAR SI ESTA SEMANA TOCO CAMBIO DE MES
        #Revisamos el primer dia el mes y el ultimo dia el mes, si hubo cambio vamos a ver en que dia es el ultimo o primero del nuevo mes 
        #Unique values de la cadena de todos los months de los dias de esa semana ==2 si cambio el mes, otro no
        delta = sat - sun       # as timedelta
        month_list = []
        
        for i in range(delta.days + 1):
            day = sun + timedelta(days=i)
            month_list.append(day.strftime("%d/%m/%Y")[3:5]) #list of the month of each day
        
        
        #month_list = ['09', '09', '09', '10', '10', '10', '10'] #ELIMINAR

        month_list_drop_duplicates = list(set(month_list))
        num_unique_months = len(month_list_drop_duplicates) #If we have more than 2 months we have to do something different than if we have 1 unique month
        
        if (num_unique_months==2):
            
            #Revisar en cual dia se ve el cambio de mes
            past_month = month_list_drop_duplicates[1] 
            print(past_month)
            new_month = month_list_drop_duplicates[0] 
            print(new_month)
            
            index_new_month = month_list.index(new_month) #Encontramos el dia donde inicio el mes nuevo
            #print(index_new_month)
            
            #--To First Month
            sun_end = sun + datetime.timedelta(days=index_new_month-1) #Last day of past month
            #print(sun_end)
            
            d2b = sun_end.strftime("%d/%m/%Y") #Previous Sunday before of that Saturday 
            days_month_initialb = d2b[0:2]
            
            #Ingresar el rango de fechas que se busca descargar dd/mm/yyyy ultimo mes
            fecha_inicio_a = past_month + '/' + str(days_month_initial) + '/' + year[0:2] #'08/01/20'
            fecha_fin_a = past_month + '/' + str(days_month_initialb) + '/' + year[0:2]  #'08/31/20'
            
            #--To Second Month
            sat_start = sat - datetime.timedelta(days=7-index_new_month-1)
            #print(sat_start)
            
            d1b = sat_start.strftime("%d/%m/%Y") #Previous Sunday before of that Saturday 
            days_month_b = d1b[0:2]
            
            #Ingresar el rango de fechas que se busca descargar dd/mm/yyyy ultimo mes
            fecha_inicio_b = new_month + '/' + str(days_month_b) + '/' + year[0:2] #'08/01/20'
            fecha_fin_b = new_month + '/' + str(days_month) + '/' + year[0:2]  #'08/31/20'
            
            
            #--Last Dates format
            fecha_inicio_a_format = fecha_inicio_a.replace("/", "") #'080120'
            print(fecha_inicio_a_format)
            fecha_fin_a_format = fecha_fin_a.replace("/", "")
            print(fecha_fin_a_format)
            
            fecha_inicio_b_format = fecha_inicio_b.replace("/", "") #'083120'
            print(fecha_inicio_b_format)
            fecha_fin_b_format = fecha_fin_b.replace("/", "")
            print(fecha_fin_b_format)
            
        else:
            #Proceso normal
            #Last Dates format
            fecha_inicio_format = fecha_inicio.replace("/", "") #'080120'
            fecha_fin_format = fecha_fin.replace("/", "") #'083120'        
        
    
        #Este batch solo es si queremos poner una fecha personalizada y no la ultima semana/mes...
        #fecha_inicio_format = '090120'
        #fecha_fin_format = '073120'
        
        self.PageInitial.start_session(email,pswd)
        self.PageWholesale.wholesale()
        self.PageProcess.first_window()
        self.PageProcess.clear_all()
        self.PageProcess.set_MonthlyDC()
        
        
        #AQUI TAMBIEN SE HACE UN PROCESO DISTINTO SI HUBO CAMBIO DE MES ESA SEMANA O SI NO LO HUBO
        if(num_unique_months==2):
            self.PageProcess.set_date_range(fecha_inicio_a_format,fecha_fin_a_format)
            self.PageProcess.download_page()
            time.sleep(5)
            
            #Esperar a que la descarga se complete
            after = os.listdir(self.dir_download) 
            change = set(after) - set(before)
            while len(change) != 1:
                after = os.listdir(self.dir_download) 
                change = set(after) - set(before)
                if len(change) == 1:
                    file_name = change.pop()
                    break
                else:
                    continue
                        
            time.sleep(120) #REDUCIR ESTE TIEMPO DE ESPERA
            
            #CHECAR LA ULTIMA DESCARGA (PARA CAMBIAR EL NOMBRE A LA ULTIMA DESCARGA)
            Current_Date = datetime.datetime.now().strftime("%d-%b-%Y %HHr %MMin") 
            Initial_path = self.dir_download 
            filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
            new_name = 'FIRST SUPER VALU %s ' %retailers + str(Current_Date) + '.csv'
            shutil.move(filename,os.path.join(Initial_path,r'%s' %new_name))
            
            #MOVER EL ARCHIVO A LA UBICACION DESEADA
            new_download = 'C:\\Users\\SET UP PATH YO WANT TO MOVE DOWNLOAD FILE'
            shutil.move('%s'%self.dir_download+'\\%s'%new_name, '%s'%new_download+'\\%s'%new_name)
            
            #volver a checar si la carpeta de downloads tiene algun archivo (volverlo a mover) o si no tiene ninguna entonces fin, Ver que solo se descargue un archivo 
            time.sleep(2)
            number_of_files = len([name for name in os.listdir(self.dir_download) if os.path.isfile(os.path.join(self.dir_download, name))])
            if number_of_files==1:
                filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
                print(filename)
                shutil.move('%s'%filename, '%s'%new_download)
            else:
                pass
            
            
            #REGRESAR A LA PAGINA ANTERIOR PARA DESCARGAR LOS DATOS DEL MES MAS RECIENTE 
            #Close window
            before = os.listdir(self.dir_download)
            self.PageProcess.close_window()
            self.PageProcess.clear_all()
            self.PageProcess.set_MonthlyDC()     
            #clickear en otro elemento por que se queda la ventana del calendario estorbando
            tablefavorite_searches = 'facetMyFavSearch'
            self.driver.find_element_by_id(tablefavorite_searches).click()
            self.PageProcess.set_date_range(fecha_inicio_b_format,fecha_fin_b_format)
            self.PageProcess.download_page()
            time.sleep(5)
            
            #Esperar a que la descarga se complete
            after = os.listdir(self.dir_download) 
            change = set(after) - set(before)
            while len(change) != 1:
                after = os.listdir(self.dir_download) 
                change = set(after) - set(before)
                if len(change) == 1:
                    file_name = change.pop()
                    break
                else:
                    continue
                        
            time.sleep(150) #REDUCIR ESTE TIEMPO DE ESPERA
            
            #CHECAR LA ULTIMA DESCARGA (PARA CAMBIAR EL NOMBRE A LA ULTIMA DESCARGA)
            Current_Date = datetime.datetime.now().strftime("%d-%b-%Y %HHr %MMin") 
            Initial_path = self.dir_download 
            filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
            new_name = 'SECOND SUPER VALU %s ' %retailers + str(Current_Date) + '.csv'
            shutil.move(filename,os.path.join(Initial_path,r'%s' %new_name))
            
            #MOVER EL ARCHIVO A LA UBICACION DESEADA
            new_download = 'C:\\Users\\SET UP PATH YO WANT TO MOVE DOWNLOAD FILE'
            shutil.move('%s'%self.dir_download+'\\%s'%new_name, '%s'%new_download+'\\%s'%new_name)
            
            #volver a checar si la carpeta de downloads tiene algun archivo (volverlo a mover) o si no tiene ninguna entonces fin, Ver que solo se descargue un archivo 
            time.sleep(2)
            number_of_files = len([name for name in os.listdir(self.dir_download) if os.path.isfile(os.path.join(self.dir_download, name))])
            if number_of_files==1:
                filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
                print(filename)
                shutil.move('%s'%filename, '%s'%new_download)
            else:
                pass            
            
            
                
        else:
            self.PageProcess.set_date_range(fecha_inicio_format,fecha_fin_format)
            self.PageProcess.download_page()
            time.sleep(5)
            
            #Esperar a que la descarga se complete
            after = os.listdir(self.dir_download) 
            change = set(after) - set(before)
            while len(change) != 1:
                after = os.listdir(self.dir_download) 
                change = set(after) - set(before)
                if len(change) == 1:
                    file_name = change.pop()
                    break
                else:
                    continue
                        
            time.sleep(150) #REDUCIR ESTE TIEMPO DE ESPERA
            #CHECAR LA ULTIMA DESCARGA (PARA CAMBIAR EL NOMBRE A LA ULTIMA DESCARGA)
            Current_Date = datetime.datetime.now().strftime("%d-%b-%Y %HHr %MMin") 
            Initial_path = self.dir_download 
            filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
            new_name = 'SUPER VALU %s ' %retailers + str(Current_Date) + '.csv'
            shutil.move(filename,os.path.join(Initial_path,r'%s' %new_name))
            
            #MOVER EL ARCHIVO A LA UBICACION DESEADA
            new_download = 'C:\\Users\\SET UP PATH YO WANT TO MOVE DOWNLOAD FILE'
            shutil.move('%s'%self.dir_download+'\\%s'%new_name, '%s'%new_download+'\\%s'%new_name)
            
            #volver a checar si la carpeta de downloads tiene algun archivo (volverlo a mover) o si no tiene ninguna entonces fin, Ver que solo se descargue un archivo 
            time.sleep(2)
            number_of_files = len([name for name in os.listdir(self.dir_download) if os.path.isfile(os.path.join(self.dir_download, name))])
            if number_of_files==1:
                filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
                print(filename)
                shutil.move('%s'%filename, '%s'%new_download)
            else:
                pass            
            
            
        #Listo
        print("%s SV is READY!!" %retailers) 
        time.sleep(3)
    


    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        
        
        
if __name__ == '__main__':
    unittest.main()
       
        
        
        
        
        
        
        
        
        

        