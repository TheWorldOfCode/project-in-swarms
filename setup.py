""" Install the package vslam """
from setuptools import setup, find_packages, Extension

setup(
    name='swarm',
    version='0.1.0',
    author='TheWorldOfCode',
    author_email='dajak17@student.sdu.dk',
    packages=[
        'swarm',
        'swarm.world',
        'swarm.agent'
    ],
#    scripts=['bin/vo3D'],
#    entry_points={
#        'console_scripts': ['package = package.__main__:main',
#                            ]
#   },
#   description='An awesome package that does something',
    #        long_description=open('README.txt').read(),
    install_requires=[
        "numpy",
        "networkx",
        "matplotlib",
        "pygraphviz"
    ],
#   package_data={'': ['*.png']},
#   include_package_data=True,
#   ext_modules=[Extension("vslam.graph.loop_closure.lowe",
#                          ["vslam/graph/loop_closure/compare.c"])]
)
