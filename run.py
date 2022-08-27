import undetected_chromedriver as uc
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os, random, time, requests
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd

cwd = os.getcwd()
opts = uc.ChromeOptions()

 
 
opts.add_argument('--start-maximized')
 
def xpath_type(el,mount):
    return wait(browser,15).until(EC.element_to_be_clickable((By.XPATH, el))).send_keys(mount)
 
def xpath_el(el):
    element_all = wait(browser,30).until(EC.element_to_be_clickable((By.XPATH, el)))
    
    return browser.execute_script("arguments[0].click();", element_all)
 
def get_otp():
    browser.execute_script('''window.open("https://accounts.google.com/AddSession?service=accountsettings&continue=https://myaccount.google.com/&ec=GAlAwAE","_blank");''')
    browser.switch_to.window(browser.window_handles[1])
    sleep(1)
    xpath_type('//input[@type="email"]',rec_mail.split("|")[0])
    sleep(1)
    xpath_type('//input[@type="email"]',Keys.ENTER)
    sleep(1)
    xpath_type('//input[@type="password"]',rec_mail.split("|")[1])
    sleep(1)
    xpath_type('//input[@type="password"]',Keys.ENTER)
    print(f'[*] [{email}] Delay 20s to verify email!')
    sleep(20)
    browser.get('https://mail.google.com/mail/u/1/#inbox')
    sleep(1)
    your_otp = wait(browser,30).until(EC.presence_of_element_located((By.XPATH, '(//span[contains(text(),"verifikasi") or contains(text(),"verification")])[2]'))).text
    return your_otp
    
def login(data):
    global email
    email = data.split("|")[0]
    password = data.split("|")[1]
    
    global browser
    browser = uc.Chrome(driver_executable_path=f"{cwd}//chromedriver.exe")
    browser.get("https://accounts.google.com/signin/v2/identifier?service=accountsettings&continue=https%3A%2F%2Fmyaccount.google.com%3Futm_source%3Daccount-marketing-page%26utm_medium%3Dgo-to-account-button&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
    try:
        print(f'[*] [{email}] Login')
        sleep(1)
        xpath_type('//input[@type="email"]',email)
        sleep(1)
        xpath_type('//input[@type="email"]',Keys.ENTER)
        xpath_type('//input[@type="password"]',password)
        sleep(1)
        xpath_type('//input[@type="password"]',Keys.ENTER)
        sleep(5)
        browser.get('https://myaccount.google.com/security')
        print(f'[*] [{email}] Change Password')
        xpath_el('//a[contains(@href,"signinoptions/password?")]')
        sleep(1)
        xpath_type('//input[@type="password"]',password)
        sleep(1)
        xpath_type('//input[@type="password"]',Keys.ENTER)
        sleep(5)
        xpath_type('(//input[@type="password"])[1]',new_password)
        sleep(1)
        xpath_type('(//input[@type="password"])[2]',new_password)
        sleep(1)
        xpath_type('(//input[@type="password"])[2]',Keys.ENTER)
        sleep(5)
        print(f'[*] [{email}] Change Password & add Email')
        xpath_el('//a[contains(@href,"recovery/email?")]')
        sleep(1)
        xpath_type('//input[@type="password"]',new_password)
        sleep(1)
        xpath_type('//input[@type="password"]',Keys.ENTER)
        sleep(5)
        xpath_type('//input[contains(@placeholder,"@")]',rec_mail.split("|")[0])
        sleep(1)
        xpath_type('//input[contains(@placeholder,"@")]',Keys.ENTER)
        
        otp = get_otp()
        print(f'[*] [{rec_mail.split("|")[0]}] Get OTP: {otp.split(" ")[-1]}')
        browser.close()
        sleep(1)
        browser.switch_to.window(browser.window_handles[0])
        sleep(0.5)
        xpath_type('(//input[@type="text"])[3]',otp)
        sleep(1)
        xpath_type('(//input[@type="text"])[3]',Keys.ENTER)
        try:
            xpath_type('//input[@type="password"]',password)
            sleep(1)
            xpath_type('//input[@type="password"]',Keys.ENTER)
            sleep(5)
        except:
            pass
        print(f"[*] [{email}] Add email recovery done!")
        list_accountsplit.remove(data)
        with open('list.txt','w',encoding='utf-8') as f: f.write(f'') 
        for m in list_accountsplit[:]: 
            with open('list.txt','a',encoding='utf-8') as f: f.write(f'{m}\n')
            
        with open('done.txt','a',encoding='utf-8') as f: f.write(f'{data}\n')
    except:
        print(f"[*] [{email}] Failed!")
        with open('failed.txt','a',encoding='utf-8') as f: f.write(f'{data}\n')
    browser.quit()
if __name__ == '__main__':
    print('[*] Google change Password & add Email')
    global new_password 
    global rec_mail
    new_password = input("[*] New Password: ")
    rec_mail = input("[*] Email Recovery|Password: ")
    myfile = open(f"{cwd}\\list.txt","r")
    list_account = myfile.read()
    list_accountsplit = list_account.split("\n")
    for i in list_accountsplit:
        login(i)
 
    print("[*] Automation Google!")
    
            
