# Genius-Invokation
七圣召唤强化学习环境

[Document]() | [详细信息文档](https://j0mmhq251c1.feishu.cn/drive/folder/Xl6ZfevqplEfNud10YLcgP44nGh?from=from_copylink) | Attach(qq:192339964)

## 介绍

我们的项目目标是基于python搭建原神七圣召唤游戏的RL对战环境，并基于AI和RL技术训练七圣召唤的AI牌手。目前我们实现了原神七圣召唤游戏的主要功能。由于我们的贡献者都是出于热爱的工作，精力有限，目前只实现了部分卡片的实现，但需要的主要接口都已完成。如果您在体验过程中发现有任何bug或者实现了部分卡片的功能，请及时联系我们。我们的文档

预期工作阶段：
1. 实现Genius Invokation的主要接口 [已完成]
2. 完成与游戏进度同步的卡片更新 [进行中]
3. 搭建本地终端和网页端的对战环境 [进行中]
4. 基于该环境进行RL的AI训练

## 本地运行

### `Install environment`

    pip install -r requirments.txt
    pip install -e .


### `Fix deck`

    在 genius_invocation/main.py 中修改 deck1 和 deck2 来确定两位 player 的出战牌组。 目前您可以任意组合您的手牌选择。

### `Play game`

    python main.py 来游玩我们的游戏。我们有三种形式的信息输出：

    1. logoru.logger: 用于进行关键步骤的输出
    2. print: 用于告知玩家Action
    3. rice.Layout: 展示对战信息
