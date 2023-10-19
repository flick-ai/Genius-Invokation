from typing import List, TYPE_CHECKING
import numpy as np
from utils import *
from collections import defaultdict
from game.action import Action
from .player import GeniusPlayer
from event.events import EventManager
from card.character.base import Damage
from card.action.base import ActionCard
from game.zone import Dice
from loguru import logger
if TYPE_CHECKING:
    from card.character.base import CharacterSkill

class GeniusGame:
    '''
    主游戏
    '''
    def __init__(self, player0_deck, player1_deck) -> None:
        self.manager = EventManager()

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
        self.special_phase = None
        self.round: int = 0

        self.current_dice: Dice = None
        self.current_action: Action = None
        self.current_damage: Damage = None
        self.current_skill: CharacterSkill = None
        self.current_card: ActionCard = None
        self.damage_list: List[Damage] = []
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

        self.manager.invoke(EventType.BEFORE_ANY_ACTION, self)

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

        self.manager.invoke(EventType.AFTER_ANY_ACTION, self)

        if self.is_change_player and (not oppenent_player.is_pass):
            self.change_active_player()

    def add_damage(self, damage: Damage):
        self.damage_list.append(damage)

    def resolve_damage(self):
        while len(self.damage_list) >0:
            self.current_damage = self.damage_list.pop(0)
            self.current_damage.on_damage(self)
            logger.debug(f"len of damage list {len(self.damage_list)}")
            del(self.current_damage)
            self.current_damage = None

        self.check_dying() # TODO: Not Implement yet.

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

        target.health_point -= self.current_damage.main_damage

        if self.current_damage.piercing_damage > 0:
            target_player = target.from_player
            for char in target_player.character_list:
                if char==target: continue
                if char.is_alive:
                    logger.info("Target {} suffers {} piercing damage".format(char.name, self.current_damage.piercing_damage))
                    char.health_point -= self.current_damage.piercing_damage

    def check_dying(self):
        for player in self.players:
            for idx, char in enumerate(player.character_list):
                if char.health_point <= 0:
                    char.is_alive = False
                    self.manager.invoke(EventType.CHARACTER_DIE, self)
                    if not char.is_alive:
                        char.character_zone.clear() # TODO: Not Implement Yet.
                        if player.active_idx == idx:
                            Active_Die(player).on_call(self)
        #TODO: Not Implement yet.
        # pass

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
        self.active_player.choose_character(action)

        if self.special_phase is None:
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
        self.players[self.active_player_index].begin_action_phase(self)
        self.change_active_player()
        self.players[self.active_player_index].begin_action_phase(self)
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
            尝试将Game的信息编码成str呈现给使用者
        '''
        message = {'game':{}, 0:{}, 1:{}}
        message['game']['round'] = self.round
        message['game']['round_phase'] = self.game_phase.name
        message['game']['active_player'] = int(self.active_player_index)
        message['game']['first_player'] = int(self.first_player)
        for player in [0, 1]:
            message[player]['active_zone_shiled'] = self.players[player].team_combat_status.shield
            message[player]['active_zone_status'] = self.players[player].team_combat_status.space
            message[player]['active_character_idx'] = self.players[player].active_idx
            message[player]['card_zone'] = {'num':self.players[player].card_zone.num()}
            message[player]['hand_zone'] = [card.name for card in self.players[player].hand_zone.card]
            message[player]['support_zone'] = [support.name for support in self.players[player].support_zone.space]
            message[player]['dice_zone'] = self.players[player].dice_zone.show()
            for character in self.players[player].character_list:
                message[player][character.name] = {}
                message[player][character.name]['active'] = character.is_active
                message[player][character.name]['alive'] = character.is_alive
                message[player][character.name]['character_zone'] = character.character_zone.status_list

            # message[player]['summon_zone'] = [summon.name for summon in self.players[player].summons_zone.space]
        return message

    def change_active_player(self):
        self.active_player_index = 1 - self.active_player_index
        self.active_player = self.players[self.active_player_index]
        oppenent_player = self.players[1 - self.active_player_index]
        if self.active_player.prepared_skill is not None:
            character = self.active_player.prepared_skill.from_character
            if character.is_active and character.is_frozen:
                self.active_player.prepared_skill.on_call(self)
            if oppenent_player.is_pass:
                while self.active_player.prepared_skill is not None:
                    character = self.active_player.prepared_skill.from_character
                    if character.is_active and character.is_frozen:
                        self.active_player.prepared_skill.on_call(self)
            else:
                self.change_active_player()



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
        game.game_phase = self.now_phase
        game.special_phase = None
        game.active_player_index = self.activate_player_index
        game.active_player = game.players[game.active_player_index]