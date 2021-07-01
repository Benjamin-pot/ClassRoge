import datetime


##datetime

#當前時間
a = datetime.datetime.now()

#日期時間轉換
b = datetime.datetime(2021, 8, 20)

#
#M:分 m:月
c = datetime.datetime.now().strftime("%Y %m %d")

print(c)
