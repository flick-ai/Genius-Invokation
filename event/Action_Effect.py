from game.game import GeniusGame
from card.character.base import CharacterSkill
from utils import *
'''
    我先按自己的理解写一个小action
'''
class Action:
    def __init__(self) -> None:
        pass

    def on_call(self, game: GeniusGame) -> None:
        pass

class GainEnergyForActive(Action):
    # 给出战角色回复x点能量
    def __init__(self, skill: CharacterSkill) -> None:
        super().__init__(self)
        self.energy_gain = skill.energy_gain
    
    def __call__(self, game: 'GeniusGame') -> None:
        # ix = game.players[game.active_player_index].active_idx
        # target = game.players[game.active_player_index].character_list[ix]
        target = get_active_character(game)
        cur_power = target.power + self.energy_gain
        target.power = cur_power if cur_power <= target.max_power else target.max_power