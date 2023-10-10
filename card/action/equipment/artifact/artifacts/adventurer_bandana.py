from utils import *
from ..base import ArtifactCard
from game.game import GeniusGame


# artifacts
class AdventurerBandana(ArtifactCard):
    '''冒险家头巾'''
    id: int = 0
    name: str = 'Adventurer\'s Bandana'
    cost_num: int = 1
    cost_type: CostType = CostType.WHITE
    max_usage: int = 3

    def __init__(self) -> None:
        super().__init__()
        # self.usages = defaultdict(int)
    
    def post_played(self, game: GeniusGame) -> None:
        pass
        # TODO: register event on_round_start
        # TODO: register event on_attack_end

    def on_round_start(self, game: GeniusGame) -> None:
        self.max_usage = 3
    
    def on_skill_end(self, game: GeniusGame) -> None:
        # check if is active player
        if game.active_player != self.player:
            return
        # check if still have usage
        if self.max_usage <= 0:
            return
        # check if is normal attack
        if game.current_action.choice_idx != 0:
            return
        self.max_usage -= 1
        # heal 1 HP