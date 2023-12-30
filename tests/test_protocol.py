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

@pytest.mark.parametrize("buffer, expected", [
    (b"-Par", (None, 0)),
    (b"-Error message\r\n", (SimpleError("Error message"), 16))
])
def test_read_frame_simple_error(buffer, expected):
    actual = extract_frame_from_buffer(buffer)
    assert actual == expected