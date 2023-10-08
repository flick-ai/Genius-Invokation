from typing import List
from player import GeniusPlayer
from game.action import Action
import random
from utils import *

class GeniusGame:
    '''
    主游戏
    '''
    def __init__(self, seed, player0_deck, player1_deck) -> None:
        self.num_players = 3
        self.seed = seed
        random.seed(seed)
        self.first_player: int
        self.active_player: int
        player0 = GeniusPlayer(player0_deck)
        player1 = GeniusPlayer(player1_deck)
        self.players = [player0, player1]
        self.game_phase: GamePhase
    
    def reset(self):
        pass

    def init_game(self):
        '''
        初始化阶段,包括选择起始手牌,选择出战角色
        '''
        # 决定谁方先手
        first = random.choice([0, 1])
        self.first_player = first
        # 进入选择起始手牌阶段
        self.game_phase = GamePhase.SET_CARD
        self.active_player = first

    def resolve_action(self, action: Action):
        
        match self.game_phase:
            case GamePhase.ROLL_PHASE:
                pass
            case GamePhase.ACTION_PHASE:
                if action.choice_type == ActionChoice.HAND_CARD:
                    pass
                elif action.choice_type == ActionChoice.CHARACTER_SKILL:
                    pass
                elif action.choice_type == ActionChoice.CHANGE_CHARACTER:
                    pass


    def step(self, action: Action):
        '''
        回合轮次
        '''
        match self.game_phase:
            case GamePhase.SET_CARD:
                self.set_hand_card()
            case GamePhase.SET_CHARACTER:
                self.set_active_character
            case _:
                self.resolve_action(action)
        
    def set_hand_card(self, action):
        '''
        选择手牌部分, action: [5,1]的0/1
        '''
        active = self.active_player
        self.players[active].choose_card(action)
        if self.active_player == self.first_player:
            self.active_player = not active
        else:
            self.game_phase = GamePhase.SET_CHARACTER
            self.active_player = self.first_player

    def set_active_character(self, action):
        '''
        选择出战角色, action: [3,1]的one-hot
        '''
        active = self.active_player
        self.players[active].choose_character(action)
        if self.active_player == self.first_player:
            self.active_player = not active
        else:
            self.game_phase = GamePhase.ROLL_PHASE
            self.active_player = self.first_player
    
    def roll_phase(self, player, now_dice):
        '''
        掷骰子阶段, 输入为需要投掷的骰子个数和每个的类别(默认为8和随机),返回一个数组
        '''
        if now_dice is None:
            # 此时为第一次投掷
            return List
        else: 
            pass

    