from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.character import Character
from genius_invocation.utils import *
from genius_invocation.entity.summon import Summon
from genius_invocation.event.damage import Damage
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Abyssal_Summons_Summmon(Summon):
    name: str = 'Abyssal Summons'
    name_ch = '深渊的呼唤'
    element: ElementType
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2

    def on_end_phase(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
        if self.current_usage <= 0:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]

class Cryo_Hilichurl(Abyssal_Summons_Summmon):
    name = "Cryo Hilichurl Shooter"
    name_ch = '冰箭丘丘人'
    element = ElementType.CRYO
    id = 33201511

class Hydeo_Hilichurl(Abyssal_Summons_Summmon):
    name = "Hydro Samachurl"
    name_ch = '水丘丘萨满'
    element = ElementType.HYDRO
    id = 33201512

class Pyro_Hilichurl(Abyssal_Summons_Summmon):
    name = "Hilichurl Berserker"
    name_ch = '冲锋丘丘人'
    element = ElementType.PYRO
    id = 33201513

class Electro_Hilichurl(Abyssal_Summons_Summmon):
    name = "Electro Hilichurl Shooter"
    name_ch = '雷箭丘丘人'
    element = ElementType.ELECTRO
    id = 33201514

def choose_one_summon(game: 'GeniusGame'):
    un_summon_list = []
    for summon in [Cryo_Hilichurl, Hydeo_Hilichurl, Pyro_Hilichurl, Electro_Hilichurl]:
        if game.active_player.summon_zone.has_entity(summon) is None:
            un_summon_list.append(summon)

    x = un_summon_list[game.random.randint(0,len(un_summon_list))]
    summon = x(game, game.active_player, None)
    game.active_player.summon_zone.add_entity(summon)

class Abyssal_Summons(ActionCard):
    id: int = 332015
    name: str = 'Abyssal Summons'
    name_ch = '深渊的呼唤'
    country = CountryType.MONSTER
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT_COUNTRY

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        choose_one_summon(game)

    def find_target(self, game:'GeniusGame'):
        if game.active_player.summon_zone.num() < MAX_SUMMON:
            return [1]
        else:
            return []
