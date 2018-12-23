from DBPool import Mysql
from Book import BookAPI
import datetime

class BorrowAPI(object):
    #获取num个借阅表记录，num = 0时获取所有
    def GetBorrowRecord(self,num):
        mysql = Mysql()
        if(str(num) == '0'):
            sqlAll = "select * from borrow"
        else:
            sqlAll= "select * from borrow limit " + str(num)
        result = mysql.getAll(sqlAll)
        print("borrowid\tuserid\tbookid\tborrowdate\tpresretdate\tactretdate")
        if result :
            for row in result :
                print("%s\t%s\t%s\t%s\t%s\t%s" %\
                      (row[0],row[1],row[2],row[3],row[4],row[5]))
        mysql.dispose()
    #按字段获取借阅记录
    def GetBorrowRecordByField(self,Dict):
        mysql = Mysql()
        sql = "select * from borrow where "
        keys = tuple(Dict.keys())
        vals = tuple(Dict.values())
        Len = len(Dict)
        for i in range(Len):
            if (i != Len-1):
                sql = sql + keys[i] + "='" + str(vals[i]) + "' and "
            else:
                sql = sql + keys[i] + "='" + str(vals[i]) + "'"
        Book = mysql.getAll(sql)
        if len(Book) == 0:
            print("No borrow record found!")
        else:
            print("The borrow record you found:")
            if Book:
                for row in Book:
                    print("%s\t%s\t%s\t%s\t%s\t%s" %\
                          (row[0],row[1],row[2],row[3],row[4],row[5]))
        mysql.dispose()
        return Book
    #插入借阅表记录,传入一个接口
    def InsertBorrowRecord(self,List):
        mysql = Mysql()
        sql = "insert into borrow(borrowid,userid,bookid,borrowdate,presretdate,actretdate) values(%s,%s,%s,%s,%s,%s)"
        try:
            mysql.insertMany(sql, List)
            mysql.end('commit')
            print("insert success!")
        except Exception as e:
            print("except")
            mysql.end(None)
        mysql.dispose()
    #用户借书的接口，需要传入用户id和书籍id,如果借书成功就修改借阅表
    def BorrowBook(self,uid,bid):
        #获取系统时间当作借阅时间并计算出应该归还的时间
        borrow_time = datetime.datetime.now().strftime('%Y-%m-%d')
        return_time = (datetime.datetime.now() + datetime.timedelta(days=90)).strftime('%Y-%m-%d')
        book = BookAPI()
        record = book.GetBookByField({'bookid':bid})
        if(record[0][11] == '正常'):
            print("You can borrow this book!")
            if(input("Do you want to borrow this book?(press YES to borrow)") == 'YES'):
                print("Successful borrowing!")
                addborr = BorrowAPI()
                addborr.InsertBorrowRecord([('30000',uid,bid,borrow_time,'0000-00-00',return_time)])
            else:
                print("You don't want to borrow this book......OK")
        else:
            print("Abnormal book state,you can't borrow this book!")
    #按照当前系统时间返回借阅表中超时违章的记录
    def RetureIllegalRecord(self):
        mysql = Mysql()
        # 获取系统时间
        systime = datetime.datetime.now().strftime('%Y-%m-%d')
        #返回超过系统时间还未还的图书借阅记录
        sql = "select * from borrow where actretdate < '" + systime + "' and presretdate = '0000-00-00'"
        result = mysql.getAll(sql)
        mysql.dispose()
        return result
    #对借阅表进行修改
    #可调用Book.py的UpdateRecord()函数
    #改
    def UpdateRecord(self,table,key1,val1,key2,val2):#key1和val1是修改键和值，val1和val2是条件键和值，如果是val是非数字，则需要写成'"数"'传入
        mysql = Mysql()
        sql = "update " + table + " set " + key1 + "='" + val1 + "' where " + key2 + "='" + val2 + "'"
        try:
            mysql.update(sql,None)
            # mysql.update("update book")
            mysql.end('commit')
            print("update succes!")
        except Exception as e:
            print("except")
            mysql.end(None)
        mysql.dispose()
bo = BorrowAPI()
# bo.GetBorrowRecord(5)
# bo.GetBorrowRecordByField({'userid':'10000'})
# bo.InsertBorrowRecord([('30000','10001','100045','2017-03-06','2017-03-20','2017-05-09')])
# bo.BorrowBook('30000','100016')
# print(bo.RetureIllegalRecord())


