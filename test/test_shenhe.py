import unittest
from typing import List, Dict, Tuple, Optional, Union

from test_base import TestBase
from test_utils import *
from genius_invocation.game.action import *

#TODO: 测试扩散伤害

class TestShenhe(TestBase, unittest.TestCase):
    player0_deck: Dict[str, List[str]] = {
        'character': ['Shenhe', 'Yae_Miko', 'Arataki_Itto'],
        'action_card': ['Thunder_and_Eternity'] * 30
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
            Action(0, 9, []),#打出雷与永恒
            Action(11, 0, [0, 1, 2])#E
        ]
        self.run_actions_for_player(player0_actions, 0)
        #对方角色0受到2点伤害，剩余生命值为8
        self.assertEqual(self.game.players[1].character_list[0].health_point, 8)
        self.assertEqual(self.game.players[1].character_list[0].elemental_application, [ElementType.CRYO])

        player0_actions = [
            Action(11, 0, [0, 1, 2])#E
        ]
        self.run_actions_for_player(player0_actions, 0)
        #对方角色0受到3点伤害，剩余生命值为5
        self.assertEqual(self.game.players[1].character_list[0].health_point, 5)

        player0_actions = [
            end_round(),#结束回合
            #第2回合
            choose_dice_empty(),#投掷骰子
            Action(0, 9, []),#打出雷与永恒
            Action(12, 0, [0, 1, 2])#Q
        ]
        player1_actions = [
            #第2回合
            choose_dice_empty(),#投掷骰子
            Action(14, 4, [0])#切换至角色2
        ]
        self.run_actions_double(player0_actions, player1_actions)
        #对方角色2受到2点伤害，剩余生命值为8
        self.assertEqual(self.game.players[1].character_list[2].health_point, 8)
        self.assertEqual(self.game.players[1].character_list[2].elemental_application, [ElementType.CRYO])

        player0_actions = [
            Action(10, 0, [0, 1, 2])#A
        ]

        player1_actions = [
            Action(14, 3, [0])#切换至角色1
        ]
        self.run_actions_double(player0_actions, player1_actions)
        
        #对方角色1受到3点伤害，剩余生命值为7
        self.assertEqual(self.game.players[1].character_list[1].health_point, 7)
        self.assertEqual(self.game.players[1].character_list[1].elemental_application, [])

if __name__ == '__main__':
    unittest.main()
