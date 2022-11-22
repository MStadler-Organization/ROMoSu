class TopicInfo:
    def __init__(self, in_topic, type, type_info):
        self.in_topic = in_topic
        self.type = type
        self.type_info = type_info

    def __str__(self) -> str:
        return f'Name={self.in_topic}, Type={self.type}, DataTypeInfo={self.type_info}'


class RuntimeStarterRESTObject:
    """Class for better accessing the REST object of RT starter"""

    def __init__(self, rest_obj):
        self.prefix: str = rest_obj['prefix']
        self.sum_type_id: int = rest_obj['sum_type_id']
        self.config_id: int = rest_obj['config_id']


class RosTopicConfigObj:
    def __init__(self, name, data_type, is_expandable, is_checked, children):
        self.name: str = name
        self.dataType: str = data_type
        self.isExpandable: bool = is_expandable
        self.isChecked: bool = is_checked
        self.children: [RosTopicConfigObj] = children
