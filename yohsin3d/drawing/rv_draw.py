from enum import Enum
import socket
from typing import Tuple

class HeaderType(Enum):
    ANNOTATION = (2, 0)
    DRAW_CIRCLE = (1, 0)
    DRAW_LINE = (1, 1)
    AGENT_ANNOTATION = (2, 1)
    CLEAR_ANNOTATION = (2, 2)

class Color(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

class RvDraw():

    def __init__(self, port:int=3300, host:str='localhost') -> None:
        self.PORT = port
        self.HOST = host
        assert isinstance(port, int), "Port must be an integer"
        assert isinstance(host, str), "Host must be a string"
        self.defaultColor = (255, 255, 255)
        self.defaultThickness = 2.0

    def __send_message(self, message, size) -> None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bytes_sent = 0
            while (bytes_sent < size):
                bytes_sent += sock.sendto(message[bytes_sent:],
                                          (self.HOST, self.PORT))

        except socket.error as err:
            exit()

    def __swap_buffer(self, buffer: bytearray, setName: str) -> None:
        buffer.append(0)
        buffer.append(0)
        buffer.extend(list(map(ord, setName)))
        buffer.append(0)

    def __float_to_buffer(self, buffer: bytearray, value: float) -> None:
        buffer.extend((str(value).ljust(6, '0')).encode('ASCII'))

    def __color_to_buffer(self, buffer: bytearray, color: Color) -> None:
        buffer.append(color.value[0])
        buffer.append(color.value[1])
        buffer.append(color.value[2])

    def __str_to_buffer(self, buffer: bytearray, text: str) -> None:
        buffer.extend(list(map(ord, text)))
        buffer.append(0)

    def __header_to_buffer(self, buffer: bytearray, header: HeaderType) -> None:
        buffer.append(header.value[0])
        buffer.append(header.value[1])

    

    def add_annotation(self, text: str, position: Tuple[float,float,float], name: str, color: Color=Color.RED) -> None:
        buffer = bytearray(0)

        self.__header_to_buffer(buffer, HeaderType.ANNOTATION)
        self.__float_to_buffer(buffer, position[0])
        self.__float_to_buffer(buffer, position[1])
        self.__float_to_buffer(buffer, position[2])
        self.__color_to_buffer(buffer, color)
        self.__str_to_buffer(buffer, text)
        self.__str_to_buffer(buffer, name)

        self.__swap_buffer(buffer, name)

        self.__send_message(bytes(buffer), len(buffer))

    def draw_circle(self, center: Tuple[float,float,float], radius: float, name: str, color: Color = Color.RED, thickness: float = 2.0) -> None:
        buffer = bytearray(0)
        self.__header_to_buffer(buffer, HeaderType.DRAW_CIRCLE)
        self.__float_to_buffer(buffer, center[0])
        self.__float_to_buffer(buffer, center[1])
        self.__float_to_buffer(buffer, radius)
        self.__float_to_buffer(buffer, thickness)
        self.__color_to_buffer(buffer, color)
        buffer.extend(list(map(ord, name)))
        buffer.append(0)
        self.__swap_buffer(buffer, name)
        self.__send_message(bytes(buffer), len(buffer))

    def draw_line(self, pointA: Tuple[float], pointB: Tuple[float,float,float], setName: str, color: Color = Color.BLUE, thickness: float = 2.0) -> None:
        buffer = bytearray(0)
        self.__header_to_buffer(buffer, HeaderType.DRAW_LINE)
        self.__float_to_buffer(buffer, pointA[0])
        self.__float_to_buffer(buffer, pointA[1])
        self.__float_to_buffer(buffer, pointA[2])
        self.__float_to_buffer(buffer, pointB[0])
        self.__float_to_buffer(buffer, pointB[1])
        self.__float_to_buffer(buffer, pointB[2])
        self.__float_to_buffer(buffer, thickness)
        self.__color_to_buffer(buffer, color)
        self.__str_to_buffer(buffer, setName)

        self.__swap_buffer(buffer, setName)

        self.__send_message(bytes(buffer), len(buffer))

    def add_agent_annotation(self, text: str, color: Color=Color.RED) -> None:
        buffer = bytearray(0)

        self.__header_to_buffer(buffer, HeaderType.AGENT_ANNOTATION)

        buffer.append(10)
        self.__color_to_buffer(buffer, color)
        self.__str_to_buffer(buffer, text)

        self.__send_message(bytes(buffer), len(buffer))

    def clear_agent_annotation(self, agentNum: int):
        buffer = bytearray(0)

        self.__header_to_buffer(buffer, HeaderType.CLEAR_ANNOTATION)
        buffer.append(agentNum)

        self.__sendMessage(bytes(buffer), len(buffer))

