from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.status import Combat_Status

from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class  Stone_and_Contracts_Entity(Combat_Status):
    id: int = 33180231
    name: str = 'Stone and Contracts'
    name_ch = '岩与契约'
    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
    
    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.from_player.dice_zone.add([DiceType.OMNI.value,DiceType.OMNI.value,DiceType.OMNI.value])
            self.on_destroy(self)
        
    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.ACTIVE_ZONE, self.on_begin),
        ]
    

        
class Stone_and_Contracts(ActionCard):
    id: int = 331802
    name: str = 'Stone and Contracts'
    name_ch = '岩与契约'
    time = 3.7
    country = CountryType.LIYUE
    cost_num = 3
    cost_type = CostType.BLACK
    card_type = ActionCardType.EVENT_COUNTRY

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        if game.active_player.team_combat_status.has_status(Stone_and_Contracts_Entity):
            return
        else:
            game.active_player.team_combat_status.add_entity(Stone_and_Contracts_Entity(
                game,
                from_player=game.active_player,
                from_character=None
            ))

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.3] = "事件牌「岩与契约」新增效果：“下回合行动阶段开始时：抓1张牌”"
        return log