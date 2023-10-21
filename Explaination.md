# Genius-Invokation Environment Base Architecture

#  七圣召唤环境构建

## 1. Class: Game ， Game 类

In a `Game`, we have 5 different phase in total. 在 `Game` 类中，我们共有5个不同的阶段：

-   *SET_CARD* ：The phase of choosing hand cards, 选择手牌阶段
    -   At the start of a game. 游戏开始时。Choose initial hand cards. 选择初始手牌。
    -   EventCard `Nature and Wisdom`. 事件牌“草与智慧”。Insert a special phase of *SET_CARD*， 插入一个特殊的选择手牌阶段。
-   *SET_CHARACTER*: The phase of choosing active character，选择出战角色阶段。
    -   After choosing initial hand cards. 选择初始手牌后。Choose initial active character. 选择初始出战角色。
    -   When an active character dies. 在某个出战角色死亡时。Choose the new active character. 选择一个新的出战角色。
-   *ROLL_PHASE*: 掷骰子阶段
    -   Begin of each round. 每个回合开始时。
    -   `Toss-up`, `Knights of Favonius Library` are played.  "一掷乾坤", "骑士团图书馆" 打出之时。Insert a special phase. 插入一个特殊阶段。
-   *ACTION_PHASE*: 行动阶段
    -   In each *ACTION_PHASE* ， two player act alternately. 在每一个行动阶段，双方轮流行动。
-   *END_PHASE*: 回合结束阶段



## Class Player, Player 类

In a game, we have 2 players, which are instances of class `Player`. 一局游戏里，每个玩家时一个`Player`类的实例。

We maintain some global team state in this class: 我们在这个类中维护了一些全队的状态：

-   `is_pass` The player has finished its action in this round. 玩家已结束该回合行动。
-   `play_arcane_legend`： The player has played one of `arcane legend` cards. 玩家已打出一张秘传牌。
-   `is_after_change`: The player just finishs an action of change character. 玩家刚进行了切人操作。 Used to check `plunging attack`， 用于判断下落攻击。
-   `is_quick_change`: The action of changing character is an quick action. 切人操作为快速行动。
-   `change_num`: The number of change character in a round. 该回合内切人数量。 Used to check `Red Feather Fan`. 用于确认 “红羽团扇”的触发。
-   Maybe more to come. 可能未来会新增内容。

The other states are divided in to the following zones: 剩余的状态被划分到一下几个区域内：

-   *Card_Zone*：牌库， Number of remaining cards. 牌库剩余牌数。
-   *Hand_Zone*： 手牌区。
-   *Team_Combat_Status_Zone*: 队伍状态区： We may call it *Active_Zone* for convience, which contains `Combat_Status` . 我们简称其为出战状态区，其中包含 `出战状态`。
-   `Dice_Zone`: 骰子区。
-   `Support_Zone`: 支援区。
-   `Summon_Zone`: 召唤物区。

A player has a character list, instances of `Character` are in it. 每一个玩家有一个角色列表，每一个均为一个`Character`实例。



## Class Entity, Entity 类

All of `Status`, `Shield`,  `Combat_Status`, `Combat_Shield`, `Summon`, `Support`,  `Weapon`, `Artifact` and `Character` are entities (subclass of `Entity`). 包括状态、护盾、出战状态、出战护盾，召唤物，支援物，武器，圣遗物，角色在内的对象均为实例，是`Entity`类的子类。

### Class Status， Status 类

Class of character status, maintain in `Character_Zone` of each `Character`. 角色状态类，在每个角色的角色区内维护。

#### Class Shield, Shield 类

Same as `Status`. Design for shield on single character. 和角色状态一致，用于附着在单个角色的盾。

### Class Combat_Status, Combat_Status 类

Class of `Combat_Status`, maintain in `Team_Combat_Status_Zone`. 出战状态类，在出战状态区内。

#### Class of Combat_Shield, Combat_Shield 类

Same as `Combat_Status` for shields.  与出战状态一致，用于盾。

### Class Summon， Summon 类

Class of `Summon`, lying in `Summon_Zone`. 召唤物类，置于召唤物区。

### Class Support, Support 类

Class of `Support`, lying in `Support_Zone`。 支援，于支援区。

### Class Weapon, Weapon 类

Class of weapon, stored the card information of the weapon. 武器类，存有武器牌信息。

### Class Artifact, Artifact 类

Similar with `weapon`. 与武器类似。 Not Implement Yet. 还未实现。 

## Class Character, Character 类

Each character should has the following attributes: 每个角色需要维护以下属性:

-   `id`: Indentity Document. 角色卡牌编号
-   `name`: name, 姓名
-   `element`: element type, 元素类别。
-   `weapon_type`: weapon type, 武器类别。
-   `country`: country, 所属国家。
-   `health_point`： current health point，当前血量。
-   `init_health_point`: init health point. 初始血量。
-   `max_health_point`: max health point. 血量上限。
-   `skill_list`: list of skills, containing several `CharacterSkill` class. 技能列表，包含若干个“角色技能”类。
-   `skills`: list of instances of skill, the instance can be called by game. 技能实例列表，每个实例均可以被游戏调用。
-   `power`: current power, 角色当前充能数。
-   `max_power`：max power, 角色充能上限。
-   `element_application`: list, element applications on the character. 列表，当前角色的附着元素。
-   `index`： index of the character in the player's character list. 该角色在玩家在角色列表中的编号。
-   `talent`: whether equips talent. 是否装有天赋。
-   `is_active`: whether the active character. 是否出战。
-   `is_alive`: whether alive. 是否存活。
-   `is_frozen`: whether frozen. 是否冻结。
-   `is_satisfied`: whether satisfies. 是否饱腹。
-   `character_zone`: Character Zone,  角色区域。

In this base class, several basic operations have been defined. 在该基类中，定义了许多基本操作。

More detail could be viewed in 更多信息可以在以下文件中查看： `genius_invocation/entity/character.py`。 

### Class CharacterZone, CharacterZone 类

This zone contains `Weapon`, `Artifact`, `Status` List. 该区域包含装备的武器牌，圣遗物牌，角色状态列表。



## Event System, 事件系统

