
# 用于推理匹配，检查规则库中是否有符合的知识
class Check:

    def check_rule(self,fact,rule):
        for r in rule:
            if r != '':
                if r not in fact:
                    return 0  #匹配失败
        return 1


