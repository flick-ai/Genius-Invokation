import numpy as np

a = [1,2,3,4,5]
# np.random.shuffle(a)
a.insert(5,6)
print(a)

a = []

class A:
    def __init__(self):
        self.a = 1
        self.b = 2
    
    def aaa(self):
        a.append(A())

A().aaa()
print(a)