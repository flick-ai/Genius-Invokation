from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.status import Combat_Status
from genius_invocation.utils import *

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Fervent_Flames_Entity(Combat_Status):
    id: int = 331302
    name: str = "Fervent_Flames"
    name_ch = "热诚之火"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
        self.from_player = from_player
    
    # def on_destroy(self, game):
    #     super().on_destroy(game)
    #     self.from_player.team_combat_status.remove_entity(self)

    def on_damage_add_after_reaction(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == get_active_character(game, self.from_player.index):
            if game.current_damage.reaction in [ElementalReactionType.Melt, 
                                                ElementalReactionType.Vaporize,
                                                ElementalReactionType.Overloaded,
                                                ElementalReactionType.Burning]:
                game.current_damage.main_damage += 3
                self.current_usage -=1
                if self.current_usage <=0:
                    self.on_destroy(game)
            elif game.current_damage.swirl_crystallize_type == ElementType.PYRO and game.current_damage.reaction in [ElementalReactionType.Crystallize, 
                                                                                                                ElementalReactionType.Swirl]:
                game.current_damage.main_damage += 3
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

class Fervent_Flames(ActionCard):
    id: int = 331302
    name: str = "Fervent_Flames"
    name_ch = "热诚之火"
    cost_num = 1
    card_type = ActionCardType.EVENT_ELEMENTAL_RESONANCE.value
    cost_type = CostType.PYRO

    def __init__(self) -> None:
        super().__init__()
        self.elemental_resonance_entity = Fervent_Flames_Entity

    def on_played(self, game: 'GeniusGame') -> None:
        target_player = game.active_player
        target_player.team_combat_status.add_entity(self.elemental_resonance_entity(game, from_player=game.active_player, from_character=None))