"""
game_version: 4.1
card_involved:
- Timmie
"""

import unittest
from typing import List, Dict, Tuple, Optional, Union

from test_base import TestBase
from test_utils import *
from genius_invocation.game.action import *

class TestTimmie(TestBase, unittest.TestCase):
    player0_deck: Dict[str, List[str]] = {
        'character': ['Rhodeia_of_Loch', 'Nahida', 'Fischl'],
        'action_card': ['Timmie'] * 30
    }
    player1_deck: Dict[str, List[str]] = {
        'character': ['Rhodeia_of_Loch', 'Nahida', 'Fischl'],
        'action_card': ['Timmie'] * 30
    }
    
    def test(self):
        self.initialize_game()
        player0_actions = [
            choose_cards_empty(),#初始换牌
            choose_character(0),#选择出战角色
            #第1回合
            choose_dice_empty(),#投掷骰子
            Action(0, 9, []),#打出Timmie
            end_round(),#结束回合
            #第2回合
            choose_dice_empty(),#投掷骰子
        ]
        player1_actions = [
            choose_cards_empty(),#初始换牌
            choose_character(0),#选择出战角色
            #第1回合
            choose_dice_empty(),#投掷骰子
            end_round(),#结束回合
            #第2回合
            choose_dice_empty(),#投掷骰子
        ]
        self.run_actions_double(player0_actions, player1_actions)
        #第2回合，player0的支援区应仅有1个提米，鸽子数量为2
        self.assertEqual(self.game.players[0].support_zone.num(), 1)
        self.assertEqual(self.game.players[0].support_zone.space[0].name, 'Timmie')
        self.assertEqual(self.game.players[0].support_zone.space[0].show(), '2')
        self.assertEqual(self.game.players[0].dice_zone.num(), 8)
        self.assertEqual(self.game.players[0].hand_zone.num(), 6)

        player0_actions = [
            end_round(),#结束回合
            #第3回合
            choose_dice_empty(),#投掷骰子
        ]
        player1_actions = [
            end_round(),#结束回合
            #第3回合
            choose_dice_empty(),#投掷骰子
        ]
        self.run_actions_double(player0_actions, player1_actions)
        #第3回合，player0的提米生效，支援区为空，骰子数量+1，手牌数量+1
        self.assertEqual(self.game.players[0].support_zone.num(), 0)
        self.assertEqual(self.game.players[0].dice_zone.num(), 9)
        self.assertEqual(self.game.players[0].hand_zone.num(), 9)
        

if __name__ == '__main__':
    unittest.main()
