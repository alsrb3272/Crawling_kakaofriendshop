import csv

import pymysql

db = pymysql.connect(
    host='database-1.cd6uosjs1jca.ap-northeast-2.rds.amazonaws.com',
    port=3306,
    user='admin',
    passwd='12345678',
    db='chauk',
    charset='utf8')
cursor = db.cursor()

sql = """INSERT INTO products2
        (sId, sName, sTitle, sContents, sCategory, sPrice, sHalf_title, slideImg,
        mainTopImg, mainMidImg, mainBottomImg)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

f = open('C:/Users/mink/PycharmProjects/pythonProject1/test.csv', 'r',  encoding="UTF-8")
csvReader = csv.reader(f)

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
    cursor.execute(sql, (Id, name,
                         Title, Contents,
                         Category, Price, Half_title,
                         SlideImg, MainTopImg,
                         MainMidImg, MainBottomImg,
                         ))

# 결과 저장 및 데이터베이스 종료
db.commit()
db.close()