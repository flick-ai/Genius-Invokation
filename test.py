import numpy as np

a = [1,2,3,4,5]
# np.random.shuffle(a)
a.insert(5,6)
print(a)

a = []

class A:
    def __init__(self):
        self.a = []
        self.b = 2
    
    def aaa(self):
        self.a.append(A())

alist = A()
alist.aaa()
print(alist.a[0].aaa)