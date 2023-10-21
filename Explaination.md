# Genius-Invokation Environment Base Architecture

#  七圣召唤环境构建

## 1. Class: GeniusGame ， GeniusGame 类

### 1.1 Game Phase, 游戏阶段

In a `Game`, we have 5 different phase in total. 在 `Game` 类中，我们共有5个不同的阶段：

-   *SET_CARD* ：The phase of choosing hand cards, 选择手牌阶段
    -   At the start of a game. 游戏开始时。Choose initial hand cards. 选择初始手牌。
    -   EventCard `Nature and Wisdom`. 事件牌“草与智慧”。Insert a special phase of *SET_CARD*， 插入一个特殊的选择手牌阶段。
-   *SET_CHARACTER*: The phase of choosing active character，选择出战角色阶段。
    -   After choosing initial hand cards. 选择初始手牌后。Choose initial active character. 选择初始出战角色。
    -   When an active character dies. 在某个出战角色死亡时。Choose the new active character. 选择一个新的出战角色。
-   *ROLL_PHASE*: 投掷阶段
    -   Begin of each round. 每个回合开始时。
    -   `Toss-up`, `Knights of Favonius Library` are played.  "一掷乾坤", "骑士团图书馆" 打出之时。Insert a special phase. 插入一个特殊阶段。
-   *ACTION_PHASE*: 行动阶段
    -   In each *ACTION_PHASE* ， two player act alternately. 在每一个行动阶段，双方轮流行动。
-   *END_PHASE*: 回合结束阶段

### 1.2 Attributes, 属性

-   `first_player`: which player acts first in this round，当前轮次内先手。 (Index only,  只记录了序号)
-   `active_player`: which player is active. 当前行动角色。 (Instance of `GeniusPlayer`)
-   `active_player_index`: the index of active player. 当前行动角色编号。
-   `player0`, `player1`: two player instance. 2个玩家实例。
-   `players=[player0, player1]`:  list of players，玩家列表。
-   `game_phase` Game Phase, 游戏阶段。
-   `special_phase`: The insert special phase to deal, default as `None`. 需要处理的插入阶段，默认为`None`.
-   `round`: round of the game, 游戏轮次。
-   `current_dice`:  # TODO
-   `current_action`:
-   `current_damage`: 
-   `current_skill`:
-   `current_card`:
-   `damage_list`:
-   `is_changed_player`:
-   `is_end`:
-   `manager`: 



## 2. Class GeniusPlayer, GeniusPlayer 类

In a game, we have 2 players, which are instances of class `GeniusPlayer`. 一局游戏里，每个玩家时一个`GeniusPlayer`类的实例。

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



## 3. Class Entity, Entity 类

All of `Status`, `Shield`,  `Combat_Status`, `Combat_Shield`, `Summon`, `Support`,  `Weapon`, `Artifact` and `Character` are entities (subclass of `Entity`). 包括状态、护盾、出战状态、出战护盾，召唤物，支援物，武器，圣遗物，角色在内的对象均为实例，是`Entity`类的子类。

### 3.1 Class Status， Status 类

Class of character status, maintain in `Character_Zone` of each `Character`. 角色状态类，在每个角色的角色区内维护。

#### 3.1.1 Class Shield, Shield 类

Same as `Status`. Design for shield on single character. 和角色状态一致，用于附着在单个角色的盾。

### 3.2 Class Combat_Status, Combat_Status 类

Class of `Combat_Status`, maintain in `Team_Combat_Status_Zone`. 出战状态类，在出战状态区内。

#### 3.2.1 Class of Combat_Shield, Combat_Shield 类

Same as `Combat_Status` for shields.  与出战状态一致，用于盾。

### 3.3 Class Summon， Summon 类

Class of `Summon`, lying in `Summon_Zone`. 召唤物类，置于召唤物区。

### 3.4 Class Support, Support 类

Class of `Support`, lying in `Support_Zone`。 支援，于支援区。

### 3.5 Class Weapon, Weapon 类

Class of weapon, stored the card information of the weapon. 武器类，存有武器牌信息。

### 3.6 Class Artifact, Artifact 类

Similar with `weapon`. 与武器类似。 Not Implement Yet. 还未实现。 

### 3.7 Class Character, Character 类

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

#### 3.7.1 Class CharacterZone, CharacterZone 类

This zone contains `Weapon`, `Artifact`, `Status` List. 该区域包含装备的武器牌，圣遗物牌，角色状态列表。



## 4. Event System, 事件系统

Event System provides the simulator with the event listening (`listen`), event triggering (`invoke`) functions. When an event occurs, the `listener` can be notified to perform a predefined `action`. 事件系统为模拟环境提供了事件监听 (`listen`) 和触发 (`invoke`) 功能。在事件 (`event`) 发生时，可以通知监听者 (`listener`) 执行预定义的动作 (`action`)。

The event system provides unified management and triggering mechanism for tasks with uncertain source, quantity, frequency, and timing. 事件系统提供了不确定来源、数量、次数、时机的任务的统一管理、触发机制。



### 4.1 Event, 事件

Event represents some abstract timing. 事件代表某种抽象时刻。

We can treat any gaps during execution as events. 我们可以把代码执行的任何间隔时刻当作事件。

Here are the `Event` used in the project： 一下为我们使用到的事件： `Enum: EventType`

-   `BEGIN_ROLL_PHASE` 开始投掷阶段
-   `BEGIN_ACTION_PHASE` 开始行动阶段 
-   `CALCULATE_DICE` 计算骰子需求
-   `ON_PLAY_CARD` 打出手牌
-   `AFTER_PLAY_CARD`打出手牌后
-   `ON_USE_SKILL`执行技能
-   `AFTER_USE_SKILL`执行技能后
-   `ON_CHANGE_CHARACTER` 切换角色
-   `AFTER_CHANGE_CHARACTER` 切换角色后
-   `END_PHASE` 结束阶段
-   `AFTER_TAKES_DMG` 受到伤害后
-   `DAMAGE_ADD`计算伤害增加量
-   `DAMAGE_ADD_AFTER_REACTION`: 计算由于触发反应引起的加伤。 e.g. `Elemental Resonance: Fervent Flames` 例如：`元素共鸣：热诚之火`。
-   `DEALING_DAMAGE`: 结算伤害时，for Mona only right now, 现仅对莫娜起作用
-   `INFUSION`: 伤害元素附着
-   `EXECUTE_DAMAGE`: 执行伤害时，Calculate the damage discount from shield and status, 计算由盾、状态产生的伤害减免。
-   `CHARACTER_DIE` 角色死亡时
-   `BEFORE_ANY_ACTION` 任意行动之前
-   `AFTER_ANY_ACTION`任意行动之后
-   `ON_SUMMON_REMOVE`召唤物移除时
-   `ELEMENTAL_APPLICATION_REACTION`: The timing that a reaction is triggered by an elemental application (no damage).  附着元素造成反应之时（无伤害）。

### 4.2 Event Execution Order 事件执行顺序

The execution order is defined by the priority of zones. 执行顺序由各区域的优先级确定。 

As far as we known, the priority is as bellow: 具我们所知，优先级按下列排列：

-   `CHARACTER_ZONE` $0$ 
-   `ACTIVE_ZONE_SHIELD` $1$ 
-   `ACTIVE_ZONE` $2$
-   `SUMMON_ZONE`: $3$
-   `SUPPORT_ZONE`: $4$

In the same priority, the event registered earlier will be triggered earlier, too. 在同一优先级内，先注册的事件会优先执行。

###4.3  Listen 监听

-   Each entity may need to be listened at some specific event timing. 每个实例都有可能需要在某些时刻被监听。

-   Please maintain the listener list of each `Entity`: `listeners` in its function `update_listener_list`. 请对每个需要监听的`Entity`对象维护 listener 列表: 在所属函数`update_listener_list`中维护`listeners`。

-   The list consists tuples: (`EventType`, `ZoneType`, `ACTION`)，the `ACTION` is the called function when the event is invoked. 这个列表由一个或多个三元组构成，(`EventType`, `ZoneType`, `ACTION`), 其中， `ACTION` 为触发时调用的函数。

-   ·`ACTION` always has the only input param: `game`. `ACTION`的输入总是只有`game`一项。

### 4.4 Invoke 触发

You only need to give the `event`to  the event manager, the `ACTION`s will automatically invoked. 仅需将需要触发的事件发送给事件管理器，对应的函数将自动触发。



## 5. Damage 伤害

## 6. Dice 骰子

## 7. Skill 技能

## 8. Card 牌

