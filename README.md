# ipv4_int_utils

Convert IPv4 addresses between dotted-quad strings and packed 32-bit integers.

```python
from ipv4_int_utils import ipv4_to_int, int_to_ipv4

n = ipv4_to_int("192.168.0.1")   # 3232235521
s = int_to_ipv4(3232235521)      # "192.168.0.1"
```

## Why this exists

Storing an IPv4 address as an integer makes it cheap to sort, range-check, and
compare addresses, and it avoids the allocation of a string per address. Python's
standard library has `ipaddress`, which is excellent but heavyweight if all you
need is the conversion: it builds objects, validates networks, and carries a lot of
machinery. This module is the two functions, nothing else.

The trade-off is strictness. The parser accepts only canonical dotted-quad input:
four decimal octets, each 0-255, no leading zeros, no surrounding whitespace, no
CIDR suffix, no shorthand forms. That means `010.0.0.1` and `1.2.3` are rejected
rather than guessed at. If you need to accept the looser forms that some tools
allow, use `ipaddress` instead.

## API

- `ipv4_to_int(address: str) -> int`
- `int_to_ipv4(value: int) -> str`

Both raise `ValueError` for out-of-domain values and `TypeError` for wrong types.
`int_to_ipv4` rejects `bool` even though `bool` is a subclass of `int`, because
`True` is not an address.

## The awkward edge

Leading zeros are the trap. `ipv4_to_int("010.0.0.1")` raises `ValueError`
because `010` could mean decimal 10 or octal 8 depending on the caller, and
silently choosing one produces addresses that differ between systems. Rejecting
it is the only safe behaviour for an integer representation.
