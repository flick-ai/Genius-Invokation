from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Combat_Status
from genius_invocation.event.damage import Damage
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class TadaEntity(Combat_Status):
    id = 33203731
    name: str = "Tada!"
    name_ch = '噔噔！'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def on_end(self, game:'GeniusGame'):
        self.from_player.get_card(num=1)
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.ACTIVE_ZONE, self.on_end)
        ]

class Tada(ActionCard):
    id = 332037
    name: str = "Tada!"
    name_ch = '噔噔！'
    time = 4.8
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        dmg = Damage.create_damage(
            game,
            damage_type=SkillType.OTHER,
            main_damage_element=ElementType.PHYSICAL,
            main_damage=1,
            piercing_damage=0,
            damage_from=self.zone,
            damage_to=get_active_character(game, 1-self.zone.from_player.index),
        )
        game.add_damage(dmg)
        game.resolve_damage()

        zone = game.active_player.team_combat_status
        if not zone.has_status(TadaEntity):
            zone.add_entity(TadaEntity(game, game.active_player, None))

    def find_target(self, game:'GeniusGame'):
        return [1]