from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.request
import os
import requests
from bs4 import BeautifulSoup as bs
import shutil
from tkinter import *
import tkinter.font as TkFont

       

class Instargram(object):
    def __init__(self,user,username,password):
        # IG PROCESS
        self.user = user
        self.Img_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)),self.user)
        print(self.Img_folder)
        # exit()
        try:
            os.mkdir(self.Img_folder)
            print("Creat folder")
        except FileExistsError:
            print("Aleady Folder")
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.BaseUrl = "https://www.instagram.com/"

    def login(self):
        self.driver.get(f"{self.BaseUrl}accounts/login/")
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(self.username)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(self.password + Keys.ENTER)
        time.sleep(3)
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click()

    def Nav_to(self):
        self.driver.get(f"{self.BaseUrl}{self.user}")

    def download(self):
        time.sleep(3)
        SCROLL_PAUSE_TIME = 1.5
        images_unique=[]
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                self.driver.execute_script("window.scrollTo(document.body.scrollHeight,0);")
                break
            # This means that there is still photos to scrap
            last_height = new_height
            time.sleep(1)
            # Retrive the html
            html_to_parse=str(self.driver.page_source)
            html=bs(html_to_parse,"html5lib")
            # Get the image's url
            images_url=html.findAll("img", {"class": "FFVAD"})

            # Check if they are unique
            in_first = set(images_unique)
            in_second = set(images_url)
            in_second_but_not_in_first = in_second - in_first
            result = images_unique + list(in_second_but_not_in_first)
            images_unique=result
         

        for i in range(len(images_unique)):
            # Save each image.jpg file
            name=self.Img_folder+"/image"+str(i)+".jpg"
            with open(name, 'wb') as handler:
                img_data = requests.get(images_unique[i].get("src")).content
                handler.write(img_data)
                print('img_'+self.user+'-'+str(i)+'.jpg ------ success')

        Label(gui, text="Success!!:",font=fontStyle_text,fg="green").place(x=220, y=320, anchor="center")
        return




gui = Tk()
gui.resizable(width=False,height=False)
gui.geometry("450x400")
gui.title("  Instagram scraper By Ratchanon Pheungta")
gui.iconbitmap(r'C:\Users\tae_t\OneDrive\เดสก์ท็อป\instagram.ico')
fontStyle_label = TkFont.Font(family="Lucida Grande", size=26)
mlabel =Label(text="Instagram scraper \n By Tae",fg="#000",font=fontStyle_label,justify=CENTER,anchor=N,width=15,height=2)

fontStyle_text = TkFont.Font(family="Helvetica", size=18)
mlabel.place(x=240, y=70, anchor="center")
Label(gui, text="Username:",font=fontStyle_text).place(x=100, y=150, anchor="center")
Label(gui, text="Password:",font=fontStyle_text).place(x=100, y=180, anchor="center")
Label(gui, text="IG Name:",font=fontStyle_text).place(x=100, y=210, anchor="center")
ig_name_value = StringVar()
username = StringVar()
password = StringVar()
username = Entry(gui,borderwidth=3,font=("Helvetica", 12), textvariable=username)
password = Entry(gui,borderwidth=3,font=("Helvetica", 12), textvariable=password)
ig_name_value = Entry(gui,borderwidth=3,font=("Helvetica", 12), textvariable=ig_name_value)
username.place(x=270, y=150, anchor="center")
password.place(x=270, y=180, anchor="center")
ig_name_value.place(x=270, y=210, anchor="center")
def process():
    # print(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
    MYBOT = Instargram(ig_name_value.get(),username.get(),password.get())
    MYBOT.login()
    MYBOT.Nav_to()
    MYBOT.download()
    return 0
Button(text = 'download',fg="white", bd = '5', command= process ,bg="green").place(x=270, y=250, anchor="center")  
gui.mainloop()

# MYBOT.login()
# MYBOT.Nav_to()
# MYBOT.download()







