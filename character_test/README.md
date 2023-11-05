# 单元测试
## 单元测试文件的组成部分
### 单元测试声明
为便于维护，每个单元测试文件应在开头声明游戏版本号和使用的卡牌，以供参考。例如：
```py
"""
game_version: 4.1
card_involved:
- Timmie
"""
```
其中，`game_version`为该单元测试所基于的游戏版本号，`card_involved`为单元测试中使用的卡牌。其中，仅使用通用普通攻击或未使用技能，且未触发角色特殊效果的角色牌无需包含。行动牌只需包含测试中实际打出的行动牌。

### 调用库
```py
import unittest
from typing import List, Dict, Tuple, Optional, Union

from test_base import TestBase
from test_utils import *
from genius_invocation.game.action import *
```

### 测试类
单元测试类应继承自TestBase和unittest.TestCase。例如：
```py
class TestTimmie(TestBase, unittest.TestCase):
```

在单元测试类中，可以定义以下变量：
- `player0_deck`、`player1_deck`：对战双方卡组（必要）
- `seed`：随机数种子（可选，默认使用系统时间）
- `is_omni`：是否为全万能骰（可选，默认为False）

### 测试函数
在单元测试类中定义测试函数，命名为`test()`。

测试函数中可以使用以下常用函数：
- `self.initialize_game()`：初始化游戏
- `self.run_actions_for_player(actions, player_idx)`：为指定的玩家执行操作，另一方空过
- `self.run_actions_double(self, player0_actions, player1_actions)`：为双方分别运行操作
- `self.assertEqual(a,b)`：确认a和b相等

### 主函数
主函数位于文件末尾，测试类外面，用来从命令行启动测试函数。
```py
if __name__ == '__main__':
    unittest.main()
```

## 批量运行测试
在 Windows 上，可以通过以下 powershell 命令运行所有测试：
```powershell
foreach($f in ls test/*.py -File) {echo $f; python3 $f}
```

在 Mac 和 Linux 上，可以通过以下 bash 命令运行所有测试：
```bash
for f in test/*.py; do echo "$f"; python3 "$f"; done
```

以上命令请在 git 仓库根目录下运行，会查找并运行test文件夹中的所有py文件。