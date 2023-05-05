import signal
import sys
import traceback

from .network import Server
from .body import AgentType
from .behavior import BaseBehavior


class Agent:
    def __init__(
        self,
        agent_num: int,
        team_name: str,
        behavior: BaseBehavior,
        agent_type: AgentType = 0,
        host_name: str = "localhost",
        global_port: int = 3100,
        monitor_port: int = 3200,
    ) -> None:

        self.team_name = team_name
        self.agent_num = agent_num
        self.agent_type = agent_type
        self.spawned = False

        self.nao_rsg = "rsg/agent/nao/nao.rsg" if agent_type == AgentType.NAO else f"rsg/agent/nao/nao_hetero.rsg {int(agent_type)}"

        self.host_name = host_name
        self.agent_running = True
        self.global_port = global_port
        self.monitor_port = monitor_port

        self.global_socket = Server()
        self.monitor_socket = Server()
        self.behavior: BaseBehavior = behavior
        self.behavior.initialize(team_name)
        self.behavior.body_model.agent_type = agent_type

    def done(self):
        self.global_socket.close()
        if self.monitor_port != -1:
            self.monitor_socket.close()

    def setup_message(self):
        print("Loading rsg: " + "(scene " + self.nao_rsg + ")")
        return f"(scene {self.nao_rsg})"

    def spawn_message(self):
        return f"(init (unum {self.agent_num})(teamname {self.team_name}))"

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
            self.global_socket.put_message(self.setup_message())

            while self.agent_running:
                try:
                    msg_from_server = self.global_socket.get_message().decode('utf-8')
                    msg_to_server = None
                    if not self.spawned:
                        msg_to_server = self.spawn_message()
                        self.spawned = True
                    else:
                        msg_to_server = behavior.think(msg_from_server)

                    if msg_to_server is not None:
                        self.global_socket.put_message(msg_to_server)
                    if self.monitor_port != -1:
                        self.monitor_socket.put_message(
                            behavior.get_monitor_message())

                except Exception as e:
                    print(traceback.format_exc())
                    self.done()
                    exit()

    def handler(self):
        def signal_handler(sig, _):
            print('\nExiting!')
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

    def start(self, custom_handler=None):
        if custom_handler:
            custom_handler()
        else:
            self.handler()

        self.run()
        self.done()
