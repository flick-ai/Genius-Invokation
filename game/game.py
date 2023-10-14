from typing import List, TYPE_CHECKING
import numpy as np
from utils import *
from collections import defaultdict
from game.action import Action
from .player import GeniusPlayer
from event.events import EventManager
from card.character.base import Damage

class GeniusGame:
    '''
    主游戏
    '''
    def __init__(self, seed, player0_deck, player1_deck) -> None:
        self.num_players = 3
        self.seed = seed
        np.random.seed(seed)
        self.first_player: int
        self.active_player: int
        player0 = GeniusPlayer(self, player0_deck)
        player1 = GeniusPlayer(self, player1_deck)
        self.players = [player0, player1]
        self.game_phase: GamePhase
        self.round: int = 0

        self.manager = EventManager()
        self.current_action: Action
        self.current_damage: Damage
        self.current_skill: SkillType

        self.is_change_player: bool

    
    def reset(self):
        pass

    def init_game(self):
        '''
            初始化阶段,包括选择起始手牌,选择出战角色
        '''
        # 决定谁方先手
        first = np.random.choice([0, 1], 1)[0]
        self.first_player = first
        # 进入选择起始手牌阶段
        self.game_phase = GamePhase.SET_CARD
        self.active_player = first

    def resolve_action(self, action: 'Action'):
        '''
            处理行动信息
        '''
        self.current_action = action
        oppenent_player = self.players[not self.active_player]
        active_player = self.players[self.active_player]

        if action.choice_type == ActionChoice.HAND_CARD:
            self.is_change_player = False
            active_player.play_card(self)
        elif action.choice_type == ActionChoice.CHARACTER_SKILL:
            self.is_change_player = True
            active_player.use_skill(self)
        elif action.choice_type == ActionChoice.CHANGE_CHARACTER:
            self.is_change_player = True
            active_player.change_character(self)
        elif action.choice_type == ActionChoice.PASS:
            active_player.is_pass = True
            if oppenent_player.is_pass:
                self.end_phase()

        if self.is_change_player and (not oppenent_player.is_pass):
            self.active_player = not active_player

    def step(self, action: 'Action'):
        '''
        回合轮次
        '''
        match self.game_phase:
            case GamePhase.SET_CARD:
                self.set_hand_card(action)
            case GamePhase.SET_CHARACTER:
                self.set_active_character(action)
            case GamePhase.ROLL_PHASE:
                self.set_reroll_dice(action)
            case GamePhase.ACTION_PHASE:
                self.resolve_action(action)
        
    def set_hand_card(self, action):
        '''
            选择手牌部分
            action: [5,1] 0/1
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
            选择出战角色
            action: [3,1] one-hot
        '''
        active = self.active_player
        self.players[active].choose_character(action)
        if self.active_player == self.first_player:
            self.active_player = not active
        else:
            self.roll_phase()
            self.active_player = self.first_player

    def set_reroll_dice(self, action):
        '''
            选择重新投掷的骰子
            action: [num_dice, 1] 0/1
        '''
        active = self.active_player
        self.players[active].choose_dice(action)
        if self.active_player == self.first_player:
            self.active_player = not active
        else:
            self.action_phase()
            self.active_player = self.first_player
    
    def roll_phase(self):
        '''
            进入投掷骰子的阶段, 回合开始
        '''
        self.round += 1
        self.game_phase = GamePhase.ROLL_PHASE
        for player in self.players:
            player.dice_zone = player.roll_dice()
    
    def action_phase(self):
        '''
            进入交替行动阶段
        '''
        self.players[self.active_player].begin_round(self)
        self.players[not self.active_player].begin_round(self)
        self.game_phase = GamePhase.ACTION_PHASE

    def end_phase(self):
        '''
            
        '''
        self.game_phase = GamePhase.END_PHASE
        self.players[self.active_player].end_round(self)
        self.players[not self.active_player].end_round(self)
        self.roll_phase()
        
    def encode_message(self):
        '''
            尝试将Game的信息编码成str呈现给使用者
        '''
        message = {0:{}, 1:{}}
        for player in message.keys():
            message[player]['card_zone'] = {'num':self.players[player].card_zone.num()} 
            message[player]['hand_zone'] = {}
            message[player]['support_zone'] = {}