import json
import os

from haikunator import Haikunator

from azuresearch.azure_search_object import AzureSearchObject

path = os.path.dirname(os.path.abspath(__file__))


def get_json_file(name):
    """
    Returns the content of a test json
    :param name: name of file
    :return: json contents
    """
    return json.load(open(os.path.join(path, 'output_jsons', name)))

def get_fake_name():
    """
    Returns a random string to be used as a name
    :return:
    """
    haikunator = Haikunator()
    return haikunator.haikunate()

def ordered(obj):
    """
    Order dictionary by keys, recursively
    :param obj:
    :return:
    """
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, AzureSearchObject):
        dict = obj.to_dict()
        return dict
    else:
        return obj.__dict__
