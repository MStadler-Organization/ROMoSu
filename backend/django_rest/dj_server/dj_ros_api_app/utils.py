from json import JSONEncoder


class DefaultEncoder(JSONEncoder):
    """Helps to serialize complex object dictionaries to json"""

    def default(self, o):
        return o.__dict__
