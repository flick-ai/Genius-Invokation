from entity.entity import Entity
from utils import *
from game.game import GeniusGame
#TODO: FINISH THE ENTITIES
class Dendro_Core(Entity):
    def __init__(self, game):
        super().__init__(game)
        pass
    
    pass
        
class Catalyzing_Feild(Entity):
    # Name Maybe Wrong
    pass

class Crystallize_Shield(Entity):
    # Name Maybe Wrong
    pass

class Infusion(Entity):
    def __init__(self, game, ElementType: ElementType, times: int, StatusCountingType: Status_Counting_Type):
        super().__init__(game)
        self.ElementType = ElementType
        self.times = times
        self.StatusCountingType = StatusCountingType
    
    def __call__(self, game: GeniusGame):
        if game.current_damage.main_damage_element is ElementType.PHYSICAL:
            game.current_damage.main_damage_element = self.ElementType
            

