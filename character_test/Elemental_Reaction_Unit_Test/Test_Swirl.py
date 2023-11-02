'''
game_version: 4.1
card_involved:
- Barbara
- Sucrose
'''
import unittest
from typing import List, Dict, Tuple, Optional, Union

from character_test.test_base import TestBase
from character_test.test_utils import *
from genius_invocation.game.action import *


class TestBarbara(TestBase, unittest.TestCase):
    player0_deck: Dict[str, List[str]] = {
        'character': ['Barbara', 'Sucrose', 'Nahida'],
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
        ]
        self.run_actions_double(player0_init_actions, player1_init_actions)
        skill_action_list = [
            [Action(10, 0, [0, 1, 2])],
            [Action(11, 0, [0, 1, 2])],
            [Action(12, 0, [0, 1, 2])]
        ]

        # 用例执行 回合1:我方行动，对方空过 （伤害测试）
        # 芭芭拉平a
        self.restore_dice(0)
        self.run_actions_for_player([choose_character(0)], 0)
        self.run_actions_for_player(skill_action_list[0], 0)
        self.check_health(1, [99, 10, 10])
        self.check_elemental_application(1, [[ElementType.HYDRO], [], []])
        # 砂糖平a
        self.restore_dice(0)
        self.run_actions_for_player([choose_character(1)], 0)
        self.run_actions_for_player(skill_action_list[0], 0)
        self.check_health(1, [98, 9, 9])
        self.check_elemental_application(1, [[], [ElementType.HYDRO], [ElementType.HYDRO]])


    def check_health(self, player, health):
        for i in range(len(health)):
            self.assertEqual(self.game.players[player].character_list[i].health_point, health[i])

    def check_elemental_application(self, player, element):
        for i in range(len(element)):
            self.assertEqual(self.game.players[player].character_list[i].elemental_application, element[i])

    def restore_dice(self, player_id):
        num = self.game.players[player_id].dice_zone.dice_num
        self.game.players[player_id].dice_zone.add([0] * (8 - num))


if __name__ == '__main__':
    unittest.main()
