# https://velog.io/@haileeyu21/PROJECT-%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88-%ED%81%B4%EB%A1%A0%EC%BD%94%EB%94%A9-web-scraping
#
import time
import random

import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# 2. Driver & BeautifulSoup
driver = webdriver.Chrome(ChromeDriverManager().install())

org_crawling_url = "https://store.kakaofriends.com/kr/index?tab=today"
driver.get(org_crawling_url)

# 3. Parsing html code
full_html = driver.page_source
soup = BeautifulSoup(full_html, 'html.parser')

# 4. Get element selector
# 4-1. Get character list
# hamburger_button = driver.find_element(By.XPATH, r'//*[@id="innerHead"]/div/button[2]').click()

# char_button = driver.find_element_by_xpath('/html/body/div[6]/div/div/div/ul/li[3]/button').click()
# driver.find_element(By.CLASS_NAME, "btn_menu.ng-tns-c58-3").click()
# li = b.find_elements(By.TAG_NAME, 'li')
# li[2].click()
time.sleep(3)
a = ['라이언', '어피치', '무지', '프로도', '네오', '튜브', '제이지', '콘', '춘식이', '죠르디']

Idlist = []
namelist = []
Titlelist = []
Contentslist = []
Pricelist = []
Likelist = []
Viewlist = []
Half_titlelist = []
Categorylist = []
SlideImglist = []
MainTopImglist = []
mainMidImglist = []
mainBottomImglist = []

#
for h in a:
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "btn_util").click()
    time.sleep(2)
    driver.find_elements(By.CLASS_NAME, "btn_menu.ng-tns-c58-1")[2].click()
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, h).click()
    time.sleep(3)
    #
    if h == '라이언':
        driver.find_element(By.CLASS_NAME, 'btn_close').click()
        time.sleep(3)
    else:
        pass
    for i in range(0, 15):
        try:
            driver.find_elements(By.CLASS_NAME, 'wrap_thumb')[i].click()
            time.sleep(6)
        except Exception as e:
            continue
        soup1 = BeautifulSoup(driver.page_source, 'html.parser')
        good_list = soup1.select('div.section_prddetail')
        time.sleep(5)
        for v in good_list:
            # if v.find("div", "product_contents top ng-star-inserted"):
            # 상품 사진,모델명, 가격
            name = v.select_one('div.box_prdinfo > strong').text.strip()
            try:
                Title = v.select_one('div > h3').text.strip()
            except Exception as e:
                continue
            try:
                Contents = v.select_one('div.IX_DESCRIPTION').text.strip()
            except Exception as e:
                continue
            # print(v.select_one('').text.strip())
            Price = v.select_one('div.box_prdinfo > span.prd_price > span > span.txt_num').text.strip()
            #        Like = v.select_one('div. > ').text.strip()
            #        View = v.select_one('div. > ').text.strip()
            try:
                Half_title = v.select_one('div > h3').text.strip()
            except Exception as e:
                continue
            #        Category = v.select_one('div. > ').text.strip()
            SlideImg = v.select_one('div.flicking-camera > div > img').get('src')
            # print(v.select('div.wrap_prd.prd_info > div.box_prddetail > p > div > img')[0].get('src'))
            MainTopImg = v.select('div.wrap_prd.prd_info > div.box_prddetail > p > div > img')[0].get('src')
            MainMidImg = v.select('div.wrap_prd.prd_info > div.box_prddetail > p > div > img')[1].get('src')
            MainBottomImg = v.select('div.wrap_prd.prd_info > div.box_prddetail > p > div > img')[2].get('src')

            sId = random.randint(10000, 60000)
            Category = h;


            # 추가하기
            Idlist.append(sId)
            Categorylist.append(Category)
            namelist.append(name)
            Titlelist.append(Title)
            Contentslist.append(Contents)
            Pricelist.append(Price)
            Half_titlelist.append(Half_title)
            SlideImglist.append(SlideImg)
            MainTopImglist.append(MainTopImg)
            mainMidImglist.append(MainMidImg)
            mainBottomImglist.append(MainBottomImg)
        driver.back()
    driver.get(org_crawling_url)
driver.close()

# "Like": Likelist, "View": Viewlist,
data = {"Id": Idlist, "name": namelist, "Title": Titlelist, "Contents": Contentslist, "Category" : Categorylist,
        "Price": Pricelist, "Half_title": Half_titlelist, "SlideImg": SlideImglist, "MainTopImg": MainTopImglist,
        "MainMidImg": mainMidImglist, "MainBottomImg": mainBottomImglist}
df = pd.DataFrame(data)
df.drop_duplicates(subset='name', keep='first', inplace=False, ignore_index=True)
df = df.where((pd.notnull(df)), None)
print(df.head(10))
#
# df.to_csv("products.csv", encoding="utf-8-sig", index_label=['Id'])
df.to_csv("test.csv", encoding="utf-8-sig")
