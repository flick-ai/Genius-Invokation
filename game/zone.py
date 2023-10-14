from typing import List, TYPE_CHECKING
import numpy as np
from utils import *
from copy import deepcopy
from card.action import *
from card.action.equipment.weapon.weapons.raven_bow import RavenBow


if TYPE_CHECKING:
    from entity.entity import Entity
    from game.player import GeniusPlayer
    from entity.summon import Summon
    from entity.support import Support
    from entity.status import Status, Shield
    from entity.character import Character

class DiceZone:
    '''
        骰子区
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.player = player
        '''
            我们用一个[16, 9]的数组来维护骰子
        '''
        self.num = 0
        self.space = np.zeros((MAX_DICE, DICENUM)).astype(np.int16)
        for i in range(MAX_DICE):
            self.space[i][-1] = -1
        self.sort_map = self.get_sort_map()


    def get_sort_map(self):
        sort_map = {i:DICENUM-i for i in range(DICENUM)}
        sort_map[-1] = -1
        sort_map[DiceType.OMNI.value] = 4000 # 万能最优先

        # 有效骰子优先
        for character in self.player.character_list:
            if character.character_zone.is_alive:
                sort_map[ElementToDice[character.element].value] += 200

        # 数量多优先
        sum_dice = self.space.sum(axis=0)[:-1]
        for i in range(DICENUM-1):
            sort_map[i] += 10 * sum_dice[i]
        return sort_map

    def add(self, dices: List):
        '''
            获取骰子
        '''
        dices = sorted(dices, key=lambda x:self.sort_map[x])
        for idx, dice in enumerate(dices):
            if dice != 7:
                self.space[idx][-1] = dice
                self.space[idx][dice] = 1
            else:
                self.space[idx][-1] = dice
                for i in range(DICENUM-1):
                    self.space[idx][i] = 1
            self.num += 1
            if self.num == MAX_DICE:
                break
        self.sort_dice()

    def delete(self, idx):
        self.space[idx][-1] = -1
        for i in range(DICENUM-1):
            self.space[idx][i] = 0

    def remove(self, dices: List):
        '''
            使用骰子
        '''
        dices.sort(reverse=True)
        for dice in dices:
            self.delete(dice)

    def calculate_dice(self, game):
        '''
            计算是否有满足某种要求的骰子
        '''
        # TODO


    def sort_dice(self):
        ''''
            对骰子进行排序
        '''
        self.sort_map = self.get_sort_map()
        self.space = np.array(sorted(self.space, key=lambda x:self.sort_map[x[-1]], reverse=True))

    def show(self):
        '''
            展示骰子区状况
        '''
        if self.num == 0:
            return None
        else:
            return self.space[0:self.num, -1]

    def num(self):
        '''
            计算骰子区数量
        '''
        return self.num

class CardZone:
    '''
        牌堆区,
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer', card: List) -> None:
        '''
            牌堆结构为一个随机过的固定顺序列表
        '''
        self.card = []
        for card_name in card:
            self.card.append(eval(card_name)())
        self.card_num = len(self.card)
        # 随机固定牌序
        np.random.shuffle(self.card)

    def find_card(self, card_type: 'ActionCardType', num=1):
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
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.max_num = 4
        self.space: List[Summon] = []

    def destroy(self, entity):
        for idx, exist in enumerate(self.space):
            if entity.name == exist.name:
                self.space.pop(idx)
                return
    def has_entity(self, entity):
        # entity here is the class, not the instace
        # Check whether a kind of entity already exists in self.character_zone.status_list.
        # If exists, return the status instance in the list to let the caller know and just use entity.update.
        # If not, return None to let the caller know and use add_entity.
        for summon in self.space:
            if isinstance(summon, entity):
                return summon
        return None

    def check_full(self):
        return len(self.space) == self.max_num

    def add_entity(self, entity: 'Summon'):
        if not self.check_full():
            self.space.append(entity)
        # for idx, exist in enumerate(self.space):
        #     if entity.name == exist.name:
        #         self.space[idx].update()
        #         return
        # if len(self.space) < self.max_num:
        #     self.space.append(entity)

    def num(self):
        return len(self.space)

class SupportZone:
    '''
        支援区
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.space: List[Support] = []

    def destroy(self, entity: 'Support'):
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
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.weapon_card: WeaponCard
        self.artifact_card: ArtifactCard
        self.talent_card: TalentCard

        self.is_active: bool = False
        self.is_alive: bool = True
        self.status_list: List['Status'] = []
        self.elemental_application: List = []


    def heal(self, heal):
        self.hp += heal
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def has_entity(self, entity):
        # entity here is the class, not the instace
        # Check whether a kind of entity already exists in self.character_zone.status_list.
        # If exists, return the status instance in the list to let the caller know and just use entity.update.
        # If not, return None to let the caller know and use add_entity.

        for status in self.status_list:
            if isinstance(status, entity):
                return status
        return None

    def add_entity(self, entity: 'Status'):
        self.status_list.append(entity)

    def skill(self, skill, game: 'GeniusGame'):
        self.character.characacter_skill_list[skill].on_call(game)

class ActiveZone:
    '''
        全队战斗状态区
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.player = player
        self.space: List[Status] = []
        self.shield: List[Shield] = []

    def destroy(self, entity):
        for idx, exist in enumerate(self.space):
            if entity.name == exist.name:
                self.space.pop(idx)

    def has_status(self, entity):
        # entity here is the class, not the instace
        # Check whether a kind of entity already exists in self.character_zone.status_list.
        # If exists, return the status instance in the list to let the caller know and just use entity.update.
        # If not, return None to let the caller know and use add_entity.
        for exist in self.space:
            if isinstance(exist, entity):
                return exist
        return None

    def has_shield(self, entity):
        # entity here is the class, not the instace
        # Check whether a kind of entity already exists in self.character_zone.status_list.
        # If exists, return the status instance in the list to let the caller know and just use entity.update.
        # If not, return None to let the caller know and use add_entity.
        for exist in self.shield:
            if isinstance(exist, entity):
                return exist
        return None

    def add_entity(self, entity):
        # When using add_entity, please make sure that the same kind of entity is not exisits in the list.
        if isinstance(entity, Shield):
            self.shield.append(entity)
        else:
            self.space.append(entity)

class HandZone:
    '''
        手牌区
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.card = []

    def remove(self, idx: List):
        if type(idx) == int:
            idx = [idx]
        idx.sort(reverse=True)
        return [self.card.pop(i) for i in idx]


    def add(self, cards):
        for card in cards:
            if len(self.card)>= MAX_HANDCARD:
                break
            self.card.append(card)
            sorted(self.card, key=lambda card: card.id)

    def num(self):
        return len(self.card)


