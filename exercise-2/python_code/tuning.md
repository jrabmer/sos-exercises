# iris

```python
par_C1 = 0.8
par_C2 = 1.7
par_W = 0.5
par_SwarmSize = 100
batchsize = 80  # The number of data instances used by the fitness function
n_hidden = 10
activation = ELU 
n_iteration = 1000
learning_rate = 0.05
```
Accuracy PSO-NN: 1.00
Accuracy Classic-NN: 1.00

# magic gamma
```python
par_C1 = 1.2
par_C2 = 1.6
par_W = 0.8
par_SwarmSize = 50
batchsize = 500  # The number of data instances used by the fitness function
n_hidden = 10
activation = TANH 
learning_rate = 0.05
```
Accuracy Classic-NN: 0.75
Accuracy PSO-NN: 0.76


# glass
```python
par_C1 = 0.8
par_C2 = 1.9
par_W = 0.8
par_SwarmSize = 100
batchsize = 80  # The number of data instances used by the fitness function
activation = SIGMOID 
n_iteration = 5000
learning_rate = 0.05
```
Accuracy PSO-NN: 0.84 (can be from 0.77 to 0.86)
Accuracy Classic-NN: 0.93 (can be anywhere from 0.86 to 0.98)