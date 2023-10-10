# Calculation for Damages including elemental reactions
from utils import *
from card.character.base import *
from copy import deepcopy
from game.zone import ActiveZone
from event.damage.damage import Damage

#TODO Not Implement Yet, maybe can be unify with Class Settle.
def settleDamage(damage: Damage, myActiveZone: ActiveZone, targetActiveZone: ActiveZone, targetId=-1):
    pass
def updateDamageAndZone(damage: Damage, myActiveZone: ActiveZone, targetActiveZone: ActiveZone, targetId=-1):
    #BOTH damage, myActiveZone, targetActiveZone should be changed.
    pass

def elemental_reactions(damage: Damage, myActiveZone: ActiveZone, targetActiveZone: ActiveZone, targetId=-1):
    #During the process, myActiveZone, targetActiveZone may be changed. Return the Reaction Type.
    damage = deepcopy(damage)
    if targetId == -1:
        targetId = targetActiveZone.active_idx
    targetElementTypes = targetActiveZone.character_list[targetId].element_attach
    Extra_Damage_list = []
    reaction = "None"
    match damage.main_damage_type:
        case ElementType.CRYO:
            for targetElement in targetElementTypes:
                match targetElement:
                    case ElementType.HYDRO:
                        if damage.main_damage >0:
                            damage.main_damage += 1
                        targetActiveZone.character_list[targetId].element_attach.remove(ElementType.HYDRO)
                        targetActiveZone.character_list[targetId].is_frozen = True
                        reaction = "Frozen"
                        break
                    case ElementType.PYRO:
                        if damage.main_damage >0:
                            damage.main_damage += 2
                        targetActiveZone.character_list[targetId].element_attach.remove(ElementType.PYRO)
                        reaction = "Melt"
                        break
                    case ElementType.ELECTRO:
                        if damage.main_damage >0:
                            damage.main_damage += 1
                            damage.piercing_damage += 1
                        targetActiveZone.character_list[targetId].element_attach.remove(ElementType.ELECTRO)
                        reaction = "Super-Conduct"
                        break
                    case _:
                        continue
            
        case ElementType.HYDRO:
            targetElement = targetElementTypes[0] #Always have a reaction
            match targetElement:
                case ElementType.CRYO:
                    if damage.main_damage >0:
                        damage.main_damage += 1
                    targetActiveZone.character_list[targetId].element_attach.remove(ElementType.CRYO)
                    targetActiveZone.character_list[targetId].is_frozen = True # TODO: Should add frozen status， No implement state sequence yet.
                    reaction = "Frozen"
                case ElementType.PYRO:
                    if damage.main_damage >0:
                        damage.main_damage += 2
                    targetActiveZone.character_list[targetId].element_attach.remove(ElementType.PYRO)
                    reaction = "Vaporize"
            
                case ElementType.ELECTRO:
                    if damage.main_damage >0:
                        damage.main_damage += 1
                        damage.piercing_damage += 1
                    targetActiveZone.character_list[targetId].element_attach.remove(ElementType.ELECTRO)
                    reaction = "Electro-Charged"
                
                case ElementType.DENDRO:
                    if damage.main_damage >0:
                        damage.main_damage += 1
                    targetActiveZone.character_list[targetId].element_attach.remove(ElementType.DENDRO)
                    myActiveZone.add_status("Bloom") #TODO: Add bloom status， No implement state sequence yet.
                    reaction = "Bloom"

        case ElementType.PYRO:
            targetElement = targetElementTypes[0] #Always have a reaction
            match targetElement:
                case ElementType.CRYO:
                    if damage.main_damage >0:
                        damage.main_damage += 2
                    targetActiveZone.character_list[targetId].element_attach.remove(ElementType.CRYO)
                    reaction = "Melt"
                case ElementType.HYDRO:
                    if damage.main_damage >0:
                        damage.main_damage += 2
                    targetActiveZone.character_list[targetId].element_attach.remove(ElementType.HYDRO)
                    reaction = "Vaporize"
            
                case ElementType.ELECTRO:
                    if damage.main_damage >0:
                        damage.piercing_damage += 2
                    targetActiveZone.character_list[targetId].element_attach.remove(ElementType.ELECTRO)
                    if targetId == targetActiveZone.active_idx:
                        targetActiveZone.change_to_next_character() #TODO: Check here whether such an easy implement is correct, when some status exists.
                    reaction = "Overload"
                
                case ElementType.DENDRO:
                    if damage.main_damage >0:
                        damage.main_damage += 1
                    targetActiveZone.character_list[targetId].element_attach.remove(ElementType.DENDRO)
                    myActiveZone.summons_zone.insert("Buring") #TODO: Add burning summon, summon shuold be checked whether exists first. The function is not implemented.
                    reaction = "Burning"

        case ElementType.ELECTRO:
            targetElement = targetElementTypes[0] #Always have a reaction
            match targetElement:
                case ElementType.CRYO:
                    if damage.main_damage >0:
                        damage.main_damage += 1
                        damage.piercing_damage += 1
                    targetActiveZone.character_list[targetId].element_attach.remove(ElementType.CRYO)
                    reaction = "Super-Conduct"
                case ElementType.HYDRO:
                    if damage.main_damage >0:
                        damage.main_damage += 1
                        damage.piercing_damage += 1
                    targetActiveZone.character_list[targetId].element_attach.remove(ElementType.HYDRO)
                    reaction = "Electro-Charged"
                case ElementType.PYRO:
                    if damage.main_damage >0:
                        damage.piercing_damage += 2
                    targetActiveZone.character_list[targetId].element_attach.remove(ElementType.PYRO)
                    if targetId == targetActiveZone.active_idx:
                        targetActiveZone.change_to_next_character() #TODO: Check here whether such an easy implement is correct, when some status exists.
                    reaction = "Overload"
                
                case ElementType.DENDRO:
                    if damage.main_damage >0:
                        damage.main_damage += 1
                    targetActiveZone.character_list[targetId].element_attach.remove(ElementType.DENDRO)
                    myActiveZone.add_status("Quicken") # TODO: Not implement yet.
                    reaction = "Quicken"

        case ElementType.ANEPMO:
            for targetElement in targetElementTypes:
                match targetElement:
                    case ElementType.CRYO | ElementType.HYDRO | ElementType.PYRO | ElementType.ELECTRO:
                        targetActiveZone.character_list[targetId].element_attach.remove(ElementType.CRYO)
                        targetlist = []
                        for id in range(3):
                            targetlist.append((id + targetActiveZone.active_idx)%3)
                        targetlist.remove(targetId)
                        Swirl_Damage = Damage("OTHER", ElementType.CRYO, 1, 0)
                        
                        for id in targetlist:
                            if targetActiveZone.character_list[id].is_alive:
                                Extra_Damage_list.append((Swirl_Damage, id))
                        reaction = "Swirl"
                        break
                    case _:
                        continue

        case ElementType.GEO:
            for targetElement in targetElementTypes:
                match targetElement:
                    case ElementType.CRYO | ElementType.HYDRO | ElementType.PYRO | ElementType.ELECTRO:
                        if damage.main_damage >0:
                            damage.main_damage += 1
                        targetActiveZone.character_list[targetId].element_attach.remove(targetElement)
                        myActiveZone.add_status("Crystallize") # TODO: Not implement yet.
                        reaction = "Crystallize"
                        break
        case ElementType.DENDRO:
            # the only two element case is CRYO & DEBDRO, No reaction. Only consider the first element.
            targetElement = targetElementTypes[0]
            match targetElement:
                case ElementType.HYDRO:
                    if damage.main_damage >0:
                        damage.main_damage += 1
                    targetActiveZone.character_list[targetId].element_attach.remove(ElementType.HYDRO)
                    myActiveZone.add_status("Bloom") #TODO: Add bloom status， No implement state sequence yet.
                    reaction = "Bloom"
                case ElementType.PYRO:
                    if damage.main_damage >0:
                        damage.main_damage += 1
                    targetActiveZone.character_list[targetId].element_attach.remove(ElementType.PYRO)
                    myActiveZone.summons_zone.insert("Buring") #TODO: Add burning summon, summon shuold be checked whether exists first. The function is not implemented.
                    reaction = "Burning"
                case ElementType.ELECTRO:
                    if damage.main_damage >0:
                        damage.main_damage += 1
                    targetActiveZone.character_list[targetId].element_attach.remove(ElementType.ELECTRO)
                    myActiveZone.add_status("Quicken") # TODO: Not implement yet.
                    reaction = "Quicken"
        case ElementType.PHYSICAL:
            pass
    
    settleDamage(damage, myActiveZone, targetActiveZone, targetId)
    for Extra_Damage, Extra_TargetId in Extra_Damage_list:
        updateDamageAndZone(Extra_Damage, myActiveZone, targetActiveZone, Extra_TargetId)
        elemental_reactions(Extra_Damage, myActiveZone, targetActiveZone, Extra_TargetId)
        
    if reaction is "None":
        match damage.main_damage_element:
            case ElementType.CRYO | ElementType.HYDRO | ElementType.PYRO | ElementType.ELECTRO:
                targetActiveZone.character_list[targetId].element_attach.insert(0, damage.main_damage_element)
            case ElementType.DENDRO:
                targetActiveZone.character_list[targetId].element_attach.append(damage.main_damage_element)

    return reaction  