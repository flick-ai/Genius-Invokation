import unittest
from typing import List, Dict, Tuple, Optional, Union

from character_test.test_base import TestBase
from character_test.test_utils import *
from genius_invocation.game.action import *


class TestWanderer(TestBase, unittest.TestCase):
    player0_deck: Dict[str, List[str]] ={
        'character': ['Wanderer'],
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
        self.check_health(1, [97, 10, 10])
        self.check_elemental_application(1, [[], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[0], 0)  # 强化平a
        self.check_health(1, [97, 7, 10])
        self.check_elemental_application(1, [[], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[2], 0)  # Q技能
        self.check_health(1, [89, 7, 10])
        self.check_elemental_application(1, [[], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[0], 0)  # 平a
        self.check_health(1, [88, 7, 10])
        self.check_elemental_application(1, [[], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[1], 0)  # 第一个E技能
        self.check_health(1, [86, 7, 10])
        self.check_elemental_application(1, [[], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[0], 0)  # 强化平a
        self.check_health(1, [86, 4, 10])
        self.check_elemental_application(1, [[], [], []])
        self.assertEqual(self.game.players[0].dice_zone.num(), 5)
        self.game.players[0].dice_zone.add([7] * 3)

        self.run_actions_for_player(skill_action_list[2], 0)  # Q技能
        self.check_health(1, [78, 4, 10])
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
        self.check_health(1, [78, 4, 10])
        self.check_elemental_application(1, [[], [], []])

    def check_health(self, player, health):
        for i in range(len(health)):
            self.assertEqual(self.game.players[player].character_list[i].health_point, health[i])

    def check_elemental_application(self, player, element):
        for i in range(len(element)):
            self.assertEqual(self.game.players[player].character_list[i].elemental_application, element[i])


if __name__ == '__main__':
    unittest.main()
