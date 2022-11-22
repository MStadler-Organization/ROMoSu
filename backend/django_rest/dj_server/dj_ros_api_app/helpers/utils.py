import logging
from json import JSONEncoder


class NotFoundError(Exception):
    """A custom error if nothing is found in the DB"""
    pass


def singleton(class_):
    """Introduces a singleton decorator"""

    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


class DefaultEncoder(JSONEncoder):
    """Helps to serialize complex object dictionaries to json"""

    def default(self, o):
        return o.__dict__


def get_base_topic_string(p_topic_string):
    """Takes a topic string and returns the base topic string. E.g., /tb3_2/joint_states => tb3_2"""

    # remove preceding slash
    trunc_topic_name = p_topic_string[1:]
    # check if topic is a root-topic
    if trunc_topic_name.count('/') > 0:
        # no root-topic, get base topic
        trunc_topic_name = trunc_topic_name[:trunc_topic_name.index('/')]

    return trunc_topic_name


def get_sub_topic_string(p_topic_string):
    """Takes a topic string and returns the next sub-topic string. E.g., /tb3_2/joint_states => joint_states"""

    # check if subtopic is possible
    if not p_topic_string or p_topic_string.count('/') != 2:
        logging.warning(f'Could not derive subtopic string for topic: {p_topic_string}')
        return None

    # substring from second
    return p_topic_string[p_topic_string[1:].index('/') + 2:]
