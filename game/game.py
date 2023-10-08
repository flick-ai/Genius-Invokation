

class GeniusGame:
    def __init__(self) -> None:
        self.num_players = 3

    def init_game(self, player1, player2):
        '''
        初始化阶段,包括选择起始手牌,选择出战角色
        '''
        # TODO: 
        # 完成一个初始选择牌的代码
        
        self.set_active_character()
        pass

    def step(self):
        '''
        回合轮次
        '''
        pass

    def set_active_character(self):
        '''
        选择出战角色
        '''
        pass

    def roll_phase(self):
        '''
        掷骰子阶段, 输入为需要投掷的骰子个数和每个的类别(默认为8和随机),返回一个数组
        '''