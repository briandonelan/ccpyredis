import pytest

from pyredis.protocol import extract_frame_from_buffer, SimpleString, SimpleError, Integer, Array, BulkString


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

@pytest.mark.parametrize("buffer, expected", [
    (b"*0\r\n", (Array([]), 4)),
    (b"*2\r\n:1\r\n:2\r\n", (Array([Integer(1), Integer(2)]), 12)),
    (b"*3\r\n:1\r\n:2\r\n:3\r\n", (Array([Integer(1), Integer(2), Integer(3)]), 16)),
    (b"*1\r\n$4\r\nping\r\n", (Array([BulkString("ping")]), 14)),
    (b"*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n", (Array([BulkString("echo"), BulkString("hello world")]), 32)),
    (b"*2\r\n$3\r\nget\r\n$3\r\nkey\r\n", (Array([BulkString("get"), BulkString("key")]), 22))
])
def test_read_frame_array(buffer, expected):
    actual = extract_frame_from_buffer(buffer)
    assert actual == expected

@pytest.mark.parametrize("buffer, expected", [
    (b"$0\r\n\r\n", (BulkString(""), 6))
])
def test_read_frame_bulkstring(buffer, expected):
    actual = extract_frame_from_buffer(buffer)
    assert actual == expected