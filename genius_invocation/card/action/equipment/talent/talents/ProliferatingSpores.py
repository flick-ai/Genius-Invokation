from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Jadeplume_Terrorshroom import *


class ProliferatingSpores(TalentCard):
    id: int = 227011
    name: str = "Proliferating Spores"
    name_ch = "孢子增殖"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 6}]
    cost_power = 0
    character = Jadeplume_Terrorshroom
    skill_idx: int = 1
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        target_character = game.active_player.character_list[game.current_action.target_idx]
        target_character.talent = True
        target_character.character_zone.has_entity(Radical_Vitality).equip_talent()

        if self.is_action:
            target_character.skills[self.skill_idx].on_call(game)

        