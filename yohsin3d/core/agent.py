from .network.server import Server
from .behavior import Behavior
import signal, sys, traceback


class Agent:
    def __init__(
        self,
        agent_num: int,
        agent_type: int,
        team_name: str = "FCYohsin",
        host_name: str = "localhost",
        global_port: int = 3100,
        monitor_port: int = 3200,
    ) -> None:

        self.team_name = team_name
        self.agent_num = agent_num
        self.agent_type = agent_type

        self.nao_rsg = "rsg/agent/nao/nao.rsg" if agent_type == 0 else f"rsg/agent/nao/nao_hetero.rsg {agent_type}"

        self.host_name = host_name
        self.agent_running = True
        self.global_port = global_port
        self.monitor_port = monitor_port

        self.global_socket = Server()
        self.monitor_socket = Server()
        self.behavior: Behavior = Behavior(
            team_name=self.team_name,
            rsg=self.nao_rsg,
            agent_type=self.agent_type,
            agent_unum=self.agent_num,
            start_coordinates=(0,0,0)
        )

    def done(self):
        self.global_socket.close()
        if self.monitor_port != -1:
            self.monitor_socket.close()

    def run(self):

        behavior = self.behavior
        if behavior:
            try:
                self.global_socket.connect(self.host_name, self.global_port)
                if self.monitor_port != -1:
                    self.monitor_socket.connect(self.host_name,
                                                self.monitor_port)
            except ConnectionRefusedError:
                print("Connection Refused Error...")
                print("Make sure you have the server running...")
                self.done()
                exit()

            print("Connection Established...")
            self.global_socket.put_message(behavior.spawn_message())

            while self.agent_running:
                try:
                    msg_from_server = self.global_socket.get_message().decode('utf-8')
                    msg_to_server = behavior.think(msg_from_server)
                    if msg_to_server is not None:
                        self.global_socket.put_message(msg_to_server)
                    if self.monitor_port != -1:
                        self.monitor_socket.put_message(behavior.get_monitor_message())

                except Exception as e:
                    print(traceback.format_exc())
                    self.done()
                    exit()

    def start(self):
        def signal_handler(sig, _):
            print('\nExiting!')
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        self.run()
        self.done()