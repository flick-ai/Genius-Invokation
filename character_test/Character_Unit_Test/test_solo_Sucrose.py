import unittest
from typing import List, Dict, Tuple, Optional, Union

from character_test.test_base import TestBase
from character_test.test_utils import *
from genius_invocation.game.action import *

'''
Error
Traceback (most recent call last):
  File "E:\GitHub\Genius-Invokation\test\test_character_solo\test_solo_Sucrose.py", line 50, in test
    self.run_actions_for_player(skill_action_list[1], 0)  # 第一个E技能
  File "E:\GitHub\Genius-Invokation\test\test_base.py", line 83, in run_actions_for_player
    game.step(action)
  File "E:\GitHub\Genius-Invokation\genius_invocation\game\game.py", line 221, in step
    self.resolve_action(action)
  File "E:\GitHub\Genius-Invokation\genius_invocation\game\game.py", line 100, in resolve_action
    active_player.use_skill(self)
  File "E:\GitHub\Genius-Invokation\genius_invocation\game\player.py", line 165, in use_skill
    self.character_list[self.active_idx].skill(idx, game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\entity\character.py", line 91, in skill
    self.skills[skill].on_call(game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\card\character\characters\Sucrose.py", line 67, in on_call
    self.resolve_damage(game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\card\character\base.py", line 52, in resolve_damage
    game.resolve_damage()
  File "E:\GitHub\Genius-Invokation\genius_invocation\game\game.py", line 146, in resolve_damage
    self.manager.invoke(EventType.SPECIAL_SWITCH, self)
  File "E:\GitHub\Genius-Invokation\genius_invocation\event\events.py", line 84, in invoke
    self.events[event_type](zone_type)(game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\event\events.py", line 61, in __call__
    listener(game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\event\events.py", line 23, in __call__
    self.action(game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\card\character\characters\Sucrose.py", line 179, in special_switch
    opponent = get_opponent(self.from_character.from_player.index)
AttributeError: 'NoneType' object has no attribute 'from_player'
'''

class TestSucrose(TestBase, unittest.TestCase):
    player0_deck: Dict[str, List[str]] ={
        'character': ['Sucrose'],
        'action_card': ['Thunder_and_Eternity'] * 30
    }
    player1_deck: Dict[str, List[str]] = {
        'character': ['Fischl', 'Cyno', 'Eula'],
        'action_card': ['Thunder_and_Eternity'] * 30
    }

    def test(self):
        # 用例初始化
        self.initialize_game()
        self.game.active_player_index = 0
        self.game.players[1].character_list[0].health_point = 100
        player0_init_actions = [
            choose_cards_empty(),  # 初始换牌
            choose_character(0),  # 选择出战角色
            choose_dice_empty(),  # 投掷骰子
            Action(0, 9, []),  # 打出雷与永恒
        ]
        player1_init_actions = [
            choose_cards_empty(),  # 初始换牌
            choose_character(0),  # 选择出战角色
            choose_dice_empty(),  # 投掷骰子
            Action(0, 9, []),  # 打出雷与永恒
        ]
        self.run_actions_for_player(player0_init_actions, 0)
        skill_action_list = [
            [Action(10, 0, [0, 1, 2])],
            [Action(11, 0, [0, 1, 2])],
            [Action(12, 0, [0, 1, 2])]
        ]

        # 用例执行 回合1:我方行动，对方空过 （伤害测试）
        self.run_actions_for_player(skill_action_list[0], 0)  # 平a
        self.check_health(1, [99, 10, 10])
        self.check_elemental_application(1, [[], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[1], 0)  # 第一个E技能
        self.check_health(1, [96, 10, 10])
        self.check_elemental_application(1, [[], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[1], 0)  # 第二个E技能，如果没有，则重复释放
        self.check_health(1, [96, 10, 7])
        self.check_elemental_application(1, [[], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[2], 0)  # Q技能
        self.check_health(1, [96, 9, 7])
        self.check_elemental_application(1, [[], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[0], 0)  # 平a
        self.check_health(1, [96, 8, 7])
        self.check_elemental_application(1, [[], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[1], 0)  # 第一个E技能
        self.check_health(1, [96, 5, 7])
        self.check_elemental_application(1, [[], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[1], 0)  # 第二个E技能，如果没有，则重复释放
        self.check_health(1, [93, 5, 7])
        self.check_elemental_application(1, [[], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[2], 0)  # Q技能 # 打在第三个
        self.check_health(1, [93, 5, 6])
        self.check_elemental_application(1, [[], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        # 用例执行 回合2:我方空过，对方行动 （承伤测试）
        self.game.active_player_index = 1
        self.run_actions_for_player(player1_init_actions, 1)
        # 对方A
        self.run_actions_for_player(skill_action_list[0], 1)
        self.assertEqual(self.game.players[0].character_list[0].health_point, 8)
        self.assertEqual(self.game.players[0].character_list[0].elemental_application, [])
        # 对方A
        self.run_actions_for_player(skill_action_list[0], 1)
        self.assertEqual(self.game.players[0].character_list[0].health_point, 6)
        self.assertEqual(self.game.players[0].character_list[0].elemental_application, [])

        # 回合1节末伤害检测
        self.check_health(1, [93, 5, 4])
        self.check_elemental_application(1, [[], [], []])

    def check_health(self, player, health):
        for i in range(len(health)):
            self.assertEqual(self.game.players[player].character_list[i].health_point, health[i])

    def check_elemental_application(self, player, element):
        for i in range(len(element)):
            self.assertEqual(self.game.players[player].character_list[i].elemental_application, element[i])


if __name__ == '__main__':
    unittest.main()