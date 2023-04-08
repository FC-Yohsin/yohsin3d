from ..world import WorldModel
from ..localizer import BaseLocalizer
from typing import List

class HeardMessage:
    def __init__(self, message: str, heard_time: str, team_name: str, voice_orientation: str) -> None:
        self.message = message
        self.heard_time = heard_time
        self.team_name = team_name
        self.voice_orientation = voice_orientation

communication_alphabet =  "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789*#"
NUM_AGENTS=11
class BaseCommunicator:

    def __init__(self) -> None:
        self.said_message: str = ""
        self.heard_messages: List[HeardMessage] = []
        self.world_model: WorldModel = None
        self.localizer: BaseLocalizer = None

    def initialize(self, world_model: WorldModel, localizer: BaseLocalizer) -> None:
        self.world_model = world_model
        self.localizer = localizer

    def reset(self):
        self.heard_messages.clear()
        self.said_message = ""


    def can_say(self): 

        server_time = self.world_model.get_time()
        cycles = int(server_time * 50 + 0.1)
        is_my_turn = (cycles % (NUM_AGENTS * 2) == (self.world_model.my_number - 1) * 2)
        is_message_valid = (self.said_message.strip() != "" and self.said_message is not None)

        return is_my_turn and is_message_valid
        
    def make_say_message(self):
        if self.can_say():
            return "(say " + self.said_message + ")"
        return ""
    
    def hear(self):
        raise NotImplementedError

    def say(self):
        raise NotImplementedError
    

FIELD_Y = 20
FIELD_X = 30
HALF_FIELD_Y = FIELD_Y / 2.0
HALF_FIELD_X = FIELD_X / 2.0

min_ball_x = -HALF_FIELD_X - 2.0
max_ball_x = HALF_FIELD_X + 2.0
min_ball_y = -HALF_FIELD_Y - 2.0
max_ball_y = HALF_FIELD_Y + 2.0

min_agent_x = -HALF_FIELD_X - 5.0
max_agent_x = HALF_FIELD_X + 5.0
min_agent_y = -HALF_FIELD_Y - 5.0
max_agent_y = HALF_FIELD_Y + 5.0


class Yohsin3dCommunicator(BaseCommunicator):

    def __init__(self) -> None:
        super().__init__()

        self.teammate_positions = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None,
            9: None,
            10: None,
            11: None,
        }


    def bits_to_int(self, bits: List, start, end):
        if start < 0 or end >= len(bits):
            return 0  # Error

        n = 0
        for i in range(start, end+1):
            n *= 2
            n += bits[i]

        return n


    def int_to_bits(self, n: int, numBits: int, debug=False) -> List[int]:
        if n < 0:
            return []

        bits = [0] * numBits
        for i in range(numBits-1, -1, -1):
            bits[i] = n % 2
            n //= 2

        return bits
    
    def bits_to_string(self, bitfield_list):
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

    def data_to_bits(self, time, ball_last_seen_time, ball_x, ball_y, my_x, my_y, f_fallen):
        bits = []

        cycles = int(time * 50 + 0.1) % (1 << 16)
        time_bits = self.int_to_bits(cycles, 16, True)

        ball_last_seen_cycle = int(ball_last_seen_time * 50 + 0.1) % (1 << 16)
        ball_last_seen_time_bits = self.int_to_bits(ball_last_seen_cycle, 16)

        clipped_ball_x = min(max(ball_x, min_ball_x), max_ball_x)
        bx = int(((clipped_ball_x - min_ball_x) * 1023) / (max_ball_x - min_ball_x) + 0.5)
        ball_x_bits = self.int_to_bits(bx, 10)

        clipped_ball_y = min(max(ball_y, min_ball_y), max_ball_y)
        by = int(((clipped_ball_y - min_ball_y) * 1023) / (max_ball_y - min_ball_y) + 0.5)
        ball_y_bits = self.int_to_bits(by, 10)

        clipped_my_x = min(max(my_x, min_agent_x), max_agent_x)
        mx = int(((clipped_my_x - min_agent_x) * 1023) / (max_agent_x - min_agent_x) + 0.5)
        my_x_bits = self.int_to_bits(mx, 10)

        clipped_my_y = min(max(my_y, min_agent_y), max_agent_y)
        my = int(((clipped_my_y - min_agent_y) * 1023) / (max_agent_y - min_agent_y) + 0.5)
        my_y_bits = self.int_to_bits(my, 10)

        fallen_bit = 1 if f_fallen else 0

        bits.extend(time_bits)
        bits.extend(ball_last_seen_time_bits)
        bits.extend(ball_x_bits)
        bits.extend(ball_y_bits)
        bits.extend(my_x_bits)
        bits.extend(my_y_bits)
        bits.append(fallen_bit)

        return bits

    def say(self):
        ball = self.localizer.ball_position
        me = self.localizer.my_location.position
        bits = self.data_to_bits(
            self.world_model.get_time(),
            0,
            ball[0],
            ball[1],
            me[0],
            me[1],
            False            
        )        

        message = self.bits_to_string(bits)
        self.said_message = message


    def bits_to_data(self, bits):
        time, ballLastSeenTime, ballX, ballY, agentX, agentY, fFallen = 0, 0, 0, 0, 0, 0, False

        if len(bits) < (16 + 16 + 10 + 10 + 10 + 10 + 1):
            return False, time, ballLastSeenTime, ballX, ballY, agentX, agentY, fFallen

        ctr = 0

        cycles = self.bits_to_int(bits, ctr, ctr + 15)
        time = cycles * 0.02
        ctr += 16

        ballLastSeenCycles = self.bits_to_int(bits, ctr, ctr + 15)
        ballLastSeenTime = ballLastSeenCycles * 0.02
        ctr += 16

        bx = self.bits_to_int(bits, ctr, ctr + 9)
        ballX = min_ball_x + ((max_ball_x - min_ball_x) * (bx / 1023.0))
        ctr += 10

        by = self.bits_to_int(bits, ctr, ctr + 9)
        ballY = min_ball_y + ((max_ball_y - min_ball_y) * (by / 1023.0))
        ctr += 10

        ax = self.bits_to_int(bits, ctr, ctr + 9)
        agentX = min_agent_x + ((max_agent_x - min_agent_x) * (ax / 1023.0))
        ctr += 10

        ay = self.bits_to_int(bits, ctr, ctr + 9)
        agentY = min_agent_y + ((max_agent_y - min_agent_y) * (ay / 1023.0))
        ctr += 10

        fFallen = not (bits[ctr] == 0) #
        ctr += 1

        return (True, time, ballLastSeenTime, ballX, ballY, agentX, agentY, fFallen)


    def string_to_bits(self, message):
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

    def hear(self):    
        for message in self.heard_messages:
            bits = self.string_to_bits(message.message)
            success, time, ballLastSeenServerTime, ballX, ballY, agentX, agentY, fFallen = self.bits_to_data(bits)

