import unittest

from ipv4_int_utils import ipv4_to_int, int_to_ipv4


class TestIpv4ToInt(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(ipv4_to_int("0.0.0.0"), 0)

    def test_max(self):
        self.assertEqual(ipv4_to_int("255.255.255.255"), 0xFFFFFFFF)

    def test_typical(self):
        self.assertEqual(ipv4_to_int("192.168.0.1"), 0xC0A80001)

    def test_loopback(self):
        self.assertEqual(ipv4_to_int("127.0.0.1"), 0x7F000001)

    def test_octet_boundaries(self):
        self.assertEqual(ipv4_to_int("1.0.0.0"), 0x01000000)
        self.assertEqual(ipv4_to_int("0.1.0.0"), 0x00010000)
        self.assertEqual(ipv4_to_int("0.0.1.0"), 0x00000100)
        self.assertEqual(ipv4_to_int("0.0.0.1"), 0x00000001)

    def test_rejects_wrong_octet_count(self):
        for bad in ("1.2.3", "1.2.3.4.5", "", "1..2.3"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    ipv4_to_int(bad)

    def test_rejects_leading_zeros(self):
        for bad in ("01.2.3.4", "1.02.3.4", "1.2.03.4", "1.2.3.04", "00.0.0.0"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    ipv4_to_int(bad)

    def test_accepts_single_zero_octets(self):
        self.assertEqual(ipv4_to_int("0.0.0.0"), 0)
        self.assertEqual(ipv4_to_int("10.0.0.0"), 0x0A000000)

    def test_rejects_out_of_range_octets(self):
        for bad in ("256.0.0.1", "1.256.0.1", "1.2.256.1", "1.2.3.256", "999.1.1.1"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    ipv4_to_int(bad)

    def test_rejects_non_digit_octets(self):
        for bad in ("a.1.1.1", "1.a.1.1", "1.1.a.1", "1.1.1.a", "1.1.1.1 ", " 1.1.1.1", "1.1.1.-1"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    ipv4_to_int(bad)

    def test_rejects_non_string(self):
        for bad in (123, None, b"1.2.3.4", 1.2):
            with self.subTest(bad=bad):
                with self.assertRaises(TypeError):
                    ipv4_to_int(bad)


class TestIntToIpv4(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(int_to_ipv4(0), "0.0.0.0")

    def test_max(self):
        self.assertEqual(int_to_ipv4(0xFFFFFFFF), "255.255.255.255")

    def test_typical(self):
        self.assertEqual(int_to_ipv4(0xC0A80001), "192.168.0.1")

    def test_octet_boundaries(self):
        self.assertEqual(int_to_ipv4(0x01000000), "1.0.0.0")
        self.assertEqual(int_to_ipv4(0x00010000), "0.1.0.0")
        self.assertEqual(int_to_ipv4(0x00000100), "0.0.1.0")
        self.assertEqual(int_to_ipv4(0x00000001), "0.0.0.1")

    def test_rejects_negative(self):
        with self.assertRaises(ValueError):
            int_to_ipv4(-1)

    def test_rejects_too_large(self):
        with self.assertRaises(ValueError):
            int_to_ipv4(0x100000000)

    def test_rejects_non_int(self):
        for bad in ("0", None, 1.0, b"0"):
            with self.subTest(bad=bad):
                with self.assertRaises(TypeError):
                    int_to_ipv4(bad)

    def test_rejects_bool(self):
        with self.assertRaises(TypeError):
            int_to_ipv4(True)


class TestRoundTrip(unittest.TestCase):
    def test_round_trip_strings(self):
        for addr in (
            "0.0.0.0",
            "255.255.255.255",
            "192.168.0.1",
            "127.0.0.1",
            "10.0.0.1",
            "172.16.254.1",
            "8.8.8.8",
            "1.2.3.4",
        ):
            with self.subTest(addr=addr):
                self.assertEqual(int_to_ipv4(ipv4_to_int(addr)), addr)

    def test_round_trip_ints(self):
        for value in (0, 1, 0x01000000, 0x7F000001, 0xC0A80001, 0xFFFFFFFF):
            with self.subTest(value=value):
                self.assertEqual(ipv4_to_int(int_to_ipv4(value)), value)


if __name__ == "__main__":
    unittest.main()
