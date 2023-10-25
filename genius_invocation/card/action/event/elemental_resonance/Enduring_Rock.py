from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.status import Combat_Status, Combat_Shield
from genius_invocation.utils import *

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Enduring_Rock_Entity(Combat_Status):
    id: int = 331602
    name: str = "Enduring_Rock"
    name_ch = "坚定之岩"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
        self.is_trigger = False
        self.from_player = from_player

    def after_any_action(self, game: 'GeniusGame'):
        if self.is_trigger == True:
            combat_shield = self.from_player.team_combat_status.has_shield(Combat_Shield)
            print(combat_shield)
            if combat_shield is not None:
                combat_shield.current_usage += 3
            if self.current_usage <=0:
                self.on_destroy(game)
        else:
            return

    def after_takes_dmg(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == get_active_character(game, self.from_player.index) or game.current_damage.damage_from in get_my_standby_character(game):
            if game.current_damage.main_damage_element == ElementType.GEO:
                self.is_trigger = True
                self.current_usage -= 1
            else:
                return

    def on_end(self, game: 'GeniusGame'):
        self.current_usage = 0
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_TAKES_DMG, ZoneType.ACTIVE_ZONE, self.after_takes_dmg),
            (EventType.AFTER_ANY_ACTION, ZoneType.ACTIVE_ZONE, self.after_any_action),
            (EventType.BEGIN_ROLL_PHASE, ZoneType.ACTIVE_ZONE, self.on_end)
        ]

class Enduring_Rock(ActionCard):
    id: int = 331602
    name: str = "Enduring_Rock"
    name_ch = "坚定之岩"
    elment = ElementType.GEO
    cost_num = 1
    card_type = ActionCardType.EVENT_ELEMENTAL_RESONANCE
    cost_type = CostType.GEO

    def __init__(self) -> None:
        super().__init__()
        self.elemental_resonance_entity = Enduring_Rock_Entity

    def on_played(self, game: 'GeniusGame') -> None:
        target_player = game.active_player
        target_player.team_combat_status.add_entity(self.elemental_resonance_entity(game, from_player=game.active_player, from_character=None))