from argparse import ArgumentParser, Action, Namespace
from collections.abc import Sequence
from typing import Any

class DriverAction(Action):
    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: str | Sequence[Any] | None, option_string: str | None = ...) -> None:
        driver, destination = values
        namespace.driver = driver.lower()
        namespace.destination = destination

def create_parser():
    parser = ArgumentParser(description="""
        Back up PostgreSQL databases locally or to AWS S3 buckets.
        """)

    parser.add_argument("url", help="URL of the database to backup")
    parser.add_argument("--driver",
        help="How & where to store the backup",
        nargs=2,
        action=DriverAction,
        required=True)

    return parser