from typing import List, TYPE_CHECKING
import numpy as np
from utils import *
from copy import deepcopy

if TYPE_CHECKING:
    from entity.entity import Entity
    from entity.summon import Summon
    from entity.support import Support
    from entity.status import Status, Shield
    from card.action.base import ActionCard
    from entity.character import Character
    from card.action import WeaponCard, ArtifactCard, TalentCard

class DiceZone:
    '''
        骰子区
    '''
    def __init__(self, player) -> None:
        self.player = player

    def get_dice(self):
        '''
            获取骰子
        '''
    
    def use_dice(self):
        '''
            使用骰子
        '''

    def calculate_dice(self):
        '''
            计算骰子
        '''

    def sort_dice(self):
        ''''
            对骰子进行排序
        '''
        # 默认骰子排序
    
class CardZone:
    '''
        牌堆区,
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

    def num(self):
        return len(self.card)

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
                return

    def add_entity(self, entity: Summon):
        for idx, exist in enumerate(self.space):
            if entity.name == exist.name:
                self.space[idx].update()
                return
        if len(self.space) < self.max_num:
            self.space.append(entity)

    def num(self):
        return len(self.space)

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
                return

    def add_entity(self, entity, idx):
        if len(self.space) == self.max_num:
            # 如果支援区已经满了
            self.space[idx].destroy()
        self.space.append(entity)
    
    def num(self):
        return len(self.space)


class CharacterZone:
    '''
        单个角色状态区, 包括角色牌、装备区、角色状态
    '''
    def __init__(self, name) -> None:
        self.character: Character = eval(name)
        self.character.init_state()
        self.weapon_card: WeaponCard
        self.artifact_card: ArtifactCard
        self.talent_card: TalentCard

        self.is_active: bool = False
        self.is_alive: bool = True
        self.special_state: List = []
        self.elemental_application: List = []

    def heal(self, heal):
        self.hp += heal
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def add_entity(self, entity: Status):
        pass

    def skill(self, skill, game: GeniusGame):
        self.character.characacter_skill_list[skill].on_call(game)

class ActiveZone:
    '''
        全队战斗状态区
    '''
    def __init__(self) -> None:
        self.space: List[Status] = []
        self.shield: List[Shield] = []

    def destroy(self, entity):
        for idx, exist in enumerate(self.space):
            if entity.name == exist.name:
                self.space.pop(idx)

    def add_entity(self, entity):
        if type(entity) == Shield:
            for idx, exist in enumerate(self.space):
                if entity.name == exist.name:
                    self.shield[idx].update()
                    return
            self.shield.append(entity)
        else:
            for idx, exist in enumerate(self.space):
                if entity.name == exist.name:
                    self.space[idx].update()
            self.space.append(entity)

class HandZone:
    '''
        手牌区
    '''
    def __init__(self) -> None:
        self.card = []

    def remove(self, idx):
        self.card.pop(idx)

    def add(self, cards):
        for card in cards:
            if len(self.card)>= MAX_HANDCARD:
                break
            self.hand_zone.append(card)
            sorted(self.hand_zone, key=lambda card: card.id)

    def num(self):
        return len(self.card)


