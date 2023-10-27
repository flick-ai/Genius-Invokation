from typing import List, TYPE_CHECKING
import numpy as np
from genius_invocation.utils import *
from collections import defaultdict
from genius_invocation.game.action import Action
from genius_invocation.game.player import GeniusPlayer
from genius_invocation.event.events import EventManager
from genius_invocation.card.character.base import Damage
from genius_invocation.card.action.base import ActionCard
from genius_invocation.game.zone import Dice
from genius_invocation.event.heal import Heal
from loguru import logger
from rich.console import Console
from rich.table import Column, Table
from genius_invocation.user_layout import *
from genius_invocation.utils_dict import *
from time import time
if TYPE_CHECKING:
    from genius_invocation.card.character.base import CharacterSkill

class GeniusGame:
    '''
    主游戏
    '''
    def __init__(self, player0_deck, player1_deck, seed=None, is_omni=False) -> None:
        self.manager = EventManager()

        self.is_omni = is_omni
        self.num_players = 3
        if seed:
            self.random = np.random.RandomState(seed)
        else:
            seed = int(time())
            self.random = np.random.RandomState(seed)
        self.first_player: int
        self.active_player_index: int
        self.active_player: GeniusPlayer # should be ref of player0 or player1
        player0 = GeniusPlayer(self, player0_deck, 0)
        player1 = GeniusPlayer(self, player1_deck, 1)
        self.players: List[GeniusPlayer] = [player0, player1]
        self.game_phase: GamePhase
        self.special_phase = None
        self.round: int = 0

        self.current_die: Character = None
        self.current_heal: Heal = None
        self.current_dice: Dice = None
        self.current_action: Action = None
        self.current_damage: Damage = None
        self.current_switch: dict(Character) = {"from": None, "to": None}
        self.current_skill: CharacterSkill = None
        self.current_card: ActionCard = None
        self.damage_list: List[Damage] = []
        self.is_change_player: bool
        self.is_end: bool = False
        self.is_overload:GeniusPlayer = None

        self.init_game()


    def reset(self):
        pass

    def init_game(self):
        '''
            初始化阶段,包括选择起始手牌,选择出战角色
        '''
        # 决定谁方先手
        first = self.random.choice([0, 1], 1)[0]
        self.first_player = first
        # 进入选择起始手牌阶段
        self.game_phase = GamePhase.SET_CARD
        self.active_player_index = first
        self.active_player = self.players[first]
        self.active_player.generate_mask(self)
        
    def reset_current(self):
        self.current_skill = None
        self.current_damage = None
        self.current_dice = None
        self.current_action = None
        self.current_card = None
        self.current_dice = None
        self.current_heal = None
        self.current_switch = {"from": None, "to": None}

    def resolve_action(self, action: 'Action'):
        '''
            处理行动信息
        '''
        self.current_action = action
        oppenent_player = self.players[1 - self.active_player_index]
        active_player = self.active_player

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
            
        self.manager.invoke(EventType.AFTER_ANY_ACTION, self)
        self.reset_current()
        if active_player.is_pass:
            if oppenent_player.is_pass:
                self.end_phase()
            else:
                self.first_player = self.active_player_index
        
        if self.is_change_player and (not oppenent_player.is_pass):
            self.change_active_player()
        
        oppenent_player = self.players[1 - self.active_player_index]
        self.manager.invoke(EventType.BEFORE_ANY_ACTION, self)
        while self.active_player.prepared_skill is not None:
            character = self.active_player.prepared_skill.from_character
            if not character.is_active:
                break
            if character.is_frozen:
                break
            self.active_player.prepared_skill.on_call(self)
            if not oppenent_player.is_pass:
                self.change_active_player()

    def add_damage(self, damage: Damage):
        self.damage_list.append(damage)

    def resolve_damage(self):
        while len(self.damage_list) >0:
            self.current_damage = self.damage_list.pop(0)
            self.current_damage.on_damage(self)
            # logger.debug(f"len of damage list {len(self.damage_list)}")
            # del(self.current_damage)
            self.current_damage = None

        if self.is_overload != None:
            self.is_overload.change_to_next_character()
            self.is_overload = None
        self.manager.invoke(EventType.SPECIAL_SWITCH, self)
        self.manager.invoke(EventType.FINAL_EXECUTE, self)
        self.check_dying()

    def suffer_current_damage(self):
        target = self.current_damage.damage_to
        main_dmg = self.current_damage.main_damage
        main_dmg_ele = self.current_damage.main_damage_element
        logger.info("Target {} suffers {} {} damage".format(target.name, main_dmg, main_dmg_ele.name))
        if self.current_damage.damage_from is not None:
            logger.info("The damage is from {}".format(self.current_damage.damage_from.name))
        else:
            logger.info("The damage is from None (A status attached on the target character.)")
        main_dmg = min(target.health_point, main_dmg)

        target.health_point -= main_dmg

        if self.current_damage.piercing_damage > 0:
            target_player = target.from_player
            for char in target_player.character_list:
                if char==target: continue
                if char.is_alive:
                    logger.info("Target {} suffers {} piercing damage".format(char.name, self.current_damage.piercing_damage))
                    char.health_point -= self.current_damage.piercing_damage

    def check_dying(self):
        for player in self.players:
            num = 0
            for idx, char in enumerate(player.character_list):
                if not char.is_alive:
                    num += 1
                    continue
                if char.health_point <= 0:
                    char.is_alive = False
                    self.manager.invoke(EventType.CHARACTER_WILL_DIE, self)
                    if not char.is_alive:
                        num += 1
                        char.dying(self)
                        char.from_player.last_die_round = self.round
                        self.current_die = char
                        self.manager.invoke(EventType.CHARACTER_DIE, self)
            if num == 3:
                print(f"player{1-player.index} is winner!")
                exit()
            if not player.character_list[player.active_idx].is_alive:
                Active_Die(player).on_call(self)
            # num = 0
            # for idx, char in enumerate(player.character_list):
            #     if not char.is_alive:
            #         num += 1
            #         continue
            #     if char.health_point <= 0:
            #         char.is_alive = False
            #         self.manager.invoke(EventType.CHARACTER_DIE, self)
            #         if not char.is_alive:
            #             char.dying(self)
            #             num += 1
            #             if num == 3:
            #                 print("Winner is oppenent!")
            #                 exit()
            #             if player.active_idx == idx:
            #                 Active_Die(player).on_call(self)

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

        self.active_player.generate_mask(self)

    def set_hand_card(self, action):
        '''
            选择手牌部分
        '''
        self.active_player.choose_card(action)
        if self.special_phase is None:
            self.change_active_player()
            if self.active_player_index == self.first_player:
                self.game_phase = GamePhase.SET_CHARACTER
        else:
            self.special_phase.on_finished(self)

    def set_active_character(self, action):
        '''
            选择出战角色
        '''
        self.current_action = action
        if self.special_phase is None:
            self.active_player.choose_character(action)
            self.change_active_player()
            if self.active_player_index == self.first_player:
                self.roll_phase()
        else:
            self.special_phase.on_finished(self)


    def set_reroll_dice(self, action):
        '''
            选择重新投掷的骰子
        '''
        self.active_player.choose_dice(action)
        self.active_player.roll_time -= 1
        if self.active_player.roll_time == 0:
            if self.special_phase is None:
                self.change_active_player()
                if self.active_player_index == self.first_player:
                    self.action_phase()
            else:
                self.special_phase.on_finished(self)

    def roll_phase(self):
        '''
            进入投掷骰子的阶段
        '''
        self.round += 1
        self.active_player_index = self.first_player
        self.active_player = self.players[self.active_player_index]
        self.game_phase = GamePhase.ROLL_PHASE

        self.active_player.begin_roll_phase(self)
        self.change_active_player()
        self.active_player.begin_roll_phase(self)
        self.change_active_player()


    def action_phase(self):
        '''
            进入交替行动阶段
        '''

        self.active_player.begin_action_phase(self)
        self.change_active_player()
        self.active_player.begin_action_phase(self)
        self.change_active_player()
        self.game_phase = GamePhase.ACTION_PHASE

    def end_phase(self):
        '''
            进入回合结束阶段
        '''
        self.game_phase = GamePhase.END_PHASE
        # 谁先pass谁先结算
        self.active_player_index = self.first_player
        self.active_player = self.players[self.active_player_index]

        self.active_player.end_phase(self)
        self.change_active_player()
        self.active_player.end_phase(self)
        self.change_active_player()

        # 进入下一个回合
        self.roll_phase()

    def encode_message(self):
        '''
            新版: 尝试将Game信息编码成table呈现给使用者
        '''
        return layout(self)
        # return get_dict(self)

    def change_active_player(self):
        self.active_player_index = 1 - self.active_player_index
        self.active_player = self.players[self.active_player_index]



class Active_Die:
    def __init__(self, player) -> None:
        self.die_player = player
        self.now_phase: GamePhase
        self.activate_player_index: int

    def on_call(self, game: 'GeniusGame'):
        self.now_phase = game.game_phase
        game.game_phase = GamePhase.SET_CHARACTER
        self.activate_player_index = game.active_player_index
        if game.active_player != self.die_player:
            game.change_active_player()
        game.special_phase = self
        game.active_player.generate_mask(game)
        action = Action.from_input(game)
        game.step(action)

    def on_finished(self, game: 'GeniusGame'):
        game.active_player.choose_character(game.current_action)
        game.change_active_player()
        game.game_phase = self.now_phase
        game.special_phase = None
        game.active_player_index = self.activate_player_index
        game.active_player = game.players[game.active_player_index]