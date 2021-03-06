import socket
import os
import mock
from unittest import TestCase
from mfutil import get_unique_hexa_identifier
from mfutil.net import get_ip_for_hostname, get_domainname, \
    get_simple_hostname, get_full_hostname, get_real_ip, \
    _get_real_ip_netifaces, _get_domainname_from_resolv_conf, ping_tcp_port


class TestCaseNet(TestCase):

    def test_get_ip_for_hostname_auto(self):
        tmp = get_ip_for_hostname("AUTO")
        self.assertEqual(tmp, "AUTO")
        self.assertTrue(isinstance(tmp, str))

    def test_get_ip_for_hostname_localhost(self):
        tmp = get_ip_for_hostname("localhost")
        self.assertEqual(tmp, "127.0.0.1")
        self.assertTrue(isinstance(tmp, str))

    def test_get_ip_for_hostname_not_found(self):
        tmp = get_ip_for_hostname("foo.bar")
        self.assertTrue(tmp is None)

    def test_get_ip_for_hostname(self):
        tmp = get_ip_for_hostname(socket.gethostname())
        self.assertTrue("." in tmp)
        self.assertTrue(isinstance(tmp, str))

    def test_get_domainname(self):
        tmp = get_domainname()
        if tmp is not None:
            self.assertTrue(isinstance(tmp, str))

    def test_get_simple_hostname(self):
        tmp = get_simple_hostname()
        self.assertTrue("." not in tmp)
        self.assertTrue(len(tmp) > 0)
        self.assertTrue(isinstance(tmp, str))

    def test_get_full_hostname(self):
        tmp = get_full_hostname()
        self.assertTrue(len(tmp) > 0)
        self.assertTrue(isinstance(tmp, str))

    def test_get_real_ip(self):
        tmp = get_real_ip()
        self.assertTrue(len(tmp) > 0)
        self.assertTrue(isinstance(tmp, str))

    def test_get_real_ip_netifaces(self):
        tmp = _get_real_ip_netifaces()
        self.assertTrue(len(tmp) > 0)
        self.assertTrue(isinstance(tmp, str))

    def test_get_domainname_from_resolv_conf(self):
        tmp_file = get_unique_hexa_identifier()
        with open(tmp_file, "w") as f:
            f.write("# Generated by NetworkManager\n")
            f.write("search foo.bar\n")
            f.write("nameserver 1.2.3.4\n")
            f.write("nameserver 1.2.3.5\n")
            f.write("domain foo.bar\n")
        tmp = _get_domainname_from_resolv_conf(tmp_file)
        self.assertTrue(isinstance(tmp, str))
        self.assertEqual(tmp, "foo.bar")
        os.unlink(tmp_file)

    def test_ping_tcp_port1(self):
        res = ping_tcp_port("foobar.notfound.fr", 80)
        self.assertFalse(res)

    @mock.patch('socket.socket')
    def test_ping_tcp_port2(self, mock_socket_socket):
        class FakeSocketClass(object):
            close_called = False
            timeout_set = 0

            def connect_ex(self, *args, **kwargs):
                return 0

            def close(self):
                self.close_called = True

            def settimeout(self, timeout):
                self.timeout_set = timeout

        fake_socket_object = FakeSocketClass()
        mock_socket_socket.return_value = fake_socket_object
        res = ping_tcp_port("foobar", 80, timeout=2)
        self.assertTrue(res)
        self.assertTrue(fake_socket_object.close_called)
        self.assertEqual(fake_socket_object.timeout_set, 2)
