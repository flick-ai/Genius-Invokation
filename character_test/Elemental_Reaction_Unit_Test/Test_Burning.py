'''
game_version: 4.1
card_involved:
- Nahida
- Klee
'''
import unittest
from typing import List, Dict, Tuple, Optional, Union

from character_test.test_base import TestBase
from character_test.test_utils import *
from genius_invocation.game.action import *

'''
Error
Traceback (most recent call last):
  File "E:\GitHub\Genius-Invokation\character_test\Elemental_Reaction_Unit_Test\Test_Burning.py", line 62, in test
    self.run_actions_for_player([end_round()], 0)
  File "E:\GitHub\Genius-Invokation\character_test\test_base.py", line 83, in run_actions_for_player
    game.step(action)
  File "E:\GitHub\Genius-Invokation\genius_invocation\game\game.py", line 221, in step
    self.resolve_action(action)
  File "E:\GitHub\Genius-Invokation\genius_invocation\game\game.py", line 112, in resolve_action
    self.end_phase()
  File "E:\GitHub\Genius-Invokation\genius_invocation\game\game.py", line 302, in end_phase
    self.active_player.end_phase(self)
  File "E:\GitHub\Genius-Invokation\genius_invocation\game\player.py", line 368, in end_phase
    game.manager.invoke(EventType.END_PHASE, game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\event\events.py", line 84, in invoke
    self.events[event_type](zone_type)(game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\event\events.py", line 61, in __call__
    listener(game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\event\events.py", line 23, in __call__
    self.action(game)
  File "E:\GitHub\Genius-Invokation\genius_invocation\entity\summon.py", line 66, in on_end_phase
    dmg = Damage.create_damage(
NameError: name 'Damage' is not defined
'''

class TestBarbara(TestBase, unittest.TestCase):
    player0_deck: Dict[str, List[str]] = {
        'character': ['Barbara', 'Klee', 'Nahida'],
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
        # 可莉平a
        self.restore_dice(0)
        self.run_actions_for_player([choose_character(1)], 0)
        self.run_actions_for_player(skill_action_list[0], 0)
        self.check_health(1, [99, 10, 10])
        self.check_elemental_application(1, [[ElementType.PYRO], [], []])
        # 纳西妲平a
        self.restore_dice(0)
        self.run_actions_for_player([choose_character(2)], 0)
        self.run_actions_for_player(skill_action_list[0], 0)
        self.check_health(1, [97, 10, 10])
        self.check_elemental_application(1, [[], [], []])
        # 回合结束
        self.run_actions_for_player([end_round()], 0)
        # 节末伤害检测
        self.check_health(1, [96, 10, 10])
        self.check_elemental_application(1, [[ElementType.PYRO], [], []])

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
