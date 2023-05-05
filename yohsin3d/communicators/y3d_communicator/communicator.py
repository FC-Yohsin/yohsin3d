from ...core.common.constants import *
from ...core import BaseCommunicator
from .bit_codec import BitCodec


class CommunicationData:
    def __init__(
            self,
            heard_from=None,
            time=None,
            ball_x=None,
            ball_y=None,
            my_x=None,
            my_y=None):
        self.heard_from = heard_from
        self.time = time
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.my_x = my_x
        self.my_y = my_y

    def __str__(self):
        return f"Agent {self.heard_from} heard: time={self.time}, ball_x={self.ball_x}, ball_y={self.ball_y}, position = ({self.my_x}, {self.my_y})"


class Y3dCommunicator(BaseCommunicator):

    def __init__(self) -> None:
        super().__init__()
        self.heard_data = CommunicationData()
        self.heard_data_type = CommunicationData

    def data_to_bits(self, time, ball_x, ball_y, my_x, my_y):
        bits = []

        cycles = int(time * 50 + 0.1) % (1 << 16)
        time_bits = BitCodec.int_to_bits(cycles, 16)
        ball_x_bits = BitCodec.encode_float(ball_x, min_ball_x, max_ball_x)
        ball_y_bits = BitCodec.encode_float(ball_y, min_ball_y, max_ball_y)
        my_x_bits = BitCodec.encode_float(my_x, min_agent_x, max_agent_x)
        my_y_bits = BitCodec.encode_float(my_y, min_agent_y, max_agent_y)

        bits.extend(time_bits)
        bits.extend(ball_x_bits)
        bits.extend(ball_y_bits)
        bits.extend(my_x_bits)
        bits.extend(my_y_bits)

        return bits

    def say(self):
        ball = self.localizer.ball_position
        me = self.localizer.my_location.position
        bits = self.data_to_bits(
            self.world_model.get_time(),
            ball[0],
            ball[1],
            me[0],
            me[1],
        )

        message = BitCodec.bits_to_string(bits)
        self.said_message = message

    def bits_to_data(self, bits):
        time, ballX, ballY, agentX, agentY = 0, 0, 0, 0, 0

        ctr = 0

        cycles = BitCodec.bits_to_int(bits, ctr, ctr + 15)
        time = cycles * 0.02
        ctr += 16

        bx_bits = bits[ctr:ctr + 10]
        ballX = BitCodec.decode_bit_array(bx_bits, min_ball_x, max_ball_x)
        ctr += 10

        by_bits = bits[ctr:ctr + 10]
        ballY = BitCodec.decode_bit_array(by_bits, min_ball_y, max_ball_y)
        ctr += 10

        ax_bits = bits[ctr:ctr + 10]
        agentX = BitCodec.decode_bit_array(ax_bits, min_agent_x, max_agent_x)
        ctr += 10

        ay_bits = bits[ctr:ctr + 10]
        agentY = BitCodec.decode_bit_array(ay_bits, min_agent_y, max_agent_y)
        ctr += 10

        return time, ballX, ballY, agentX, agentY

    def hear(self) -> None:
        heard_message = self.heard_message
        message = heard_message.message

        if message is None:
            self.heard_data = CommunicationData()
            return

        bits = BitCodec.string_to_bits(message)
        time, ballX, ballY, agentX, agentY = self.bits_to_data(bits)

        heard_time = heard_message.heard_time
        delta_game_time = self.world_model.get_time() - self.world_model.get_gametime()
        heard_server_time = heard_time + delta_game_time

        time += int((heard_server_time - time) / 1310.72) * 1310.72
        cycles = int(time * 50 + 0.1)
        unum = (cycles % (NUM_AGENTS * 2)) // 2 + 1
        self.heard_data = CommunicationData(
            unum, time, ballX, ballY, agentX, agentY)
