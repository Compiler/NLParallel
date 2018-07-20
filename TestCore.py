from multiprocessing import *
from functools import partial
from itertools import repeat
class Foo:
    def __init__(self, n):
        self.n = n
    def __repr__(self):
        return "TopicNode(%d)" % self.n


aylmao ={}

def test(a, q):
	print('1')
	s = q.get()
	print(s)
	s[str(a)] = Foo(a)
	pritn('2')

if __name__ == '__main__':
	m = Manager()
	q = m.Queue()
	aylmao = Manager().dict()
	q.put(aylmao)
	d = [1,2,3]
	pool = Pool(cpu_count() * 2)
	pool.starmap(test, zip(d, repeat(q)))
	print(aylmao)
	print(q.get())
