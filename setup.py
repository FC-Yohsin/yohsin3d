from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='yohsin3d',
    version='0.4.1',
    description='Program your own RoboCup 3D soccer playing agents in python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Habib Shahzad, Abuzar Rasool, Faaz Abidi',
    author_email='habibshehzad55@gmail.com, availabuzar@gmail.com, hasanfaaz10@gmail.com',
    url='https://github.com/FC-Yohsin/yohsin3d',
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="robocup, soccer, 3d, simulation, agents, robotics, machine learning, python, artificial intelligence, locomotion, localization",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.6",
)
