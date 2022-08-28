import argparse
import os


def get_args():
    parser = argparse.ArgumentParser(description="Page loader")
    parser.add_argument(dest="url", help="URL")
    parser.add_argument("-o", "--output",
                        help="destination for download",
                        default=os.getcwd(),
                        type=str)

    return parser
