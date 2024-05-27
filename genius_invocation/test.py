# from genius_invocation.game import GeniusGame, ActiveDie
# import threading

# # 创建一个多线程来运行游戏
# class GameThread(threading.Thread):
#     def __init__(self, game: GeniusGame):
#         threading.Thread.__init__(self)
#         self.game = game

#     def run(self):
#         self.game.run()

if __name__ == '__main__':

    import random
    source_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    idx = random.randint(11-5, 11)
    source_list.insert(11, 11)
    print(source_list)


