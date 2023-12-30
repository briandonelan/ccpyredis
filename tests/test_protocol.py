import pytest

from pyredis.protocol import extract_frame_from_buffer, SimpleString, SimpleError


@pytest.mark.parametrize("buffer, expected", [
    (b"+Par", (None, 0)),
    (b"+OK\r\n", (SimpleString("OK"), 5)),
    (b"+OK\r\n+Next", (SimpleString("OK"), 5))
])
def test_read_frame_simple_string(buffer, expected):
    actual = extract_frame_from_buffer(buffer)
    assert actual == expected

def test_read_frame_simple_error():
    buffer = b"-Error message\r\n"
    actual = extract_frame_from_buffer(buffer)
    assert actual == (SimpleError("Error message"), 16)