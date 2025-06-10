import functools

from src.exceptions import InvalidArgumentException


def change_reporter(func):
    """Rejestrator zmian
    Dekoruje funkcję, która może zapisywać jakieś zmiany, które
    zaszły w wyniku jej wykonania.
    Args:
        func: Funkcja, która może zapisywać jakieś zmiany
    """
    def wrapper(*args, **kwargs):
        wrapper.changes = []
        return func(*args, **kwargs)
    return wrapper

def args_validator(**validators):
    """Walidator argumentów
    Weryfikuje, czy podane argumenty spełniają przekazane wymogi
    Args:
        validators: Funkcje, które weryfikują argumenty
    """
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