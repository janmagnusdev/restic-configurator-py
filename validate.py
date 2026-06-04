#!/usr/bin/env -S uv run --script
import argparse
import os
import subprocess

env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}

parser = argparse.ArgumentParser()
parser.add_argument("--no-test", action="store_true")
args = parser.parse_args()


def main() -> int:
    cmds = [
        ["uv", "run", "ruff", "format"],
        ["uv", "run", "ruff", "check", "--fix"],
    ]
    if not args.no_test:
        cmds.append(["uv", "run", "pytest"])

    for cmd in cmds:
        subprocess.run(cmd, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
