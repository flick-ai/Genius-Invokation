from genius_invocation.utils import *
from genius_invocation.card.action.equipment.specialskill.base import SpecialSkillCard
from genius_invocation.entity.status import SpecialSkill, Shield
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class TepetlisaurusEntity(SpecialSkill):
    name: str = "Tepetlisaurus"
    name_ch = "特佩利龙"
    id = "313004s1"
    cost = [{'cost_num': 2, 'cost_type': CostType.BLACK}]
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, card = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2

    def on_call(self, game: 'GeniusGame') -> None:
        super().on_call(game)
        self.from_player.get_card(num=2)
        num = 0
        for card in self.from_player.hand_zone.card:
            card_name = card.name
            if card_name not in self.from_player.card_zone.card_name:
                num += 1
        self.from_character.character_zone.add_entity(Shield(
            game, self.from_player, self.from_character, usage=num,
        ))
        game.manager.invoke(EventType.AFTER_USE_SPECIAL, game)



class Tepetlisaurus(SpecialSkillCard):
    id: int = 313004
    name: str = "Koholasaurus"
    name_ch = "嵴锋龙"
    time: float = 5.1
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = TepetlisaurusEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
