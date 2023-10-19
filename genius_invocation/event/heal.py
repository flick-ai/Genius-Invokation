from typing import TYPE_CHECKING
from genius_invocation.utils import *
from genius_invocation.event.Elemental_Reaction import *

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Heal:
    # 治疗基本类
    def __init__(
            self, 
            heal: int, 
            target_fn: lambda g: get_my_active_character(g, require_player_idx=True)
            ) -> None:
        '''
        heal: the amount of heal
        target_fn: the function to get the target indices of heal
            input: game
            output: tuple of (player_id, chara_id), or list of tuple of (player_id, chara_id)
        '''
        self.heal: int = heal
        self.target_fn: target_fn
        self.heals: list = []
        self.target_ids: list = []
        self.heal_sum: int = 0

    @classmethod
    def create_heal(
        cls, 
        game: 'GeniusGame', 
        heal: int, 
        target_fn):
        return cls(heal, target_fn)

    @staticmethod
    def resolve_heal(game: 'GeniusGame', heal: int, target_fn):    
        heal = Heal.create_heal(game, heal, target_fn)
        heal.cal(game)
        heal.execute(game)
        Heal.after_heal(game)
    
    @staticmethod
    def after_heal(game: 'GeniusGame'):
        game.manager.invoke('after_heal', game)

    def execute(self, game: 'GeniusGame'):
        for (player_id, chara_id), heal in zip(self.target_ids, self.heals):
            chara = game.players[player_id].active_zone.character_list[chara_id]
            chara.heal(heal)

    def cal(self, game: 'GeniusGame'):
        self.target_ids = self.target_fn(game)
        if type(self.target_ids) == tuple:
            self.target_ids = [self.target_ids]
        
        for player_id, chara_id in self.target_ids:
            chara = game.players[player_id].active_zone.character_list[chara_id]
            self.heals += [min(chara.hp_max - chara.hp, self.heal)]
            self.heal_sum += self.heals[-1]


