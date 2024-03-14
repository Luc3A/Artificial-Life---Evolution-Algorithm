## Artificial-Life---Evolution-Algorithm
# Youtube Video of Experimental Results
https://youtu.be/FBToKYKdB50

# Contents
Bugboss.py - the main program which runs the entire simulation
Buginator.py - the directory of helper functions
Final Simulation Results.csv - the test results of my own experiment, outlined later

# Project
This is the final project for the class Mech Eng 495: Artificial Life at Northwestern University in which students were tasked to model artificial life in Mujoco and create an evolutionary algorithm to optimize the species to perform a certain task.
For my project, I create a bug-like species and optimized them based on the distance travelled in their lifetime.  

To run the project, first ensure that Python and Mujoco are installed on your system.
Then, navigate to the folder containing the directory and run bugboss.py.
Bugboss.py runs the entire simulation and evolutionary algorithm.  It starts by randomly generating a specified population size then simulating each individual by creating a .xml file to run in Mujoco.  The initial and final positions of the individual are recorded to determine their fitness based on the fitness function specified in Buginator.py - which contains helper functions used in the program.  It then stores each individual in a .csv file ranked by their fitness and takes the most fit individuals to copy and then mutate based on the mutation function in Buginator.py.  This processed is repeated for the specified number of generations - storing and ranking each generation in the same .csv file.

To change how fitness is calculated, the user can change the fitness function in Buginator.py as well as how much weight is given to the distance travelled and size of the bug - both of which are currently used to calculate fitness.  

# How species are mutated
The code takes the specified number of most fit parent and makes a specified number of mutated version.  The mutations randomly change either the number of segments, number of legs, position of legs, or hinges, or a combination of several.  Of course, there is a chance no mutation will occur, in which case an individual offspring may be a direct copy of the parent.    

# How fitness is judged
In the example provided, fitness is a function, fitness = (distance travelled)^2/size, in which size is just the number of body segments (including the head of the individual).  This is done to discourage species to converge to an incredibly long insect.  The distance and size are weighted by factors of 1 and 0.5 respectively.  This is done so species will evolve prioritizing distance travelled over size while still considering both factors.  

# Results 
The 'Final Simulation.csv' file in this repository is the results of the algorithm presented in the video linked above.  For this test, 10 generations of 250 individuals were tested with a parent generation (Generation 0) of the same size.  By running many bugs with short life spans, a wide variety of designs were able to be tested.  In the CSV file, the generation, fitness, number of segments, speed, torques, and positions and hinges of limbs are stored.  

From looking at the results, an upward trend in fitness is displayed as well as a convergence of designs.  While there are some outliers, namely the two most fit bugs are outliers, the most fit members of the generation largely converge to having 12 segments and 6 legs with occasional mutations.  In addition to this, Generation 10 shows much fewer differences amongst individuals compared to Generation 0.
