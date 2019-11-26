from collections import defaultdict, OrderedDict

from toolz.dicttoolz import merge_with


def deep_merge(*ds):
    def combine(vals):
        if len(vals) == 1 or not all(isinstance(v, dict) for v in vals):
            return vals[-1]
        else:
            return deep_merge(*vals)

    return merge_with(combine, *ds)


def nested_dict():
    return defaultdict(nested_dict)


def pop_nullable_values_recursively(data):
    if type(data) == dict:

        new_data = {}

        for key, value in data.items():
            popped = pop_nullable_values_recursively(value)
            if popped:
                new_data[key] = popped

    elif type(data) == list:

        new_data = []

        for idx, value in enumerate(data):
            popped = pop_nullable_values_recursively(value)
            if popped:
                new_data.append(popped)

    else:
        if data in ["", {}, [], None]:
            new_data = {}
        else:
            new_data = data

    return new_data


def single_select(resource, selection):
    if not selection:
        return pop_nullable_values_recursively(resource)

    if type(resource) is dict:
        _resource = {}
        key = selection[0]
        _resource[key] = single_select(resource.get(key, {}), selection[1:])

    elif type(resource) is list:
        _resource = OrderedDict({"__type__": 'marked'})
        for idx, value in enumerate(resource):
            if type(value) not in [dict, list]:
                continue
            _resource[idx] = single_select(value, selection)

    else:
        _resource = resource

    return pop_nullable_values_recursively(_resource)


def transform(resource):
    if type(resource) in [dict, OrderedDict] and resource.get('__type__') == 'marked':
        _resource = []
        resource.pop('__type__', None)
        for key, value in resource.items():
            _resource.append(transform(value))

    elif type(resource) in [dict, OrderedDict]:
        _resource = {}
        for key, value in resource.items():
            _resource[key] = transform(value)

    else:
        _resource = resource

    return _resource


def select_fields(resource, selections):

    if not isinstance(selections, list):
        raise TypeError('Selection must be a list.')

    selections = [f.split('.') for f in selections]

    outputs = []

    for selection in selections:
        selected = single_select(resource, selection)
        if not selected:
            continue
        outputs.append(selected)

    merged = deep_merge(outputs)

    return transform(merged)
