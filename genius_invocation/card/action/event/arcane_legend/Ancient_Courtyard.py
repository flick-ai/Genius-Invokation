from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Ancient_Courtyard_Entity(Status):
    id: int = 330001
    name = "Ancien Courtyard"
    name_ch = "旧时庭园"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
    
    def on_play(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_card.card_type == ActionCardType.EQUIPMENT_ARTIFACT or game.current_card.card_type == ActionCardType.EQUIPMENT_WEAPON:
                if game.current_dice.cost[0]['cost_num'] > 0:
                    game.current_dice.cost[0]['cost_num'] = max(0, game.current_dice.cost[0]['cost_num']-2)
                    self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_PLAY_CARD, ZoneType.ACTIVE_ZONE, self.on_play),
        ]


class Ancient_Courtyard(ActionCard):
    id: int = 330001
    name: name = "Ancien Courtyard"
    name_ch = "旧时庭园"
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT_ARCANE_LEGEND
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        game.active_player.team_combat_status.add_entity(Ancient_Courtyard_Entity(
            game,
            from_player=game.active_player,
            from_character=None
        ))
    
    def find_target(self, game: 'GeniusGame'):
        if game.active_player.play_arcane_legend:
            return []
        has_equipment = False
        for character in game.active_player.character_list:
            if character.character_zone.weapon_card != None:
                has_equipment = True
                break
            if character.character_zone.artifact_card != None:
                has_equipment = True
                break
        if has_equipment:
            return [1]
        else:
            return []
