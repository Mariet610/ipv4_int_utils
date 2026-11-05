"""Core conversion functions for IPv4 dotted-quad strings and 32-bit integers."""


def ipv4_to_int(address: str) -> int:
    """Convert a dotted-quad IPv4 address string to its 32-bit integer value.

    The address must be in strict dotted-quad form: exactly four decimal octets
    separated by single dots, each octet 0-255, no leading zeros (except "0"
    itself), no whitespace, no extra characters.

    We reject leading zeros because they are ambiguous: some systems interpret
    them as octal, and accepting them silently creates a class of bugs where
    "010.0.0.1" means something different to different tools. Strictness here
    means the caller gets a clear error instead of a surprising number.

    Args:
        address: The IPv4 address string, e.g. "192.168.0.1".

    Returns:
        The integer value of the address, in range 0 .. 2**32 - 1.

    Raises:
        ValueError: If the string is not a valid strict dotted-quad address.
        TypeError: If `address` is not a string.
    """
    if not isinstance(address, str):
        raise TypeError("address must be a str")

    parts = address.split(".")
    if len(parts) != 4:
        raise ValueError("IPv4 address must have exactly four octets")

    value = 0
    for part in parts:
        if not part:
            raise ValueError("empty octet in IPv4 address")
        # Reject leading zeros: "0" is fine, "00" and "01" are not.
        if len(part) > 1 and part[0] == "0":
            raise ValueError("octet must not have leading zeros")
        if not part.isdigit():
            raise ValueError("octet must contain only decimal digits")
        octet = int(part)
        if octet > 255:
            raise ValueError("octet out of range 0-255")
        value = (value << 8) | octet

    return value


def int_to_ipv4(value: int) -> str:
    """Convert a 32-bit integer to its dotted-quad IPv4 address string.

    Args:
        value: An integer in range 0 .. 2**32 - 1.

    Returns:
        The dotted-quad string, e.g. "192.168.0.1".

    Raises:
        TypeError: If `value` is not an int (bool is rejected too, since it is
            a subclass of int but not a meaningful address).
        ValueError: If `value` is outside 0 .. 2**32 - 1.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("value must be an int")
    if value < 0 or value > 0xFFFFFFFF:
        raise ValueError("value must be in range 0 .. 2**32 - 1")

    return "{}.{}.{}.{}".format(
        (value >> 24) & 0xFF,
        (value >> 16) & 0xFF,
        (value >> 8) & 0xFF,
        value & 0xFF,
    )
