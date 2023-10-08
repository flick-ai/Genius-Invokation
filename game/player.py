from card import *

class GeniusPlayer:
    def __init__(self, deck) -> None:
        # 获取基本的牌组信息
        self.id = deck.id
        self.character_card = deck.character
        self.hand_card = deck.card

        # 环境中的基本状态
        self.dice_zone: None
        self.card_zone: None
        self.support_zone: None
        self.summons_zone: None
        self.card_zone: None
        self.hand_zone: None
        self.character_zone: None
        self.activate_satets: None

    def init_player(self):
        pass
