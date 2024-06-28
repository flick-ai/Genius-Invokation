# from genius_invocation.game import GeniusGame, ActiveDie
# import threading

# # 创建一个多线程来运行游戏
# class GameThread(threading.Thread):
#     def __init__(self, game: GeniusGame):
#         threading.Thread.__init__(self)
#         self.game = game

#     def run(self):
#         self.game.run()
import os
from utils import *
from typing import Dict, List, Tuple, Optional, Union
from genius_invocation.game.game import GeniusGame
from genius_invocation.game.action import *
from genius_invocation.utils import *
from genius_invocation.entity.status import Status, Shield, Combat_Status, Combat_Shield
from genius_invocation.entity.summon import Summon
from genius_invocation.entity.support import Support
from genius_invocation.game.zone import CharacterZone, ActiveZone, SupportZone, SummonZone, DiceZone, HandZone, CardZone
from genius_invocation.entity.status import Weapon, Artifact
from genius_invocation.card.character.base import CharacterSkill
class Test():
    def __init__(self):
        player0_deck: Dict[str, List[str]] = {
            'character': [],
            'action_card': []
        }
        player1_deck: Dict[str, List[str]] = {
            'character': [],
            'action_card': []
        }
        self.game = GeniusGame(
            player0_deck=player0_deck,
            player1_deck=player1_deck,
            seed = 0,
            is_omni=False
        )

    def add_talent(self, ):
        pass
    def add_status(self, status: Union[Status, Shield], target_zone: CharacterZone, independent:bool=False, **kwargs):
        # Add status(maybe shield) into the target character zone
        target_zone.add_entity(status, independent, **kwargs)

    def add_combat_status(self, status: Union[Combat_Status, Combat_Shield], target_zone: ActiveZone, independent:bool=False, **kwargs):
        # Add combat status (maybe combat shield) into the target active zone.
        target_zone.add_entity(status, independent, **kwargs)

    def add_summon(self, summon: Summon, target_zone: SummonZone, independent:bool=False, **kwargs):
        # Add Summon to target summon zone.
        target_zone.add_entity(summon, independent, **kwargs)

    def add_support(self, support: Support, target_zone: SupportZone, **kwargs):
        target_zone.add_entity(support, **kwargs)

    def add_weapon(self, weapon: Weapon, target_zone: CharacterZone):
        target_zone.weapon_card = weapon
    
    def add_artifact(self, artifact: Artifact, target_zone: CharacterZone):
        target_zone.artifact_card = artifact

    def set_dice(self, dices: List[DiceType], target_zone: DiceZone):
        target_zone.remove_all()
        target_zone.add(dices)

    def set_hands(self, card_names: List[str], target_zone: HandZone):
        target_zone.card = []
        target_zone.add_card_by_name(card_names)
    
    def set_cards(self, card_names: List[str], target_zone: CardZone):
        # set cards, without random shuffle !
        target_zone.card = []
        target_zone.card_name = []
        target_zone.card_type = []
        for card_name in card_names:
            target_zone.card.append(eval(card_name)())
            if card_name not in target_zone.card_name:
                target_zone.card_name.append(card_name)
                target_zone.card_type.append(target_zone.card[-1].card_type)


    def set_skill_attri(self, skill_attri: any, attribute_value: any):
        try:
            skill_attri = attribute_value
        except:
            raise "Something wrong when directly change the value of the attribute."
        
    def set_situation(self, file: "str"):
        #load file, 
        pass

        
    def call_skill(self, skill: CharacterSkill):
        skill.on_call(self.game)
    
    
    def step_one_forward(self, action: Action):
        self.game.step(action)
    

if __name__ == '__main__':
    base_dir = './Test'
    package_dirs = ["./card/character/characters","./card/action/support/companion",
                    "./card/action/support/item","./card/action/support/location",
                    "./card/action/event/events","./card/action/event/foods",
                    "./card/action/event/elemental_resonance", "./card/action/event/arcane_legend",
                    "./card/action/equipment/artifact/artifacts",
                    "./card/action/equipment/talent/talents",
                    "./card/action/equipment/weapon/weapons"]
    for package_dir in package_dirs:
        available_name = [f for f in os.listdir(package_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
        target_dir = base_dir + package_dir.split('.')[-1]
        target_names = ['test_'+ f for f in available_name]
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        for target_name in target_names:
            name = os.path.join(target_dir, target_name)
            with open(name, 'w') as f:
                pass



