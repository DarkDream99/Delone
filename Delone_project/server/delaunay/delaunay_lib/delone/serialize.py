from .event import Event
from .locator import Node


def serialize(obj):
    if isinstance(obj, Event):
        if obj.data is None:
            data = {}
        else:
            data = obj.data
        return f"{{\"type\": \"{obj.type}\", \"data\": {data}, \"description\": \"{obj.description}\" }}"

    if isinstance(obj, Node):
        return str(obj)

    print(obj)
    raise TypeError(
        "Unserializable object {} of type {}".format(obj, type(obj))
    )
