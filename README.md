# RobotPathFinderIA
RobotPathFinderIA is a robotics research project focused on finding optimal paths between two points for industrial robots using Evolutionary algorithms.

The project is developed in Python and integrated with RoboDK for robot simulation.
The Genetic Algorith was built from scratch and evaluates the robot paths using a fitness function based on multiple criteria:

-Estimated execution time
-Robot reachabilty
-Collisions detected

Each candidate path is assigned a fitness score according to these metrics, through selection, corssover and mutation. The population evolves after a few generations progressively improving path quality.

The highest-fitness solution is selected and displayed to the user.

Generation 1
![Robot movments in Gen1](media/gen1.gif)
At the beggining of training,robot moves are completly random without any ogical sequence, often crashing into the obstacles or attempting to go to non reachable points.
