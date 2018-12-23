from DBPool import Mysql

class BookAPI(object):
    # 获取任何表中的所有记录
    def GetAllBookRecord(self,num):
        mysql = Mysql()
        if(str(num) == '0'):
            sqlAll = "select * from book"
        else:
            sqlAll= "select * from book limit " + str(num)
        result = mysql.getAll(sqlAll)
        print("bookid\tbookname\tauthor\tpages\tcollecttime\tversion\tmajor\tdiscipline\tisbn\tbooklanguage\tpublisher\tstatus\tabstract\tstack\tshelf\tfloor\tbookvalue")
        if result :
            for row in result :
                print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" %\
                      (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],\
                     row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16]))
        mysql.dispose()
    #按分类查找图书
    #按discipline字段分类
    def GetBookByDis(self,desci):
        mysql = Mysql()
        Dis_List = mysql.getAll("select * from book where discipline = '" + desci +"'")
        print("Classification of " + desci + ":\n")
        print("bookid\tbookname\tauthor\tpages\tcollecttime\tversion\tmajor\tdiscipline\tisbn\tbooklanguage\tpublisher\tstatus\tabstract\tstack\tshelf\tfloor\tbookvalue")
        if Dis_List:
            for row in Dis_List:
                print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" %\
                      (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],\
                     row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16]))

        mysql.dispose()
    #按major字段分类
    def GetBookByMaj(self,maj):
        mysql = Mysql()
        Maj_List = mysql.getAll("select * from book where major = '" + maj +"'")
        #Dis_List = Dis_List.decode('utf-8')
        print(Maj_List)
        print("Classification of " + maj + ":\n")
        print("bookid\tbookname\tauthor\tpages\tcollecttime\tversion\tmajor\tdiscipline\tisbn\tbooklanguage\tpublisher\tstatus\tabstract\tstack\tshelf\tfloor")
        if Maj_List:
            for row in Maj_List:
                print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" %\
                      (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],\
                     row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16]))

        mysql.dispose()
    #按图书名查询
    def GetBookByName(self,bookname):
        mysql = Mysql()
        Book_num = mysql.getAll("select * from book where bookname = '" + bookname + "'")
        if len(Book_num) == 0:
            print("No books found!")
        else:
            print("The book you found:")
            if Book_num:
                for row in Book_num:
                    print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" %\
                          (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],\
                         row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16]))

        mysql.dispose()
    #按字段查询,输入字段的字典
    #返回查询到的书籍数量
    def GetBookByField(self,Dict):
        mysql = Mysql()
        sql = "select * from book where "
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
            print("No books found!")
        else:
            print("The book you found:")
            if Book:
                for row in Book:
                    print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" %\
                          (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],\
                         row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16]))
        mysql.dispose()
        return Book
    #插入图书记录，列表传入
    def InsertBookRecord(self,List):
        mysql = Mysql()
        # 插入图书
        # sql
        sql = "insert into book(bookid,bookname,author,pages,collecttime,version,\
        major,discipline,isbn,booklanguage,publisher,status,abstract,stack,shelf,floor,bookvalue) " + \
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # val
        try:
            mysql.insertMany(sql, List)
            mysql.end('commit')
            print("insert success！")
        except Exception as e:
            mysql.end(None)
        mysql.dispose()
    #输入表名、字段和条件，删除一条记录(通用)
    def DeleteRecord(self,table,key,val):#key字段名 val值
        mysql = Mysql()
        sql = "delete from " + table + " where " + str(key) + "=" + str(val)
        try:
            mysql.delete(sql,None)
            mysql.end('commit')
            print("delete success!")
        except Exception as e:
            print("except")
            mysql.end(None)
        mysql.dispose()
    #更改数据表记录,输入条件字段和修改字段（通用）
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


add = BookAPI()
# add.GetAllBookRecord('20')
# add.GetBookByDis("气象学")
# add.GetBookByMaj("工业技术")
# add.GetBookByName("地下地上中级概论")
# add.InsertBookRecord([('300000', '数据结构', '测试', '500', '2000-11-10', '第一版', '工业技术', '矿业技术', '943-234-2424-23-1', '中文', '测试', '测试', '','测试', '15', '2', '200')])
# add.DeleteRecord('book','bookid','300000')
# add.UpdateRecord('book','bookname','Unix编程','bookid','300000')@修改bookid为300000时候的bookname值为Unix编程
# add.GetBookByField({'bookid':'100014','author':'韩强军'})