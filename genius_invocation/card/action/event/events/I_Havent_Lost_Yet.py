from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Combat_Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class I_Havent_Lost_Yet(ActionCard):
    id: int = 332005
    name: str = "I Haven't Lost Yet!"
    name_ch = '本大爷还没有输！'
    cost_num = 0
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        game.active_player.team_combat_status.add_entity(Not_Loss(game, game.active_player))
        active_char = get_my_active_character(game)
        if active_char.power < active_char.max_power:
            active_char.power += 1
        game.active_player.dice_zone.add([DiceType.OMNI.value])


    def find_target(self, game: 'GeniusGame'):
        if game.active_player.last_die_round == game.round :
            if game.active_player.team_combat_status.has_status(Not_Loss) is None:
                return [1]
        return []

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.0] = "调整了事件牌「本大爷还没有输」的效果：现在该事件牌每回合限制使用1次"
        return log

class Not_Loss(Combat_Status):
    name = 'No Loss AGAIN!'
    name_ch = '本大爷不能再输了!'
    id = 33200531
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
    
    def on_begin(self, game: 'GeniusGame'):
        self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.ACTIVE_ZONE, self.on_begin)
        ]

