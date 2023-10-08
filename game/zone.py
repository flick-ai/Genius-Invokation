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


class CharacterZone:
    def __init__(self, name) -> None:
        self.character_card: CharacterCard = eval(name)
        self.weapon_card: WeaponCard
        self.artifact_card: None
        self.talent_card: None

        self.is_active = False
        self.is_alive = True
        self.power: int
        self.hp = self.character_card.health_point
        self.shield: List

class ActiveZone:
    def __init__(self, active_idx, character_list) -> None:
        self.number_of_characters = len(character_list)
        self.active_idx = active_idx
        self.character_list = self.generate_character_zone(character_list)
        self.states_list = []
    
    def generate_character_zone(self, character_list):
        character_zone_list = []
        for name in character_list:
            character_zone_list.append(CharacterZone(name))
        return character_zone_list

    def change_to_previous_character(self):
        ix = self.active_idx-1
        if ix < 0:
            ix = self.number_of_characters-1
        while self.character_list[ix].is_alive == False:
            ix -= 1
            if ix < 0:
                ix = self.number_of_characters-1
        self.active_idx = ix
        return ix
    
    def change_to_next_character(self):
        ix = self.active_idx+1
        if ix >= self.number_of_characters:
            ix = 0
        while self.character_list[ix].is_alive == False:
            ix += 1
            if ix >= self.number_of_characters:
                ix = 0
        self.active_idx = ix
        return ix
        
