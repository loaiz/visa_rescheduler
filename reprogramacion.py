# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:38:17 2023

@author: Yeferson Loaiza
"""
import re
import time
import requests
import locale
from datetime import datetime, timedelta
from time import sleep
# from bs4 import BeautifulSoup
from selenium import webdriver
# from browsermobproxy import Server
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

# parametros
url = 'https://ais.usvisa-info.com/es-co/niv/users/sign_in'

user = 'vivianazapata2679@gmail.com'
password = '3024128781'
# ruta_extension = r"C:\Users\AMD\Documents\Proyectos\visa_rescheduler\VPN-Gratis-ZenMate-Mejor-Free-VPN-para-Chrome-Chrome-Web-Store.crx"

# Configurar ChromeOptions para cargar la extensión

# C:\Users\AMD\AppData\Local\Google\Chrome\User Data

# Configura las opciones del navegador
opc = webdriver.ChromeOptions()
opc.add_argument("--start-maximized")
# opc.add_argument(r"user-data-dir=C:\Users\AMD\AppData\Local\Google\Chrome\User Data")  # Ruta a los datos del usuario
# opc.add_extension(ruta_extension)
# extension_id = "fdcgdnkidjaadafnichfpabhfomcebme"
# opc.add_argument(f"--load-extension=C:/Users/usuario/AppData/Local/Google/Chrome/User Data/Default/Extensions/{extension_id}")

# opc.add_argument("--window-size=1920x1080")
opc.add_argument('--ignore-certificate-errors')
opc.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36')
opc.add_experimental_option("excludeSwitches", ["enable-automation"])
opc.add_argument("disable-infobars")
# opc.add_argument("disable-gpu")

opc.add_argument("--disable-blink-features=AutomationControlled")

# Desactivar sandbox y especificar puerto de DevTools
# opc.add_argument("--no-sandbox")
# opc.add_argument("--remote-debugging-port=0")  # O usa 9222 si es necesario

opc.add_experimental_option('useAutomationExtension', False)
prefs = {'download.default_directory': r"C:\Users\Yeferson Loaiza\OneDrive\Documentos\Poliseguros\DocumentosSura", "download.prompt_for_download": False, "safebrowsing_for_trusted_sources_enabled": False}
opc.add_experimental_option('prefs', prefs)


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=opc)
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


# Habilitar la interceptación de red
# driver.execute_cdp_cmd('Network.enable', {})

def LimpiarCampos(xpath):
    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.XPATH,xpath,)))\
        .clear()

def clic(ruta):
    try:
        WebDriverWait(driver, 2)\
        .until(EC.element_to_be_clickable((By.XPATH,ruta)))\
        .click()
    except:
        WebDriverWait(driver, 2)\
        .until(EC.presence_of_element_located((By.XPATH,ruta)))\
        .click()

def typeInXPATH(ruta,teclas):
    #time.sleep(3)
    try:
        WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.XPATH,ruta,)))\
        .send_keys(teclas)
    except:
        WebDriverWait(driver, 5)\
        .until(EC.presence_of_element_located((By.XPATH,ruta,)))\
        .send_keys(teclas)

def sFrameSearch(driver1,xpath):
    driver1.find_element_by_xpath(xpath).clear()
    time.sleep(5)
   
def sCheck(driver1,xpath):
    driver1.find_element_by_xpath(xpath).click()
    time.sleep(5)
 
# driver.implicitly_wait(10)  # Espera implícita para que los elementos carguen

# driver.get("chrome-extension://fdcgdnkidjaadafnichfpabhfomcebme/popup.html")
    
# se conecta a la pagina de citas de la visa
driver.get(url)

time.sleep(1)
# ingresamos usuario
typeInXPATH('//*[@id="user_email"]', user)
time.sleep(1)
# ingresamos contraseña
typeInXPATH('//*[@id="user_password"]', password)
time.sleep(1)
# se aceptan terminos y condiciones
clic('//*[@id="sign_in_form"]/div[3]/label')
time.sleep(1)
# se da click en el boton del login
clic('//*[@id="sign_in_form"]/p[1]/input')




# ciclo para validar inicio de sesion exitoso
cond = True
contador = 0
while cond:
    if contador == 10:
        cond = False
    else:
        try:
            iterador = driver.find_element(By.XPATH, '//*[@id="header"]/nav/div/div/div[1]/div[2]').text
            if iterador == 'Colombia':
                time.sleep(1)
                citaConsular = driver.find_element(By.XPATH, '/html/body/div[4]/main/div[2]/div[2]/div[1]/div/div/div[2]/p[1]').text
                citaCas = driver.find_element(By.XPATH, '/html/body/div[4]/main/div[2]/div[2]/div[1]/div/div/div[2]/p[2]').text
                cond = False
            else:
                cond = True
        except Exception:
            cond = True
    contador +=1



# regex fechas
pattern = r"(\d{1,2} \w+, \d{4})"

matchConsular = re.search(pattern, citaConsular).group(1)
matchCas = re.search(pattern, citaCas).group(1)


# formato fechas
locale.setlocale(locale.LC_TIME, 'es_ES')

dateConsular = datetime.strptime(matchConsular, '%d %B, %Y').strftime('%Y-%m-%d')
dateCas = datetime.strptime(matchCas, '%d %B, %Y').strftime('%Y-%m-%d')


#menu reprogrmar cita
time.sleep(1)
continue_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Continuar')]"))
        )
    
continue_link.click()

WebDriverWait(driver, 10).until(
    EC.url_to_be("https://ais.usvisa-info.com/es-co/niv/schedule/58108463/continue_actions")
)

driver.get("https://ais.usvisa-info.com/es-co/niv/schedule/58108463/appointment")

# Espera a que la URL de la página se cargue completamente
WebDriverWait(driver, 10).until(
    EC.url_to_be("https://ais.usvisa-info.com/es-co/niv/schedule/58108463/appointment")
)

reschedulerVisa = True

while reschedulerVisa:
    
    time.sleep(3)
    
    date_input = driver.find_element("id", "appointments_consulate_appointment_date")
    date_input.click()
    
    calendarConsular = True
    
    while calendarConsular:
    
        available_dates = driver.find_elements(By.XPATH,"//td[not(contains(@class, 'ui-state-disabled'))]//a")
        
        if available_dates:
            # Selecciona la primera fecha disponible
            available_dates[0].click()
            
            calendarConsular = False
    
        else:
            print("No hay fechas disponibles")
            next_button = driver.find_element(By.XPATH,"//a[@data-handler='next']")
            next_button.click()
    
    dateInputConsular = driver.find_element("id", "appointments_consulate_appointment_date").get_attribute('value')
    
    selectedDateConsular = datetime.strptime(dateInputConsular, "%Y-%m-%d").date()
    comparisonDateConsular = datetime.strptime(dateConsular, "%Y-%m-%d").date()
    
    
    clic('//*[@id="appointments_consulate_appointment_time"]')
    try:
        clic('/html/body/div[4]/main/div[4]/div/div/form/fieldset[1]/ol/fieldset/div/div[1]/div[3]/li[2]/select/option[2]')
        pass
    except Exception:
        pass
           
    if selectedDateConsular < comparisonDateConsular:
        print(f"La fecha seleccionada ({selectedDateConsular}) es anterior a {comparisonDateConsular}.")
        
        time.sleep(2)
        date_input = driver.find_element("id", "appointments_asc_appointment_date")
        date_input.click()

        calendarCas = True

        while calendarCas:

            available_dates = driver.find_elements(By.XPATH,"//td[not(contains(@class, 'ui-state-disabled'))]//a")
            
            if available_dates:
                # Selecciona la primera fecha disponible
                available_dates[0].click()
                
                calendarCas = False

            else:
                print("No hay fechas disponibles")
                next_button = driver.find_element(By.XPATH,"//a[@data-handler='next']")
                next_button.click()

        dateInputCas = driver.find_element("id", "appointments_asc_appointment_date").get_attribute('value')

        selectedDateCas = datetime.strptime(dateInputCas, "%Y-%m-%d").date()

        clic('//*[@id="appointments_asc_appointment_time"]')


        try:
            clic('/html/body/div[4]/main/div[4]/div/div/form/fieldset[2]/ol/fieldset/div/div/div[1]/div/div[3]/li/select/option[2]')

            pass
        except Exception:
            pass

        if selectedDateCas < selectedDateConsular:
            print(f"La fecha seleccionada ({selectedDateConsular}) es anterior a {comparisonDateConsular}.")
            reschedulerVisa = False
        else:
            print(f"La fecha seleccionada ({selectedDateConsular}) NO es anterior a {comparisonDateConsular}.")
            time.sleep(1)
            # driver.refresh()
            
        # reschedulerVisa = False
    else:
        print(f"La fecha seleccionada ({selectedDateConsular}) NO es anterior a {comparisonDateConsular}.")
        time.sleep(1)
        
        # try:
        #     driver.refresh()
        #     pass
        # except Exception:
        #     driver.refresh()
        #     pass
        
             




         





# statusDate = True
# # ciclo fechas Consular
# time.sleep(2)
# while statusDate:
#     time.sleep(2)
#     try:
#         endDateConsular = datetime.strptime(dateConsular, '%Y-%m-%d')
#         startDate = datetime.now()
#         statusConsular = False
#         datesConsular = []
#         # Localizar el elemento por su id
#         element = driver.find_element("id", "appointments_consulate_appointment_date")

#         # Elimina el atributo readonly usando JavaScript
#         driver.execute_script("arguments[0].removeAttribute('readonly')", element)
#         while startDate <= endDateConsular:
        
#             datesConsular.append(startDate.strftime('%Y-%m-%d'))
#             # Envía la fecha al campo
#             element.send_keys("2026-08-31")
#             element.send_keys(startDate.strftime('%Y-%m-%d'))
#             element.send_keys(Keys.ENTER)
#             elemento = driver.find_element("xpath", '//*[@id="non-consulate-business-day-message"]/small').text
#             if elemento == '':
#                 print('exitosamente encontro fecha')
#                 statusConsular = True
#                 break
#             else:
#                 # print(startDate)
#                 startDate += timedelta(days=1)
#                 element.clear()
        
#         # element.click()
#         # clic('/html/body/div[4]/main/div[4]/div/div/form/fieldset[1]/ol/fieldset/legend')
        

        
#         # Localizar el elemento por su id
#         element = driver.find_element("id", "appointments_asc_appointment_date")
        
#         # Elimina el atributo readonly usando JavaScript
#         driver.execute_script("arguments[0].removeAttribute('readonly')", element)
        
#         # ciclo fechas Consular
        
#         clic('//*[@id="appointments_asc_appointment_date"]')
        
#         # Fecha de inicio en formato string (cadena de texto)
#         # fecha_inicio_str = "2026-08-31"
#         fecha_inicio_str = startDate
#         # Convertir la cadena a un objeto datetime
#         fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        
#         statusCas = False
#         # Iterar 5 días hacia atrás
#         for i in range(6):
#             fecha_actual = fecha_inicio - timedelta(days=i)
#             print(fecha_actual.strftime('%Y-%m-%d'))
#             element.send_keys(fecha_actual.strftime('%Y-%m-%d'))
#             # element.send_keys('2026-08-23')
#             # time.sleep(0.5)
#             element.send_keys(Keys.ENTER)
#             elemento = driver.find_element("xpath", '//*[@id="non-asc-business-day-message"]/small').text
#             if elemento == '':
#                 print('exitosamente encontro fecha')
#                 statusCas = True
#                 break
#             else:
#                 element.clear()
        
#         clic('//*[@id="appointments_asc_appointment_time"]')
        
        
#         try:
#             clic('/html/body/div[4]/main/div[4]/div/div/form/fieldset[2]/ol/fieldset/div/div/div[1]/div/div[3]/li/select/option[2]')
        
#             pass
#         except Exception:
#             pass
#         statusDate = False
#     except:
#         # driver.refresh()
#         statusDate = True
#         time.sleep(2)

# Localizar el elemento por su XPath

# clic('/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[4]/a/h5')

# clic('/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[4]/div/div/div[2]/p[2]/a')

# yatri_session_cookie = driver.get_cookie('_yatri_session')
# csrf_token_element = driver.find_element(By.XPATH, "//meta[@name='csrf-token']")
# csrf_token = csrf_token_element.get_attribute("content")

# Accept: application/json, text/javascript, */*; q=0.01
# Accept-Encoding: gzip, deflate, br, zstd
# Accept-Language: es-419,es;q=0.9
# Connection: keep-alive
# Cookie: _gid=GA1.2.225060524.1725681149; _ga_CSLL4ZEK4L=GS1.1.1725681148.1.1.1725681162.0.0.0; _ga=GA1.2.1016261456.1725681149; _ga_W1JNKHTW0Y=GS1.2.1725681148.1.1.1725681198.0.0.0; _yatri_session=OmwMkqcsrfthif%2F64jkpGUMSoEFzxGgKe3inmAkzbgD4ppV2obtXBxcG3424K%2B4BvRLbHfo0sI9NLKdpCXqpmdJtRXMSAUV2kQKVj2yef3PW1pk4oeo8jLNynBOp7yYUo2lKeINT4UCUC6GtjomcGGAOM3sxMYZVh0qk4CUx9Sxuf2EN4dmuzQUVmdA1lorRbK7%2FGkDQmDoeW7c%2FMyglGdjzGTNlVImUwavAM4P4eDq8Ct93iB4w7cWcdZR6BfN8JoGOXFTECvJTprxPwSo3o8Oa5s3diTLPVwejtdl3GXkPU5ay2V0ptbw7bcYYL1IonnkrsMrsixCLg3yjwHe00V7PC53k1cFcL%2FWLjej%2B%2Fi%2FMSqx8Dw%2FK21sGO37ZUu8BAwtxt%2Fsk75b3wUy%2BXDwsHUhcNbR74oQytwk%2FhZbCw3IsI3QwBoLtstMmKhp9z5A1E8Tuu6ndYnMiGB1boWYP4FFQhYlt3MfkDwD4thQBY3JYSNDEAD4Yl0%2FYU4fP2it%2BOUXoCSkqZfL6fHyoi%2FlCJ5hS8oyRHX%2FmAWlmOp3MMghdeqCwe7fHDcjNKLjU6RjJn9o%2FMS0CUdXudHbKc7bNIJn%2FQW%2BhhHpUKh%2F1C9Ug3ScqFAbe684v%2BAxaBBB8hrqPu7vCebwcY9VWFb95cgdhUEGoa1TbKAsO2Yg4yVMPTkLVtDCUa4cEO5d26%2BosUYyW1wcm%2F%2FNLymo4qIGCO7H0l003Q%2FD32znijPtiGIvE9OUcnOP1j4aKL%2FUiW5hVcxLmH65gBEZHIzMck7ci9xqxBi3o5GtPz95kr%2FyaBJ5PTXSlMWq7kkd95je14ggdwBculxA%3D--7XPiSbS25VkTy7kc--Dw9aLnSIm668QhWsbdOHIQ%3D%3D
# Host: ais.usvisa-info.com
# If-None-Match: W/"478252f284492e5346acffe243c18bf0"
# Referer: https://ais.usvisa-info.com/es-co/niv/schedule/58108463/appointment
# Sec-Fetch-Dest: empty
# Sec-Fetch-Mode: cors
# Sec-Fetch-Site: same-origin
# User-Agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
# X-CSRF-Token: UKvfGHvyMP0baxtPhjhAda2TtFcihKJ4TmsZ6rCboHU3CRT5t9BBt317Gp+b3fKHt9+c/Ssek80rYYJHfj5hKQ==
# X-Requested-With: XMLHttpRequest
# sec-ch-ua: "Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"
# sec-ch-ua-mobile: ?0
# sec-ch-ua-platform: "Windows"

# headers = {
#     "Accept": "application/json, text/javascript, */*; q=0.01",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Accept-Language": "es-419,es;q=0.9",
#     "Connection": "keep-alive",
#     "DNT": "1",
#     "Host": "ais.usvisa-info.com",
#     "If-None-Match": 'W/"478252f284492e5346acffe243c18bf0"',
#     "Referer": "https://ais.usvisa-info.com/es-co/niv/schedule/58108463/appointment",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-origin",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
#     "X-CSRF-Token": csrf_token,
#     "X-Requested-With": "XMLHttpRequest",
#     "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128',
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": '"Windows"',
# }

# cookies = {
#     '_yatri_session': yatri_session_cookie['value']
# }

# sesion = requests.Session()

# r = sesion.get('https://ais.usvisa-info.com/es-co/niv/schedule/58108463/appointment/address/25', headers=headers, cookies=cookies)

# response = sesion.get('https://ais.usvisa-info.com/es-co/niv/schedule/58108463/appointment/days/25.json?appointments[expedite]=false', headers=headers, cookies=cookies)

# content = response.text


# urlCalendar = driver.current_url
# ---------------------------despues mirar requests
# headers = {
#     "User-Agent": driver.execute_script("return navigator.userAgent;"),
#     "Referer": urlCalendar,
#     "Cookie": "_yatri_session=" + driver.get_cookie("_yatri_session")["value"]
# }



# driver.current_url
# driver.page_source
# driver.get(f'https://ais.usvisa-info.com/es-co/niv/schedule/58108463/appointment/days/25.json?appointments[expedite]=false')
# sesion = requests.Session()

# pageSchedule = sesion.get('https://ais.usvisa-info.com/es-co/niv/schedule/58108463/appointment', headers = headers)

# soup = BeautifulSoup(pageSchedule.text, 'html.parser')

# meta_tag = soup.find('meta', {'name': 'csrf-token'})
# csrf_token = meta_tag.get('content')

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
#     "Referer": pageSchedule.url,
#     "Cookie": "_yatri_session=" + sesion.cookies.get('_yatri_session'),
#     "x-csrf-token": csrf_token
# }

# https://ais.usvisa-info.com/es-co/niv/schedule/58108463/appointment/days/25.json?appointments[expedite]=false

# driver.get()
# dayValidation = sesion.get('https://ais.usvisa-info.com/es-co/niv/schedule/58108463/appointment/address/25', headers = headers)

# days = sesion.get('https://ais.usvisa-info.com/es-co/niv/schedule/58108463/appointment/days/25.json?appointments[expedite]=false',headers = headers)

# days.text


# soup = BeautifulSoup(pageInformation.text, 'html.parser')
# linkscheduler = soup.find('a', class_='button primary small').get('href')


# driver.get(f'https://ais.usvisa-info.com{linkscheduler}')

# headers = {
#     "User-Agent": driver.execute_script("return navigator.userAgent;"),
#     "Referer": "https://ais.usvisa-info.com/es-co/niv/groups/41049991",
#     "Cookie": "_yatri_session=" + driver.get_cookie("_yatri_session")["value"]
# }

# pageSelectItem = sesion.get(f'https://ais.usvisa-info.com{linkscheduler}', headers = pageInformation.headers)

