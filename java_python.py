# -*- coding: utf-8 -*-
""" 
@Time    : 2022/6/28 14:45
@Author  : xuhaotian
@FileName: java_python.py
@SoftWare: PyCharm
"""

""" 
规则类型分两大类：简单规则，复杂规则
简单规则：一条数据即可即时判断；
复杂规则：需多条数据连续判断。

规则触发方式不同，上下限，报警
上下限：数据比大比小
报警：数据是否等于报警值
"""

'''
输入：{数值:[],规则:[]}    {value:[],rule:[]}
数值：int,float
规则：[规则类型，规则描述，触发方式，上限，下限，报警值，报警号]
     [rule_type, rule_desc, trigger_mode, max_val, min_val, alarm_val, alarm_no]
     rule_type: "simple" or "complicated"
     rule_desc: e.g. "超出预设温度区间"
     trigger_mode: "alarm" or "range"
     max_val: int or float, only trigger_mode=="range"
     min_val: int or float, only trigger_mode=="alarm"
     alarm_val: int, only trigger_mode=="alarm"
     alarm_no: int  
'''
class RuleJudgment():
    def __init__(self, rule_dict):
        self.value=rule_dict["value"]
        self.rule=rule_dict["rule"]
        self.rule_type = self.rule[0]
        self.rule_desc = self.rule[1]
        self.trigger_mode = self.rule[2]
        self.max_val=self.rule[3]
        self.min_val = self.rule[4]
        self.alarm_val = self.rule[5]
        self.alarm_no = self.rule[6]
        self.alarm_flag=0

# trigger_mode=="range"，将数值进行上下限判断
    def max_min_judge(self):
        if self.max_val != None and self.min_val != None:
            if self.min_val<self.value<self.max_val:
                self.alarm_flag=0
            else:
                self.alarm_flag=1
        elif self.max_val != None and self.min_val == None:
            if self.value>self.max_val:
                self.alarm_flag = 1
        elif self.max_val == None and self.min_val != None:
            if self.value<self.min_val:
                self.alarm_flag = 1
        else:
            print("规则上下限格式错误！")

# trigger_mode=="alarm"，报警值判断
    def alarm_judge(self):
        if self.alarm_val is None:
            print("规则报警格式错误")
        elif self.alarm_val==self.value:
            self.alarm_flag=1


# 运行规则判断
    def run(self):
        if self.rule_type == 'simple':
            if self.trigger_mode =="range":
                self.max_min_judge()
            elif self.trigger_mode =="alarm":
                self.alarm_judge()
        # TODO(复杂规则判断)
        elif self.rule_type == 'complicated':


        else:
            print("规则类型不明")

        if self.alarm_flag==1:
            return self.rule_desc, self.alarm_no

