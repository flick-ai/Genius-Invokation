from utils import *
from ..base import WeaponCard
from game.game import GeniusGame


# weapons
class RavenBow(WeaponCard):
    '''鸦羽弓'''
    id: int = 0
    name: str = 'Raven Bow'
    weapon_type: WeaponType = WeaponType.BOW
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        # self.usages = defaultdict(int)
    
    def post_played(self, game: GeniusGame) -> None:
        pass 
        # register on_player_activated DamageAdd
        # register on_player_deactivated remove DamageAdd
        
        

    # def on_played(self, game: GeniusGame, target: int) -> None:
    #     game.players[game.active_player].active_zone.character_list[target].weapon_card = RavenBow