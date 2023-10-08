from typing import List
from player import GeniusPlayer
import random

class GeniusGame:
    def __init__(self, seed, player0_deck, player1_deck) -> None:
        self.num_players = 3
        self.seed = seed
        random.seed(seed)
        self.first_player: bool
        self.active_player: bool
        player0 = GeniusPlayer(player0_deck)
        player1 = GeniusPlayer(player1_deck)
        self.players = [player0, player1]

    def init_game(self):
        '''
        初始化阶段,包括选择起始手牌,选择出战角色
        '''
        # 决定谁方先手
        first = random.choice([0, 1])
        self.first_player = first

        # 初始化双方状态
        self.set_hand_card()
        self.set_active_character()

    def step(self):
        '''
        回合轮次
        '''
        self.roll_phase()
        self.action_phase()
        self.end_phase()
        
    def set_hand_card(self):
        for player in self.players:
            pass

    def set_active_character(self):
        '''
        选择出战角色
        '''
        pass
    
    def roll_phase(self, player, now_dice):
        '''
        掷骰子阶段, 输入为需要投掷的骰子个数和每个的类别(默认为8和随机),返回一个数组
        '''
        if now_dice is None:
            # 此时为第一次投掷
            return List
        else: 
            pass

    