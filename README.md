# Artificial-Life---Evolution-Algorithm
## Youtube Video of Experimental Results
https://youtu.be/FBToKYKdB50

## Repository Contents
Bugboss.py - the main program which runs the entire simulation
Buginator.py - the directory of helper functions
Final Simulation Results.csv - the test results of my own experiment, outlined later

## Project
This is the final project for the class Mech Eng 495: Artificial Life at Northwestern University in which students were tasked to model artificial life in Mujoco and create an evolutionary algorithm to optimize the species to perform a certain task.
For my project, I create a bug-like species and optimized them based on the distance travelled in their lifetime.  

To run the project, first ensure that Python and Mujoco are installed on your system.
Then, navigate to the folder containing the directory and run bugboss.py.
Bugboss.py runs the entire simulation and evolutionary algorithm.  It starts by randomly generating a specified population size then simulating each individual by creating a .xml file to run in Mujoco.  The initial and final positions of the individual are recorded to determine their fitness based on the fitness function specified in Buginator.py - which contains helper functions used in the program.  It then stores each individual in a .csv file ranked by their fitness and takes the most fit individuals to copy and then mutate based on the mutation function in Buginator.py.  This processed is repeated for the specified number of generations - storing and ranking each generation in the same .csv file.

To change how fitness is calculated, the user can change the fitness function in Buginator.py as well as how much weight is given to the distance travelled and size of the bug - both of which are currently used to calculate fitness.  

## How Species are Mutated
The code takes the specified number of most fit parent and makes a specified number of mutated version.  The mutations randomly change either the number of segments, number of legs, position of legs, or hinges, or a combination of several.  Of course, there is a chance no mutation will occur, in which case an individual offspring may be a direct copy of the parent.    

## How Fitness is Judged
In the example provided, fitness is a function, fitness = (distance travelled)^2/size, in which size is just the number of body segments (including the head of the individual).  This is done to discourage species to converge to an incredibly long insect.  The distance and size are weighted by factors of 1 and 0.5 respectively.  This is done so species will evolve prioritizing distance travelled over size while still considering both factors.  

## Results 
The 'Final Simulation.csv' file in this repository is the results of the algorithm presented in the video linked above.  For this test, 10 generations of 250 individuals were tested with a parent generation (Generation 0) of the same size.  By running many bugs with short life spans, a wide variety of designs were able to be tested.  In the CSV file, the generation, fitness, number of segments, speed, torques, and positions and hinges of limbs are stored.  In this experiment, as detailed previously, the fitness was determined by the function f = (distance)^2/size, with weights for distance = 1 and size = 0.5.  

### Convergence of design
From looking at the results, an upward trend in fitness is displayed as well as a convergence of designs.  While there are some outliers, namely the two most fit bugs are outliers, the most fit members of the generation largely converge to having 12 segments and 6 legs with occasional mutations.  In addition to this, Generation 10 shows much fewer differences amongst individuals compared to Generation 0.  Plotting the number of segments and number of legs per segment for generations 0 and 10 give the same conclusion.  

![image](https://github.com/Luc3A/Artificial-Life---Evolution-Algorithm/assets/129191037/89e470e1-1ea1-44a8-a8dd-ef3015df35a8)

![image](https://github.com/Luc3A/Artificial-Life---Evolution-Algorithm/assets/129191037/820928ed-165e-4fbd-ba4c-c6a8a3ae3cdd)

From these two plots, we can see much less variation in design in generation 10.  Plotting these parameters against the fitness of individuals in generation 10 emphasizes this convergence, individuals who have converged to this design are the most fit.

![image](https://github.com/Luc3A/Artificial-Life---Evolution-Algorithm/assets/129191037/d01939d0-a581-4ae9-b86d-04e7f229a927)

![image](https://github.com/Luc3A/Artificial-Life---Evolution-Algorithm/assets/129191037/40c19a19-2e5d-4bc1-a126-731dc3a41cc1)


Finally, by plotting the fitness of each individual, separated by generations 0-10, we can see an upwards trend in the fitness of the species.  Each generation has a peak - the most fit individual of the generation, and a dip - the least fit individual of the generation.  In generation 0, we see the lowest of the dips and in generation 10 we see the highest peak.  Furthermore, in generation 10, the least fit individual than many of the individuals in prior generations. This upwards trend shows evolution occured over the 10 generations.  

![image](https://github.com/Luc3A/Artificial-Life---Evolution-Algorithm/assets/129191037/906a0465-0649-4450-96b2-d396ff209d79)

### Speed of Individuals
Another parameter tested was the speed with which each individual moved.  This speed was how quickly the joints moved up and down.  For example, a speed of 10 meant that if a leg was raised upwards, after 10 units of time the leg would begin to lift down.  In generation 0, the speed fluctuated, showing little bearing on the fitness of the individual.  However, by generation 10, the speed of the individuals mostly flatlined, showing convergence to a final value.  

![image](https://github.com/Luc3A/Artificial-Life---Evolution-Algorithm/assets/129191037/f3096490-36c5-4e25-8a0e-2d2d88117045)
![image](https://github.com/Luc3A/Artificial-Life---Evolution-Algorithm/assets/129191037/e1141b8a-1ebd-4eb2-8fe3-8216d58f7b65)

### Position of Legs and Rotational Axes of Hinges
The final parameters tested were the positions of the legs and the rotations by which hinges rotated about.  From the individuals shown in the video it can be seen the the position of the legs converged to being located near the individual's bodies and that the rotation of hinges converged to be largely the same.  This data is emphasized in the .csv file provided where in Generation 10 (individuals 2502-2571), there is little change in the rotational axes and positions of the legs.

