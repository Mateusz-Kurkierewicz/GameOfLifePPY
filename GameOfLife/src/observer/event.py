from typing import Final


class EventType:

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class Event:

    def __init__(self, ev_type: EventType):
        self.ev_type = ev_type


class EventTypes:

    PROPERTY_CHANGE_EVENT: Final[EventType] = EventType("property_change")
    BOARD_UPDATE_EVENT: Final[EventType] = EventType("board_update")
    GAME_COMPLETE_EVENT: Final[EventType] = EventType("game_complete")


class PropertyChangeEvent(Event):

    def __init__(self, obj):
        super().__init__(EventTypes.PROPERTY_CHANGE_EVENT)
        self.obj = obj


class BoardUpdateEvent(Event):

    def __init__(self, column: int, row: int, alive: bool):
        super().__init__(EventTypes.BOARD_UPDATE_EVENT)
        self.column = column
        self.row = row
        self.alive = alive


class GameCompleteEvent(Event):

    def __init__(self):
        super().__init__(EventTypes.GAME_COMPLETE_EVENT)