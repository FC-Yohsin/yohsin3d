from yohisn3d.agent.noa_behavior import NaoBehavior
from server import Server

class Agent:
    def __init__(
        self,
        agent_number: int,
        agent_type: int,
        behavior_type: str,
        team_name: str,
        host_name: str = "localhost",
        global_port: int = 3100,
        monitor_port: int = 3200,
    ) -> None:

        self.team_name = team_name
        self.agent_number = agent_number
        self.agent_type = agent_type
        self.behavior_type = behavior_type

        self.nao_rsg = "rsg/agent/nao/nao.rsg" if agent_type == 0 else f"rsg/agent/nao/nao_hetero.rsg {agent_type}"

        self.host_name = host_name
        self.agent_running = True
        self.global_port = global_port
        self.monitor_port = monitor_port

        self.global_socket = Server()
        self.monitor_socket = Server()

        self.behavior: NaoBehavior = None

    