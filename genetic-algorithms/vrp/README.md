# Vehicle Routing Problem

Formulating the Quadratic Assignment Problem as a GA problem requires the following properties:

## Encoding
A solution is a permutation of the facilities to the locations. This permutation can be represented as a chromosome in the genetic algorithm (GA).
For example, a permutation of facilities $[f_1,f_2,...,f_n]$ represents assigning the facility $f_1$ to location 1, $f_2$ to location 2, and so on.


## Fitness function
Minimize the total cost:
$$
\sum_{a,b \in P}{w_{a,b}d_{f(a), f(b)}}
$$
Where $w$ is the weight function, $d$ a distance function and $f$ an assigment of facilities to locations. 

## Genetic Operators

1. **Selection**: Roulette Wheel Selection
2. **Crossover**: Two point crossover
3. **Mutation**: Swap mutation

## Initialization
Generate a population of random permutations of the facilities. This can be done by randomly shuffling the list of facilities multiple times to create the initial solutions.