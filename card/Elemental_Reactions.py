# Calculation for elemental reactions
from utils import *
from card.character.base import *
from copy import deepcopy
#Damage x List[ElementType] x List[States] -> Damage x List[ElementType] x List[States]

def Calculation(Damage: Damage, Elements, Char_States, Active_States):
    damage = deepcopy(Damage)
    elments = deepcopy(Elements)
    char_states = deepcopy(Char_States)
    active_states = deepcopy(Active_States)

    match Damage.main_damage_type:
        case ElementType.CRYO:
            pass
        case ElementType.HYDRO:
            pass
        case ElementType.PYRO:
            pass
        case ElementType.ELECTRO:
            pass
        case ElementType.ANEPMO:
            pass
        case ElementType.GEO:
            pass
        case ElementType.DENDRO:
            pass
        case ElementType.PHYSICAL:
            pass
        
        