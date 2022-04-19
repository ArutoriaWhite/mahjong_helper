from cProfile import run


def run_first (marg):
    def deco (func):
        def wrapper ():
            print('Hi, I am')
            marg()
            func()
        return wrapper
    return deco

def f1():
    print('i am f1')

@run_first(f1)
def f2():
    print('i am f2')

f2()
