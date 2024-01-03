from pyredis.types import SimpleString, Error, Integer, BulkString, Array

MSG_SEPARATOR = b"\r\n"

def extract_frame_from_buffer(buffer):
    separator = buffer.find(MSG_SEPARATOR)

    match chr(buffer[0]):
        case '+':
            if separator != -1:
                return SimpleString(buffer[1:separator].decode()), separator + 2

        case '-':
            if separator != -1:
                return Error(buffer[1:separator].decode()), separator + 2

        case ':':
            if separator != -1:
                return Integer(int(buffer[1:separator].decode())), separator + 2

        case '*':
            length = len(buffer)

            if separator != -1:
                array_separator_count = int(buffer[1:separator].decode())

                if array_separator_count < 0:
                    return None, separator + 2

                array_parsed_elements = []

                buffer = buffer[separator+2:]

                for _ in range(array_separator_count):
                    (frame, length_parsed) = extract_frame_from_buffer(buffer)
                    if frame is None:
                        return None, 0
                    array_parsed_elements.append(frame)
                    buffer = buffer[length_parsed:]

                return Array(array_parsed_elements), length

        case '$':
            if separator != -1:
                length = int(buffer[1:separator].decode()) + separator + 2

                if int(buffer[1:separator].decode()) < 0:
                    return None, len(buffer[:separator + 2])

                if int(buffer[1:separator].decode()) != len(buffer.split(b"\r\n")[1]):
                    return None, 0

                return BulkString(buffer[separator + 2 : length].decode()), length + 2

    return None, 0