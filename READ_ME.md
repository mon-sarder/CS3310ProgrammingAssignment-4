# Critical Path Method (CPM) Implementation
## CS3310 - Programming Assignment #4

This implementation provides a complete solution for the Critical Path Method algorithm with both class-based and array-based approaches.

## Files Included

1. **critical_path_method.py** - Main implementation with both methods
2. **my_project.py** - Template for your own project data
3. **README.md** - This file

## Features

- ✅ Topological sorting using Kahn's algorithm
- ✅ Forward pass to calculate ES (Earliest Start) and EF (Earliest Finish)
- ✅ Backward pass to calculate LS (Latest Start) and LF (Latest Finish)
- ✅ Slack calculation (LS - ES)
- ✅ Critical path identification (tasks with slack = 0)
- ✅ Two implementation methods:
  - Method 1: Using Node class (Object-Oriented)
  - Method 2: Using arrays (as specified in assignment)

## How to Use

### Option 1: Run the examples

```bash
python3 critical_path_method.py
```

This will run two example projects and display complete results.

### Option 2: Use your own project data

1. Open `my_project.py`
2. Modify the tasks list:
   ```python
   tasks = [
       Node("TaskName", time_to_complete),
       # Add more tasks...
   ]
   ```

3. Modify the adjacency matrix:
   ```python
   adj_matrix = [
       [0, 1, 0],  # Task 0 -> Task 1
       [0, 0, 1],  # Task 1 -> Task 2
       [0, 0, 0]   # Task 2 (final task)
   ]
   ```

4. Run your project:
   ```bash
   python3 my_project.py
   ```

## Understanding the Adjacency Matrix

The adjacency matrix represents task dependencies:
- `adj_matrix[i][j] = 1` means task j is an immediate successor of task i
- `adj_matrix[i][j] = 0` means no direct dependency

**Example:**
```
Tasks: A, B, C, D
Dependencies:
- A must complete before C and D
- B must complete before D

Adjacency Matrix:
     A  B  C  D
A [  0  0  1  1 ]  <- A precedes C and D
B [  0  0  0  1 ]  <- B precedes D
C [  0  0  0  0 ]  <- C has no successors
D [  0  0  0  0 ]  <- D has no successors
```

## Output Explanation

The program calculates and displays:

1. **Minimum Completion Time**: Total project duration
2. **Critical Tasks**: Tasks that cannot be delayed without delaying the project
3. **For each task**:
   - **ES** (Earliest Start): Earliest time the task can start
   - **EF** (Earliest Finish): Earliest time the task can finish
   - **LS** (Latest Start): Latest time the task can start without delaying project
   - **LF** (Latest Finish): Latest time the task can finish without delaying project
   - **Slack**: How much the task can be delayed (LS - ES)
   - **Critical**: Whether the task is on the critical path (Slack = 0)

## Example Output

```
Minimum Completion Time: 12

Critical Tasks: A, C, E, F

Task A: Time=3, ES=0, EF=3, LS=0, LF=3, Slack=0, Critical=True
Task B: Time=2, ES=0, EF=2, LS=5, LF=7, Slack=5, Critical=False
Task C: Time=4, ES=3, EF=7, LS=3, LF=7, Slack=0, Critical=True
...
```

This means:
- Task A is critical (must start immediately, no slack)
- Task B has 5 days of slack (can be delayed up to 5 days)
- The critical path is A → C → E → F
- Total project takes 12 time units

## Key Algorithms Used

### 1. Topological Sorting (Kahn's Algorithm)
- Orders tasks based on dependencies
- Ensures no cycles exist in the project graph
- Complexity: O(V + E) where V = tasks, E = dependencies

### 2. Forward Pass
- Calculates ES and EF for each task
- ES(task) = max(EF of all predecessors)
- EF(task) = ES(task) + task_time

### 3. Backward Pass
- Calculates LS and LF for each task
- LF(task) = min(LS of all successors)
- LS(task) = LF(task) - task_time

### 4. Critical Path Identification
- Slack = LS - ES
- Critical tasks have Slack = 0
- Critical path = sequence of critical tasks

## Assignment Requirements Checklist

✅ Define Node class with ES, EF, LS, LF attributes  
✅ Implement topological sorting  
✅ Forward pass for ES and EF calculation  
✅ Backward pass for LS and LF calculation  
✅ Slack calculation (LS - ES)  
✅ Critical task identification (slack = 0)  
✅ Minimum completion time calculation  
✅ Adjacency matrix representation  
✅ Both Method 1 (class) and Method 2 (arrays) implementations  

## Why Topological Sorting?

Topological sorting is needed because:
1. It ensures we process tasks in a valid dependency order
2. During forward pass, we need predecessors calculated before successors
3. During backward pass, we need successors calculated before predecessors
4. It detects cycles (invalid project graphs)

## Common Issues and Solutions

**Issue**: "Graph has a cycle!"
- **Solution**: Check your adjacency matrix - there's a circular dependency in your tasks

**Issue**: Incorrect critical path
- **Solution**: Verify your adjacency matrix is correct. Remember: adj[i][j] = 1 means j depends on i

**Issue**: Wrong completion time
- **Solution**: Make sure all final tasks (tasks with no successors) are identified correctly

## Author
CS3310 Programming Assignment #4 Solution