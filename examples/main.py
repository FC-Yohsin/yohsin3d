from yohsin3d import Agent

agent = Agent(agent_num=1,
                agent_type=0,
                behavior_type="base",
                monitor_port=-1,
                global_port=3200,
                host_name="localhost",
                team_name="FCYohsin")

agent.start()

