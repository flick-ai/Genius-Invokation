from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
import os

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class EremiteTeatime(ActionCard):
    id = 332040
    name: str = "Eremite Teatime"
    name_ch = '镀金旅团的茶歇'
    time = 5.1
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()
        cards_dirs = ["./card/action/support/item",
                      "./card/action/support/location",
                      "./card/action/event/foods"]
        self.items = []
        available_name = [f[:-3] for f in os.listdir(cards_dirs[0]) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
        self.items.extend(available_name)

        self.locations = []
        available_name = [f[:-3] for f in os.listdir(cards_dirs[1]) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
        self.locations.extend(available_name)

        self.foods = []
        available_name = [f[:-3] for f in os.listdir(cards_dirs[2]) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
        self.foods.extend(available_name)

    def on_played(self, game: 'GeniusGame'):
        same_element = {}
        same_country = {}
        same_weapon = {}
        for character in game.active_player.character_list:
            same_element[character.element] = same_element.get(character.element, 0) + 1
            same_weapon[character.weapon_type] = same_weapon.get(character.weapon_type, 0) + 1
            if hasattr(character, 'country_list'):
                for country in character.country_list:
                    same_country[country] = same_country.get(country, 0) + 1
            else:
                same_country[character.country] = same_country.get(character.country, 0) + 1

        self.location = []
        for element in same_element.keys():
            if same_element[element] >= 2:
                for i in range(3):
                    self.location.append(random.choice(self.locations))
                break

        self.item = []
        for country in same_country.keys():
            if same_country[country] >= 2:
                for i in range(3):
                    self.item.append(random.choice(self.items))
                break

        self.food = []
        for weapon in same_weapon.keys():
            if same_weapon[weapon] >= 2:
                for i in range(3):
                    self.food.append(random.choice(self.foods))
                break

        self.get_list = []
        if self.location != []:
            self.get_list.append(self.location)
        if self.item != []:
            self.get_list.append(self.item)
        if self.food != []:
            self.get_list.append(self.food)
        if self.get_list == []:
            return

        self.now_phase = game.game_phase
        game.game_phase = GamePhase.SELECT
        game.special_phase = self
        game.active_player.select_list = self.get_list.pop(0)
        game.active_player.select_num = 1

    def find_target(self, game:'GeniusGame'):
        return [1]

    def on_finished(self, game: 'GeniusGame'):
        select_list = game.active_player.select_list
        result = game.active_player.select_result
        game.active_player.hand_zone.add_card_by_name([select_list[result[0]]])
        if len(self.get_list) > 0:
            game.active_player.select_list = self.get_list.pop(0)
        else:
            game.game_phase = self.now_phase
            game.special_phase = None
            game.active_player.select_list = None
            game.active_player.select_num = 0
            game.active_player.select_result = None
