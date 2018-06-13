MOCK_TABLE = "__mock_table__"


def has_method_mock(context):
    if not has_mock_table(context):
        return False
    mock_table = getattr(context.object(), MOCK_TABLE).keys()
    return context.method_name() in mock_table


def set_method_mock(context, call):
    old_call = getattr(context.object(), context.method_name())
    setattr(context.object(), context.method_name(), call)
    return old_call


def add_method_mock(context, receiver, call):
    mock_table = getattr(context.object(), MOCK_TABLE, {})
    mock_table[context.method_name()] = receiver
    setattr(context.object(), MOCK_TABLE, mock_table)
    return set_method_mock(context, call)


def remove_method_mock(context, old_call):
    if not has_method_mock(context):
        return

    mock_table = getattr(context.object(), MOCK_TABLE)
    del mock_table[context.method_name()]
    setattr(context.object(), context.method_name(), old_call)


def get_receiver_for(context):
    if not has_method_mock(context):
        raise RuntimeError("BUG: Invalid receiver call for {}.{}"
                           .format(context.object_name(),
                                   context.method_name()))
    mock_table = getattr(context.object(), MOCK_TABLE)
    return mock_table[context.method_name()]
