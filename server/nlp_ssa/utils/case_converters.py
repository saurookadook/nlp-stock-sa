import re


def convert_to_snake_case(string):
    # TODO: this needs to be rewritten lol
    def replacement_func(matchObj):
        return "_"

    return re.sub(
        pattern=r"[^\w\d]",
        repl=replacement_func,
        string=string,
        flags=re.IGNORECASE | re.MULTILINE,
    ).lower()


def convert_to_kebab_case(string):
    def replacement_func(matchObj):
        return "-"

    return re.sub(
        pattern=r"[^\w\d]",
        repl=replacement_func,
        string=string,
        flags=re.IGNORECASE | re.MULTILINE,
    ).lower()
