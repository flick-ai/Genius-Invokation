from genius_invocation.utils import *
from genius_invocation.card.action.equipment.specialskill.base import SpecialSkillCard
from genius_invocation.entity.status import SpecialSkill
from genius_invocation.event.damage import Damage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class YumkasaurusEntity(SpecialSkill):
    name: str = "Yumkasaurus"
    name_ch = "匿叶龙"
    id = "313002s1"
    cost = [{'cost_num': 2, 'cost_type': CostType.WHITE}]
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        damage = Damage(damage_type=SkillType.OTHER,
                        main_damage_element=ElementType.PHYSICAL,
                        main_damage=1,
                        piercing_damage=0,
                        damage_from=self,
                        damage_to=get_opponent_active_character(game),
                        )
        game.add_damage(damage)
        game.resolve_damage()
        opponent = get_opponent(game)
        card_id = max_count_card(opponent.hand_zone.card)
        card = opponent.hand_zone.card[card_id]
        opponent.hand_zone.remove(card_id)
        self.from_player.hand_zone.add([card])
        self.check_usage()
        game.manager.invoke(EventType.AFTER_USE_SPECIAL, game)

    def on_calculate_dice(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.from_character == self.from_character:
                if game.current_dice.use_type == SkillType.SPECIAL_SKILL:
                    if len(self.from_player.hand_zone.card) <= 2:
                        if game.current_dice.cost[0]['cost_num'] > 0:
                            game.current_dice.cost[0]['cost_num'] -= 1
                            return True
        return False

    def on_special_skill(self, game: 'GeniusGame'):
        self.on_calculate_dice(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate_dice),
            (EventType.ON_USE_SPECIAL, ZoneType.CHARACTER_ZONE, self.on_special_skill)
        ]



class Yumkasaurus(SpecialSkillCard):
    id: int = 313002
    name: str = "Yumkasaurus"
    name_ch = "匿叶龙"
    time: float = 5.0
    cost_num: int = 1
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = YumkasaurusEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
