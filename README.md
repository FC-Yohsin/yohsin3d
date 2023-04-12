[![CodeFactor](https://www.codefactor.io/repository/github/fc-yohsin/yohsin3d/badge)](https://www.codefactor.io/repository/github/fc-yohsin/yohsin3d)

# Yohsin3d: Python Framework for RoboCup 3D Soccer Agents

Yohsin3d is an open-source Python framework that simplifies the development of RoboCup 3D soccer agents. It handles low-level details like server communication, basic locomotion, and localization, allowing you to focus on adding functionality to the agents. With extensive machine learning support and a thriving community, Python is an excellent choice for building intelligent and adaptive soccer agents.

## RoboCup 3D Simulation League

The [RoboCup 3D Simulation League](https://ssim.robocup.org/3d-simulation/) is a platform that enables software agents to control humanoid robots, running on a realistic physics engine to simulate soccer matches. It serves as a challenging and exciting way for researchers to explore robotics and AI.

To make it easier for newcomers to get started, Yohsin3d provides a user-friendly framework for building RoboCup 3D soccer agents. With Yohsin3d, anyone can dive into the field of robotics and AI without facing the typical programming difficulties associated with physical robots.

## Starting the simulation

To begin the simulation, you'll need to take a few steps to configure your machine and set up the server. We recommend starting by downloading the appropriate version of Java, which you can find by following the link we've provided. Once you have Java installed, you can then proceed to set up the server on your machine.

To make this process as easy as possible, we've created a separate repository that utilizes a Docker container. With this container, you can quickly and easily start the server without having to worry about any complex configuration. Simply follow the instructions provided in the repository to get started.

### Java Download

- For Windows, download Java [here](https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u345-b01/OpenJDK8U-jdk_x64_windows_hotspot_8u345b01.msi)
- For macOS, download Java [here](https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u345-b01/OpenJDK8U-jdk_x64_mac_hotspot_8u345b01.tar.gz)

### Docker
Make sure you configure docker on your machine. See more details from [here](https://docs.docker.com/get-docker/).

### Clone the Repository

Clone the repository using the following command:

```bash
$ git clone https://github.com/Habib-Shahzad/Roboviz-And-Rcsserver3d.git
```


### Starting the Server and Monitor

- On macOS:
  - Start the server by running `server.sh`
  - Start the monitor by running `client.sh`
- On Windows:
  - Start the server by running `server.bat`
  - Start the monitor by running `client.bat`

## Yohsin3d Overview

Yohsin3d is a highly capable framework that provides an ideal level of abstraction for developing RoboCup 3D soccer agent teams. By following solid design principles, it enables you to establish a strong foundation for your development efforts.

One of the most significant benefits of Yohsin3d is that it handles many low-level details for you, allowing you to focus on the most important aspect of your work: building the "brain" of your robot agent. This approach makes it easy to create powerful, adaptable, and intelligent soccer agents, while minimizing the onboarding friction that is often associated with RoboCup 3D soccer development.

Overall, Yohsin3d is an excellent choice for developers who want to maximize their productivity while creating top-tier RoboCup 3D soccer agents. By leveraging its robust capabilities and intuitive design, you can quickly and easily build sophisticated agents that excel on the field.

We reccomend using python 3.11 for this framework.
After starting the simulation, run these commands to get started.

```bash
$ pip install yohsin3d
$ python examples/main.py
```

The example file shows how to customize the behavior of an agent provided by yohsin3d. It does so by defining a new class, DerivedBehavior, which inherits from the BaseBehavior class provided by yohsin3d. The DerivedBehavior class overrides some functionalities, allowing users to add their own custom logic to the agent's behavior.

Next, the code initializes an instance of DerivedBehavior with starting coordinates and passes it as an argument to an instance of the Agent class. The Agent instance is then started, which connects the agent to the server based on the parameters provided and spawns it onto the soccer field.

Overall, this example file serves as a starting point for developing custom agent behaviors in yohsin3d.


## Contributing

We welcome contributions to improve Yohsin3d and make it more accessible to newcomers. Please feel free to submit issues or pull requests on our [GitHub repository](https://github.com/FC-Yohsin/yohsin3d).
