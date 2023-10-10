from entity.entity import Entity
from utils import *
from game.game import GeniusGame
#TODO: FINISH THE ENTITIES
class Dendro_Core(Entity):
    def __init__(self):
        super().__init__()
        self.events = {
            'after_skill': self.after_skill
        }
        self.entity_type = ZoneType.ACTIVE_ZONE
    
    pass
        
class Quicken_Land(Entity):
    # Name Maybe Wrong
    pass

class Crystalize_Shield(Entity):
    # Name Maybe Wrong
    pass