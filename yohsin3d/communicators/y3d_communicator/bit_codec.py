from typing import List
communication_alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789*#"


class BitCodec:

    @staticmethod
    def bits_to_int(bits: List, start, end):
        if start < 0 or end >= len(bits):
            return 0

        n = 0
        for i in range(start, end + 1):
            n *= 2
            n += bits[i]

        return n

    @staticmethod
    def int_to_bits(n: int, num_bits: int) -> List[int]:
        if n < 0:
            return []

        bits = [0] * num_bits
        for i in range(num_bits - 1, -1, -1):
            bits[i] = n % 2
            n //= 2

        return bits

    @staticmethod
    def bits_to_string(bitfield_list):
        message = ""

        index = []
        index_size = (len(bitfield_list) + 5) // 6
        index = [0] * index_size
        ctr = 0
        for i in range(index_size):
            index[i] = 0
            for j in range(6):
                index[i] *= 2
                if ctr < len(bitfield_list):
                    index[i] += bitfield_list[ctr]
                    ctr += 1

        for i in range(index_size):
            message += communication_alphabet[index[i]]

        return message

    @staticmethod
    def string_to_bits(message):
        if len(communication_alphabet) != 64:
            print("string_to_bits: alphabet size not 64!")
            return None

        bits = []
        for char in message:
            try:
                index = communication_alphabet.index(char)
                binary_value = bin(index)[2:].zfill(6)
                bits.extend([int(bit) for bit in binary_value])
            except ValueError:
                print("string_to_bits: character not in alphabet!")
                return None

        return bits

    @staticmethod
    def encode_float(number, min_value, max_value, num_bits=10):
        clipped = min(max(number, min_value), max_value)
        max_size = (1 << num_bits) - 1
        value = int(((clipped - min_value) * max_size) /
                    (max_value - min_value) + 0.5)
        return BitCodec.int_to_bits(value, num_bits)

    @staticmethod
    def decode_bit_array(bits, min_value, max_value, num_bits=10):
        value = BitCodec.bits_to_int(bits, 0, num_bits - 1)
        return min_value + (value * (max_value - min_value)
                            ) / ((1 << num_bits) - 1)
