from typing import List, TYPE_CHECKING
import numpy as np
from utils import *
from copy import deepcopy
from card.action import *
from entity.status import Status, Shield, Combat_Shield, Weapon, Artifact, Combat_Status
from card.character.characters.keqing import Lightning_Stiletto

if TYPE_CHECKING:
    from entity.entity import Entity
    from game.player import GeniusPlayer
    from entity.summon import Summon
    from entity.support import Support

    from entity.character import Character


class Dice:
    '''
        计算骰子的维护类
    '''
    def __init__(self, from_player, from_character, use_type, cost) -> None:
        self.cost: list({'cost_num': int, 'cost_type': CostType}) = cost
        self.from_player = from_player
        self.from_character: Character = from_character
        self.use_type = use_type
        self.origin_cost = cost

class DiceZone:
    '''
        骰子区
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.player = player
        '''
            我们用一个[16, 9]的数组来维护骰子
        '''
        self.dice_num = 0
        self.space = np.zeros((MAX_DICE, DICENUM+1)).astype(np.int16)
        for i in range(MAX_DICE):
            self.space[i][-1] = -1
        self.sort_map = self.get_sort_map()


    def get_sort_map(self):
        sort_map = {i:DICENUM-i for i in range(DICENUM)}
        sort_map[-1] = -1
        sort_map[DiceType.OMNI.value] = 4000 # 万能最优先

        # 有效骰子优先
        for character in self.player.character_list:
            if character.is_alive:
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
        if dices == []:
            return
        dices = sorted(dices, key=lambda x:self.sort_map[x], reverse=True)
        for idx, dice in enumerate(dices):
            if dice != 7:
                self.space[self.dice_num][-1] = dice
                self.space[self.dice_num][dice] = 1
            else:
                self.space[self.dice_num][-1] = dice
                for i in range(DICENUM-1):
                    self.space[self.dice_num][i] = 1
            self.dice_num += 1
            if self.dice_num == MAX_DICE:
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
        if dices == []:
            return
        dices.sort(reverse=True)
        for dice in dices:
            self.delete(dice)
            self.dice_num -= 1
        self.sort_dice()

    def remove_all(self):
        '''
            清空
        '''
        for dice in range(self.dice_num):
            self.delete(dice)
            self.dice_num -= 1
        self.sort_dice()

    def calculate_dice(self, dice: Dice):
        '''
            计算是否有满足某种要求的骰子
        '''
        is_zero = True
        for cost in dice.cost:
            if cost['cost_num'] != 0:
                is_zero = False
        if is_zero == True:
            return True

        if dice.use_type == 'elemental tuning':
            return self.dice_num - self.space[:, dice.cost[0]['cost_type'].value].sum() > 0
        is_cost = 0
        for cost in dice.cost:
            if cost['cost_type'] == CostType.WHITE:
                if self.space[:,:-1].sum(axis=0).max() >= cost['cost_num']:
                    is_cost += cost['cost_num']
                else:
                    return False
            elif cost['cost_type'] == CostType.BLACK:
                if self.dice_num < cost['cost_num'] + is_cost:
                    return False
            else:
                dice_type = CostToDice[cost['cost_type']].value
                if self.space[:, dice_type].sum() >= cost['cost_num']:
                    is_cost += cost['cost_num']
                else:
                    return False
        return True

    def check_dice(self, dices_idx, cost_num, cost_type):
        '''
            判断某次选择是否合法
        '''
        choose_dice = self.space[dices_idx,-1].tolist()
        if not len(choose_dice) == cost_num:
            return False
        if cost_type < 0:
            cost = CostType(-cost_type)
            for dice in choose_dice:
                if DiceType(dice) == CostToDice[cost]:
                    return False
        else:
            cost = CostType(cost_type)
            if cost == CostType.WHITE:
                if self.space[dices_idx,:-1].sum(axis=0).max() != cost_num:
                    return False
            elif cost == CostType.BLACK:
                return True
            else:
                for dice in choose_dice:
                    if dice != CostToDice[cost].value and dice != DiceType.OMNI.value:
                        return False
        return True


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
        if self.dice_num == 0:
            return None
        else:
            return self.space[0:self.dice_num, -1].tolist()

    def num(self):
        '''
            计算骰子区数量
        '''
        return self.dice_num

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
        return get_list

    def get_card(self, num):
        '''
            随机获取牌
        '''
        get_list = []
        for i in range(num):
            get_list.append(self.card.pop())
        self.card_num = len(self.card)
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
        self.game = game
        self.space: List[Summon] = []

    def remove(self, entity):
        idx = self.space.index(entity)
        self.space.pop(idx)
        self.game.manager.invoke(EventType.ON_SUMMON_REMOVE, self.game)

    def destroy(self, idx):
        self.space[idx].on_destroy(self.game)
        self.space.pop(idx)
        self.game.manager.invoke(EventType.ON_SUMMON_REMOVE, self.game)

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
        return len(self.space) == MAX_SUMMON

    def add_entity(self, entity: 'Summon'):
        if not self.check_full():
            self.space.append(entity)

    def num(self):
        return len(self.space)

class SupportZone:
    '''
        支援区
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.space: List[Support] = []

    def check_full(self):
        return len(self.space) == MAX_SUPPORT

    def destroy(self, entity: 'Support'):
        idx = self.space.index(entity)
        self.space.pop(idx)

    def add_entity(self, entity, idx):
        if self.check_full():
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

        self.weapon_card: Weapon = None
        self.artifact_card: Artifact = None
        # self.talent_card: Talent
        self.status_list: List['Status'] = [] # Including status from weapon and artifact

    def remove_entity(self, entity: 'Entity'):
        idx = self.status_list.index(entity)
        self.status_list.pop(idx)

    def has_entity(self, entity: 'Entity'):
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

    def clear(self, game:'GeniusGame'):
        self.weapon_card = None
        self.artifact_card = None
        for status in self.status_list:
            status.on_destroy(game)
            del(status)
        self.status_list = []
class ActiveZone:
    '''
        全队战斗状态区
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.player = player
        self.space: List[Combat_Status] = []
        self.shield: List[Combat_Shield] = []


    def remove_entity(self, entity: 'Entity'):
        if isinstance(entity, Combat_Shield):
            idx = self.shield.index(entity)
            self.shield.pop(idx)
        else:
            idx = self.space.index(entity)
            self.space.pop(idx)

    def destroy(self, entity: 'Entity'):
        for idx, exist in enumerate(self.space):
            if entity.name == exist.name:
                self.space.pop(idx)

    def has_status(self, entity: 'Entity'):
        # entity here is the class, not the instace
        # Check whether a kind of entity already exists in self.character_zone.status_list.
        # If exists, return the status instance in the list to let the caller know and just use entity.update.
        # If not, return None to let the caller know and use add_entity.
        for exist in self.space:
            if isinstance(exist, entity):
                return exist
        return None

    def has_shield(self, entity: 'Entity'):
        # entity here is the class, not the instace
        # Check whether a kind of entity already exists in self.character_zone.status_list.
        # If exists, return the status instance in the list to let the caller know and just use entity.update.
        # If not, return None to let the caller know and use add_entity.
        for exist in self.shield:
            if isinstance(exist, entity):
                return exist
        return None

    def add_entity(self, entity: 'Entity'):
        # When using add_entity, please make sure that the same kind of entity is not exisits in the list.
        if isinstance(entity, Combat_Shield):
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
        if idx == []:
            return []
        if type(idx) == int:
            idx = [idx]
        idx.sort(reverse=True)
        return [self.card.pop(i) for i in idx]

    def use(self, idx: int):
        return self.card.pop(idx)

    def add(self, cards: List['ActionCard']):
        if cards == []:
            return
        for card in cards:
            if len(self.card)>= MAX_HANDCARD:
                break
            self.card.append(card)
            self.card = sorted(self.card, key=lambda card: card.id)

    def num(self):
        return len(self.card)

    def has_card(self, card_class): # Check card_class
        for card in self.card:
            if isinstance(card, card_class):
                return card
        return None

    def remove_name(self, card_class):
        id = 0
        while (id < len(self.card)):
            if isinstance(self.card[id], card_class):
                self.card.pop(id)
            else:
                id += 1
