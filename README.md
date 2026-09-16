# RobotPathFinderIA
RobotPathFinderIA is an experimental robotics research project focused to find efficient paths between two points for industrial robots using Evolutionary algorithms.

The project is developed in Python and integrated with RoboDK for robot simulation.
The Genetic Algorithm was built from scratch and evaluates the robot paths using a fitness function based on multiple criteria:

- Estimated execution time
- Robot reachability
- Collisions detected

The algorithm generates random paths between the Origin point and the Destination point and then optimizes every candidate.
Each candidate path is assigned a fitness score according to these metrics, through selection, crossover and mutation. The population evolves after a few generations progressively improving path quality.

The highest-fitness solution is selected and displayed in RoboDK. 

Generation 1
![Robot movements in Gen1](media/gen1.gif)
At the beginning of optimizaion, robot moves are completely random without any logical sequence, often crashing into the obstacles or attempting to go to unreachable points.

Generation 2
![Robot movements in Gen2](media/gen2.gif)
After approximately 2-3 minutes of optimization, the population reaches Generation 2. Movements seem to be a bit more logical, but still the robot is crashing multiple times.

Generation 5
![Robot movements in Gen5](media/gen5_no_domain_injection.gif)
Around 10 minutes of training the algorithm has reached generation 5 (though this is the last one in this example, number of generations can be modified). Collisions and unreachable points have been eliminated, but the path could be still improved.

Domain Injection

Domain injection in evolutionary algorithms refers to embedding domain-specific knowledge, constraints, or representations into the optimization process to guide search toward more relevant, robust, or interpretable solutions. In this case, domain injection is inserted as coordinates, the programs takes as a reference the Origin and the Destination points generating paths that are more useful for the final solution instead of generate random paths all over the cartesian space of the robot.

Number of points, generations, and number of candidates (paths) are variables that can be modified, impacting the results and training time. Based on tests, creating a population of 200 candidates passing them through five generations shows fair results, this is achieved in approx. 10 minutes of training.

Generation 5 
![Robot movements in Gen5 training completed](media/gen5_training_complete_domain_injection.gif)

| Stage | Approximate time | Observed result |
|---|---:|---|
| Generation 1 | Initial population | Random paths, collisions and unreachable poses |
| Generation 2 | 2–3 minutes | More structured paths, but collisions remain |
| Generation 5 | About 10 minutes | Feasible path without detected collisions |


## Current limitations
- Population quickly converges into similar individuals (loss of genetic diversity) 
- Current implementation does not guarantee a 100% collision free path
