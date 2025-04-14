import argparse
from sys import exception
import utils
import os
from timeit import default_timer as timer

def main():
    parser = argparse.ArgumentParser(
        description="Compiler for the Lime programming language",
    )

    group = parser.add_mutually_exclusive_group()

    parser.add_argument("input_file", help="Path to the input file")

    group.add_argument(
        "-r", "--run", action="store_true", help="Compile the program then run it."
    )
    group.add_argument("-b", "--build", action="store_true", help="Build the program.")
    group.add_argument(
        "-s",
        "--source",
        action="store_true",
        help="Generate compiled soruce code of the program.",
    )
    group.add_argument("-t", "--time", action="store_true", help="Measure the time it takes for the program to compile.")

    args = parser.parse_args()

    code = utils.import_file(args.input_file)
    file_name = os.path.basename(args.input_file).split(".")[0]

    # To avoid start ever being unbound.
    start = 0

    if args.time:
        start = timer()

    if args.build:
        utils.compile(code, file_name)
    elif args.source:
        utils.compile(code, file_name, True)
    else:
        # If no specific option is said, or if --run
        utils.run(code, file_name)

    if args.time:
        print(f"Compilation completed in {timer() - start} seconds." )


if __name__ == "__main__":
    main()
