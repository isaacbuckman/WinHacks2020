from bs4 import BeautifulSoup
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# firebase setup
cred = credentials.Certificate('WinHacksKey.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://winhacks-2020-database2.firebaseio.com'
    })

ref = db.reference().child("Companies")

##################################################################

def mainThingy(html):
    global ref

    html_content = html
    soup = BeautifulSoup(html_content, "lxml")

    table_data = soup.find('table', {"class":"gridTemplate"})
    table_headers = table_data.find("tr", {"class":"gridHeaderStyle"})
    headers = []
    for th in table_headers.find_all("th"):
        headers.append(th.text)

    headers = headers[1:]
    results = []

    for tr in table_data.find_all("tr")[2:-2]:
        for td in tr.find_all("td"):
            thingy = str(td).replace("<br>", "\n").replace("<br/>", "\n")
            td = BeautifulSoup(thingy, "lxml")
            results.append(td.text)        
        for i in range (1, len(results)):
            ref = db.reference().child("Companies")
            if i == 1:
                results[1] = results[1].replace("\n", "").replace("\r", "").replace(".", ",")
                ref.child(results[1]).set({})
            else:
                results[i] = results[i].strip()
                results[i] = results[i].split("\n")
                print(results)
                ref.child(results[1]).update({headers[i-1]:results[i]})
        results = []
    
driver = webdriver.Chrome()
driver.get("http://www.buywindsoressex.com/SearchResult.aspx?sectorid=4&scCond=AND&scCT=&scCat=&scMat=&scCer=&scAFT=&scNAICSlvl1=&scNAICSlvl2=&scNAICSlvl3=&scIS=&scMac=&scCap=&scSearchText=")
mainThingy(driver.page_source)
time.sleep(1)

for i in range (1, 35):
    if i%5 == 0:
        try:
            driver.find_elements(By.LINK_TEXT, "...")[1].click()
        except:
            driver.find_element(By.LINK_TEXT, "...").click()
    else:
        driver.find_element(By.LINK_TEXT, str(i+1)).click()
    time.sleep(1)
    mainThingy(driver.page_source)
    time.sleep(1)






