import random


class set_operations:
    def __init__(self, seti = set()):
        self.set_i = seti
        self.name_list = ["set_i"]
    def update_set(self, new_set, name):
        # 动态设置属性
        setattr(self, name, new_set)
        # 同时更新 set_i
        self.set_i = new_set
        return getattr(self, name)
    def new_set(self, new_set=set(),name = "set"+str(random.randint(1,10000000))):
        if name in self.name_list:
            name = "set"+str(random.randint(1,10000000))
            self.name_list.append(name)
        setattr(self, name, new_set)
        return getattr(self, name)
def my_help():
            return """
            set_operations 类帮助：
            - __init__(seti=None): 初始化集合
            - update_set(new_set, name): 更新集合
            - new_set(new_set=None, name=None): 创建新集合并命名
            - my_help(): 显示帮助信息
            """
if __name__ == "__main__":
    obj = set_operations()
