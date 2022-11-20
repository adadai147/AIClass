
from Rules import Rule
from check import Check
from Rules import db


#控制程序
# 控制推理机进行推理
class Control:


    #开始推理匹配
    def identify(self,id):
        # 建立游标
        cursor = db.cursor()
        # sql命令获取事实库与知识库
        sql1 = "SELECT * FROM SYNTHESIS WHERE ID >= %d" %(id)
        sql2 = "SELECT * FROM RULES"
        # 规则类对象列表
        rules = []
        # ans保存推理得到的结论
        ans = []

        try:
            cursor.execute(sql1)
            fact_all = cursor.fetchall() #获取事实库
            cursor.execute(sql2)
            rule_all = cursor.fetchall() #获取规则库
            facts = []
            lens_fact_all = len(fact_all)
            # 整合事实库
            for index_fact_row in range(lens_fact_all):
                facts.append(fact_all[index_fact_row][0])
            # print(facts)
            # 截取规则前提条件
            for rule in rule_all:
                r = Rule()
                lens_rule = len(rule)
                # 截取规则前提条件
                r.set_condition(list(rule[1:lens_rule-1]))
                r.set_is_use(0) #表示该规则还没有匹配
                r.set_result(rule[lens_rule-1])
                rules.append(r)
            # print(rules[0].get_Result())
            # 建立匹配类的对象
            check = Check()
            # flag1判断每一轮匹配有没有匹配成功
            flag1 = 0
            # 遍历规则库
            while True:
                for r in rules:
                    if r.get_is_use() == 0 and check.check_rule(facts, r.get_condition()) == 1:
                        r.set_is_use(1)
                        facts.append(r.get_Result()) #将结论加入事实库
                        condition = r.get_condition()
                        # 保存中间推理过程
                        temp = []
                        for i in range(len(condition)):
                            if condition[i] !='':
                                temp.append(condition[i])
                        temp.append(r.get_Result())
                        # 保存结论
                        ans.append(temp)
                        # print(ans)
                        flag1 = 1
                        break
                if flag1 == 0:
                    break
                flag1 = 0
        except Exception as e:
            print("获取事实库出错！")
            # 发生错误时回滚
            db.rollback()
            print("执行MySQL: %s 时出错：%s" % (sql1, e))
        return ans





