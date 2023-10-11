from typing import List, TYPE_CHECKING
import numpy as np
from utils import *
from copy import deepcopy

if TYPE_CHECKING:
    from entity.entity import Entity
    from entity.summon import Summon
    from entity.support import Support
    from card.action.base import ActionCard
    from entity.character import Character
    from card.action import WeaponCard, ArtifactCard

class DiceZone:
    '''
        骰子区
    '''
    def __init__(self) -> None:
        pass
    
class CardZone:
    '''
        牌堆区, 一共支持三种操作:
        1. 检索并获取特定类型的牌
        2. 随机获取牌
        3. 将牌放回牌堆
    '''
    def __init__(self, card: List) -> None:
        '''
            牌堆结构为一个随机过的固定顺序列表
        '''
        self.card = []
        for card_name in card:
            self.card.append(eval(card_name)())
        self.card_num = len(self.card)
        # 随机固定牌序
        np.random.shuffle(self.card)

    def find_card(self, card_type: ActionCardType, num=1):
        '''
            检索并获取特定类型的牌
        '''
        get_list = []
        for card in reversed(self.card):
            if card.type == card_type:
                get_list.append(card)
                if len(get_list) == num:
                    break

        # 按照id顺序排序返回的牌
        get_list = sorted(get_list, key=lambda card:card.id)
        return get_list

    def get_card(self, num):
        '''
            随机获取牌
        '''
        get_list = []
        for i in range(num):
            get_list.append(self.card.pop())
        self.card_num = len(self.card)

        # 按照id顺序排序返回的牌
        get_list = sorted(get_list, key=lambda card:card.id)
        return get_list

    def return_card(self, card_list: List):
        '''
            将牌放回牌堆
        '''
        for card in card_list:
            idx = np.random.randint(0, self.card_num+1)
            self.card.insert(idx, card)
            self.card_num = len(self.card)

class SummonZone:
    '''
        召唤物区
    '''
    def __init__(self) -> None:
        self.max_num = 4
        self.space: List[Summon] = []

    def destroy(self, entity):
        for idx, exist in enumerate(self.space):
            if entity.name == exist.name:
                self.space.pop(idx)

    def add_entity(self, entity: Summon):
        for idx, exist in enumerate(self.space):
            if entity.name == exist.name:
                self.space[idx].update()
        if len(self.space) < self.max_num:
            self.space.append(entity)

class SupportZone:
    '''
        支援区
    '''
    def __init__(self) -> None:
        self.space: List[Support] = []

    def destroy(self, entity: Support):
        for idx, exist in enumerate(self.space):
            if entity.name == exist.name:
                self.space.pop(idx)

    def add_entity(self, entity, idx):
        if len(self.space) == self.max_num:
            # 如果支援区已经满了
            self.space[idx].destroy()
        self.space.append(entity)


class CharacterZone:
    def __init__(self, name) -> None:
        self.character_card: Character = eval(name)
        self.weapon_card: WeaponCard
        self.artifact_card: ArtifactCard
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
        self.elemental_application: List = []

    def on_game_start(self):
        self.power, self.hp, self.special_state = self.character_card.on_game_start()
        self.max_hp = self.hp

    def heal(self, heal):
        self.hp += heal
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def add_status(self, status: Status):
        pass

class ActiveZone:
    def __init__(self, character_list) -> None:
        self.number_of_characters = len(character_list)
        self.active_idx: int = -1
        self.character_list: List[CharacterZone] = self.generate_character_zone(character_list)
        self.summons_zone: SummonZone = SummonZone()
        self.support_zone: SupportZone = SupportZone()
        self.is_after_change_character = True
        self.states_list = []

    def add_state_entity(self, entity):
        pass

    def use_skill(self, Game, action):
        self.character_list[self.active_idx].use_skill(Game)
        self.is_after_change_character = False
    
    def generate_character_zone(self, character_list):
        character_zone_list: List[Character] = []
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
