def motcmpbzipfiles(filesnames):
    
    import os
    import zipfile
    import time
    
    # zipfile 壓縮檔
    def zip_dir(path):
        zf = zipfile.ZipFile('{}.zip'.format(path), 'w', zipfile.ZIP_DEFLATED)
       
        for root, dirs, files in os.walk(path):
            for file_name in files:
                zf.write(os.path.join(root, file_name))

    zip_dir(filesnames)
        
    # path = filesnames
    # zf = zipfile.ZipFile('{}.zip'.format(path), 'w', zipfile.ZIP_DEFLATED)
       
    # for root, dirs, files in os.walk(path):
    #     for file_name in files:
    #         zf.write(os.path.join(root, file_name))
    
    time.sleep(5)
    
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication#傳送附件
    #寄送gmail
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = "motcmpb爬蟲-20-鄭國勤"  #郵件標題
    content["from"] = "u106b203@hk.edu.tw"  #寄件者
    content["to"] = "u106b203@hk.edu.tw" #收件者
    file = './'+filesnames+'.zip'
    content.attach(MIMEText("Demo python send email"))  #郵件內容
    part_attach1 = MIMEApplication(open(file,'rb').read())   #開啟附件
    part_attach1.add_header('Content-Disposition','attachment',filename=filesnames+'.zip') #為附件命名
    content.attach(part_attach1)   #新增附件
    
    import smtplib
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("u106b203@hk.edu.tw", "duzumsufaxvakvif")  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)