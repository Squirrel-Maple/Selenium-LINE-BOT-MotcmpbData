from selenium.webdriver import Chrome
import time
import pyautogui
from bs4 import BeautifulSoup
import pandas as pd

# 設定exe檔位置
driver = Chrome("chromedriver.exe")

driver.set_window_size(1280, 1000)

# 設定要開啟的網頁
driver.get("https://data.motcmpb.gov.tw/")

# 等待時間
time.sleep(0.5)

driver.find_element_by_xpath('/html/body/header/nav/div/ul/li[7]/h3/a').click()
time.sleep(0.5)

soup = BeautifulSoup(driver.page_source)
h4 = soup.find_all('h4', class_='main_sort')

# print(h4)

# h4df
atabindex = h4[0].find_all('a')

h4href=[0]*len(atabindex)
h4title=[0]*len(atabindex)
for pagenum in range(1,3):
    for i in range(len(atabindex)):
        h4title[i]=atabindex[i]['title']
        h4href[i]=str('https://data.motcmpb.gov.tw'+atabindex[i]['href']+'?page='+str(pagenum))
        
    # for i in range(len(atabindex)):
    #     print(h4title[i])
    #     print(h4href[i])
        
        h4dict={'h4title':h4title,'h4href':h4href}
        h4df=pd.DataFrame(h4dict)
    
        driver.get(h4href[i])
        time.sleep(0.5)
            
        # lidf
        soup = BeautifulSoup(driver.page_source)
        li = soup.find_all('li', class_='clearfix')
        # print(li)
            
        ahref=[0]*len(li)
        atitle=[0]*len(li)
        
        for j in range(len(li)):
            atitle[j]=li[j].find('a')['title']
            ahref[j]=str('https://data.motcmpb.gov.tw'+li[j].find('a')['href'])
            
        # for j in range(len(li)):
        #     print(atitle[j])
        #     print(ahref[j])
            
            if atitle[j]=='None' and ahref[j]=='None':break

            driver.get(ahref[j])
            time.sleep(1)
            
            from selenium import webdriver
            
            options = webdriver.ChromeOptions()
            prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': r'E:\AI BigData Programming\20210914group_part10_thematic_plan\data_analysis_csv'}
            options.add_experimental_option('prefs', prefs)
                        
            driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
                          
            driver.find_element_by_xpath('/html/body/main/article/div/div/div[2]/p[4]/a').click()
            time.sleep(4)
            driver.quit()