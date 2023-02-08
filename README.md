# 카카오 프렌즈샵 캐릭터별 상품 데이터 웹 크롤링

## 저작권 문제로 크롤링 금지!

하지만 카카오 프렌즈샵 클론코딩 프로젝트를 리펙토링하면서 적었던 데이터 양을 좀 늘리고자 계획된 것이 수작업으로하면 오래걸려서 크롤링을 하게되었다.

다른 블로그를 참고했지만 미완성 크롤링 파일이여서 그 블로그를 참고해서 작성하게되었다. 

- [참고 사이트](https://velog.io/@haileeyu21/PROJECT-%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88-%ED%81%B4%EB%A1%A0%EC%BD%94%EB%94%A9-web-scraping) 

위에 참고 사이트를 보면 크롤링 순서를 알게되고 과정을 배우게된다.

이제 크롤링 과정을 어떻게 하고 Mysql과 연동하여 했는지 설명하겠다.

### 1. Mysql  Table 생성 쿼리

설명 :

우리 프로젝트에서 기존에 사용하던 물품 데이터 테이블과 비슷하게 만드는 방식으로 추진했다.

참고로 바뀐 내용은 table 컬럼 순서 변경 및 sCategory가 이런 식으로 바뀐 것이다.

SlideImg는  이미지 하나밖에 수집이 안 되서 하나밖에 못 했다..

![image-20230208142118720](C:\Users\mink\AppData\Roaming\Typora\typora-user-images\image-20230208142118720.png)



**코드**

**DbTableQuery.py**

```python
# Rds MYSQL 연결과정
import pymysql
db = pymysql.connect(
    host='엔드포인트',
    port=3306,
    user='mysql아이디',
    passwd='비밀번호',
    db='데이터베이스 이름',
    charset='utf8')
cursor = db.cursor()

# Table 생성 sql 구문
sql = '''
CREATE TABLE products2(
   sId int,
   sName varchar(100),
   sTitle varchar(100),
   sContents varchar(100),
   sCategory varchar(100),   
   sPrice varchar(100),
   sHalf_title varchar(100),
   slideImg varchar(100),
   mainTopImg varchar(100),
   mainMidImg varchar(100),
   mainBottomImg varchar(100)
);
'''

cursor.execute(sql)
db.commit()
db.close()
```

### 2. BeautifulSoup을 이용한 크롤링 

설명 :

아까 참고했던 사이트에서 **캐릭터 관련 스크랩**과 **캐릭터별** **전체 상품목록 크롤링**을 참고해서 만들어봤다.

참고한 사이트는 2020년 12월에 작성한 글이라 다른 부분들이 되게 많았다. 특히 **find_element_by_xpath** 이 부분은 써먹지도 못햇다..

셀레니움 버전이 업그레이드되면서 find_element(By.XPATH,'~') 식이 변경되었다.

글쓴이는 Xpath보다 class가 좀 더 편하게 작동되고 보기 편해서 class로 작성했다. 

글을 참고하고 xpath가 편한 사람들을 바꿔도 된다.

**크롤링할 데이터는 캐릭터별 상품 상세내용들이다.**



#### 클릭 순서

홈페이지 메뉴 클릭 -> 캐릭터('라이언', '어피치', '무지', '프로도', '네오', '튜브', '제이지', '콘', '춘식이', '죠르디') 클릭 -> 상품 목록 클릭 

이대로 순환.







**코드**

**Chrawling.py**

```python
# 패키지 설정
import time
import random

import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# 2. 웹 페이지 크롬으로 설정
driver = webdriver.Chrome(ChromeDriverManager().install())

# 3. 페이지 주소 설정
org_crawling_url = "https://store.kakaofriends.com/kr/index?tab=today"
driver.get(org_crawling_url)

# 4. Beautifulsoup을 이용한 html 소스 수집  
full_html = driver.page_source
soup = BeautifulSoup(full_html, 'html.parser')
time.sleep(3)

# 5. 크롤링할 캐릭터들 리스트로 작성
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

# 6. 캐릭터별 클릭 for문
for h in a:
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "btn_util").click()
    time.sleep(2)
    driver.find_elements(By.CLASS_NAME, "btn_menu.ng-tns-c58-1")[2].click()
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, h).click()
    time.sleep(3)
    # 처음 들어갈땐 팝업이 생기므로 제거해줌. 나머지부분은 pass로 넘긴다.
    if h == '라이언':
        driver.find_element(By.CLASS_NAME, 'btn_close').click()
        time.sleep(3)
    else:
        pass
    # 크롤링할 데이터 범위를 설정함
    for i in range(0, 15):
        try:
            driver.find_elements(By.CLASS_NAME, 'wrap_thumb')[i].click()
            time.sleep(6)
        except Exception as e:
            continue
        soup1 = BeautifulSoup(driver.page_source, 'html.parser')
        # 물건에대한 정보값이 들어있는 div를 가져온다.
        good_list = soup1.select('div.section_prddetail')
        time.sleep(5)
        
        # div코드들 중 상품에 필요한 text들을 호출
        for v in good_list:
            # 상품 이름
            name = v.select_one('div.box_prdinfo > strong').text.strip()
            # 상품 제목
            try:
                Title = v.select_one('div > h3').text.strip()
            except Exception as e:
                continue
            # 상품 내용
            try:
                Contents = v.select_one('div.IX_DESCRIPTION').text.strip()
            except Exception as e:
                continue
            # 상품 가격
            Price = v.select_one('div.box_prdinfo > span.prd_price > span > span.txt_num').text.strip()
            # 중간제목 - 상품 제목 동일
            try:
                Half_title = v.select_one('div > h3').text.strip()
            except Exception as e:
                continue
            # Img에대한 소스코드를 수집.
            SlideImg = v.select_one('div.flicking-camera > div > img').get('src')
            MainTopImg = v.select('div.wrap_prd.prd_info > div.box_prddetail > p > div > img')[0].get('src')
            MainMidImg = v.select('div.wrap_prd.prd_info > div.box_prddetail > p > div > img')[1].get('src')
            MainBottomImg = v.select('div.wrap_prd.prd_info > div.box_prddetail > p > div > img')[2].get('src')

            # front개발자의 요청으로 Id값을 랜덤으로 지정 
            # 프론트에서는 0,1,2..이렇게 되어있으면 호출할때 특정 고유값이 없어서 에러가 난다고한다.
            # Category는 수집된 내용의 캐릭터이름
            sId = random.randint(10000, 60000)
            Category = h;


            # 각각 빈 리스트에 추가하기
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

# 리스트값들을 dataframe으로 변환
data = {"Id": Idlist, "name": namelist, "Title": Titlelist, "Contents": Contentslist, "Category" : Categorylist,
        "Price": Pricelist, "Half_title": Half_titlelist, "SlideImg": SlideImglist, "MainTopImg": MainTopImglist,
        "MainMidImg": mainMidImglist, "MainBottomImg": mainBottomImglist}
df = pd.DataFrame(data)
# 중복된 name은 제거
df.drop_duplicates(subset='name', keep='first', inplace=False, ignore_index=True)
# null값을 none으로 표시
df = df.where((pd.notnull(df)), None)
print(df.head(10))

# csv로 저장
df.to_csv("test.csv", encoding="utf-8-sig")
```





### 3. 크롤링한 데이터(csv)를 sql 테이블에 삽입하기 

기존에 만들어두었던 SQL 연결포트로 호출한 후 sql구문을 만들고 크롤링한 csv 안 데이터들을 열별로 호출해서 저장하고 

sql구문을 실행하였다.

DbTableInsert.py

```python
# 패키지 호출
import csv
import pymysql

# Rds MYSQL 연결과정
db = pymysql.connect(
    host='엔드포인트',
    port=3306,
    user='mysql아이디',
    passwd='비밀번호',
    db='데이터베이스 이름',
    charset='utf8')
cursor = db.cursor()

# Table에 들어갈 Insert sql 구문 설정 
sql = """INSERT INTO products2
        (sId, sName, sTitle, sContents, sCategory, sPrice, sHalf_title, slideImg,
        mainTopImg, mainMidImg, mainBottomImg)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

# 아까 크롤링 후 csv 저장한 내용을 호출한다.
# utf-8은 꼭 설정.
f = open('C:/Users/mink/PycharmProjects/pythonProject1/test.csv', 'r',  encoding="UTF-8")
csvReader = csv.reader(f)

# 각각의 내용들이 들어간 열을 차례대로 적음.
for row in csvReader:
    Id = (row[1])
    name = (row[2])
    Title = (row[3])
    Contents = (row[4])
    Category = (row[5])
    Price = (row[6])
    Half_title = (row[7])
    SlideImg = (row[8])
    MainTopImg = (row[9])
    MainMidImg = (row[10])
    MainBottomImg = (row[11])
    # sql코드을 실행
    cursor.execute(sql, (Id, name,
                         Title, Contents,
                         Category, Price, Half_title,
                         SlideImg, MainTopImg,
                         MainMidImg, MainBottomImg,
                         ))

# 결과 저장 및 데이터베이스 종료
db.commit()
db.close()
```





