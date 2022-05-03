import time

def timeit(func):
    def wrapper(*args, **kw):
        start = time.perf_counter()
        res = func(*args, **kw)
        end = time.perf_counter()
        print('[Function: ' + func.__name__ + ' took ' + str(end - start) + ' seconds to complete]')
        return res
    return wrapper
