from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class WaterandJustice(ActionCard):
    id: int = 331805
    name: str = 'Water and Justice'
    name_ch = "水与正义"
    cost_num = 2
    cost_type = CostType.BLACK
    card_type = ActionCardType.EVENT_COUNTRY

    def __init__(self) -> None:
        super().__init__()

    def calculate_target_point(self,sum_point: int, max_points: List[int]):
        # 重新平均分配生命值
        target_point = []


    def on_played(self, game: 'GeniusGame'):
        sum_point = 0
        max_points = []
        target_idx = []
        for player in game.active_player.character_list:
            if player.is_alive:
                sum_point += player.health_point
                max_points.append(player.max_health_point)
                target_idx.append(player.idx)
        target_point = self.calculate_target_point(sum_point, max_points)


