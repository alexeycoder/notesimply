import functools


def once(fn):
    called = False

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        nonlocal called
        if called:
            return
        called = True
        res = fn(*args, **kwargs)
        assert res is None

    return wrapper
