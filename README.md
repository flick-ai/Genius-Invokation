# Genius-Invokation
七圣召唤强化学习环境

[Document]()

## 本地运行

### `Install environment`

    pip install -r requirments.txt
    pip install -e .


### `Fix deck`
    在 genius_invocation/main.py 中修改 deck1 和 deck2 来确定两位 player 的出战牌组。 目前您可以任意组合您的手牌选择。

### `Play game`

    python main.py 来游玩我们的游戏。我们有三种形式的信息输出：

    1. logoru.logger: 用于进行关键步骤的输出