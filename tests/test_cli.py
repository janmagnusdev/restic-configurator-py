import subprocess
import sys


def test_cli_help():
    result = subprocess.run(
        ["uv", "run", "rcy", "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert "Usage:" in result.stdout.decode()
    print(result.stdout.decode())
