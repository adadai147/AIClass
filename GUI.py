import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from Rules import Rule
from control import Control
from Rules import db

class gui:


    #初始化操作
    def __init__(self, window):

        self.win = window
        self.win.title("AI产生式系统——省会城市识别")
        # 定义窗口的宽高
        width = 800
        height = 600
        align_str = '%dx%d' % (width, height)
        window.geometry(align_str)

        #设置标签
        L1 = tk.Label(window, text="请输入特征！",
                 bg='aqua',font=('Arial', 12),width=20,height=2)
        L2 = tk.Label(window, text="推理过程与结果如下：",
                 bg='aqua',font=('Arial', 12),width=20,height=2)
        L1.grid(row=1,column=0)
        L2.grid(row=5,column=0)
        #设置输入框
        self.e1 = tk.Entry(window,font=('Arial', 12),bd=3)
        self.e1.grid(row=0,column=1,pady=10)
        self.e2 = tk.Entry(window,font=('Arial', 12),bd=3)
        self.e2.grid(row=1,column=1,pady=10)
        self.e3 = tk.Entry(window,font=('Arial', 12),bd=3)
        self.e3.grid(row=2,column=1,pady=10)
        self.e4 = tk.Entry(window,font=('Arial', 12),bd=3)
        self.e4.grid(row=3,column=1,pady=10)

        #设置按钮
        self.b1 = tk.Button(window,text="推理识别",
                            width=15,height=2,
                            command=self.matching)
        self.b1.grid(row=0,column=2,padx=10,pady=10)

        self.b2 = tk.Button(window, text="查看规则",
                            width=15,height=2,command=self.gui_rule)
        self.b2.grid(row=1,column=4,padx=10,pady=10)

        self.b3 = tk.Button(window,text="清空输入",
                            width=15,height=2,command=self.clear)
        self.b3.grid(row=0,column=3,padx=10,pady=10)

        self.b4 = tk.Button(window,text="添加规则",
                            width=15,height=2,command=self.add_rule_gui)
        self.b4.grid(row=2,column=4,padx=10,pady=10)

        self.b5 = tk.Button(window,text="删除规则",
                            width=15,height=2,command=self.delete_gui)
        self.b5.grid(row=3,column=4,padx=10,pady=10)

        self.b6 = tk.Button(window, text="修改规则",
                            width=15, height=2,command=self.update_gui)
        self.b6.grid(row=4,column=4,padx=10,pady=10)



        #结果展示
        self.t = scrolledtext.ScrolledText(window,
                                           width=60,height=15,
                                           wrap=tk.WORD)
        self.t.place(x=200,y=350)

    # 查看规则函数
    def gui_rule(self):
        self.t.delete(1.0,'end') #先清空文本框
        rule = Rule()
        results = rule.display_rule()

        for row in results:
            flag = 0
            s = str(row[0]) + '：'
            if row[1] != '':
                s += row[1]
                # global flag
                flag = 1
            if row[2] != '':
                if flag:
                    s += '+'+row[2]
                else:
                    s += row[2]
                    # global flag
                    flag = 1
            if row[3] != '':
                if flag:
                    s += '+'+row[3]
                else:
                    s += row[3]
            s += '-->' + row[4]
            self.t.insert('end',"\n"+s)
        #     i += 1


    #展示添加规则窗口界面
    def add_rule_gui(self):
        new_win = tk.Tk()
        new_win.title("添加规则")
        new_win.geometry('500x500')

        #标签
        l1 = tk.Label(new_win, text="请输入添加的规则内容：",
                 bg='pink',font=('Arial', 12),width=25,height=2)
        l1.grid(row=0,column=0,padx=10,pady=10)
        l2 = tk.Label(new_win, text="所处方位:",
                 bg='pink',font=('Arial', 12),width=25,height=2)
        l2.grid(row=1,column=0,padx=10,pady=10)
        l3 = tk.Label(new_win, text="城市规模:",
                 bg='pink',font=('Arial', 12),width=25,height=2)
        l3.grid(row=2, column=0, padx=10, pady=10)
        l4 = tk.Label(new_win, text="所属城市圈:",
                 bg='pink',font=('Arial', 12),width=25,height=2)
        l4.grid(row=3, column=0, padx=10, pady=10)
        l5 = tk.Label(new_win, text="Result(结果):",
                 bg='pink',font=('Arial', 12),width=25,height=2)
        l5.grid(row=4, column=0, padx=10, pady=10)

        #输入文本框
        e1 = tk.Entry(new_win,font=('Arial', 12),bd=3)
        e1.grid(row=1,column=1,padx=10,pady=10)
        e2 = tk.Entry(new_win, font=('Arial', 12), bd=3)
        e2.grid(row=2, column=1, padx=10, pady=10)
        e3 = tk.Entry(new_win, font=('Arial', 12), bd=3)
        e3.grid(row=3, column=1, padx=10, pady=10)
        e4 = tk.Entry(new_win, font=('Arial', 12), bd=3)
        e4.grid(row=4, column=1, padx=10, pady=10)

        #按钮
        b = tk.Button(new_win, text="确认",
                            width=15,height=2,command=lambda: self.add_rule(e1.get(),e2.get(),e3.get(),e4.get()))
        b.grid(row=5,column=1,padx=10,pady=10)
        new_win.mainloop()

    # 添加规则
    def add_rule(self, t1,t2,t3,t4):
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 获取当前最大规则id
        sql = "SELECT MAX(id) FROM RULES"
        cursor.execute(sql)
        max_id = cursor.fetchone()[0] + 1

        # SQL 插入语句
        sql = "INSERT INTO RULES(ID, LOCATION, \
            SIZE,CITY,RESULTS) \
               VALUES (%d,'%s','%s','%s','%s')" % \
              (max_id, t1,t2,t3,t4)
        try:
            # print(sql)
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
            messagebox.showinfo(title="添加成功！",message="新规则已添加知识库！请重新查看规则！")
            cursor.close()
        except Exception as e:
            print("添加规则出错！")
            # 发生错误时回滚
            db.rollback()
            print("执行MySQL: %s 时出错：%s" % (sql, e))

    # 删除界面函数
    def delete_gui(self):
        new_win = tk.Tk()
        new_win.title("删除规则")
        new_win.geometry('800x500')
        # 滚动文本框
        t = scrolledtext.ScrolledText(new_win,
                                      width=60, height=15,
                                      wrap=tk.WORD)
        t.grid(row=0, column=1, padx=10, pady=10)
        #标签
        l1 = tk.Label(new_win, text="当前知识库中的规则如下：",
                      bg='pink', font=('Arial', 12), width=25, height=2)
        l1.grid(row=0,column=0,padx =10,pady=10)

        l2 = tk.Label(new_win, text="输入您想删除的规则编号：",
                 bg='pink',font=('Arial', 12),width=25,height=2)
        l2.grid(row=1, column=0, padx=10, pady=10)
        # 输入框
        e1 = tk.Entry(new_win, font=('Arial', 12), bd=3)
        e1.grid(row=1, column=1, padx=10, pady=10)
        # 按钮
        b = tk.Button(new_win, text="确认",
                      width=15, height=2, command=lambda: self.delete_rule(e1.get()))
        b.grid(row=2, column=1, padx=10, pady=10)

        # 展示规则
        rule = Rule()
        results = rule.display_rule()

        for row in results:
            flag = 0
            s = str(row[0]) + '：'
            if row[1] != '':
                s += row[1]
                # global flag
                flag = 1
            if row[2] != '':
                if flag:
                    s += '+' + row[2]
                else:
                    s += row[2]
                    # global flag
                    flag = 1
            if row[3] != '':
                if flag:
                    s += '+' + row[3]
                else:
                    s += row[3]
            s += '-->' + row[4]
            t.insert('end', "\n" + s)
        new_win.mainloop()

    # 删除规则函数
    def delete_rule(self, t):

        #建立游标
        cursor = db.cursor()

        #查询删除的ID是否存在
        sql = "SELECT * FROM RULES WHERE ID = %s" % (t)
        # 执行SQL语句
        cursor.execute(sql)
        results = cursor.fetchone()
        if results == None:
            messagebox.showerror(title="删除的规则不存在",message="您选择删除的规则不存在，请重新输入！")
        else:
            # SQL 删除语句
            sql = "DELETE FROM RULES WHERE ID = %s" % (t)
            try:
                # 执行SQL语句
                cursor.execute(sql)
                # 提交修改
                db.commit()
                messagebox.showinfo(title="删除成功！",message="删除成功！请重新查看规则！")
                cursor.close()
            except Exception as e:
                print("删除规则出错！")
                # 发生错误时回滚
                db.rollback()
                print("执行MySQL: %s 时出错：%s" % (sql, e))

    #显示修改规则界面函数
    def update_gui(self):
        new_win = tk.Tk()
        new_win.title("修改规则")
        new_win.geometry('650x500')

        # 标签
        l1 = tk.Label(new_win, text="请输入您想修改的规则编号（ID）：",
                      bg='pink', font=('Arial', 12), width=30, height=2)
        l1.grid(row=0, column=0, padx=10, pady=10)
        l2 = tk.Label(new_win, text="所处方位:",
                      bg='pink', font=('Arial', 12), width=30, height=2)
        l2.grid(row=1, column=0, padx=10, pady=10)
        l3 = tk.Label(new_win, text="城市规模:",
                      bg='pink', font=('Arial', 12), width=30, height=2)
        l3.grid(row=2, column=0, padx=10, pady=10)
        l4 = tk.Label(new_win, text="所属城市圈:",
                      bg='pink', font=('Arial', 12), width=30, height=2)
        l4.grid(row=3, column=0, padx=10, pady=10)
        l5 = tk.Label(new_win, text="结果:",
                      bg='pink', font=('Arial', 12), width=30, height=2)
        l5.grid(row=4, column=0, padx=10, pady=10)
        l6 = tk.Label(new_win, text="p.s. 若不填则默认值为NULL",
                      bg='pink', font=('Arial', 12), width=40, height=2)
        l6.grid(row=5, column=0, padx=10, pady=10)

        # 输入文本框
        e0 = tk.Entry(new_win, font=('Arial', 12), bd=3)
        e0.grid(row=0, column=1, padx=10, pady=10)
        e1 = tk.Entry(new_win, font=('Arial', 12), bd=3)
        e1.grid(row=1, column=1, padx=10, pady=10)
        e2 = tk.Entry(new_win, font=('Arial', 12), bd=3)
        e2.grid(row=2, column=1, padx=10, pady=10)
        e3 = tk.Entry(new_win, font=('Arial', 12), bd=3)
        e3.grid(row=3, column=1, padx=10, pady=10)
        e4 = tk.Entry(new_win, font=('Arial', 12), bd=3)
        e4.grid(row=4, column=1, padx=10, pady=10)

        # 按钮
        b = tk.Button(new_win, text="确认",
                      width=15, height=2, command=lambda: self.update_rule(e0.get(),e1.get(), e2.get(), e3.get(), e4.get()))
        b.grid(row=5, column=1, padx=10, pady=10)

    #修改规则函数
    def update_rule(self,t0,t1,t2,t3,t4):

        # 建立游标
        cursor = db.cursor()
        # 查找该规则id是否存在
        sql = "SELECT * FROM RULES WHERE ID = %s" % (t0)
        cursor.execute(sql)
        if cursor.fetchone() == None:
            messagebox.showerror(title="规则不存在！",message="您要修改的规则编号不存在！请重新输入编号")
        else:

            # SQL 更新语句(修改)
            sql = "UPDATE RULES SET LOCATION='%s'," \
                  "SIZE='%s'," \
                  "CITY='%s', " \
                  "RESULTS='%s' WHERE ID = %s" % (t1,t2,t3,t4,t0)
            print(sql)
            try:
                # 执行SQL语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                messagebox.showinfo(title="修改数据成功！",message="修改规则成功！请重新查看规则！")
            except Exception as e:
                print("修改规则出错！")
                # 发生错误时回滚
                db.rollback()
                print("执行MySQL: %s 时出错：%s" % (sql, e))


    # 推理匹配函数
    def matching(self):
        self.t.delete(1.0,'end')
        cursor = db.cursor()
        # 获取用户输入的事实
        str = []
        str.append(self.e1.get())
        str.append(self.e2.get())
        str.append(self.e3.get())
        str.append(self.e4.get())
        # 查找当前综合数据库最大ID
        # print(str)
        sql = "SELECT MAX(ID) FROM SYNTHESIS"
        try:
            cursor.execute(sql)
        except Exception as e:
            print("查找事实库最大ID出错！")
            # 发生错误时回滚
            db.rollback()
            print("执行MySQL: %s 时出错：%s" % (sql, e))
        ID = cursor.fetchone()[0]
        if ID == None:
            ID = 1
        else:
            ID += 1
        print(ID)
        id = ID
        #将事实加入综合数据库
        for i in range(4):
            if str[i] != '':
                sql = "INSERT INTO SYNTHESIS(ID, FACTS) VALUES (%d,'%s')" % (ID, str[i])
                try:
                    cursor.execute(sql)
                    db.commit()
                    ID += 1
                except Exception as e:
                    print("添加事实出错！")
                    # 发生错误时回滚
                    db.rollback()
                    print("执行MySQL: %s 时出错：%s" % (sql, e))
        a = Control()
        ans = a.identify(id)
        if ans == []:
            self.t.insert('end', "无法识别！！！" + '\n')
        else:
            #lens_ans表示结论个数
            lens_ans = len(ans)
            for i in range(lens_ans):
                if i != lens_ans-1:
                    self.t.insert('end', "推理得到的中间结果：")
                else:
                    self.t.insert('end',"推理得到的最终结果：")
                lens_temp = len(ans[i])
                for j in range(lens_temp):
                    if j == 0:
                        self.t.insert('end', ans[i][j])
                    elif j != lens_temp - 1:
                        self.t.insert('end', "+" + ans[i][j])
                    else:
                        self.t.insert('end', "-->" + ans[i][j] + '\n')

    def clear(self):
        self.e1.delete(0,'end')
        self.e2.delete(0,'end')
        self.e3.delete(0,'end')
        self.e4.delete(0,'end')

        self.t.delete(1.0,'end')


