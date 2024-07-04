from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.status import Combat_Status

from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class  Wind_and_Freedom_Entity(Combat_Status):
    id: int = 331801
    name: str = 'Wind and Freedom'
    name_ch = '风与自由'
    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
    
    def on_after_skill(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_skill.from_character == self.from_character:
                self.from_player.change_to_next_character()
    
    def on_end(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.on_destroy(self)
        
    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.on_after_skill),
            (EventType.END_PHASE, ZoneType.ACTIVE_ZONE, self.on_end)
        ]
    

        
class Wind_and_Freedom(ActionCard):
    id: int = 331801
    name: str = 'Wind and Freedom'
    name_ch = '风与自由'
    time = 3.7
    country = CountryType.MONDSTADT
    cost_num = 1
    cost_type = CostType.BLACK
    card_type = ActionCardType.EVENT_COUNTRY

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        game.active_player.team_combat_status.add_entity(Wind_and_Freedom_Entity(
            game,
            from_player=game.active_player,
            from_character=None
        ))

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.1] = "调整了事件牌「风与自由」的效果，调整后为：本回合中，我方角色使用技能后：将下一个我方后台角色切换到场上"
        log[4.3] = "调整了事件牌「风与自由」所需元素骰：所需元素骰由1个调整为0个"
        return log