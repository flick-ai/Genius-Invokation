import card
from zone import Card_Zone


class GeniusPlayer:
    def __init__(self, deck) -> None:
        # 获取基本的牌组信息
        self.character_card = deck.character

        # 环境中的基本状态
        self.dice_zone: None
        self.card_zone: None
        self.support_zone: None
        self.summons_zone: None
        self.card_zone = Card_Zone(deck.action_card) # 牌库区
        self.hand_zone: None # 手牌区
        self.character_zone: None
        self.activate_satets: None

    def init_player(self):
        pass

    def take_action(self, action):
        '''
        将action信号转化为环境信号
        '''
    
    def generate_action_mask(self):
        '''
        生成action的mask
        '''
