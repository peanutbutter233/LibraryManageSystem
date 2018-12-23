from DBPool import Mysql
from Book import BookAPI
from Borrow import BorrowAPI
import random
import datetime

class IllegalAPI(object):
    # 供管理员调用
    #插入违章表,接口为参数列表
    def InsertIllegal(self,List):
        mysql = Mysql()
        sql = "insert into illegal(illegalid,userid,bookid,amount,isprocessed,illegaldate,illegaltype) " + \
              "values(%s,%s,%s,%s,%s,%s,%s)"
        # val
        try:
            mysql.insertMany(sql, List)
            mysql.end('commit')
            print("insert success！")
        except Exception as e:
            mysql.end(None)
        mysql.dispose()
    #查看某一个用户的违章记录
    def GetUserIllegal(self,Ile):
        mysql = Mysql()
        sql = "select * from illegal where "
        keys = tuple(Ile.keys())
        vals = tuple(Ile.values())
        Len = len(Ile)
        for i in range(Len):
            if (i != Len-1):
                sql = sql + keys[i] + "='" + str(vals[i]) + "' and "
            else:
                sql = sql + keys[i] + "='" + str(vals[i]) + "'"
        Ilegal = mysql.getAll(sql)
        if len(Ilegal) == 0:
            print("No illegal record!")
        else:
            print("Illegal records:")
            if Ilegal:
                for row in Ilegal:
                    print("%s\t%s\t%s\t%s\t%s\t%s\t%s" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
        mysql.dispose()
    #num = 0查看所有记录，否则查看num条记录
    def GetAllIlegal(self,num):
        mysql = Mysql()
        if(str(num) == '0'):
            sqlAll = "select * from illegal"
        else:
            sqlAll= "select * from illegal limit " + str(num)
        result = mysql.getAll(sqlAll)
        if result :
            for row in result :
                print("%s\t%s\t%s\t%s\t%s\t%s\t%s" %\
                      (row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
        mysql.dispose()
    # #用户登记还书超时情况
    # def OverTimeBook(self):
    # #用户登记损坏或丢失的书,传入图书的id
    # def DemageBook(self,bid):
    #     book = BookAPI()
    #     #修改book表的图书status
    #     book.UpdateRecord('book','status','损坏','bookid',bid)
    #自动查看borrow表中有没有已经超时的记录需要处理
    def BorrowToIllega(self):
        borrow = BorrowAPI()
        ill_rec = borrow.RetureIllegalRecord()
        if ill_rec:
            for each in ill_rec:
                #每条超时记录处理
                #将用户的状态修改为不可借书的状态------------------------------------------------------>未写完
                #修改违章表
                print(each)
                systime = datetime.datetime.now().strftime('%Y-%m-%d')
                acount = random.randint(1,10)
                illegal = IllegalAPI()
                illegal.InsertIllegal([('30000',each[1],each[2],acount,'否',systime,'超时')])
    #改
    def UpdateRecord(self, table, key1, val1, key2, val2):  # key1和val1是修改键和值，val1和val2是条件键和值，如果是val是非数字，则需要写成'"数"'传入
        mysql = Mysql()
        sql = "update " + table + " set " + key1 + "='" + val1 + "' where " + key2 + "='" + val2 + "'"
        try:
            mysql.update(sql, None)
            # mysql.update("update book")
            mysql.end('commit')
            print("update succes!")
        except Exception as e:
            print("except")
            mysql.end(None)
        mysql.dispose()

ile = IllegalAPI()
# ile.GetUserIllegal({'illegalid':'10001'})
# ile.GetAllIlegal(3)
ile.BorrowToIllega()