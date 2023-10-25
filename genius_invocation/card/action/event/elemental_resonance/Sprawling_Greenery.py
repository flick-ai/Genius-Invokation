from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.status import Combat_Status, Dendro_Core, Catalyzing_Feild
from genius_invocation.entity.summon import Burning_Flame
from genius_invocation.utils import *

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Sprawling_Greenery_Entity(Combat_Status):
    id: int = 331702
    name: str = "Sprawling_Greenery"
    name_ch = "蔓生之草"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
        self.from_player = from_player

    def on_damage_add_after_reaction(self, game: 'GeniusGame'):
        if game.current_damage.damage_to.from_player != self.from_player and game.current_damage.reaction is not None:
            game.current_damage.main_damage += 2
            self.current_usage -=1
            if self.current_usage <=0:
                self.on_destroy(game)
        else:
            return

    def on_end(self, game: 'GeniusGame'):
        self.current_usage = 0
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD_AFTER_REACTION, ZoneType.ACTIVE_ZONE, self.on_damage_add_after_reaction),
            (EventType.BEGIN_ROLL_PHASE, ZoneType.ACTIVE_ZONE, self.on_end)
        ]

class Sprawling_Greenery(ActionCard):
    id: int = 331702
    name: str = "Sprawling_Greenery"
    name_ch = "蔓生之草"
    element = ElementType.DENDRO
    cost_num = 1
    card_type = ActionCardType.EVENT_ELEMENTAL_RESONANCE
    cost_type = CostType.DENDRO

    def __init__(self) -> None:
        super().__init__()
        self.elemental_resonance_entity = Sprawling_Greenery_Entity

    def on_played(self, game: 'GeniusGame') -> None:
        target_player = game.active_player
        if target_player.team_combat_status.has_status(self.elemental_resonance_entity):
            pass
        else:
            target_player.team_combat_status.add_entity(self.elemental_resonance_entity(game, from_player=game.active_player, from_character=None))
        dendro_core_status =  target_player.team_combat_status.has_status(Dendro_Core)
        catalyzing_field_status =  target_player.team_combat_status.has_status(Catalyzing_Feild)
        burning_flame_status = target_player.summon_zone.has_entity(Burning_Flame)
        if dendro_core_status is not None:
            dendro_core_status.add_one_usage()
        if catalyzing_field_status is not None:
            catalyzing_field_status.add_one_usage()
        if burning_flame_status is not None:
            burning_flame_status.add_usage(game, count=1)