import os
import cv2
card_path = "../assets/cards"  # 卡牌图片文件夹
character_path = "../assets/characters"  # 角色图片文件夹


class img_to_deck:
    """
    将原神游戏本体中导出的卡组图片转化为代码可读取的数据。
    目前仅支持读取图片文件名并存到列表中。
    """
    def __init__(self, img):
        # 一些magic number，主要是卡组导出图片的位置特征
        self.img = cv2.imread(img)
        self.full_card_list = os.listdir(card_path)
        self.full_character_list = os.listdir(character_path)
        self.character_size = (144, 240)  # 角色图大小
        self.character_to_top = 176  # 角色图到画面顶端距离
        self.character_to_left = 352  # 最左侧的角色图到画面左侧距离
        self.character_d = 20  # 角色图间距
        self.character_num = 3  # 角色数量
        self.card_size = (96, 160)  # 卡牌图片大小
        self.card_x_num = 6  # 横向卡牌数量
        self.card_y_num = 5  # 纵向卡牌数量
        self.card_x = 520  # 卡牌到画面顶端距离
        self.card_y = 250  # 最左侧的卡牌图到画面左侧距离
        self.card_d = 18  # 卡牌间距（横向纵向均为18像素）
        self.character_list = []
        self.card_list = []

    def to_single_channel(self, img):
        # 将图片转为单通道灰度图
        if img is None:
            raise Exception("to_single_channel函数报错：未检测到图片")
        if len(img.shape) < 3:
            return img
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return img

    def template_compare(self, target, img):
        # 使用模板匹配方法 TM_CCOEFF_NORMED
        target = self.to_single_channel(target)
        img = self.to_single_channel(img)
        result = cv2.matchTemplate(target, img, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        return max_val

    def get_characters(self):
        # 获取角色列表
        for i in range(self.character_num):
            # 裁剪当前角色完整图片
            x = self.character_to_top
            y = self.character_to_left + i * (self.card_d + self.character_size[0])
            character_img = self.img.copy()[x:x+self.character_size[1], y:y+self.character_size[0]]
            # 进行模板匹配，选择匹配值最大的作为结果
            max_val = 0.0
            target_character = None
            for character in self.full_character_list:
                target = cv2.imread(os.path.join(character_path, character))
                target = cv2.resize(target, self.character_size)
                tmp = self.template_compare(target, character_img)
                if tmp > max_val:
                    max_val = tmp
                    target_character = character
            # 将结果加入到列表中
            assert target_character is not None
            target_character = target_character.split(".")[0]
            print("检测到角色：%s" % target_character)
            self.character_list.append(target_character)

    def get_cards(self):
        # 获取卡牌列表
        for i in range(self.card_y_num):
            for j in range(self.card_x_num):
                # 裁剪当前卡牌完整图片
                x = self.card_x + i * (self.card_d + self.card_size[1])
                y = self.card_y + j * (self.card_d + self.card_size[0])
                card_img = self.img.copy()[x:x + self.card_size[1], y:y + self.card_size[0]]
                # 进行模板匹配，选择匹配值最大的作为结果
                max_val = 0.0
                target_card = None
                for card in self.full_card_list:
                    target = cv2.imread(os.path.join(card_path, card))
                    target = cv2.resize(target, self.card_size)
                    tmp = self.template_compare(target, card_img)
                    if tmp > max_val:
                        max_val = tmp
                        target_card = card
                # 将结果加入到列表中
                assert target_card is not None
                target_card = target_card.split(".")[0]
                print("检测到卡牌：%s" % target_card)
                self.card_list.append(target_card)


if __name__ == '__main__':
    # 使用示例
    test = img_to_deck("../assets/test.jpg")
    test.get_cards()
    test.get_characters()
    print(test.character_list)
    print(test.card_list)
