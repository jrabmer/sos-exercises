# Job Shop Scheduling Problem

Use the following available [Github repo](https://en.wikipedia.org/wiki/Job-shop_scheduling) for instances. On top of this there is a python library for the problem [here](https://pypi.org/project/job-shop-lib/).

## Instances:

### ft06, la01, la29, la40:

The structure is:
- Every line represents one job
- A job consists of multiple parts, each of which is manufactured on a specific machine for a specific amount of time
- In the file, this is represented in the form: 
`[Machine for first part] [Time for first part] [Machine for second part] [Time for second part] ...`
- E.g. the line `03 55 01 12 05 10` represents a job that needs 55 min on machine `#3`, 12 min on machine `#1` and 10 min on machine `#5`


Code for reading the file (from [Github Repo](https://github.com/BrenoCPimenta/Ant-Colony-Optimization)):
```
def __readData(self, file_name):
    """
    Reads file and create a first data structure.
    The structure is a Matrix:
        Line:Jobs 
        Column: Machines
        Content:time of execution.

    returns:
        The matrix.
    """        
    jobs = []
    with open("test_instances/" + file_name,'r') as file: 
        for line in file: 
            machines = {}
            this_machine = None
            for j,value in enumerate(line.split()):
                if j%2 != 0:
                    machines.update({this_machine : value})
                else:
                    this_machine = value
            jobs.append(machines)

    return jobs #Named as <data> outside this method
```
