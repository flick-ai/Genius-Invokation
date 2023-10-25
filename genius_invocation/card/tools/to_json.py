from genius_invocation.utils import *


class foo:
    def __init__(self):
        self.a = "1234"
        self.b = 234
        self.c = [1, "32", self.b]
        self.d = bar(12)
        self.e = {1: 3, 5: 0}
        self.f = ElementType.GEO

    def to_json(self):
        # 创建一个空字典用于存储json数据
        json_data = {}
        # 遍历类的所有成员变量
        for attr, value in self.__dict__.items():
            json_data[attr] = object_to_json(value)
        # 返回json格式的字符串
        return json_data


class bar:
    def __init__(self, value):
        self.value = value
        self.key = "key"
        self.element = [ActionTarget.CARD_REGION, ActionChoice.PASS, DiceType.DENDRO]

    def to_json(self):
        # 创建一个空字典用于存储json数据
        json_data = {}
        # 遍历类的所有成员变量
        for attr, value in self.__dict__.items():
            json_data[attr] = object_to_json(value)
        # 返回json格式的字符串
        return json_data


def object_to_json(item):
    # 如果成员变量为常数，字符串等，则直接转为"变量名": 值
    if isinstance(item, (int, float, bool, str)):
        return item
    # 如果成员变量为列表，则转为["0": 值, "1": 值, ... ]
    elif isinstance(item, list):
        return [object_to_json(i) for i in item]
    # 如果成员变量为字典，则转为{"key0": 值, "key1": 值, ... }
    elif isinstance(item, dict):
        return item
    # 如果成员变量为枚举，则转为对应的num
    elif isinstance(item, Enum):
        return {"enum_type": type(item).__name__, "enum_name": item.name}
    # 如果成员变量为class类，则转为"类名": 类.to_json()
    elif isinstance(item, object):
        return {type(item).__name__: item.to_json()}


if __name__ == "__main__":
    test = foo()
    data = test.to_json()
    print(data)
    with open("test.json", "w") as f:
        json.dump(data, f, indent=4)

    with open("test.json") as f:
        data = json.load(f, object_hook=decode_enum)
        print(data)
