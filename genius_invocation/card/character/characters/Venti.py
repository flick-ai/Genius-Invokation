from genius_invocation.card.character.import_head import *
from genius_invocation.entity.character import Character
from genius_invocation.game.game import GeniusGame
from genius_invocation.utils import Character, GeniusGame


class Venti(Character):
    id: int = 1503
    name: str = "Venti"
    name_ch = "温迪"
    element: ElementType = ElementType.ANEMO
    weapon_type: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = []
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent

class Divine_Marksmanship(NormalAttack):
    name = "Divine Marksmanship"
    name_ch = ""
    id = 150301
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.ANEMO
        },
        {
            'cost_num': 2,
            'cost_type': CostType.BLACK
        }
    ]

    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)

    def on_call(self, game: GeniusGame):
        super().on_call(game)

        self.resolve_damage(game)

        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class 



