import operator
from functools import reduce  # forward compatibility for Python 3


def dict_get(root, items, default=None):
    """
    Access a nested object in root by item sequence.

    Usage::
       data = {"nested": {"a_list": [{"finally": "target_data"}]}}
       value = dict_get(["nested", "a_list", 0, "finally"], "Not_found")

    """
    try:
        value = reduce(operator.getitem, items, root)
    except (KeyError, IndexError):
        return default
    return value


def dict_undefined_set(dict_obj, key, value):
    if key not in dict_obj:
        dict_obj[key] = value
