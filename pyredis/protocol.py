from dataclasses import dataclass

MSG_SEPARATOR = b"\r\n"

@dataclass
class SimpleString:
    data: str

@dataclass
class SimpleError:
    data: str

@dataclass
class Integer:
    data: int

class BulkString(SimpleString):
    pass

@dataclass
class Array:
    data: list

def extract_frame_from_buffer(buffer):
    match chr(buffer[0]):
        case '+':
            separator = buffer.find(MSG_SEPARATOR)

            if separator != -1:
                return SimpleString(buffer[1:separator].decode()), separator + 2

        case '-':
            separator = buffer.find(MSG_SEPARATOR)

            if separator != -1:
                return SimpleError(buffer[1:separator].decode()), separator + 2

        case ':':
            separator = buffer.find(MSG_SEPARATOR)

            if separator != -1:
                return Integer(int(buffer[1:separator].decode())), separator + 2

        case '*':
            separator = buffer.find(MSG_SEPARATOR)
            length = len(buffer)

            if separator != -1:
                array_separator_count = int(buffer[1:separator].decode())

                if array_separator_count < 0:
                    return None, separator + 2

                array_parsed_elements = []

                buffer = buffer[separator+2:]

                for ii in range(array_separator_count):
                    (frame, length_parsed) = extract_frame_from_buffer(buffer)
                    array_parsed_elements.append(frame)
                    buffer = buffer[length_parsed:]

                return Array(array_parsed_elements), length

        case '$':
            separator = buffer.find(MSG_SEPARATOR)

            if separator != -1:
                length = int(buffer[1:separator].decode()) + separator + 2

                if int(buffer[1:separator].decode()) < 0:
                    return None, len(buffer[:separator + 2])

                return BulkString(buffer[separator + 2 : length].decode()), length + 2

    return None, 0