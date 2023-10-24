from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.ElectroHypostasis import ElectroHypostasis

class AbsorbingPrism(TalentCard):
    id: int = 224011
    name: str = "Absorbing Prism"
    name_ch = "汲能棱晶"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 3}]
    cost_power = 0
    character = ElectroHypostasis
    skill_idx: int = -1
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        target_character = game.active_player.character_list[game.current_action.target_idx]
        target_character.talent = True
        target_character.talent_skill.on_call(game)
        
        