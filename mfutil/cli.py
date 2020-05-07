"""Utility functions to build CLI."""

from __future__ import print_function
import six
import os
import sys
from mfutil.exc import MFUtilException


def is_interactive(target=None):
    """Return True if we are in an interactive terminal.

    For historical reasons, the following algorithm is used to determine
    if we are in an interactive terminal or not:

    - if the `NOINTERACTIVE` env var is set to 1 => we return False
    - if the `/tmp/nointeractive` file exists => we return False
    - if target is None:
        - if stdout AND stderr are a tty => we return True (else False)
    - elif target == "stdout":
        - if stdout is a tty => we return True (else False)
    - elif target == "stderr":
        - if stderr is a tty => we return True (else False)
    - else:
        - we raise a MFUtilException

    Args:
        target (string): can be None (for stdout AND stderr checking),
            "stdout" (for stdout checking only or "stderr" (for stderr checking
            only).

    Returns:
        boolean (True (interactive) or False (non-interactive).

    Raises:
        MFUtilException: if target is invalid

    """
    if os.environ.get("NOINTERACTIVE", "").strip() == "1":
        return False
    if os.path.isfile("/tmp/nointeractive"):
        return False
    if target is None:
        return sys.stdout.isatty() and sys.stderr.isatty()
    elif target == "stdout":
        return sys.stdout.isatty()
    elif target == "stderr":
        return sys.stderr.isatty()
    else:
        raise MFUtilException("invalid target parameter: %s" % target)


def echo_ok(message=""):
    """Write [OK] with colors if supported a little optional message.

    Args:
        message (string): little optional message.

    """
    if is_interactive("stdout"):
        echo_clean()
        print("\033[60G[ \033[32mOK\033[0;0m ] %s" % message)
    else:
        print(" [ OK ] %s" % message)


def echo_nok(message=""):
    """Write [ERROR] with colors if supported a little optional message.

    Args:
        message (string): little optional message.

    """
    if is_interactive("stdout"):
        echo_clean()
        print("\033[60G[ \033[31mERROR\033[0;0m ] %s" % message)
    else:
        print(" [ ERROR ] %s" % message)


def echo_warning(message=""):
    """Write [WARNING] with colors if supported a little optional message.

    Args:
        message (string): little optional message.

    """
    if is_interactive("stdout"):
        echo_clean()
        print("\033[60G[ \033[33mWARNING\033[0;0m ] %s" % message)
    else:
        print( "[ WARNING ] %s" % message)


def echo_bold(message):
    """Write a message in bold (if supported).

    Args:
        message (string): message to write in bold.

    """
    if is_interactive("stdout"):
        print("\033[1m%s\033[0m" % message)
    else:
        print(message)


def echo_running(message=None):
    """Write [RUNNING] with colors if supported.

    You can pass an optional message which will be rendered before [RUNNING]
    on the same line.

    Args:
        message (string): little optional message.

    """
    if message is not None:
        if is_interactive("stdout"):
            if six.PY2:
                print(message, end="")
                sys.stdout.flush()
            else:
                print(message, end="", flush=True)
        else:
            print(message, end="")
    if is_interactive("stdout"):
        echo_clean()
        print("\033[60G[ \033[33mRUNNING\033[0;0m ]", end="")


def echo_clean():
    """Clean waiting status."""
    if is_interactive("stdout"):
        print("\033[60G[ \033           ", end="")
