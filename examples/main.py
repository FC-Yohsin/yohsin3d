from yohsin3d import Agent

agent = Agent(agent_num=1,
                agent_type=0,
                monitor_port=3200,
                global_port=3100,
                host_name="localhost",
                team_name="FCYohsin",
                )

agent.start()

