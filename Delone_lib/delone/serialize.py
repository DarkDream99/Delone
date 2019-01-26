from .event import Event


def serialize(obj):
    if isinstance(obj, Event):
        return f"{{type={obj.type}, data={obj.data}, description={obj.description} }}"

    return obj.__dict__
