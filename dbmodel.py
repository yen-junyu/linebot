import pymongo

class MongoDB:
    def __init__(self,db,collections):
        """
        初始化数据库
        :param db:数据库名称 
        :param collections: 数据库的集合的名称
        """
        self.client = pymongo.MongoClient("mongodb://mpyhacct092622:asdf2847@ds147461.mlab.com:47461/mao") 
        self.db = self.client[db]           #db
        self.post = self.db[collections]    #table or collections

    def update(self,factor,data,upsert=False):
        """
        更新數據庫中的數據，如果upsert為Ture，當没有找到指定的數據時就直接插入，反之不執行插入
        :param factor 插入的條件
        :param data: 要插入的数据
        :param upsert: 判断是插入还是不插入
        :return: 
        """
        self.post.update(factor, {'$set': data} , upsert)
    def find(self,select=None):
        """
        根据传入的参数查找指定的值，注意这里的select是字典
        :param select: 指定的查找条件，这里的是字典类型的，比如{"name":"chenjiabing","age":22}
        :return: 返回的是查询的结果，同样是字典类型的
        """
        return self.post.find(select)

    def insert(self,data):
        """
        向数据库中插入指定的数据
        :param data: 要插入的数据，这里的是字典的类型比如：{"name":"chenjiabing","age":22}
        :return: 插入成功返回True,反之返回false
        """
        try:
            self.post.insert(data)
            return True
        except:
            return False

    def remove(self,select):
        """
        删除指定条件的记录
        :param select: 指定的条件，这里是字典类型的，比如{"age":22} 表示删除age=22的所有数据
        :return: 如果删除成功返回True，else返回False
        """
        try:
            self.post.remove(select)
            return True
        except:
            return False
