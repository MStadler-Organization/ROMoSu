import json
import logging
from json import JSONEncoder
from types import SimpleNamespace

import yaml


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


def setup():
    """Basic configs for the application """
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S %Z'
    )


def convert_boolean_str(object_with_string_booleans):
    # convert to boolean
    object_with_string_booleans.isExpandable = object_with_string_booleans.isExpandable == 'True'
    object_with_string_booleans.isChecked = object_with_string_booleans.isChecked == 'True'

    # call recursive for children if there are any
    if hasattr(object_with_string_booleans, 'children') and len(object_with_string_booleans.children) > 0:
        for child in object_with_string_booleans.children:
            convert_boolean_str(child)


def convert_to_json(config: str):
    """Converts a js-config object to a valid json and returns a dictionary"""

    config = config.replace('True', '"True"')
    config = config.replace('False', '"False"')
    config = config.replace("'", '"')
    config = json.loads(config, object_hook=lambda d: SimpleNamespace(**d))
    for entry in config:
        convert_boolean_str(entry)

    return config


def ros_msg2json(msg):
    """Convert a ROS message to JSON format"""
    y = yaml.safe_load(str(msg))
    return json.dumps(y, indent=4)
