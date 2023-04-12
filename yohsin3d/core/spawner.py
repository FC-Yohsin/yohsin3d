import threading
import time
from .agent import Agent

from typing import List


class Spawner:
    def __init__(self) -> None:
        self.agents: List[Agent] = []

    def add(self, agent: Agent) -> None:
        self.agents.append(agent)

    def done(self):
        for agent in self.agents:
            agent.done()

    def start(self) -> None:
        threads: List[threading.Thread] = []
        for agent in self.agents:
            threads.append(threading.Thread(
                target=agent.start, args=(lambda: None, )))
        for thread in threads:
            thread.start()
            time.sleep(1)
        for thread in threads:
            thread.join()
