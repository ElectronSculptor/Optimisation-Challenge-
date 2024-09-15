
# Challenge Optim 2024 - Process Assignment Problem

## Introduction

This project tackles an optimization problem inspired by the ROADEF/EURO 2012 challenge. The goal is to assign processes to machines while adhering to capacity constraints and minimizing a specific cost function.

## Problem Description

The objective is to allocate `P` processes to `M` machines, ensuring that:
- Each machine's resource capacity is respected.
- Additional constraints (e.g., conflict and geographic constraints) are also met.

### Input Data:
- **M**: Number of machines
- **P**: Number of processes
- **R**: Number of resources
- **r(p, r)**: Resource consumption of process `p` for resource `r`
- **c(m, r)**: Capacity of machine `m` for resource `r`

### Constraints:
1. **Capacity constraints**: Ensure that the sum of resource consumption for processes assigned to a machine does not exceed the machine's capacity for that resource.
2. **Conflict constraints**: Processes belonging to the same service cannot be assigned to the same machine.
3. **Geographic constraints**: Processes from a given service must be spread across a minimum number of locations.

### Solution:
The solution must assign each process to a machine while respecting these constraints. The cost function to minimize involves reducing excess resource consumption beyond a machine's desired limits.

## Example

An example with 5 processes, 2 machines, and 2 resources:

| Resource | Machine 0 | Machine 1 |
|----------|-----------|-----------|
| Resource 0 | 6         | 4         |
| Resource 1 | 6         | 5         |

The processes are assigned in such a way that all capacity constraints are respected.

## Algorithm

The proposed algorithm is a greedy approach that tries to assign processes to machines:
1. For each process, if its service does not cover the required number of locations, attempt to assign it to a machine in a new location.
2. If no machine in a new location is available, assign the process to any available machine.
3. The assignment is valid if it respects capacity and conflict constraints.

### Data Structures:
- **Processes**: Represented by an ID, resource consumption, and service ID.
- **Machines**: Represented by an ID, resource capacities, and locations.

## Input/Output

### Input:
Each instance is provided in a file containing:
- The number of machines, processes, resources, and services.
- Machine details (location, capacity for each resource).
- Service and process details (resource consumption).

### Output:
For each solved instance, the output should be in a text file `res_n.txt`, where `n` is the instance number. The file should include the team name and the solution.

Example output format:
```
TeamName
Instance 1
0 3 0 1 ...
```
Where each number represents the machine assigned to each process.

## Execution Instructions

### Compilation:
To compile the project, navigate to the project folder and run:
```
make
```

### Running the Checker:
Use the provided `check.exe` to verify your solutions:
```
check.exe res_1.txt res_2.txt ...
```

### Submission:
- Submit your solutions and code before the deadline.
- The best results will be projected throughout the day.

## Evaluation

The solutions are graded based on:
- Whether a solution as good as the baseline algorithm (`ALGO1`) has been submitted (minimum grade 8).
- A higher grade (up to 20) for solutions better than the baseline.

## Acknowledgments

This challenge was organized by the teaching staff at the École des Mines, who provided valuable assistance and feedback throughout the day.
