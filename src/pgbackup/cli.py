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
    parser.add_argument("--driver", "-d",
        help="How & where to store the backup",
        nargs=2,
        metavar=("DRIVER", "DESTINATION"),
        action=DriverAction,
        required=True)

    return parser

def main():
    import boto3
    import time
    from pgbackup import pgdump, storage

    args = create_parser().parse_args()
    dump = pgdump.dump(args.url)
    if args.driver == 's3':
        client = boto3.client('s3')
        timestamp = time.strftime("%Y-%m-%dT%H%M", time.localtime())
        file_name = pgdump.dump_file_name(args.url, timestamp)
        print(f"Backing database up to {args.destination} in S3 as {file_name}")
        storage.s3(client, dump.stdout, args.destination, file_name)
    else:
        outfile = open(args.destination, 'wb')
        print(f"Backing database up locally to {outfile.name}")
        storage.local(dump.stdout, outfile)
