import subprocess
from os import uname

from rich import console as rconsole

from restic_configurator_py.constants import MACOS, LINUX

console = rconsole.Console()

restic_console = rconsole.Console(
    markup=False,
)


def copy2clip(txt):
    if uname().sysname == MACOS:
        cmd = "pbcopy"
    elif uname().sysname == LINUX:
        cmd = "xclip -selection clipboard"
    else:
        raise RuntimeError(f"Unsupported operating system: {uname()}")
    return subprocess.run(cmd, text=True, input=txt)
