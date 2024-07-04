from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.status import Status
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Machine_Assembly_Line_Entity(Status):
    name: str = 'Machine Assembly Line'
    name_ch = '机关铸成之链'
    max_count = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.battlereadiness = 0

    def on_damage(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_damage.damage_to == get_my_active_character(game):
                self.prohibition = min(self.max_count, self.battlereadiness+1)

    def on_heal(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_heal.heal_to_character == get_my_active_character(game):
                self.prohibition = min(self.max_count, self.battlereadiness+1)

    def on_end(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if not game.from_character.is_active:
                self.from_player.change_to_id(self.from_character.index)

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type in [ActionCardType.EQUIPMENT_ARTIFACT,
                                              ActionCard.EQUIPMENT_WEAPON]:
                if game.current_dice.origin_cost[0] <= self.transmutation_material:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] = 0
                        return True
        return False

    def on_use(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.battlereadiness = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.ACTIVE_ZONE, self.on_damage),
            (EventType.AFTER_HEAL, ZoneType.ACTIVE_ZONE, self.on_heal),
            (EventType.CALCULATE_DICE, ZoneType.ACTIVE_ZONE, self.on_calculate),
            (EventType.ON_PLAY_CARD, ZoneType.ACTIVE_ZONE, self.on_use),
        ]


class Machine_Assembly_Line(ActionCard):
    id: int = 332028
    name: str = 'Machine Assembly Line'
    name_ch = '机关铸成之链'
    time = 4.4
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        target = game.current_action.target_idx
        game.active_player.character_list[target].character_zone.add_entity(
            Machine_Assembly_Line_Entity(game, game.active_player, game.active_player.character_list[target])
        )

    def find_target(self, game: 'GeniusGame'):
        target = []
        for idx, character in enumerate(game.active_player.character_list):
            target.append(idx+2)
        return target
