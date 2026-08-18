def none():
    print("没有技能")
class xingkashi:
    def __init__(self,name="星卡师", hp=100, skills=[]):
        self.name = name
        self.hp = hp
        self.skills = skills
    def skill(self, num):
        if 0 <= num < len(self.skills):
            print(f"{self.name}使用了技能：{self.skills[num]}")
            return self.skills[num]
        else:
            print("无效的技能")
    def die(self):
        if self.hp <= 0 and self.hp != "*":
            print(f"{self.name} 已经死亡")
class skill:
    def __init__(self, name='', n=0):
        self.name = name
        self.n = n
    def kill(self,your):
        print(f"技能 {self.name} 造成了 {self.n} 点伤害")
        your.hp -= self.n
        your.die()
        return self
    def hp_plus(self, myself):
        print(f"技能 {self.name} 回复了 {self.n} 点生命值")
        myself.hp += self.n
        return self
    def Cannot_check(self,myself):
        print(f" {myself.name} 无法选中")
        myself.hp = "*"
        return self


player1 = xingkashi(name="玩家1", hp=100, skills=[])
player2 = xingkashi(name="玩家2", hp=100, skills=[])
skill1 = skill(name="火球术", n=99)
skill2 = skill(name="无法选中")
player2.skills.append(skill2)
player1.skills.append(skill1)
def player1_skill_1():
    player1.skill(0).kill(player2)
def player2_skill_1():
    player2.skill(0).Cannot_check(player2)
player1_skill_1()
player2_skill_1()
