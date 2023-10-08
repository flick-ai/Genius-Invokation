from typing import Type

class A:
    a = 2
    @staticmethod
    def d():
        return 5

    @classmethod
    def aa(cls):
        print(cls.a)

class B(A):
    a = 1
    @staticmethod
    def d():
        return B.a
    # @classmethod
    # def aa(cls):
    #     print(4)

B.aa()

a: Type[A] = B

print(a)
