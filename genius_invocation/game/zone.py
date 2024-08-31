from typing import List, TYPE_CHECKING, Dict, Union, Optional
import numpy as np
from genius_invocation.utils import *
from copy import deepcopy
from genius_invocation.card.action import *
from genius_invocation.entity.status import Status, Shield, Combat_Shield, Weapon, Artifact, Combat_Status, SpecialSkill
from genius_invocation.card.character.characters.Keqing import Lightning_Stiletto

import random
import copy

if TYPE_CHECKING:
    from genius_invocation.entity.entity import Entity
    from genius_invocation.game.player import GeniusPlayer
    from genius_invocation.entity.summon import Summon
    from genius_invocation.entity.support import Support

    from genius_invocation.entity.character import Character

class Switch:
    def __init__(self, from_character, to_character, swicth_type) -> None:
        self.from_player = to_character.from_player
        self.from_character: 'Character' = from_character
        self.to_character: 'Character' = to_character
        self.type = swicth_type

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
        self.from_player = player
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
        for character in self.from_player.character_list:
            if character.is_alive:
                for element in character.get_element():
                    sort_map[ElementToDice[element].value] += 200
                # sort_map[ElementToDice[character.element].value] += 200
                # if character.id == 2501:
                #     # 剑鬼特判
                #     sort_map[DiceType.CRYO.value] += 200

        # 数量多优先
        sum_dice = self.space.sum(axis=0)[:-1]
        for i in range(DICENUM):
            sort_map[i] += 10 * sum_dice[i]
        return sort_map

    def add(self, dices: List):
        '''
            获取骰子
        '''
        if dices == []:
            return
        for i in range(len(dices)):
            self.from_player.game.current_player = self.from_player
            self.from_player.game.manager.invoke(EventType.ON_GET_DICE, self.from_player.game)
            self.from_player.game.current_player = None

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
        self.from_player = player
        game.random.shuffle(self.card)

    def invoke_get_card(self, num):
        '''
            触发获取牌事件
        '''
        self.from_player.game.current_get_card = GetCard(from_player=self.from_player, num=num)
        self.from_player.game.manager.invoke(EventType.ON_GET_CARD, self.from_player.game)
        self.from_player.game.current_get_card = None

    def find_card(self, card_type: 'ActionCardType', num=1, invoke=True, random_choice=False):
        '''
            检索并获取特定类型的牌
            默认取自顶向下前几张符合条件的牌
            若random_choice=True, 则为随机选取。
        '''
        get_list = []
        idx_list = []
        for idx, card in enumerate(reversed(self.card)):
            if card.card_type == card_type:
                get_list.append(card)
                idx_list.append(len(self.card) - idx -1)
                if num > 0 and not random_choice:
                    if len(get_list) == num:
                        break
        if not random_choice:
            for idx in idx_list:
                self.card.pop(idx)
        else:
            index_of_condidates = self.from_player.game.random.choice(len(idx_list), num, replace=False)
            # idx_choice = self.from_player.game.random.choice(idx_list, num, replace=False)
            idx_choice = np.array(idx_list)[index_of_condidates].tolist()
            get_list = np.array(get_list)[index_of_condidates].tolist()
            for idx in idx_choice:
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
            if self.num() == 0:
                break
            get_list.append(self.card.pop())

        if invoke and len(get_list) > 0:
            self.invoke_get_card(len(get_list))
        return get_list

    def return_card(self, card_list: List):
        '''
            将牌放回牌堆
        '''
        for card in card_list:
            idx = self.from_player.game.random.randint(0, self.num()+1)
            card.zone = self
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
        num = self.num()+len(card_list) if num == -1 else num
        if type(card_list) != List:
            card_list = [card_list]

        insert_indices = random.sample(range(self.num()+len(card_list)-num,
                                             self.num()+len(card_list)), len(card_list))
        insert_indices.sort()
        for index in insert_indices:
            card = card_list.pop()
            card.zone = self
            self.card.insert(index, card)

    def return_card_bottom(self, card_list: List):
        '''
            将牌放回牌堆底
        '''
        for card in card_list:
            card.zone = self
            self.card.insert(0, card)

    def discard_card(self, idx):
        '''
            舍弃牌
        '''
        card: ActionCard = self.card.pop(idx)
        card.on_discard(self.from_player.game)
        card.zone = None

        self.from_player.tune_or_discard_cards.append(card)
        self.from_player.round_discard_cards += 1
        self.from_player.game.invoke(EventType.ON_DISCARD_CARD, self.from_player.game)
        return card

    def num(self):
        return len(self.card)

    def show(self)->List[ActionCard]:
        return self.card

class SummonZone:
    '''
        召唤物区
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.space: List['Summon'] = []
        self.from_player=player

    def remove(self, entity):
        idx = self.space.index(entity)
        self.space.pop(idx)
        self.from_player.game.manager.invoke(EventType.ON_SUMMON_REMOVE, self.from_player.game)

    def destroy(self, idx):
        self.space[idx].on_destroy(self.from_player.game)
        self.space.pop(idx)
        self.from_player.game.manager.invoke(EventType.ON_SUMMON_REMOVE, self.from_player.game)

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

    def add_entity(self, entity: 'Summon', independent=False, replace_update=False, **kwargs):
        if independent or self.has_entity(entity.__class__) is None:
            if not self.check_full():
                self.space.append(entity)
            else:
                entity.on_destroy(self.from_player.game)
        else:
            self.has_entity(entity.__class__).update(**kwargs)
            if replace_update:
                old_entity = self.has_entity(entity.__class__)
                new_entity = copy.deepcopy(old_entity)
                old_entity.on_destroy(self.from_player.game)
                self.space.appendd(new_entity)

    def num(self):
        return len(self.space)

    def show(self)->List['Summon']:
        return self.space
class SupportZone:
    '''
        支援区
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.from_player = player
        self.space: List['Support'] = []
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
        self.from_player.game.manager.invoke(EventType.ON_SUPPORT_REMOVE, self.from_player.game)

    def destroy_by_idx(self, idx):
        self.space[idx].on_destroy(self.from_player.game)

    def add_entity(self, entity, idx, **kwargs):
        if self.check_full():
            # 如果支援区已经满了
            self.space[idx].on_destroy(self.from_player.game)
        self.space.append(entity)

    def add_entity_by_name(self, entity_name, idx, **kwargs):
        entity = eval(entity_name)().entity(self.from_player.game, self.from_player)
        self.add_entity(entity, self.num(), **kwargs)

    def num(self):
        return len(self.space)

    def show(self)->List['Support']:
        return self.space


class CharacterZone:
    '''
        单个角色状态区, 包括角色牌、装备区、角色状态
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.weapon_card: Weapon = None
        self.artifact_card: Artifact = None
        self.talent_card: TalentCard = None
        self.special_skill: SpecialSkill = None
        self.status_list: List['Status'] = [] # Including status from weapon and artifact
        self.immune_list = None

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

    def check_immune(self, entity: 'Status'):
        if self.immune_list is None:
            return False
        for immune in self.immune_list:
            if isinstance(entity, immune):
                return True
        return False


    def add_entity(self, entity: 'Status', independent=False, replace_update=False, **kwargs):
        # If replace_update is True, the entity will be copy after update, and the origin entity will be destroy and add the new entity at the end of the status list.
        if self.check_immune(entity):
            return
        if independent or self.has_entity(entity.__class__) is None:
            self.status_list.append(entity)
        else:
            self.has_entity(entity.__class__).update(**kwargs)
            if replace_update:
                old_entity = self.has_entity(entity.__class__)
                new_entity = old_entity.copy(self.from_player.game)
                old_entity.on_destroy(self.from_player.game)
                self.status_list.append(new_entity)


    def clear(self, game:'GeniusGame'):
        if self.weapon_card is not None:
            self.weapon_card.on_destroy(game)
            self.weapon_card = None
        if self.artifact_card is not None:
            self.artifact_card.on_destroy(game)
            self.artifact_card = None
        if self.talent_card is not None:
            self.talent_card.on_destroy(game)
            self.talent_card = None
        if self.special_skill is not None:
            self.special_skill.on_destroy(game)
            self.special_skill = None
        for status in self.status_list:
            status.on_destroy(game)
            # del(status)
        self.status_list = []

    def show_equip_card(self)->Dict[str, Optional[EquipmentCard]]:
        '''
        Return a dict to show THE CARD of equipments, None for no such an equipment
        {
            'weapon_card': WEAPON_CARD,
            'artifact_card': ARTIFACT_CARD,
            'talent_card': TALENT_CARD
        }
        '''
        return {
            'weapon_card': self.weapon_card.weapon_card if self.weapon_card is not None else None,
            'artifact_card': self.artifact_card.artifact_card if self.artifact_card is not None else None,
            'talent_card': self.talent_card
        }

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

    def add_entity(self, entity: 'Entity', independent=False, replace_update=False, **kwargs):
        # When using add_entity, please make sure that the same kind of entity is not exisits in the list.
        if isinstance(entity, Combat_Shield):
            if self.has_shield(entity.__class__) is None or independent:
                self.shield.append(entity)
            else:
                self.has_shield(entity.__class__).update(**kwargs)
                if replace_update:
                    old_entity = self.has_shield(entity.__class__)
                    new_entity = copy.deepcopy(old_entity)
                    old_entity.on_destroy(self.from_player.game)
                    self.shield.appendd(new_entity)
        else:
            if self.has_status(entity.__class__) is None or independent:
                self.space.append(entity)
            else:
                self.has_status(entity.__class__).update(**kwargs)
                if replace_update:
                    old_entity = self.has_status(entity.__class__)
                    new_entity = copy.deepcopy(old_entity)
                    old_entity.on_destroy(self.from_player.game)
                    self.space.appendd(new_entity)

    def show(self)-> Dict[str, List['Entity']]:
        '''
        Return a dict to show combat status and shield:
        {
            'Combat_Status': [],
            'Combat_Shield': []
        }
        '''
        return {
            'Combat_Status': self.space,
            'Combat_Shield': self.shield
        }

class HandZone:
    '''
        手牌区
    '''
    def __init__(self, game: 'GeniusGame', player: 'GeniusPlayer') -> None:
        self.card = []
        self.from_player = player

    def remove(self, idx: List):
        if idx == []:
            return []
        if type(idx) == int:
            idx = [idx]
        idx.sort(reverse=True)

        remove_list = []
        for i in idx:
            card = self.card.pop(i)
            card.zone = None
            remove_list.append(card)
        return remove_list

    def use(self, idx: int):
        card = self.card.pop(idx)
        card.zone = None
        return card

    def add(self, cards: List['ActionCard']):
        if cards == []:
            return
        for card in cards:
            if len(self.card)>= MAX_HANDCARD:
                break
            self.card.append(card)
            card.zone = self
            self.card = sorted(self.card, key=lambda card: card.id)

    def add_card_by_name(self, card_names):
        '''
            通过名字获取牌
        '''
        for card_name in card_names:
            self.add([eval(card_name)()])

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
        if idx == None:
            return None
        card: ActionCard = self.card.pop(idx)
        card.zone = None
        card.on_discard(self.from_player.game)

        self.from_player.tune_or_discard_cards.append(card)
        self.from_player.round_discard_cards += 1
        self.from_player.game.invoke(EventType.ON_DISCARD_CARD, self.from_player.game)
        return card

    def discard_card_by_name(self, name, max_num=100):
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

    def show(self)->List:
        '''Return the List of Hand Cards'''
        return self.card