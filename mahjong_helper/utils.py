import sys

def eprint(*args, **kwargs):    # for debugging
    print(*args, file=sys.stderr, **kwargs)