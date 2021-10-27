def selemotcmpbcsv():
    
    from selenium import webdriver
    import time
    from bs4 import BeautifulSoup
    import pandas as pd
    
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': r'E:\AI BigData Programming\20210914group_part10_thematic_plan\analysiscsv2'}
    # 設定檔案下載位置，並設定不另開網頁
    
    options.add_experimental_option('prefs', prefs)
                
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
    # 設定chromedriver.exe
    
    driver.set_window_size(1280, 1000)
    # 設定網頁開啟大小
    
    # 設定要開啟的網頁
    driver.get("https://data.motcmpb.gov.tw/")
    
    # 等待時間
    time.sleep(1)
    
    # 模擬滑鼠點擊
    driver.find_element_by_xpath('/html/body/header/nav/div/ul/li[7]/h3/a').click()
    time.sleep(1)
    
    # 進行整個網頁解析，找出'h4', class_='main_sort'
    soup = BeautifulSoup(driver.page_source)
    h4 = soup.find_all('h4', class_='main_sort')
    
    # print(h4)
    
    ### h4df
    atabindex = h4[0].find_all('a') # 找所有頁籤
    '''
    <h4 class="main_sort">
        <a title="貨物" tabindex="5" class="btn_in the_color_blue1" href="/ListFolders/Index/182">貨物</a>
        <a title="貨櫃" tabindex="5" class="" href="/ListFolders/Index/183">貨櫃</a>
        <a title="船舶" tabindex="5" class="" href="/ListFolders/Index/184">船舶</a>
        <a title="航線" tabindex="5" class="" href="/ListFolders/Index/185">航線</a>
        <a title="港口" tabindex="5" class="" href="/ListFolders/Index/186">港口</a>
        <a title="海事" tabindex="5" class="" href="/ListFolders/Index/187">海事</a>
        <a title="航港局" tabindex="5" class="" href="/ListFolders/Index/188">航港局</a>
    </h4>
    '''
    
    h4href=[0]*len(atabindex)  # 做list空間宣告變數
    h4title=[0]*len(atabindex) # 做list空間宣告變數
    
    for pagenum in range(1,3):
        for i in range(len(atabindex)):
            h4title[i]=atabindex[i]['title']
            # 找所有頁籤title
            
            h4href[i]=str('https://data.motcmpb.gov.tw'+atabindex[i]['href']+'?page='+str(pagenum))
            # 找所有頁籤href
            
        # for i in range(len(atabindex)):
        #     print(h4title[i])
        #     print(h4href[i])
            
            # 做成pd.DataFrame
            h4dict={'h4title':h4title,'h4href':h4href}
            h4df=pd.DataFrame(h4dict)
        
            # 將h4href進行逐一開啟
            driver.get(h4href[i])
            time.sleep(1)   
            
            ### lidf
            soup = BeautifulSoup(driver.page_source)
            li = soup.find_all('li', class_='clearfix')
            # 進行整個網頁解析，找出'li', class_='clearfix'
            # print(li)
            '''
            <li class="clearfix">
                <div style="width:100%;">
                    <p class="day p_news">2021/08/13</p>
                    <a style="width:83%;" tabindex="5" title="臺灣地區各港出港散裝大宗貨物量" href="/ListFolders/Document/106910?name=106910">
                        <h5 style="width:100%;">臺灣地區各港出港散裝大宗貨物量</h5>
                    </a>
                </div>          
            </li>
            '''
            
            # 做list空間宣告變數
            ahref=[0]*len(li)
            atitle=[0]*len(li)
            annextitle=[0]*len(li)
            annexhref=[0]*len(li)
            
            # 將所有資料清單的'title'及'href'爬取下來
            for j in range(len(li)):
                atitle[j]=li[j].find('a')['title']
                ahref[j]=str('https://data.motcmpb.gov.tw'+li[j].find('a')['href'])
                
            # for j in range(len(li)):
            #     print(atitle[j])
            #     print(ahref[j])
                
                # 判斷該頁籤清單的'title'及'href'是否是空的
                if atitle[j]=='None' and ahref[j]=='None':break
    
                # 將清單內的csv檔網址開啟並點擊
                driver.get(ahref[j])
                time.sleep(1)
                driver.find_element_by_xpath('/html/body/main/article/div/div/div[2]/p[4]/a').click()
                time.sleep(4)
                
                # 將清單內的csv檔'title'及'href'存起來
                soup = BeautifulSoup(driver.page_source)
                annex = soup.find_all('p', class_='annex')
                '''
                <p class="annex">
                        附件
                            <a tabindex="5" title="臺灣地區各港進港散裝大宗貨物量.csv" href="/Common/DocumentDownload/b3f2dc05-f9a4-4060-ae94-f5cc589871f4">臺灣地區各港進港散裝大宗貨物量.csv</a>
                </p>
                '''
                annextitle[j]=annex[0].find('a')['title']
                annexhref[j]=str('https://data.motcmpb.gov.tw'+annex[0].find('a')['href'])
                
                driver.back()
                
            # 將頁籤清單的'title'及'href'製作成pd.DataFrame
            adict={'atitle':atitle,'ahref':ahref}
            lidf=pd.DataFrame(adict)    
            
            # 將清單內的csv檔'title'及'href'製作成pd.DataFrame
            annexdict={'annextitle':annextitle,'annexhref':annexhref}
            annexdf=pd.DataFrame(annexdict) 
                
            # 判斷該頁籤是否為全空
            if (adict['atitle'] ==[] and adict['ahref'] ==[]) or (annexdict['annextitle'] ==[] and annexdict['annexhref'] ==[]):
                continue
            else:  
                html = lidf.to_html()
                with open("htmldata/htmlindex/motcmpb"+h4title[i]+"page"+str(pagenum)+".html", "w", encoding = "utf-8-sig") as file: 
                    file.writelines('<meta charset = "UTF-8">\n')
                    file.write(html)
                
                html = annexdf.to_html()
                with open("htmldata/htmldata/htmldata"+h4title[i]+"page"+str(pagenum)+".html", "w", encoding = "utf-8-sig") as file: 
                    file.writelines('<meta charset = "UTF-8">\n')
                    file.write(html)    
                
                # csv = lidf.to_csv()
                # with open("csvdata/motcmpb"+h4title[i]+"page"+str(pagenum)+".csv", "w",index=False, encoding = "utf-8-sig") as file: 
                #     file.write(csv)
                
                lidf.to_csv("csvdata/csvindex/motcmpb"+h4title[i]+"page"+str(pagenum)+".csv", sep=',',index=False, encoding = "utf-8-sig")
                annexdf.to_csv("csvdata/csvdata/csvdata"+h4title[i]+"page"+str(pagenum)+".csv", sep=',',index=False, encoding = "utf-8-sig")
                    
                lidf.to_excel("xlsxdata/xlsxindex/motcmpb"+h4title[i]+"page"+str(pagenum)+".xlsx", encoding='utf-8-sig',sheet_name = h4title[i], index=False, header=True)
                annexdf.to_excel("xlsxdata/xlsxdata/xlsxdata"+h4title[i]+"page"+str(pagenum)+".xlsx", encoding='utf-8-sig',sheet_name = h4title[i], index=False, header=True)
    driver.close()
         
    # 爬完結束時間5:27