from game.game import GeniusGame

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
    def __init__(self, energy_gain) -> None:
        super().__init__(self)
        self.energy_gain = energy_gain
    
    def __call__(self, game: GeniusGame) -> None:
        ix = game.players[game.active_player].active_zone.active_idx
        target = game.players[game.active_player].active_zone.character_list[ix]
        cur_power = target.power + self.energy_gain
        target.power = cur_power if cur_power <= target.max_power else target.max_power