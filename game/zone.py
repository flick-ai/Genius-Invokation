from typing import List
import random
# from card.action import *
from card.character.base import CharacterCard
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
        idx_list = random.choices(range(self.card_num), k=num)
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
    def __init__(self) -> None:
        self.character_card: CharacterCard
        self.weapon_card: None
        self.artifact_card: None
        self.is_active: bool
        self.is_alive: bool
        self.shield: List

class ActiveZone:
    def __init__(self, active_idx, charater_list) -> None:
        self.number_of_characters = len(charater_list) # int
        self.active_idx = active_idx # int, Should be 0,1,2,... from left to right.
        self.character_list= deepcopy(charater_list)
        self.states_list = []

    def change_to_previous_character(self):
        ix = self.active_idx-1
        if ix < 0:
            ix = self.number_of_characters-1
        while self.character_list[ix].states.alive == False:
            ix -= 1
            if ix < 0:
                ix = self.number_of_characters-1
        self.active_idx = ix
        return ix
    
    def change_to_next_character(self):
        ix = self.active_idx+1
        if ix >= self.number_of_characters:
            ix = 0
        while self.character_list[ix].states.alive == False:
            ix += 1
            if ix >= self.number_of_characters:
                ix = 0
        self.active_idx = ix
        return ix
        
