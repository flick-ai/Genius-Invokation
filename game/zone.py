from typing import List
import random
from card.action import *

class Card_Zone:
    def __init__(self, card: List) -> None:
        self.card = []
        for card_name in card:
            self.card.append(eval(card_name)())

    def get_card(self, num):
        '''
        从牌堆中获取牌
        '''
        random.sample(self.card, num)
        

    def return_card(self, card_list: List):
        for card in card_list:
            self.card.append(card)