import functools

def change_reporter(func):
    def wrapper(*args, **kwargs):
        wrapper.changes = []
        return func(*args, **kwargs)
    return wrapper

def xor(bool_1: bool, bool_2: bool) -> bool:
    if (not bool_1 and bool_2) or (bool_1 and not bool_2): return True
    return False

def args_validator(**validators):
    def decorator(func):
        arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(len(args)):
                name = arg_names[i]
                if validators.__contains__(name) and not validators[name](args[i]):
                    raise InvalidArgumentException(f"Argument nie spełnia wymagania: {args[i]}")
            for arg in kwargs.keys():
                if validators.__contains__(arg) and not validators[arg](kwargs[arg]):
                    raise InvalidArgumentException(f"Argument nie spełnia wymagania: {kwargs[arg]}")
            return func(*args, **kwargs)
        return wrapper
    return decorator