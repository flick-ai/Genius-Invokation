from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Opera_Epiclese_Entity(Support):
    id: int = 322017
    name = 'Opera Epiclese'
    name_ch = '欧庇克莱歌剧院'
    max_usage = 3
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage
        self.use_round = -1

    def calculate_equipment_cost(self, game: 'GeniusGame', player: 'GeniusPlayer'):
        sum_cost = 0
        for character in player.character_list:
            if character.character_zone.artifact_card != None:
                sum_cost += character.character_zone.artifact_card.count_cost()
            if character.character_zone.weapon_card != None:
                sum_cost += character.character_zone.weapon_card.count_cost()
            if character.character_zone.talent_card != None:
                sum_cost += character.character_zone.talent_card.count_cost()
        return sum_cost

    def on_begin(self, game:'GeniusGame'):
        if self.use_round != game.round:
            if game.active_player_index == self.from_player.index:
                my_cost = self.calculate_equipment_cost(game, self.from_player)
                opponent_cost = self.calculate_equipment_cost(game, get_opponent(game))
                if my_cost >= opponent_cost:
                    self.use_round = game.round
                    element_dice = ElementToDice[get_my_active_character(game).element]
                    self.from_player.dice_zone.add([element_dice.value])
                    self.usage -= 1
                    if self.usage == 0:
                        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEFORE_ANY_ACTION, ZoneType.SUPPORT_ZONE, self.on_begin)
        ]
    def show(self):
        return str(self.usage)

class Opera_Epiclese(SupportCard):
    id: int = 321017
    name: str = 'Opera Epiclese'
    name_ch = '欧庇克莱歌剧院'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Opera_Epiclese_Entity(game, from_player=game.active_player)
        super().on_played(game)