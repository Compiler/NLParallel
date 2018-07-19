from multiprocessing import *

class Foo:
    def __init__(self, n):
        self.n = n
    def __repr__(self):
        return "Foo(%d)" % self.n

manager = Manager()
aylmao = manager.dict()

def test(a):
    aylmao[str(a)] = Foo(a)

d = [1,2,3,4,5,6,7,8,9]
pool = Pool(cpu_count() * 2)
pool.map(test, d)

print(aylmao)
