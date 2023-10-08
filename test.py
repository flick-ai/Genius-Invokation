import numpy as np

class Lu:
    @staticmethod
    def pr():
        print(np.random.choice(range(30), 5))

eval('Lu').pr()