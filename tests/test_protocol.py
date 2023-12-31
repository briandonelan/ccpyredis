import pytest

from pyredis.protocol import extract_frame_from_buffer, SimpleString, SimpleError, Integer


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

@pytest.mark.parametrize("buffer, expected", [
    (b":1\r\n", (Integer(1), 4)),
    (b":12\r\n", (Integer(12), 5))
])
def test_read_frame_integer(buffer, expected):
    actual = extract_frame_from_buffer(buffer)
    assert actual == expected
