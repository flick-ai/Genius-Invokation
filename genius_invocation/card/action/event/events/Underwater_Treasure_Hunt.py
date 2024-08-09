from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class Treasure_Heal(Status):
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def on_end(self, game: 'GeniusGame'):
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.FINAL_END, ZoneType.ACTIVE_ZONE, self.on_end),
        ]

class Undersea_Treasure(ActionCard):
    name: str = 'Underwater Treasure'
    name_ch = '海底宝藏'
    cost_num = 0
    cost_type = None
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        activte_character = get_my_active_character(game)
        if not activte_character.has_status(Treasure_Heal):
            activte_character.heal(1, game)
        else:
            activte_character.character_zone.add_entity(Treasure_Heal(game, game.active_player, activte_character))
        dices = game.active_player.roll_dice(num=1, is_basic=True)
        game.active_player.dice_zone.add(dices)


class Underwater_Treasure_Hunt(ActionCard):
    id: int = 332031
    name: str = 'Underwater Treasure Hunt'
    name_ch = '海中寻宝'
    time = 4.6
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()
        self.num = 6

    def on_played(self, game: 'GeniusGame'):
        cards = [Undersea_Treasure() for _ in range(6)]
        game.active_player.card_zone.insert_randomly(cards, num=-1)

    def balance_adjustment():
        log = {
            4.8:"事件牌「海中寻宝」生成的「海底宝藏」增加了使用次数限制：每个角色每回合最多受到1次来自本效果的治疗。",
        }
        return log

