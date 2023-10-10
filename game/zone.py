from typing import List
import numpy as np
# from card.action import *
from card.character.base import CharacterCard
from card.action.base import WeaponCard
from copy import deepcopy


class CardZone:
    def __init__(self, card: List) -> None:
        self.card = []
        for card_name in card:
            self.card.append(eval(card_name)())
        self.card_num = len(self.card)

    def get_card(self, num):
        '''
        从牌堆中获取牌
        '''
        idx_list = np.random.choice(range(self.card_num), num)
        get_list = []
        for i in idx_list:
            get_list.append(self.card.pop(i))
        self.card_num = len(self.card)
        return get_list

    def return_card(self, card_list: List):
        for card in card_list:
            self.card.append(card)
        self.card_num = len(self.card)

class FourZone:
    '''
    一个用于维护召唤物区和支援区的区域
    '''
    def __init__(self) -> None:
        self.space = [None, None, None, None]

    def destroy(self, idx):
        assert idx>=0 and idx<4
        assert self.space[idx] == None
        self.space[idx] = None

    def put(self, card, idx):
        self.space[idx] = card

class CharacterZone:
    def __init__(self, name) -> None:
        self.character_card: CharacterCard = eval(name)
        self.weapon_card: WeaponCard
        self.artifact_card: None
        self.talent_card: None

        self.is_active: bool = False
        self.is_alive: bool = True
        self.is_satisfied: bool = False
        self.is_frozen: bool = False
        self.special_state: List = []
        self.shield_list: List = []
        self.power: int = 0
        self.hp: int 
        self.max_hp: int
        self.element_attach: List = []

    def on_game_start(self):
        self.power, self.hp, self.special_state = self.character_card.on_game_start()
        self.max_hp = self.hp

class ActiveZone:
    def __init__(self, active_idx, character_list) -> None:
        self.number_of_characters = len(character_list)
        self.active_idx = active_idx
        self.character_list: List[CharacterZone] = self.generate_character_zone(character_list)
        self.summons_zone: FourZone = FourZone()
        self.support_zone: FourZone = FourZone()
        self.is_after_change_character = True
        self.states_list = []

    def use_skill(self, Game, action):
        self.character_list[self.active_idx].use_skill(Game)
        self.is_after_change_character = False
    
    def generate_character_zone(self, character_list):
        character_zone_list: List[CharacterCard] = []
        for name in character_list:
            character_zone_list.append(CharacterZone(name))
        return character_zone_list
    
    def change_character(self, Game, action):
        ##### TODO: 一个需要判断如何切人的接口
        ix: int
        #####
        self.character_list[ix].on_switched(Game)
        ##### TODO: 一个需要判断这次切人是否是快速行动的接口
        is_quick_action: bool
        #####
        return is_quick_action

    def change_to_previous_character(self):
        ix = self.active_idx-1
        if ix < 0:
            ix = self.number_of_characters-1
        while self.character_list[ix].is_alive == False:
            ix -= 1
            if ix < 0:
                ix = self.number_of_characters-1

        self.character_list[self.active_idx].is_active = False
        self.active_idx = ix
        self.character_list[self.active_idx].is_active = True
        self.is_after_change_character = True
        return ix
    
    def change_to_next_character(self):
        ix = self.active_idx+1
        if ix >= self.number_of_characters:
            ix = 0
        while self.character_list[ix].is_alive == False:
            ix += 1
            if ix >= self.number_of_characters:
                ix = 0
        self.character_list[self.active_idx].is_active = False
        self.active_idx = ix
        self.character_list[self.active_idx].is_active = True
        self.is_after_change_character = True
        return ix
        
    def change_to_id(self, id):
        assert id >= 0 and id < self.number_of_characters
        assert self.character_list[id].is_alive == True
        self.character_list[self.active_idx].is_active = False
        self.active_idx = id
        self.character_list[self.active_idx].is_active = True
        self.is_after_change_character = True
        return id
