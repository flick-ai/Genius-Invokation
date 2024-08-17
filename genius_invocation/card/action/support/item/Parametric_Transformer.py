from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Parametric_Transformer_Entity(Support):
    id: int = 32300161
    name = 'Parametric Transformer'
    name_ch = '参量质变仪'
    max_usage = -1
    max_count = 3
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.qualitative_progress = 0
        self.is_calculate = False

    def on_after(self, game:'GeniusGame'):
        if self.is_calculate:
            self.qualitative_progress += 1
            if self.qualitative_progress == self.max_count:
                self.from_player.dice_zone.add(self.from_player.roll_dice(num=3, is_basic=True, is_different=True))
                self.on_destroy(game)
            self.is_calculate = False

    def on_damage(self, game:'GeniusGame'):
        damage = game.current_damage
        if damage.main_damage_element not in [ElementType.PHYSICAL, ElementType.PIERCING]:
            self.is_calculate = True

    def on_begin(self, game:'GeniusGame'):
        self.is_calculate = False

    def on_skill(self, game:'GeniusGame'):
        self.is_calculate = False

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.SUPPORT_ZONE, self.on_after),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
            (EventType.EXECUTE_DAMAGE, ZoneType.SUPPORT_ZONE, self.on_damage),
            (EventType.BEFORE_ANY_ACTION, ZoneType.SUPPORT_ZONE, self.on_skill)
        ]

    def show(self):
        return str(self.qualitative_progress)

class Parametric_Transformer(SupportCard):
    '''
        参量质变仪
    '''
    id: int = 323001
    name: str = 'Parametric Transformer'
    name_ch = '参量质变仪'
    cost_num = 2
    cost_type = CostType.BLACK
    card_type = ActionCardType.SUPPORT_ITEM

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Parametric_Transformer_Entity(game, from_player=game.active_player)
        super().on_played(game)
