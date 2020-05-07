from unittest import TestCase
from mfutil.cli import echo_ok, echo_nok, echo_warning, echo_bold, \
    echo_running, echo_clean


class TestCaseCli(TestCase):

    def test_echo_ok(self):
        echo_ok("foo ok")

    def test_echo_nok(self):
        echo_nok("foo nok")

    def test_echo_warning(self):
        echo_warning("foo warning")

    def test_echo_bold(self):
        echo_bold("foo bold")

    def test_echo_running_clean(self):
        echo_running()
        echo_clean()
