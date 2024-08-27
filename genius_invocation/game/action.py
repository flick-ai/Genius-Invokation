'''
    definition of action space
    consist of three stage of actions: choice, target and dice
'''

from genius_invocation.utils import *
from genius_invocation.user_layout import print_prompt
import genius_invocation.user_input as user_input
from genius_invocation.utils_dict import compare_dict
from loguru import logger

'''
    choice action (1 dim)
    0-9: 10 hand cards (from left to right)
    10-13: 4 character skills
    14: change character
    15: pass this turn
    16: dice region
    17: card region
    18: special action
'''
# 16: none (to solve problem caused by "Toss-up" and "Nature and Wisdom" and so on)

'''
    target action (1 dim)
    0: opponent
    1: myself or none
    2-4: my characters (from left to right)
    5-8: opponent summon region
    9-12: my support region
    13: dice region
    14: card region
'''

'''
    multi action (n dim), for each dim
    0-16: the i th dice
'''

# class Action:
#     def __init__(self) -> None:


class Action:
    def __init__(self, choice, target, dice) -> None:
        self.choice: int = choice
        self.target: int = target
        self.choice_list: List[int] = dice

        self.choice_type: ActionChoice
        self.target_type: ActionTarget

        self.choice_idx: int
        self.target_idx: int

        self.set_type()


    def set_type(self) -> None:
        '''
            将Action从Tuple形式解码
        '''
        if 0 <= self.choice < 10:
            self.choice_type = ActionChoice.HAND_CARD
            self.choice_idx = self.choice
        elif 10 <= self.choice < 14:
            self.choice_type = ActionChoice.CHARACTER_SKILL
            self.choice_idx = self.choice - 10
        elif self.choice == 14:
            self.choice_type = ActionChoice.CHANGE_CHARACTER
            self.choice_idx = -1
        elif self.choice == 15:
            self.choice_type = ActionChoice.PASS
            self.choice_idx = -1
        elif self.choice == 16 or self.choice == 17:
            self.choice_type = ActionChoice.NONE
            self.choice_idx = -1
        elif self.choice == 18:
            self.choice_type = ActionChoice.CHARACTER_SKILL
            self.choice_idx = self.choice

        if self.target == 0:
                self.target_type = ActionTarget.OPPONENT
                self.target_idx = -1
        elif self.target == 1:
            self.target_type = ActionTarget.MYSELF
            self.target_idx = -1
        elif 2 <= self.target < 5:
            self.target_type = ActionTarget.MY_CHARACTER
            self.target_idx = self.target - 2
        elif 5 <= self.target < 9:
            self.target_type = ActionTarget.OPPONENT_SUMMON
            self.target_idx = self.target - 5
        elif 9 <= self.target < 13:
            self.target_type = ActionTarget.MY_SUPPORT_REGION
            self.target_idx = self.target - 9
        elif self.target == 13:
            self.target_type = ActionTarget.DICE_REGION
            self.target_idx = -1
        elif self.target == 14:
            self.target_type = ActionTarget.CARD_REGION
            self.target_idx = -1

    @staticmethod
    def from_tuple(action: tuple):
        '''
            (1, 1, list(n))
        '''
        return Action(action[0], action[1], action[2])

    @staticmethod
    def from_dict(action: dict):
        '''
            (1, 1, list(n))
        '''
        return Action(action['choice'], action['target'], action['dice'])
    
    @staticmethod
    def from_layout(game: 'GeniusGame', layout, jump=True):
        action = None
        history = []
        while action is None:
            if game.incoming_state:
                true_active_player = game.active_player
                true_active_player_index = game.active_player_index
                game.active_player = game.incoming_state.active_player
                game.active_player_index = game.incoming_state.active_player_index

            mask, use_dice = game.active_player.action_mask[:,:,0], game.active_player.action_mask[:,:,1:]
            choice_dict = {0:'打出本方第1张手牌',
                        1:'打出本方第2张手牌',
                        2:'打出本方第3张手牌',
                        3:'打出本方第4张手牌',
                        4:'打出本方第5张手牌',
                        5:'打出本方第6张手牌',
                        6:'打出本方第7张手牌',
                        7:'打出本方第8张手牌',
                        8:'打出本方第9张手牌',
                        9:'打出本方第10张手牌',
                        10:'使用出战角色第1个技能',
                        11:'使用出战角色第2个技能',
                        12:'使用出战角色第3个技能',
                        13:'使用出战角色第4个技能',
                        14:'切换角色',
                        15:'结束回合',
                        16:'选择操作本方骰子',
                        17:'选择操作本方手牌',
                        18:'使用特技'}
            history.append(f"您是{game.active_player_index}号玩家")
            choose_prompt = f"以下是你可以选择的行动,请输入一个数字表示你的行动选择(按确认以提交或清空选择):\n"
            choose_list = []
            last_choice = -1
            mask_sum = mask.sum(axis=1)
            for i in range(CHOICE_NUM):
                if mask_sum[i] >= 1:
                    choose_prompt = choose_prompt+str(i)+'.'+choice_dict[i]+'\n'
                    choose_list.append(i)
                    last_choice = i

            if len(choose_list) == 1:
                choice = last_choice
                print_prompt(layout, history, choose_prompt+'您目前只能选择如下行动:'+str(last_choice)+'.'+choice_dict[last_choice]+'\n')
                if jump and choice == 16:
                    return Action(16, 13, [])
                if jump and choice == 17:
                    return Action(17, 14, [])
            else:
                print_prompt(layout, history, choose_prompt)
                choice = int(user_input.get_sel('', choose_list))
            history.append("您选择的行动为:"+str(choice)+'.'+choice_dict[choice])

            target_dict = {0:'选择对方',
                        1:'选择本方',
                        2:'选择角色0',
                        3:'选择角色1',
                        4:'选择角色2',
                        5:'选择0号召唤',
                        6:'选择1号召唤',
                        7:'选择2号召唤',
                        8:'选择3号召唤',
                        9:'选择0号支援',
                        10:'选择1号支援',
                        11:'选择2号支援',
                        12:'选择3号支援',
                        13:'选择操作本方骰子',
                        14:'选择操作本方手牌'}
            target_prompt = '根据您选择的行动，您可以选择以下目标\n'
            target_list = []
            last_target = -1
            for i in range(TARGET_NUM):
                if mask[choice][i] == 1:
                    target_prompt = target_prompt+str(i)+'.'+target_dict[i]+'\n'
                    target_list.append(i)
                    last_target = i

            if len(target_list) == 1:
                target = last_target
                print_prompt(layout, history, target_prompt+'您目前只能选择如下目标:'+str(last_target)+'.'+target_dict[last_target]+'\n')
            else:
                print_prompt(layout, history, target_prompt)
                target = user_input.get_sel('', target_list)
            history.append("您选择的目标为:"+str(target)+'.'+target_dict[target])
            
            if choice == 16:
                list_prompt = f'您需要选择重新投掷的骰子的位置,形式如0 1 2所示,数值应该在{0}-{use_dice[choice][target][0]-1}之间:'
                dice = user_input.get_special_rng_mul_sel(list_prompt, min=0, max=use_dice[choice][target][0]-1)
            elif choice == 17:
                list_prompt = f'您需要选择重新获取的手牌的位置,形式如0 1 2所示,数值应该在{0}-{use_dice[choice][target][0]-1}之间:'
                dice = user_input.get_special_rng_mul_sel(list_prompt, min=0, max=use_dice[choice][target][0]-1)
            elif use_dice.sum() == 0:
                dice = []
            else:  # what is this?
                while True:
                    try:
                        dice = []
                        for i in range(2):
                            cost_num = use_dice[choice][target][i*2]
                            if cost_num != 0:
                                if use_dice[choice][target][i*2+1] < 0:
                                    cost_type = DiceType(-use_dice[choice][target][i*2+1])
                                    list_prompt = f'您需要选择使用的{cost_num}个非{cost_type}骰子的位置,形式如0 1 2所示:'
                                else:
                                    cost_type = CostType(use_dice[choice][target][i*2+1])
                                    list_prompt = f'您需要选择使用的{cost_num}个{cost_type}骰子的位置,形式如0 1 2所示:'
                                
                                print_prompt(layout, history, list_prompt)
                                sub_dice = user_input.get_rng_mul_sel(
                                    '', min=0, max=game.active_player.dice_zone.num()-1,
                                    assert_fn=lambda x: game.active_player.dice_zone.check_dice(x, cost_num, use_dice[choice][target][i*2+1]))
                                # sub_dice = [ int(i) for i in sub_dice.split()]
                                dice = dice + sub_dice

                        assert not check_duplicate_dice(dice)
                        break
                    except KeyboardInterrupt:
                        exit()
                    except:
                        print(layout, "您选择的骰子包含重复位置,非法,请重新选择")
            history.append("您选择的多目标为:"+str(dice))


            if game.incoming_state:
                game.active_player = true_active_player
                game.active_player_index = true_active_player_index
            action = Action(choice, target, dice)

            if game.game_phase == GamePhase.ACTION_PHASE:
                copy_game = game.copy_game()
                copy_game.step(action)
                old_dict = game.encoder_dict()
                new_dict = copy_game.encoder_dict()
                diff_zone = compare_dict(old_dict, new_dict)

                copy_layout = copy_game.encode_message(base=diff_zone)
                print_prompt(copy_layout, history, '预览效果,请按1确认进行行动')

                fix_input = input()
                fix_input = bool(int(fix_input))
                if not fix_input:
                    action = None
                    history = ["重新输入行动"]
        return action

    @staticmethod
    def from_input(game: 'GeniusGame', log=None, mode='a', jump=True):
        if game.incoming_state:
            true_active_player = game.active_player
            true_active_player_index = game.active_player_index
            game.active_player = game.incoming_state.active_player
            game.active_player_index = game.incoming_state.active_player_index

        mask, use_dice = game.active_player.action_mask[:,:,0], game.active_player.action_mask[:,:,1:]
        choice_dict = {0:'打出本方第1张手牌',
                       1:'打出本方第2张手牌',
                       2:'打出本方第3张手牌',
                       3:'打出本方第4张手牌',
                       4:'打出本方第5张手牌',
                       5:'打出本方第6张手牌',
                       6:'打出本方第7张手牌',
                       7:'打出本方第8张手牌',
                       8:'打出本方第9张手牌',
                       9:'打出本方第10张手牌',
                       10:'使用出战角色第1个技能',
                       11:'使用出战角色第2个技能',
                       12:'使用出战角色第3个技能',
                       13:'使用出战角色第4个技能',
                       14:'切换角色',
                       15:'结束回合',
                       16:'选择操作本方骰子',
                       17:'选择操作本方手牌',
                       18:'使用特技'}

        choose_prompt = f"您是{game.active_player_index}号玩家,以下是你可以选择的行动,请输入一个数字表示你的行动选择(按确认以提交或清空选择):\n"
        choose_list = []
        last_choice = -1
        mask_sum = mask.sum(axis=1)
        for i in range(CHOICE_NUM):
            if mask_sum[i] >= 1:
                choose_prompt = choose_prompt+str(i)+'.'+choice_dict[i]+'\n'
                choose_list.append(i)
                last_choice = i

        if len(choose_list) == 1:
            choice = last_choice
            print(choose_prompt+'您目前只能选择如下行动:'+str(last_choice)+'.'+choice_dict[last_choice]+'\n')
            if jump and choice == 16:
                return Action(16, 13, [])
            if jump and choice == 17:
                return Action(17, 14, [])
        else:
            choice = int(user_input.get_sel(choose_prompt, choose_list))

        target_dict = {0:'选择对方',
                       1:'选择本方',
                       2:'选择角色0',
                       3:'选择角色1',
                       4:'选择角色2',
                       5:'选择0号召唤',
                       6:'选择1号召唤',
                       7:'选择2号召唤',
                       8:'选择3号召唤',
                       9:'选择0号支援',
                       10:'选择1号支援',
                       11:'选择2号支援',
                       12:'选择3号支援',
                       13:'选择操作本方骰子',
                       14:'选择操作本方手牌'}
        target_prompt = '根据您选择的行动，您可以选择以下目标\n'
        target_list = []
        last_target = -1
        for i in range(TARGET_NUM):
            if mask[choice][i] == 1:
                target_prompt = target_prompt+str(i)+'.'+target_dict[i]+'\n'
                target_list.append(i)
                last_target = i

        if len(target_list) == 1:
            target = last_target
            print(target_prompt+'您目前只能选择如下目标:'+str(last_target)+'.'+target_dict[last_target]+'\n')
        else:
            target = user_input.get_sel(target_prompt, target_list)

        if choice == 16:
            list_prompt = f'您需要选择重新投掷的骰子的位置,形式如0 1 2所示,数值应该在{0}-{use_dice[choice][target][0]-1}之间:'
            dice = user_input.get_special_rng_mul_sel(list_prompt, min=0, max=use_dice[choice][target][0]-1)
        elif choice == 17:
            list_prompt = f'您需要选择重新获取的手牌的位置,形式如0 1 2所示,数值应该在{0}-{use_dice[choice][target][0]-1}之间:'
            dice = user_input.get_special_rng_mul_sel(list_prompt, min=0, max=use_dice[choice][target][0]-1)
        elif use_dice.sum() == 0:
            dice = []
        else:  # what is this?
            while True:
                try:
                    dice = []
                    for i in range(2):
                        cost_num = use_dice[choice][target][i*2]
                        if cost_num != 0:
                            if use_dice[choice][target][i*2+1] < 0:
                                cost_type = DiceType(-use_dice[choice][target][i*2+1])
                                list_prompt = f'您需要选择使用的{cost_num}个非{cost_type}骰子的位置,形式如0 1 2所示:'
                            else:
                                cost_type = CostType(use_dice[choice][target][i*2+1])
                                list_prompt = f'您需要选择使用的{cost_num}个{cost_type}骰子的位置,形式如0 1 2所示:'
                            sub_dice = user_input.get_rng_mul_sel(
                                list_prompt, min=0, max=game.active_player.dice_zone.num()-1,
                                assert_fn=lambda x: game.active_player.dice_zone.check_dice(x, cost_num, use_dice[choice][target][i*2+1]))
                            # sub_dice = [ int(i) for i in sub_dice.split()]
                            dice = dice + sub_dice

                    assert not check_duplicate_dice(dice)
                    break
                except KeyboardInterrupt:
                    exit()
                except:
                    print("您选择的骰子包含重复位置,非法,请重新选择")
        if log is not None:
            log.append({"choice":choice, "target":target, "dice":dice})
            with open("./action.log", mode) as f:
                json.dump(log, f, indent=4)

        if game.incoming_state:
            game.active_player = true_active_player
            game.active_player_index = true_active_player_index
        return Action(choice, target, dice)

def choose_card(card: List[int]):
    return Action(17, 14, card)

def choose_dice(dice: List[int]):
    return Action(16, 13, dice)

def choose_character(idx: int):
    return Action(14, idx+2, dice=[])