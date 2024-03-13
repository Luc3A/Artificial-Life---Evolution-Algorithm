# Artificial-Life---Evolution-Algorithm
This is the final project for the class Mech Eng 495: Artificial Life at Northwestern University in which students were tasked to model artificial life in Mujoco and create an evolutionary algorithm to optimize the species to perform a certain task.
For my project, I create a bug-like species and optimized them based on the distance travelled in their lifetime.  

To run the project, first ensure that Python and Mujoco are installed on your system.
Then, navigate to the folder containing the directory and run bugboss.py.
Bugboss.py runs the entire simulation and evolutionary algorithm.  It starts by randomly generating a specified population size then simulating each individual to determine their fitness based on the fitness function specified in Buginator.py - which contains helper functions used in the program.  It then stores each individual in a .csv file ranked by their fitness and takes the most fit individuals to copy and then mutate based on the mutation function in Buginator.py.  This processed is repeated for the specified number of generations - storing and ranking each generation in the same .csv file.

To change how fitness is calculated, the user can change the fitness function in Buginator.py as well as how much weight is given to the distance travelled and size of the bug - both of which are currently used to calculate fitness.  
