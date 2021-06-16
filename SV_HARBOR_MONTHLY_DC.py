# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 12:51:58 2020

@author: alejandro.gutierrez
"""

#Importar paqueterias
import os
import shutil
os.chdir('C:\\Users\\alejandro.gutierrez\\OneDrive - Carlin Group - CA Fortune\\Documents\\ALEJANDRO RAMOS GTZ\\PYTHON')

import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By

from datetime import date, timedelta
import time 
import datetime
import calendar
import json

from SV_HARBOR_PAGINA_INICIO import initial_page
from SV_HARBOR_PAGINA_WHOLESALE import whole_sale_page
from SV_HARBOR_PAGINA_PROCESO import process_page


class Download_SuperValue_Data(unittest.TestCase):
    
    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        prefs = {'download.default_directory' : 'C:\\Users\\alejandro.gutierrez\\OneDrive - Carlin Group - CA Fortune\\Documents\\KROGER SELENIUM\\DOWNLOADS'} #'C:\\Users\\alejandro.gutierrez\\OneDrive - Carlin Group - CA Fortune\\Documents\\ALEJANDRO RAMOS GTZ\\TEST'} #CAMBIAR ESTO PARA CADA TEST
        chrome_options.add_experimental_option('prefs', prefs)
       #chrome_options.add_argument('--headless')
        chromedriver_path = 'C:\\Users\\alejandro.gutierrez\\OneDrive - Carlin Group - CA Fortune\\Documents\\ALEJANDRO RAMOS GTZ\\PYTHON\\chromedriver'
        url = 'https://myhome.svharbor.com/siteminderagent/forms/svhlogin.fcc?TYPE=33554433&REALMOID=06-000d8ea6-308c-1c8b-8ca7-651f0aaa0000&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=$SM$A2B0iCpbmbLLMgkIF4IjrjvRfda87wfgFDIDSEjuhps4ZSB%2bGCC9OELQczQ9D4b7&TARGET=$SM$https%3a%2f%2fmyhome%2esvharbor%2ecom%2fcontent%2fsvhb%2fhome%2ehtml'
        self.driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
        self.driver.get(url)
        self.WebDriverWait = WebDriverWait
        #self.driver.implicity_wait(7)
        self.PageInitial = initial_page(self.driver)
        self.PageWholesale = whole_sale_page(self.driver)
        self.PageProcess = process_page(self.driver)
        self.dir_download = 'C:\\Users\\alejandro.gutierrez\\OneDrive - Carlin Group - CA Fortune\\Documents\\KROGER SELENIUM\\DOWNLOADS'
        self.driver.maximize_window()
        
        with open('C:\\Users\\alejandro.gutierrez\\OneDrive - Carlin Group - CA Fortune\\Documents\\ALEJANDRO RAMOS GTZ\\PYTHON\\SV HARBOR BOT\\info.json') as json_file:
            data = json.load(json_file)
            self.email = data["user_sv"]
            self.pswd = data["pass_sv"]
    
    #@unittest.skip('Not need now') #AQUI INICIA EL TEST PARA MONTHLY DC, BAJA EL ARCHIVO DESDE EL 1RO DEL MES HASTA EL ULTIMO SABADO (A PARTIR DE LA FECHA DE EJECUCION)
    def test_Descarga_archivos_MONTLHY_DC(self):
        before = os.listdir(self.dir_download) 

        #Cargamos los datos del inicio de sesion
        email = self.email  
        pswd = self.pswd 
        
        #Seleccionamos el retailer deseado
        retailers = ['7556838', '5983846', '7576696', '682484', '7360407', '157008', '5752092', '7354383', '133181', '7528374', '293894',
                     '7397373', '647438', '5068390', '699421', '7126469', '7390112', '432625', '7614403', '7544402', '5290002', '7570839',
                     '460865', '7574550', '782490', '7388212', '7389454', '385666', '7533421', '7597929', '6958565', '740951', '5153309',
                     '754507', '7553720', '7550276', '7352064', '194423', '616235', '7396567', '130192', '880450', '392571', '7341589',
                     '7507868', '7353576'] #' Montlhy DC' # 38811 - Plb Sports Inc' #'all' #or ' 24158 - American Licorice Co' or 'all'
        
        #Fecha de hoy
        today = date.today()
        #today = datetime.date(2021, 1, 20) #Este solo lo usamos si queremos modificar la fecha en la que se esta corriendo el script formato ANO MES DIA

        # format dd/mm/YY and we get a STR value
        #Revisamos si el mes del dia de hoy cambio con respecto al mes de la semana pasada
        idx = (today.weekday() + 1) % 7
        d0 = today - datetime.timedelta(7+idx)  
        d0 = d0.strftime("%d/%m/%Y")
        monthd0 = d0[3:5]
        
        d1 = today.strftime("%d/%m/%Y")
        monthd1 = d1[3:5]
        
        if (monthd0 != monthd1):
            month = monthd0
        else:
            month = monthd1
            
        day = d1[0:2]
        year = d1[6:11]
        
        #Encontrar el utlimo dia sabado
        idx = (today.weekday() + 1) % 7
        sat = today - datetime.timedelta(7+idx-6)  
        
        d1 = sat.strftime("%d/%m/%Y") #Last Saturday complete date
        days_month = d1[0:2]
        
        sun = sat - datetime.timedelta(days=6)
        d2 = sun.strftime("%d/%m/%Y") #Previous Sunday before that Saturday 
        days_month_initial = d2[0:2]
            
        #Ingresar el rango de fechas que se busca descargar dd/mm/yyyy ultimo mes
        fecha_inicio = month + '/' + str(days_month_initial) + '/' + year[2:4] #'08/01/20'
        print(fecha_inicio)
        fecha_fin = month + '/' + str(days_month) + '/' + year[2:4]  #'08/31/20'
        print(fecha_fin)

        #REVISAR SI ESTA SEMANA TOCO CAMBIO DE MES
        #Revisamos el primer dia el mes y el ultimo dia el mes, si hubo cambio vamos a ver en que dia es el ultimo o primero del nuevo mes 
        #Unique values de la cadena de todos los months de los dias de esa semana ==2 si cambio el mes, otro no
        delta = sat - sun       # as timedelta
        month_list = []
        year_list = []
        
        for i in range(delta.days + 1):
            day = sun + timedelta(days=i)
            month_list.append(day.strftime("%d/%m/%Y")[3:5]) #list of the month of each day
            year_list.append(day.strftime("%d/%m/%Y")[6:10])
        
        
        #month_list = ['09', '09', '09', '10', '10', '10', '10'] #ELIMINAR

        month_list_drop_duplicates = list(set(month_list))        
        num_unique_months = len(month_list_drop_duplicates) #If we have more than 2 months we have to do something different than if we have 1 unique month
        
        year_list_drop_duplicates = list(set(year_list))
        num_unique_years = len(year_list_drop_duplicates)
        
        #num_unique_months=0 #Solo poner en caso de poner manualmente las fechas 
        
        if (num_unique_months==2):
            if (num_unique_years==2):
                #Revisar en cual dia se ve el cambio de mes
                past_month = month_list_drop_duplicates[1] 
                print(past_month)
                new_month = month_list_drop_duplicates[0] 
                print(new_month)
                
                past_year = year_list_drop_duplicates[1] 
                print(past_year)
                new_year = year_list_drop_duplicates[0] 
                print(new_year)
                
                index_new_month = month_list.index(new_month) #Encontramos el dia donde inicio el mes nuevo
                #print(index_new_month)
                
                #--To First Month
                sun_end = sun + datetime.timedelta(days=index_new_month-1) #Last day of past month
                #print(sun_end)
                
                d2b = sun_end.strftime("%d/%m/%Y") #Previous Sunday before of that Saturday 
                days_month_initialb = d2b[0:2]
                
                #Ingresar el rango de fechas que se busca descargar dd/mm/yyyy ultimo mes
                fecha_inicio_a = past_month + '/' + str(days_month_initial) + '/' + past_year[2:4] #'08/01/20'
                fecha_fin_a = past_month + '/' + str(days_month_initialb) + '/' + past_year[2:4]  #'08/31/20'
                
                #--To Second Month
                sat_start = sat - datetime.timedelta(days=7-index_new_month-1)
                #print(sat_start)
                
                d1b = sat_start.strftime("%d/%m/%Y") #Previous Sunday before of that Saturday 
                days_month_b = d1b[0:2]
                
                #Ingresar el rango de fechas que se busca descargar dd/mm/yyyy ultimo mes
                fecha_inicio_b = new_month + '/' + str(days_month_b) + '/' + new_year[2:4] #'08/01/20'
                fecha_fin_b = new_month + '/' + str(days_month) + '/' + new_year[2:4]  #'08/31/20'
                
                
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
                
                month_list_drop_duplicates = [min(month_list_drop_duplicates),max(month_list_drop_duplicates)]
                
                #Revisar en cual dia se ve el cambio de mes
                past_month = month_list_drop_duplicates[0] 
                print(past_month)
                new_month = month_list_drop_duplicates[1] 
                print(new_month)
                
                index_new_month = month_list.index(new_month) #Encontramos el dia donde inicio el mes nuevo
                #print(index_new_month)
                
                #--To First Month
                sun_end = sun + datetime.timedelta(days=index_new_month-1) #Last day of past month
                #print(sun_end)
                
                d2b = sun_end.strftime("%d/%m/%Y") #Previous Sunday before of that Saturday 
                days_month_initialb = d2b[0:2]
                
                #Ingresar el rango de fechas que se busca descargar dd/mm/yyyy ultimo mes
                fecha_inicio_a = past_month + '/' + str(days_month_initial) + '/' + year[2:4] #'08/01/20'
                fecha_fin_a = past_month + '/' + str(days_month_initialb) + '/' + year[2:4]  #'08/31/20'
                
                #--To Second Month
                sat_start = sat - datetime.timedelta(days=7-index_new_month-1)
                #print(sat_start)
                
                d1b = sat_start.strftime("%d/%m/%Y") #Previous Sunday before of that Saturday 
                days_month_b = d1b[0:2]
                
                #Ingresar el rango de fechas que se busca descargar dd/mm/yyyy ultimo mes
                fecha_inicio_b = new_month + '/' + str(days_month_b) + '/' + year[2:4] #'08/01/20'
                fecha_fin_b = new_month + '/' + str(days_month) + '/' + year[2:4]  #'08/31/20'
                
                
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
            print(fecha_inicio_format)
            fecha_fin_format = fecha_fin.replace("/", "") #'083120'        
            print(fecha_fin_format)

    
        #Este batch solo es si queremos poner una fecha personalizada y no la ultima semana/mes...
        #fecha_inicio_format = '090120'
        #fecha_fin_format = '073120'

        
        self.PageInitial.start_session(email,pswd)
        self.PageWholesale.wholesale()
        self.PageProcess.first_window()
        self.PageProcess.clear_all()
        self.PageProcess.set_week_ending()

        #ID_FAVSEARCHES = 'facetMyFavSearch' #CLICK
        #XPATH_MONTHLY_DC = '//*[@id="myFavoriteSearches:j_idt126:4:j_idt128"]' #Monthly DC '/html/body/div[1]/div[2]/div[2]/div[2]/div/form/div[2]/span[2]/span[1]/div/div[2]/span/span/div/span/div/table/tbody[1]/tr[5]/td[1]/a'
        #'//*[@id="myFavoriteSearches:j_idt126:4:j_idt127"]'
        #self.PageProcess.set_MonthlyDC()
        #self.PageProcess.set_vendor('7614403 - Jump Start Foods')
        self.PageProcess.set_vendor(retailers,1)
        #self.PageProcess.set_endweekday()
        
        #AQUI SI LOS MESES SON DOS ENTONCES SE REGRESA A LA PAGINA Y DESCARGA EL ARCHIVO B
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
                        
            time.sleep(200) #REDUCIR ESTE TIEMPO DE ESPERA
            #CHECAR LA ULTIMA DESCARGA (PARA CAMBIAR EL NOMBRE A LA ULTIMA DESCARGA)
            Current_Date = datetime.datetime.now().strftime("%d-%b-%Y %HHr %MMin") 
            Initial_path = self.dir_download 
            filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
            new_name = 'FIRST SUPER VALU MONTLHY DC ' + str(Current_Date) + '.csv'
            shutil.move(filename,os.path.join(Initial_path,r'%s' %new_name))
            
            #MOVER EL ARCHIVO A LA UBICACION DESEADA
            new_download = 'C:\\Users\\alejandro.gutierrez\\OneDrive - Carlin Group - CA Fortune\\Documents\\KROGER SELENIUM\\SUPER VALU\\MONTHLY_DC'
            shutil.move('%s'%self.dir_download+'\\%s'%new_name, '%s'%new_download+'\\%s'%new_name)
            
            #Mas bien una vez que termine, volver a checar si la carpeta de downloads tiene algun archivo (volverlo a mover) o si no tiene ninguna entonces fin, Ver que solo se descargue un archivo 
            #dir_download = 'C:\\Users\\alejandro.gutierrez\\OneDrive - Carlin Group - CA Fortune\\Documents\\KROGER SELENIUM\\DOWNLOADS'
            #print(len([name for name in os.listdir(dir_download) if os.path.isfile(os.path.join(dir_download, name))]))
            time.sleep(2)
            number_of_files = len([name for name in os.listdir(self.dir_download) if os.path.isfile(os.path.join(self.dir_download, name))])
            if number_of_files==1:
                filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
                print(filename)
                shutil.move('%s'%filename, '%s'%new_download)
            else:
                pass
            
            
            #REGRESAR A LA PAGINA ANTERIOR FALTA PONER ESO
            #Close window
            before = os.listdir(self.dir_download)
            self.PageProcess.close_window()
            self.PageProcess.clear_all()

            #ESTO LO COMENTE EL 06/08/2021 YA QUE NO SE VEIA EL VENDOR BUTTON
            #CLickar en otro boton y para que el de la fecha se vea 
            organization = '//*[@id="facetOrgs"]/div[1]'
            #self.driver.find_element_by_xpath(organization).click()
            dist_center = '//*[@id="facetDc"]/div[1]/div'
            #self.driver.find_element_by_xpath(dist_center).click()
            fav_searches = '//*[@id="facetMyFavSearch"]/div[1]/div'
            #self.driver.find_element_by_xpath(fav_searches).click()
            
            week_end_button = WebDriverWait(self.driver,50).until(EC.visibility_of_element_located((By.ID ,'facetWeekEnding')))
            week_end_button.click()
            
            #Dist. center 
            self.driver.find_element_by_xpath(dist_center).click()
            
            
            
            #click date and range
            date_button = (By.XPATH, '//*[@id="facetDate"]/div[1]') #Click en seccion Date 
            date_range = '//*[@id="date:dateEntryType:1"]'
            
            datebutton = WebDriverWait(self.driver,20).until(EC.element_to_be_clickable(date_button))
            datebutton.click()
            
            time.sleep(5)
            
            rango = self.driver.find_element_by_xpath(date_range)
            rango.click()
            time.sleep(5)
           
            day_end_id= 'date:rangeEndDate'
            dia_end = self.driver.find_element_by_id(day_end_id)
            dia_end.send_keys(fecha_fin_b_format) #EL VALOR DE LA FECHA EN FORMATO MMDDYY EJ. 080120 (08 DE AGOSTO DEL 2020)
            
        
            self.driver.find_element_by_xpath(fav_searches).click()
            week_end_button.click()
            datebutton.click()
            
            
            
            self.PageProcess.set_vendor(retailers,2) #El dos es para que no vuelva a clickar en el boton de vendors al final

            self.PageProcess.set_week_ending()

            #clickear en otro elemento por que se queda la ventana del calendario estorbando
            time.sleep(2)  
            
            self.driver.find_element_by_xpath(dist_center).click()

            
            week_ending = 'weekEnding:weekEndingToggleImg'
            self.driver.find_element_by_id(week_ending).click()   
            
            time.sleep(2)
            
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
                        
            time.sleep(200) #REDUCIR ESTE TIEMPO DE ESPERA
            #CHECAR LA ULTIMA DESCARGA (PARA CAMBIAR EL NOMBRE A LA ULTIMA DESCARGA)
            Current_Date = datetime.datetime.now().strftime("%d-%b-%Y %HHr %MMin") 
            Initial_path = self.dir_download 
            filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
            new_name = 'SECOND SUPER VALU MONTLHY DC ' + str(Current_Date) + '.csv'
            shutil.move(filename,os.path.join(Initial_path,r'%s' %new_name))
            
            #MOVER EL ARCHIVO A LA UBICACION DESEADA
            new_download = 'C:\\Users\\alejandro.gutierrez\\OneDrive - Carlin Group - CA Fortune\\Documents\\KROGER SELENIUM\\SUPER VALU\\MONTHLY_DC'
            shutil.move('%s'%self.dir_download+'\\%s'%new_name, '%s'%new_download+'\\%s'%new_name)
            
            #Mas bien una vez que termine, volver a checar si la carpeta de downloads tiene algun archivo (volverlo a mover) o si no tiene ninguna entonces fin, Ver que solo se descargue un archivo 
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
                        
            time.sleep(200) #REDUCIR ESTE TIEMPO DE ESPERA
            #CHECAR LA ULTIMA DESCARGA (PARA CAMBIAR EL NOMBRE A LA ULTIMA DESCARGA)
            Current_Date = datetime.datetime.now().strftime("%d-%b-%Y %HHr %MMin") 
            Initial_path = self.dir_download 
            filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
            new_name = 'SUPER VALU MONTLHY DC ' + str(Current_Date) + '.csv'
            shutil.move(filename,os.path.join(Initial_path,r'%s' %new_name))
            
            #MOVER EL ARCHIVO A LA UBICACION DESEADA
            new_download = 'C:\\Users\\alejandro.gutierrez\\OneDrive - Carlin Group - CA Fortune\\Documents\\KROGER SELENIUM\\SUPER VALU\\MONTHLY_DC'
            shutil.move('%s'%self.dir_download+'\\%s'%new_name, '%s'%new_download+'\\%s'%new_name)
            
            #Mas bien una vez que termine, volver a checar si la carpeta de downloads tiene algun archivo (volverlo a mover) o si no tiene ninguna entonces fin, Ver que solo se descargue un archivo 
            time.sleep(2)
            number_of_files = len([name for name in os.listdir(self.dir_download) if os.path.isfile(os.path.join(self.dir_download, name))])
            if number_of_files==1:
                filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
                print(filename)
                shutil.move('%s'%filename, '%s'%new_download)
            else:
                pass            
            
            
            
            
        #Listo
        print("SV MONTLHY DC is READY!!" ) 
        time.sleep(3)



    @unittest.skip('Not need now') #ESTE SOLO SE ACTIVA EN INICIO DEL MES 
    def test_VOID(self):
        before = os.listdir(self.dir_download) 

        #Cargamos los datos del inicio de sesion
        email = self.email  
        pswd = self.pswd # Silver654 'Orange987'   #CAMBIAR CONTRASE;A Indigo987 HALLOWEEN 1 JULIO AL DIA QUE SE SAQUE EL REPORTE (LUNES EN LA MANANA O A LAS 12.30)
        
        #Seleccionamos el retailer deseado
        retailers = ['5983846', '7553720', '157008', '5752092', '7396567', '7528374', '293894', '647438', '5068390', '7614403',
                     '7544402', '385666', '6958565', '194423', '880450', '7353576'] #' Montlhy DC' # 38811 - Plb Sports Inc' #'all' #or ' 24158 - American Licorice Co' or 'all'
        
        #Fecha de hoy
        today = date.today()


        # format dd/mm/YY and we get a STR value
        d1 = today.strftime("%d/%m/%Y")

        
        #Encontrar el utlimo dia sabado
        idx = (today.weekday() + 1) % 7
        sat = today - datetime.timedelta(7+idx-6)  
        
        d1 = sat.strftime("%d/%m/%Y") #Last Saturday complete date
        day = d1[0:2]
        month = d1[3:5]
        year = d1[6:11]
        
        #Encontrar el Domingo de inicio para esas 12 semanas previas
        twelve_weeks = sat - datetime.timedelta(weeks=12)
        tw_sunday = twelve_weeks + datetime.timedelta(1) 
        d2 = tw_sunday.strftime("%d/%m/%Y") #Aqui tendremos -12 semanas  
        days_month_initial = d2[0:2]
        month_initial = d2[3:5]
        year_initial = d2[6:11]
        
        #Ingresar el rango de fechas que se busca descargar dd/mm/yyyy ultimo mes
        fecha_inicio = month_initial + '/' + str(days_month_initial) + '/' + year_initial[2:4] #'08/01/20'
        print(fecha_inicio)
        fecha_fin = month + '/' + str(day) + '/' + year[2:4]  #'08/31/20'
        print(fecha_fin)
        
        fecha_inicio_format = fecha_inicio.replace("/", "") #'080120'
        print(fecha_inicio_format)
        fecha_fin_format = fecha_fin.replace("/", "") #'083120'        
        print(fecha_fin_format)
        
        self.PageInitial.start_session(email,pswd)
        self.PageWholesale.wholesale()
        self.PageProcess.first_window()
        self.PageProcess.clear_all()
        self.PageProcess.set_week_ending()      
        self.PageProcess.set_vendor(retailers,1)
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
                    
        time.sleep(200) #REDUCIR ESTE TIEMPO DE ESPERA
        #CHECAR LA ULTIMA DESCARGA (PARA CAMBIAR EL NOMBRE A LA ULTIMA DESCARGA)
        Current_Date = datetime.datetime.now().strftime("%d-%b-%Y %HHr %MMin") 
        Initial_path = self.dir_download 
        filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
        new_name = 'VOID SUPER VALU ' + str(Current_Date) + '.csv'
        shutil.move(filename,os.path.join(Initial_path,r'%s' %new_name))
        
        #MOVER EL ARCHIVO A LA UBICACION DESEADA
        new_download = 'C:\\Users\\alejandro.gutierrez\\OneDrive - Carlin Group - CA Fortune\\Documents\\KROGER SELENIUM\\SUPER VALU\\VOID'
        shutil.move('%s'%self.dir_download+'\\%s'%new_name, '%s'%new_download+'\\%s'%new_name)
        
        #Mas bien una vez que termine, volver a checar si la carpeta de downloads tiene algun archivo (volverlo a mover) o si no tiene ninguna entonces fin, Ver que solo se descargue un archivo 
        #dir_download = 'C:\\Users\\alejandro.gutierrez\\OneDrive - Carlin Group - CA Fortune\\Documents\\KROGER SELENIUM\\DOWNLOADS'
        #print(len([name for name in os.listdir(dir_download) if os.path.isfile(os.path.join(dir_download, name))]))
        time.sleep(2)
        number_of_files = len([name for name in os.listdir(self.dir_download) if os.path.isfile(os.path.join(self.dir_download, name))])
        if number_of_files==1:
            filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
            print(filename)
            shutil.move('%s'%filename, '%s'%new_download)
        else:
            pass

        print("SV VOID monthly is READY!!!!") 
        time.sleep(3)
    


    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        
        
        
if __name__ == '__main__':
    unittest.main()
       
       
        
        
        
        
        
        
        
        
        

        