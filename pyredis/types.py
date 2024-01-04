from collections.abc import Sequence
from dataclasses import dataclass


@dataclass
class SimpleString:
    data: str

    def resp_encode(self):
        return f"+{self.data}\r\n".encode()


@dataclass
class Error:
    data: str

    def resp_encode(self):
        return f"-{self.data}\r\n".encode()


@dataclass
class Integer:
    data: int

    def resp_encode(self):
        return f":{str(self.data)}\r\n".encode()


@dataclass
class BulkString:
    data: bytes

    def resp_encode(self):
        if self.data is not None:
            return f"${len(self.data)}\r\n{self.data}\r\n".encode()

        return f"$-1\r\n".encode()


@dataclass
class Array(Sequence):
    data: list

    def __getitem__(self, i):
        return self.data[i]

    def __len__(self):
        return len(self.data)

    def resp_encode(self):
        if self.data is None:
            return b"*-1\r\n"

        encoded_sub_messages = [f"*{len(self.data)}\r\n".encode()]

        for msg in self.data:
            encoded_sub_messages.append(msg.resp_encode())

        return b"".join(encoded_sub_messages)