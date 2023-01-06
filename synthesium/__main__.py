import argparse
import sys
import warnings

# TODO: add file hunting


def main():
    try:
        parser = argparse.ArgumentParser()
        module_location = parser.add_argument_group()
        module_location.add_argument(
            "file",
            nargs="?",
            help="Path to file holding the python code for the scene",
        )
        parser.add_argument(
            "scene_names",
            nargs="*",
            help="Name of the Scene class you want to see",
        )
        parser.add_argument(
            "output",
            nargs="?",
            help="Path to desired file output",
        )

    except argparse.ArgumentError as err:
        warnings.warn(str(err))
        sys.exit(2)


if __name__ == "__main__":
    main()
