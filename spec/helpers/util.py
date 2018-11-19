from collections import namedtuple


def nested_namedtuple(name, data):
    """ generate a nested named tuple out of a given dict whit values.
    """
    ntuple = namedtuple(name, [])

    for key, value in data.items():
        if not isinstance(value, dict):
            setattr(ntuple, key, value)
        else:
            sub_ntuple = nested_namedtuple(name + key.title(), value)
            setattr(ntuple, key, sub_ntuple)
    return ntuple
