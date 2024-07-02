from typing import List, TYPE_CHECKING, Dict, Union
import numpy as np
from genius_invocation.utils import *
from copy import deepcopy
from genius_invocation.card.action import *
from genius_invocation.entity.status import Status, Shield, Combat_Shield, Weapon, Artifact, Combat_Status
from genius_invocation.card.character.characters.Keqing import Lightning_Stiletto

import random

if TYPE_CHECKING:
    from genius_invocation.entity.entity import Entity
    from genius_invocation.game.player import GeniusPlayer
    from genius_invocation.entity.summon import Summon
    from genius_invocation.entity.support import Support

    from genius_invocation.entity.character import Character

class GetCard:
    '''
        获取牌的维护类
    '''
    def __init__(self, from_player, num) -> None:
        self.from_player = from_player
        self.num = num

class Dice:
    '''
        计算骰子的维护类
    '''
    def __init__(self, from_player, from_character, use_type, cost, to_character=None, name=None) -> None:
        self.cost: List[Dict[str, Union[int, CostType]]] = cost # 'cost_num', 'cost_type'
        self.from_player = from_player
        self.from_character: Character = from_character
        self.to_character: Character = to_character
        self.use_type = use_type
        self.origin_cost = cost
        self.name = name

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
        self.game = game
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
                for element in character.get_element():
                    sort_map[ElementToDice[element].value] += 200
                # sort_map[ElementToDice[character.element].value] += 200
                # if character.id == 2501:
                #     # 剑鬼特判
                #     sort_map[DiceType.CRYO.value] += 200

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
            if dice != DiceType.OMNI.value:
                self.space[self.dice_num][-1] = dice
                self.space[self.dice_num][dice] = 1
            else:
                self.space[self.dice_num][-1] = dice
                for i in range(DICENUM):
                    self.space[self.dice_num][i] = 1
            self.dice_num += 1
            if self.dice_num == MAX_DICE:
                break
        self.sort_dice()

    def delete(self, idx):
        self.space[idx][-1] = -1
        for i in range(DICENUM):
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

        if dice.use_type == SwitchType.ELEMENTAL_RESONANCE:
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
            cost = DiceType(-cost_type)
            for dice in choose_dice:
                if DiceType(dice) == cost or DiceType(dice)==DiceType.OMNI:
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

def evenly_insert(source_list, insert_list):
    result = []
    len_source = len(source_list)
    len_insert = len(insert_list)
    avg_interval = len_source // (len_insert + 1)  # 平均间隔
    remainder = len_source % (len_insert + 1)  # 余数，用于处理不能整除的情况
    insert_index = avg_interval

    for i, item in enumerate(source_list):
        result.append(item)
        if i + 1 == insert_index:
            if insert_list:  # 检查插入列表是否为空
                result.extend(insert_list.pop(0))
                # 更新插入位置
                insert_index += avg_interval
                if remainder:
                    insert_index += 1
                    remainder -= 1
    return result

def random_insert(source_list, insert_list):
    result = source_list.copy()
    insert_indices = random.sample(range(len(source_list)+1), len(insert_list))
    insert_indices.sort(reverse=True)  # 对插入位置进行排序，确保从后向前插入

    for index in insert_indices:
        result.insert(index, insert_list.pop())

    return result

class CardZone:
    '''
        牌堆区,
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer', card: List) -> None:
        '''
            牌堆结构为一个随机过的固定顺序列表
        '''
        self.card: List['ActionCard'] = []
        self.card_name = []
        self.card_type = []
        for card_name in card:
            self.card.append(eval(card_name)())
            if card_name not in self.card_name:
                self.card_name.append(card_name)
                self.card_type.append(self.card[-1].card_type)
        # 随机固定牌序
        self.game = game
        self.player = player
        game.random.shuffle(self.card)

    def invoke_get_card(self, num):
        '''
            触发获取牌事件
        '''
        self.game.current_get_card = GetCard(from_player=self.player, num=num)
        self.game.manager.invoke(EventType.ON_GET_CARD, self.game)
        self.game.current_get_card = None

    def find_card(self, card_type: 'ActionCardType', num=1, invoke=True):
        '''
            检索并获取特定类型的牌
        '''
        get_list = []
        idx_list = []
        for idx, card in enumerate(reversed(self.card)):
            if card.card_type == card_type:
                get_list.append(card)
                idx_list.append(len(self.card) - idx -1)
                if num > 0:
                    if len(get_list) == num:
                        break
        for idx in idx_list:
            self.card.pop(idx)

        if invoke:
            self.invoke_get_card(num)
        return get_list

    def find_card_by_name(self, card_name: str, num=1, invoke=True):
        '''
            检索并获取特定名称的牌
        '''
        get_list = []
        idx_list = []
        for idx, card in enumerate(reversed(self.card)):
            if card.name == card_name:
                get_list.append(card)
                idx_list.append(len(self.card) - idx -1)
                if len(get_list) == num:
                    break
        for idx in idx_list:
            self.card.pop(idx)

        if invoke:
            self.invoke_get_card(num)
        return get_list


    def random_find_card(self, card_type: 'ActionCardType', num=1):
        '''
            随机检索并获取特定类型的牌
        '''
        get_list = []
        idx_list = []
        for idx, card in enumerate(reversed(self.card)):
            if card.card_type == card_type:
                get_list.append(card)
                idx_list.append(len(self.card) - idx -1)
        get_idx = random.sample(idx_list, num)
        for idx in get_idx:
            get_list.append(self.card.pop(idx))

        self.invoke_get_card(num)
        return get_list

    def get_card(self, num, invoke=True):
        '''
            随机获取牌
        '''
        get_list = []
        for i in range(num):
            get_list.append(self.card.pop())

        if invoke:
            self.invoke_get_card(num)
        return get_list

    def return_card(self, card_list: List):
        '''
            将牌放回牌堆
        '''
        for card in card_list:
            idx = self.game.random.randint(0, self.num()+1)
            self.card.insert(idx, card)

    def insert_evenly(self, card_list: List):
        '''
            将牌平均放回牌堆
        '''
        result = evenly_insert(self.card, card_list)
        self.card = result


    def insert_randomly(self, card_list: List, num=-1):
        '''
            从牌堆顶的指定数量牌中随机插入牌
        '''
        num = self.num() if num == -1 else num
        if type(card_list) != List:
            card_list = [card_list]

        insert_indices = random.sample(range(0, num+len(card_list)), len(card_list))
        insert_indices.sort()
        for index in insert_indices:
            self.card.insert(index, card_list.pop())

    def discard_card(self, idx):
        '''
            舍弃牌
        '''
        card: ActionCard = self.card.pop(idx)
        card.on_discard(self.game)

        self.player.tunr_or_discard_cards.append(card)
        self.player.round_discard_cards += 1
        self.game.invoke(EventType.ON_DISCARD_CARD, self.game)
        return card

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

    def add_entity(self, entity: 'Summon', independent=False, **kwargs):
        if independent or self.has_entity(entity.__class__) is None:
            if not self.check_full():
                self.space.append(entity)
            else:
                entity.on_destroy(self.game)
        else:
            self.has_entity(entity.__class__).update(**kwargs)

    def num(self):
        return len(self.space)

class SupportZone:
    '''
        支援区
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.game = game
        self.space: List[Support] = []
        self.distroy_count = 0

    def check_full(self):
        return len(self.space) == MAX_SUPPORT

    def has_entity(self, entity: 'Support'):
        for support in self.space:
            if isinstance(support, entity):
                return support
        return None

    def destroy(self, entity: 'Support'):
        idx = self.space.index(entity)
        self.space.pop(idx)
        self.distroy_count += 1
        self.game.manager.invoke(EventType.ON_SUPPORT_REMOVE, self.game)

    def destroy_by_idx(self, idx):
        self.space[idx].on_destroy(self.game)

    def add_entity(self, entity, idx, **kwargs):
        if self.check_full():
            # 如果支援区已经满了
            self.space[idx].on_destroy(self.game)
        self.space.append(entity)


    def num(self):
        return len(self.space)


class CharacterZone:
    '''
        单个角色状态区, 包括角色牌、装备区、角色状态
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.game = game
        self.weapon_card: Weapon = None
        self.artifact_card: Artifact = None
        self.talent_card: TalentCard = None
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

    def add_entity(self, entity: 'Status', independent=False, **kwargs):
        if independent or self.has_entity(entity.__class__) is None:
            self.space.append(entity)
        else:
            self.has_entity(entity.__class__).update(**kwargs)

    def clear(self, game:'GeniusGame'):
        if self.weapon_card is not None:
            self.weapon_card.on_destroy(game)
            self.weapon_card = None
        if self.artifact_card is not None:
            self.artifact_card.on_destroy(game)
            self.artifact_card = None
        for status in self.status_list:
            status.on_destroy(game)
            # del(status)
        self.status_list = []
class ActiveZone:
    '''
        全队战斗状态区
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.game = game
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

    def add_entity(self, entity: 'Entity', independent=False, **kwargs):
        # When using add_entity, please make sure that the same kind of entity is not exisits in the list.
        if isinstance(entity, Combat_Shield):
            if self.has_shield(entity.__class__) is None or independent:
                self.shield.append(entity)
            else:
                self.has_shield(entity.__class__).update(**kwargs)
        else:
            if self.has_status(entity.__class__) is None or independent:
                self.space.append(entity)
            else:
                self.has_status(entity.__class__).update(**kwargs)

class HandZone:
    '''
        手牌区
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.card = []
        self.game = game
        self.from_player = player

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

    def add_card_by_name(self, card_names):
        '''
            通过名字获取牌
        '''
        for card_name in card_names:
            self.add(eval(card_name)())

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

    def discard_card(self, idx):
        '''
            舍弃牌
        '''
        card: ActionCard = self.card.pop(idx)
        card.on_discard(self.game)

        self.from_player.tunr_or_discard_cards.append(card)
        self.from_player.round_discard_cards += 1
        self.game.invoke(EventType.ON_DISCARD_CARD, self.game)
        return card

    def discard_card_by_name(self, name, max_num):
        '''
            通过名称舍弃牌
        '''
        cards = []
        for idx, card in enumerate(self.card):
            if card.name == name:
                cards.append(self.discard_card(idx))
                if len(cards) == max_num:
                    break
        return cards
