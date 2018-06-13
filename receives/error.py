class colors():
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    CLEAR = "\033[0m"


def assert_failed(context, message, expected, got):
    text = "{}.{} {}:".format(context.object_name(),
                              context.method_name(),
                              message)

    got_str = colors.RED + str(got) + colors.CLEAR
    expected_str = colors.GREEN + str(expected) + colors.CLEAR

    return "{}\nexpected:\n  {}\ngot instead:\n  {}".format(text,
                                                        expected_str,
                                                        got_str)
