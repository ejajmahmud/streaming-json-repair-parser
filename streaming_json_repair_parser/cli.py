"""CLI for Streaming JSON Repair Parser."""
import argparse
import json
from .core import StreamingJSONRepair


def main():
    parser = argparse.ArgumentParser(description="Streaming JSON Repair Parser CLI")
    parser.add_argument("--raw", default='{"action": "edit", "files": ["main.py", "uti', help="Partial JSON string")
    args = parser.parse_args()

    repairer = StreamingJSONRepair()
    print(json.dumps(repairer.parse_partial(args.raw), indent=2))


if __name__ == "__main__":
    main()
