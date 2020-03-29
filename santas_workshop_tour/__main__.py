import argparse
from santas_workshop_tour.artificial_immune_system import \
    ArtificialImmuneSystem


class MyArgumentParser(argparse.ArgumentParser):
    def convert_arg_line_to_args(self, arg_line):
        return arg_line.split()


def main(args):
    """
    Main execution function.

    :param args: dict, argparse arguments.
    """
    ArtificialImmuneSystem(args.data_file_path)


if __name__ == '__main__':
    parser = MyArgumentParser(
        description="Program to solve the Santa's Workshop Tour 2019 problem.",
        fromfile_prefix_chars='@'
    )

    # Required named arguments
    parser_required_named = parser.add_argument_group(
        'required named arguments'
    )
    parser_required_named.add_argument(
        '--data-file-path',
        required=True,
        type=str,
        help='Path to the data to be optimized.'
    )

    main(parser.parse_args())
