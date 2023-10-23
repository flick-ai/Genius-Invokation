import abc
import unittest
from typing import List, Dict, Tuple, Optional, Union

from genius_invocation.game.game import GeniusGame
from genius_invocation.game.action import *
from genius_invocation.utils import *
from test_utils import *

class TestBase(metaclass=abc.ABCMeta):
    #玩家卡组
    player0_deck: Dict[str, List[str]] = {
        'character': [],
        'action_card': []
    }
    player1_deck: Dict[str, List[str]] = {
        'character': [],
        'action_card': []
    }

    game:GeniusGame = None

    def test(self):
        pass
    
    #可能会用到的工具函数
    def initialize_game(self):
        '''
        初始化游戏
        '''
        self.game = GeniusGame(player0_deck=self.player0_deck, player1_deck=self.player1_deck)

    def run_actions_single(
        self, 
        actions:List[Action]):
        '''
        执行一系列操作，其中双方的操作保存在同一个列表中
        '''
        for action in actions:
            self.game.step(action)
            #print(action.choice, action.target, action.choice_list)
            #import rich
            #rich.print(self.game.encode_message())
            #input()
    
    def run_actions_double(
        self, 
        player0_actions:List[Action], 
        player1_actions:List[Action]):
        '''
        执行一系列操作，其中双方的操作保存在两个列表中
        '''
        action_iterators = (iter(player0_actions), iter(player1_actions))
        while not(self.game.is_end):
            try:
                action = action_iterators[self.game.active_player_index].__next__()
            except StopIteration:
                break
            self.game.step(action)
            #print(action.choice, action.target, action.choice_list)
            #import rich
            #rich.print(self.game.encode_message())
            #input()
    
    def run_actions_for_player(
        self,
        actions:List[Action],
        player_index:int):
        '''
        为指定玩家执行一系列操作，在此过程中另一方只会空过
        '''
        #TODO: 在出战角色倒下时自动选择出战角色
        game = self.game
        action_iterator = iter(actions)
        action:Optional[Action] = None
        while not(self.game.is_end):
            if game.active_player_index == player_index:
                try:
                    action = action_iterator.__next__()
                except StopIteration:
                    break
                game.step(action)
            else: 
                action = passive_action(game)
                game.step(action)
            #print(action.choice, action.target, action.choice_list)
            #import rich
            #rich.print(self.game.encode_message())
            #input()


