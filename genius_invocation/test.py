from genius_invocation.game import GeniusGame, ActiveDie
import threading

# 创建一个多线程来运行游戏
class GameThread(threading.Thread):
    def __init__(self, game: GeniusGame):
        threading.Thread.__init__(self)
        self.game = game

    def run(self):
        self.game.run()
