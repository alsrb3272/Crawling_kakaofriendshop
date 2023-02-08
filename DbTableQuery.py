import pymysql
db = pymysql.connect(
    host='database-1.cd6uosjs1jca.ap-northeast-2.rds.amazonaws.com',
    port=3306,
    user='admin',
    passwd='12345678',
    db='chauk',
    charset='utf8')
cursor = db.cursor()
#
# 스키마 생성
# 스키마 정의
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




