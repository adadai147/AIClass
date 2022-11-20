import pymysql

# 打开数据库连接
db = pymysql.connect(host="localhost", user="root", password = "123456", database = "capitals")

# 规则类
class Rule:

    def __init__(self):
        self.condition = [] # 规则前提条件
        self.is_use = 0
        self.result = None


    # 设置该条规则是否已经匹配过
    def set_is_use(self,use):
        self.is_use = use

    def get_is_use(self):
        return self.is_use

    # 获取该条规则的结论
    def get_Result(self):
        return self.result

    def set_result(self,result):
        self.result=result

    # 获取规则的前提条件
    def get_condition(self):
        return self.condition

    def set_condition(self,condition):
        self.condition = condition

    #查找规则函数
    def get_rules(self, index):
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        sql = "SELECT * FROM RULES \
               WHERE ID = %s" % (index)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            cursor.close()
            return results
        except:
            print("Error: unable to fetch data")

    # 展示所有规则函数
    def display_rule(self):
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        sql = "SELECT * FROM RULES"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            cursor.close()
            return results
        except:
            print("Error: unable to fetch data")

