from typing import List
import random
from card.action import *

class Card_Zone:
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