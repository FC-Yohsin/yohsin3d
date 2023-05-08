import time
from .agent import Agent
from multiprocessing import Process
from typing import List


def agent_start(agent: Agent):
    agent.start(lambda: None)


class Spawner:
    def __init__(self) -> None:
        self.agents: List[Agent] = []

    def add(self, agent: Agent) -> None:
        self.agents.append(agent)

    def done(self):
        for agent in self.agents:
            agent.done()


    def start(self) -> None:
        

        processes: List[Process] = []
        for agent in self.agents:
            processes.append(Process(target=agent_start, args=(agent,)))
        for process in processes:
            process.start()
            time.sleep(1)
        for process in processes:
            process.join()