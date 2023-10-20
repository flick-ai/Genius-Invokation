from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Chang_the_Ninth_Entity(Support):
    id: int = 322009
    name = 'Chang the Ninth'
    max_usage = -1
    max_count = 3
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.is_calculate = False
        self.inspiration = 0

    def on_damage(self, game:'GeniusGame'):
        damage = game.current_damage
        if damage.main_damage_element == ElementType.PHYSICAL:
            self.is_calculate =True
        elif damage.reaction != None:
            self.is_calculate =True
        elif damage.main_damage_element == ElementType.PIERCING or damage.piercing_damage > 0:
            self.is_calculate =True

    def on_skill(self, game:'GeniusGame'):
        self.is_calculate = False

    def on_after_skill(self, game:'GeniusGame'):
        if self.is_calculate:
            self.is_calculate = False
            self.inspiration += 1
            if self.inspiration == self.max_count:
                self.from_player.get_card(num=2)
                self.on_destroy(game)
        
    def update_listener_list(self):
        self.listeners = [
            (EventType.EXCUTE_DAMAGE, ZoneType.SUPPORT_ZONE, self.on_damage),
            (EventType.BEFORE_ANY_ACTION, ZoneType.SUPPORT_ZONE, self.on_skill),
            (EventType.AFTER_USE_SKILL, ZoneType.SUPPORT_ZONE, self.on_after_skill),
        ]
    
    def show(self):
        return str(self.inspiration)


class Chang_the_Ninth(SupportCard):
    '''
        常九爷
    '''
    id: int = 322009
    name: str = 'Chang the Ninth'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Chang_the_Ninth_Entity(game, from_player=game.active_player)
        super().on_played(game)
