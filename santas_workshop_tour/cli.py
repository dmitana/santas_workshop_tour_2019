import argparse


class MyArgumentParser(argparse.ArgumentParser):
    """Class representing custom argument parser."""

    def convert_arg_line_to_args(self, arg_line):
        return arg_line.split()


class MappingAction(argparse.Action):
    """Action for storing mapped value in dictionary."""

    def __init__(
        self,
        option_strings,
        mapping,
        choices=None,
        default=None,
        type=str,
        required=True,
        *args,
        **kwargs
    ):
        self._mapping = mapping
        super().__init__(
            option_strings=option_strings,
            choices=mapping.keys(),
            default=self._mapping.get(default),
            type=type,
            required=required,
            *args,
            **kwargs
        )

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self._mapping.get(values))
