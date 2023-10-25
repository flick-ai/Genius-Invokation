from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.character import Character
from genius_invocation.utils import *
from genius_invocation.entity.status import Combat_Status
from genius_invocation.event.damage import Damage
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Fatui_Conspiracy_State(Combat_Status):
    name: str = 'Fatui Conspiracy'
    name_ch = '愚人众的阴谋'
    element: ElementType
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2

    def on_after_skill(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.OTHER,
                main_damage_element=self.element,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_my_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
        if self.current_usage <= 0:
            self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.on_after_skill)
        ]

class Cryo_Cicin_Mage(Fatui_Conspiracy_State):
    name = "Cryo Cicin Mage"
    name_ch = '冰萤术士'
    element = ElementType.CRYO

class Mirror_Maiden(Fatui_Conspiracy_State):
    name = "Mirror_Maiden"
    name_ch = '藏镜仕女'
    element = ElementType.HYDRO

class Pyroslinger_Bracer(Fatui_Conspiracy_State):
    name = "Pyroslinger Bracer"
    name_ch = '火铳游击兵'
    element = ElementType.PYRO

class Electrohammer_Vanguard(Fatui_Conspiracy_State):
    name = "Electrohammer Vanguard"
    name_ch = '雷锤前锋军'
    element = ElementType.ELECTRO

def choose_one_status(game: 'GeniusGame'):
    opponent = get_opponent(game)
    un_state_list = []
    for state in [Cryo_Cicin_Mage, Mirror_Maiden, Pyroslinger_Bracer, Electrohammer_Vanguard]:
        if opponent.team_combat_status.has_status(state) is None:
            un_state_list.append(state)
    
    x = un_state_list[game.random.randint(0,len(un_state_list))]
    state = x(game, opponent , None)
    opponent.team_combat_status.add_entity(state)

class Fatui_Conspiracy(ActionCard):
    id: int = 332016
    name: str = 'Fatui Conspiracy'
    name_ch = '愚人众的阴谋'
    country = CountryType.FATUI
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT_COUNTRY

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        choose_one_status(game)
