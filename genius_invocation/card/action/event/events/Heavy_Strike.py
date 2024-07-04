from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
from genius_invocation.entity.status import Status
class Heavy_Strike(ActionCard):
    id: int = 332018
    name: str = 'Heavy Strike'
    name_ch = '重攻击'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        act_char = get_my_active_character(game)
        if act_char.character_zone.has_entity(Status_of_Heavy_Strike) is None:
            status = Status_of_Heavy_Strike(game, act_char.from_player, act_char)
            act_char.character_zone.add_entity(status)

class Status_of_Heavy_Strike(Status):
    name = 'Heavy Strike'
    name_ch = '重攻击'
    time = 3.7
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
        self.max_usage = 1
        self.usage = 1

    def on_begin_phase(self, game:'GeniusGame'):
        self.on_destroy(game)

    def om_dmg_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
            if game.current_damage.damage_from == self.from_character:
                game.current_damage.main_damage += 1
                if game.current_damage.is_charged_attack:
                    game.current_damage.main_damage += 1

                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.om_dmg_add),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin_phase)
        ]

    def find_target(game:'GeniusGame'):
        return [game.active_player.active_idx+2]