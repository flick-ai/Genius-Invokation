# from genius_invocation.game import GeniusGame, ActiveDie
# import threading

# # 创建一个多线程来运行游戏
# class GameThread(threading.Thread):
#     def __init__(self, game: GeniusGame):
#         threading.Thread.__init__(self)
#         self.game = game

#     def run(self):
#         self.game.run()
import os
from utils import *

if __name__ == '__main__':
    base_dir = './Test'
    package_dirs = ["./card/character/characters","./card/action/support/companion",
                    "./card/action/support/item","./card/action/support/location",
                    "./card/action/event/events","./card/action/event/foods",
                    "./card/action/event/elemental_resonance", "./card/action/event/arcane_legend",
                    "./card/action/equipment/artifact/artifacts",
                    "./card/action/equipment/talent/talents",
                    "./card/action/equipment/weapon/weapons"]
    for package_dir in package_dirs:
        available_name = [f for f in os.listdir(package_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
        target_dir = base_dir + package_dir.split('.')[-1]
        target_names = ['test_'+ f for f in available_name]
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        for target_name in target_names:
            name = os.path.join(target_dir, target_name)
            with open(name, 'w') as f:
                pass



