class colors():
    RED = "\e[31m"
    GREEN = "\e[32m"
    CLEAR = "\e[0m"


def assert_failed(context, message, expected, got):
    text = "{}.{} {}:".format(context.object_name(),
                              context.method_name(),
                              message)

    got_str = colors.RED + str(got) + colors.CLEAR
    expected_str = colors.GREEN + str(expected) + colors.CLEAR

    return "{}\nexpected:\n{}\ngot instead:\n{}".format(text,
                                                        expected_str,
                                                        got_str)
