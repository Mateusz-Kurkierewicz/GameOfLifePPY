from src.observer.event import Event


class Observer:

    def on_event(self):
        pass


class Observable:

    def __init__(self):
        self.observers = []

    def add_observer(self, observer: Observer):
        if type(observer) != Observer:
            raise TypeError("Obiekt dodawany jako obserwujący musi dziedziczyć po klasie Observer!")
        self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        self.observers.remove(observer)

    def call_observers(self, event: Event):
        for o in self.observers:
            o.on_event()