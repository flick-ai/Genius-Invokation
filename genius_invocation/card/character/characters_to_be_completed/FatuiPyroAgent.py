from genius_invocation.card.character.characters.import_head import *


class FatuiPyroAgent(Character):
    id: int = 2301
    name: str = "Fatui Pyro Agent"
    name_ch = "愚人众·火之债务处理人"
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.FATUI
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = []
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
