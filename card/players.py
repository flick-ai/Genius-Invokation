from copy import deepcopy

class STATES_Entity():
    def __init__(self, entity_name, count_type, count):
        self.name = entity_name
        self.count_type = count_type # Turns, 
        self.count = count
        

class ACTIVE_STATES():
        # 该功能已废弃，修改到game/zone.py下的active_zone
    def __init__(self, active_idx, charater_list) -> None:
        self.number_of_characters = len(charater_list) # int
        self.active_idx = active_idx # int, Should be 0,1,2,... from left to right.
        self.character_list= deepcopy(charater_list)
        self.states_list = []

    def change_to_previous_character(self):
        ix = self.active_idx-1
        if ix < 0:
            ix = self.number_of_characters-1
        while self.character_list[ix].states.alive == False:
            ix -= 1
            if ix < 0:
                ix = self.number_of_characters-1
        self.active_idx = ix
        return ix
    
    def change_to_next_character(self):
        ix = self.active_idx+1
        if ix >= self.number_of_characters:
            ix = 0
        while self.character_list[ix].states.alive == False:
            ix += 1
            if ix >= self.number_of_characters:
                ix = 0
        self.active_idx = ix
        return ix
    
    

class CHARACTER_STATES():
    # 该功能已废弃，修改到game/zone.py下的character_zone
    def __init__(self):
        self.alive = True # bool, alive for True, death for False
