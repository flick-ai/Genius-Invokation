from typing import List, TYPE_CHECKING
import numpy as np
from utils import *
from collections import defaultdict
from game.action import Action
from .player import GeniusPlayer
from event.events import EventManager
from card.character.base import Damage
from game.zone import Dice

if TYPE_CHECKING:
    from card.character.base import CharacterSkill

class GeniusGame:
    '''
    主游戏
    '''
    def __init__(self, player0_deck, player1_deck) -> None:
        self.num_players = 3
        # self.seed = seed
        # np.random.seed(seed)
        self.first_player: int
        self.active_player_index: int
        self.active_player: GeniusPlayer # should be ref of player0 or player1
        player0 = GeniusPlayer(self, player0_deck, 0)
        player1 = GeniusPlayer(self, player1_deck, 1)
        self.players: List[GeniusPlayer] = [player0, player1]
        self.game_phase: GamePhase
        self.round: int = 0

        self.manager = EventManager()
        self.current_dice: Dice
        self.current_action: Action
        self.current_damage: Damage
        self.current_skill: CharacterSkill
        self.damage_list: List[Damage]
        self.is_change_player: bool
        self.is_end: bool = False

        self.init_game()


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
        self.active_player_index = first
        self.active_player = self.players[first]
        for player in self.players:
            player.generate_mask(self)

    def resolve_action(self, action: 'Action'):
        '''
            处理行动信息
        '''
        self.current_action = action
        oppenent_player = self.players[1 - self.active_player_index]
        active_player = self.active_player
        active_player.use_dice(self)

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
            self.is_change_player = True
            active_player.is_pass = True
            if oppenent_player.is_pass:
                self.end_phase()
            else:
                self.first_player = self.active_player_index

        if self.is_change_player and (not oppenent_player.is_pass):
            self.active_player_index = not self.active_player_index
            self.active_player = self.players[self.active_player_index]

    def add_damage(self, damage: Damage):
        self.damage_list.append(damage)

    def resolve_damage(self):
        while len(self.damage_list >0):
            self.current_damage = self.damage_list.pop(0)
            self.current_damage.on_damage(self)
            del(self.current_damage)
            self.current_damage = None

        self.check_dying() # TODO: Not Implement yet.

    def check_dying(self):
        #TODO: Not Implement yet.
        pass

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

        for player in self.players:
            player.generate_mask(self)

    def set_hand_card(self, action):
        '''
            选择手牌部分
        '''
        active_idx = self.active_player_index
        self.active_player.choose_card(action)
        if active_idx == self.first_player:
            self.active_player_index = 1 - active_idx
            self.active_player = self.players[self.active_player_index]
        else:
            self.game_phase = GamePhase.SET_CHARACTER
            self.active_player_index = self.first_player
            self.active_player = self.players[self.first_player]

    def set_active_character(self, action):
        '''
            选择出战角色
        '''
        active_idx = self.active_player_index
        self.active_player.choose_character(action)
        if active_idx == self.first_player:
            self.active_player_index = 1 - active_idx
            self.active_player = self.players[self.active_player_index]
        else:
            self.active_player_index = self.first_player
            self.active_player = self.players[self.active_player_index]
            self.roll_phase()


    def set_reroll_dice(self, action):
        '''
            选择重新投掷的骰子
        '''
        active_idx = self.active_player_index
        self.active_player.choose_dice(action)
        if active_idx == self.first_player:
            self.active_player_index = 1 -active_idx
            self.active_player = self.players[self.active_player_index]
        else:
            self.active_player_index = self.first_player
            self.active_player = self.players[self.active_player_index]
            self.action_phase()


    def roll_phase(self):
        '''
            进入投掷骰子的阶段, 回合开始
        '''
        self.round += 1
        self.active_player_index = self.first_player
        self.game_phase = GamePhase.ROLL_PHASE
        for player in self.players:
            player.dice_zone.add(player.roll_dice())

    def action_phase(self):
        '''
            进入交替行动阶段
        '''
        self.players[self.active_player_index].begin_round(self)
        self.active_player_index = 1 - self.active_player_index
        self.active_player = self.players[self.active_player_index]

        self.players[self.active_player_index].begin_round(self)
        self.active_player_index = 1 - self.active_player_index
        self.active_player = self.players[self.active_player_index]

        self.game_phase = GamePhase.ACTION_PHASE

    def end_phase(self):
        '''
            进入回合结束阶段
        '''
        self.game_phase = GamePhase.END_PHASE

        self.players[self.active_player_index].end_round(self)
        self.active_player_index = 1 - self.active_player_index
        self.active_player = self.players[self.active_player_index]

        self.players[self.active_player_index].end_round(self)
        self.active_player_index = 1 - self.active_player_index
        self.active_player = self.players[self.active_player_index]

        self.roll_phase()

    def encode_message(self):
        '''
            尝试将Game的信息编码成str呈现给使用者
        '''
        message = {'game':{}, 0:{}, 1:{}}
        message['game']['round'] = self.round
        message['game']['round_phase'] = self.game_phase.name
        message['game']['active_player'] = int(self.active_player_index)
        message['game']['first_player'] = int(self.first_player)
        for player in [0, 1]:
            message[player]['active_character_idx'] = self.players[player].active_idx
            message[player]['card_zone'] = {'num':self.players[player].card_zone.num()}
            message[player]['hand_zone'] = [card.name for card in self.players[player].hand_zone.card]
            message[player]['support_zone'] = [support.name for support in self.players[player].support_zone.space]
            message[player]['dice_zone'] = self.players[player].dice_zone.show()
            for character in self.players[player].character_list:
                message[player][character.name] = {}
                message[player][character.name]['active'] = character.is_active
                message[player][character.name]['alive'] = character.is_alive

            # message[player]['summon_zone'] = [summon.name for summon in self.players[player].summons_zone.space]
        return message