from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.card.action.event.base import FoodCard
from genius_invocation.entity.status import Combat_Status, Satisfy_Statue
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class NoRevie(Combat_Status):
    id: int = 33300931
    name: str = "No Revive"
    name_ch = "不能复活"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.ACTIVE_ZONE, self.on_begin)
        ]
class Teyvat_Fried_Egg(FoodCard):
    id: int = 333009
    name: str = "Teyvat Fried Egg"
    name_ch = "提瓦特煎蛋"
    time = 3.7
    cost_num = 2
    cost_type = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.food_entity = NoRevie

    def on_played(self, game: 'GeniusGame'):
        target = game.current_action.target_idx
        target_character = game.active_player.character_list[target]
        target_character.revive(game)
        target_character.heal(1, game=game)
        Satisfy_Statue(game, from_player=game.active_player, from_character=target_character)
        target_character.character_zone.add_entity(Satisfy_Statue)

        game.active_player.team_combat_status.add_entity(self.food_entity(game, from_player=game.active_player, from_character=target_character))

    def find_target(self, game: 'GeniusGame'):
        target_list = []
        status = game.active_player.team_combat_status.has_status(NoRevie)
        if status is None:
            for idx, character in enumerate(game.active_player.character_list):
                if not character.is_alive:
                    target_list.append(idx+2)
        return target_list

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.1] = "调整了事件牌「提瓦特煎蛋」所需元素骰费用：所需元素骰调整为2个相同元素骰"
        return log
