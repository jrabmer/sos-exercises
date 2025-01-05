# 3-Colorability

Formulating the 3-Col problem as a GA problem requires the following properties:

## Encoding

Assume a graph has N vertices and we have 3 colors. We can represent the colors using a list of integers ```[0,1,2]```. A chromosome could then be 
represented by a list of length N, where the position in the list refers to the vertex and the entry to the color. 

An example for this would be a graph with 4 vertices. A chromosome could look like this: ```[0,1,2,0]```

## Fitness function

The fitness function should reward colorings that reduce conflicts between adjacent vertices. A simple fitness function can be:

- Count the number of edges where adjacent vertices have different colors.
- The fitness score is maximized when all edges connect vertices of different colors.
- Divide by number of edges $m$

Mathematically:
$$
fit = \sum_{edges (u,v)} \frac{\delta(color[u] \neq color[v])}{m}
$$

where $\delta$ is an indicator function that is 1 if the colors differ and 0 if they are the same. For an optimal solution, this fitness score would be equal to the total number of edges in the graph.

## Genetic Operators

1. **Selection**: Use tournament selection or roulette-wheel to favour chromosomes with higher fitness 
2. **Crossover**: Single-point crossover should be fine (consider uniform crossover if more diversity is needed)
3. **Mutation**: Randomly select vertex and assign different color

## Handling Constriants
Start off using penalty-based approaches. Subtract a penalty from fitness scroe for each conflicting edge. Other options is using repair operators. Check after mutationor crossover and randomly assign different color to one of the two vertices of conflicting edge. 

## Initialization
Generate intial population by assigning random colorsr to each vertex.