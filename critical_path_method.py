"""
CS3310 - Programming Assignment #4
Critical Path Method (CPM) Implementation
"""

from collections import deque


class Node:
    """
    Node class to represent a task in the project
    """

    def __init__(self, name, time):
        self.name = name
        self.time = time  # Time needed to complete the task
        self.ES = 0  # Earliest Start time
        self.EF = 0  # Earliest Finish time
        self.LS = 0  # Latest Start time
        self.LF = 0  # Latest Finish time
        self.slack = 0  # Slack time (LS - ES)

    def calculate_slack(self):
        """Calculate slack time for this task"""
        self.slack = self.LS - self.ES

    def is_critical(self):
        """Check if this task is critical (slack == 0)"""
        return self.slack == 0

    def __str__(self):
        return (f"Task {self.name}: Time={self.time}, ES={self.ES}, "
                f"EF={self.EF}, LS={self.LS}, LF={self.LF}, "
                f"Slack={self.slack}, Critical={self.is_critical()}")


def topological_sort(n, adj_matrix):
    """
    Perform topological sorting using Kahn's algorithm (BFS-based)

    Args:
        n: Number of tasks
        adj_matrix: Adjacency matrix where adj_matrix[i][j] = 1 if task j is
                    an immediate successor of task i

    Returns:
        List of tasks in topological order
    """
    # Calculate in-degree for each node
    in_degree = [0] * n
    for i in range(n):
        for j in range(n):
            if adj_matrix[i][j] == 1:
                in_degree[j] += 1

    # Initialize queue with nodes that have in-degree 0
    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)

    # Process nodes in topological order
    topo_order = []
    while queue:
        node = queue.popleft()
        topo_order.append(node)

        # Reduce in-degree for successor nodes
        for j in range(n):
            if adj_matrix[node][j] == 1:
                in_degree[j] -= 1
                if in_degree[j] == 0:
                    queue.append(j)

    # Check if topological sort was possible (no cycles)
    if len(topo_order) != n:
        raise ValueError("Graph has a cycle! Cannot perform topological sort.")

    return topo_order


def find_predecessors(task, adj_matrix, n):
    """
    Find all immediate predecessors of a given task

    Args:
        task: Task index
        adj_matrix: Adjacency matrix
        n: Number of tasks

    Returns:
        List of predecessor task indices
    """
    predecessors = []
    for i in range(n):
        if adj_matrix[i][task] == 1:
            predecessors.append(i)
    return predecessors


def find_successors(task, adj_matrix, n):
    """
    Find all immediate successors of a given task

    Args:
        task: Task index
        adj_matrix: Adjacency matrix
        n: Number of tasks

    Returns:
        List of successor task indices
    """
    successors = []
    for j in range(n):
        if adj_matrix[task][j] == 1:
            successors.append(j)
    return successors


def critical_path_method_class(tasks, adj_matrix):
    """
    Method 1: Critical Path Method using Node class

    Args:
        tasks: List of Node objects
        adj_matrix: Adjacency matrix representing task dependencies

    Returns:
        Tuple of (minimum_completion_time, critical_tasks, tasks_with_details)
    """
    n = len(tasks)

    # Step 1: Perform topological sorting
    topo_order = topological_sort(n, adj_matrix)

    # Step 2: Forward pass - Calculate ES and EF
    for task_idx in topo_order:
        task = tasks[task_idx]
        predecessors = find_predecessors(task_idx, adj_matrix, n)

        if not predecessors:
            # Initial task (no predecessors)
            task.ES = 0
        else:
            # ES = max(EF of all predecessors)
            task.ES = max(tasks[pred].EF for pred in predecessors)

        # EF = ES + time to complete the task
        task.EF = task.ES + task.time

    # Step 3: Find the final task(s) and minimum completion time
    # Final tasks are those with no successors
    final_tasks = []
    for i in range(n):
        if not find_successors(i, adj_matrix, n):
            final_tasks.append(i)

    # Minimum completion time is the maximum EF among final tasks
    min_completion_time = max(tasks[i].EF for i in final_tasks)

    # Step 4: Backward pass - Calculate LS and LF
    # Process tasks in reverse topological order
    for task_idx in reversed(topo_order):
        task = tasks[task_idx]
        successors = find_successors(task_idx, adj_matrix, n)

        if not successors:
            # Final task
            task.LF = task.EF
        else:
            # LF = min(LS of all successors)
            task.LF = min(tasks[succ].LS for succ in successors)

        # LS = LF - time to complete the task
        task.LS = task.LF - task.time

    # Step 5: Calculate slack and identify critical tasks
    critical_tasks = []
    for i, task in enumerate(tasks):
        task.calculate_slack()
        if task.is_critical():
            critical_tasks.append(task.name)

    return min_completion_time, critical_tasks, tasks


def critical_path_method_arrays(n, T, adj_matrix, task_names=None):
    """
    Method 2: Critical Path Method using arrays

    Args:
        n: Number of tasks
        T: Array of time required to complete each task
        adj_matrix: Adjacency matrix (A[i][j] = 1 if j is successor of i)
        task_names: Optional list of task names

    Returns:
        Dictionary with ES, EF, LS, LF, slack, and critical path information
    """
    # Initialize arrays
    ES = [0] * n
    EF = [0] * n
    LS = [0] * n
    LF = [0] * n

    # Step 1: Topological sorting
    TS = topological_sort(n, adj_matrix)

    # Step 2: Forward pass - Calculate ES and EF
    for task_idx in TS:
        predecessors = find_predecessors(task_idx, adj_matrix, n)

        if not predecessors:
            ES[task_idx] = 0
        else:
            ES[task_idx] = max(EF[pred] for pred in predecessors)

        EF[task_idx] = ES[task_idx] + T[task_idx]

    # Step 3: Find minimum completion time
    final_tasks = [i for i in range(n) if not find_successors(i, adj_matrix, n)]
    min_completion_time = max(EF[i] for i in final_tasks)

    # Step 4: Backward pass - Calculate LS and LF
    for task_idx in reversed(TS):
        successors = find_successors(task_idx, adj_matrix, n)

        if not successors:
            LF[task_idx] = EF[task_idx]
        else:
            LF[task_idx] = min(LS[succ] for succ in successors)

        LS[task_idx] = LF[task_idx] - T[task_idx]

    # Step 5: Calculate slack and identify critical tasks
    slack = [LS[i] - ES[i] for i in range(n)]
    critical_tasks = [i for i in range(n) if slack[i] == 0]

    # Prepare results
    if task_names is None:
        task_names = [f"Task{i + 1}" for i in range(n)]

    results = {
        'min_completion_time': min_completion_time,
        'ES': ES,
        'EF': EF,
        'LS': LS,
        'LF': LF,
        'slack': slack,
        'critical_tasks': [task_names[i] for i in critical_tasks],
        'topological_order': [task_names[i] for i in TS]
    }

    return results


def print_results_class(min_completion_time, critical_tasks, tasks):
    """Print results from Method 1 (class-based)"""
    print("=" * 70)
    print("CRITICAL PATH METHOD RESULTS (Using Node Class)")
    print("=" * 70)
    print(f"\nMinimum Completion Time: {min_completion_time}")
    print(f"\nCritical Tasks: {', '.join(critical_tasks)}")
    print("\nDetailed Task Information:")
    print("-" * 70)
    for task in tasks:
        print(task)
    print("=" * 70)


def print_results_arrays(results):
    """Print results from Method 2 (array-based)"""
    print("=" * 70)
    print("CRITICAL PATH METHOD RESULTS (Using Arrays)")
    print("=" * 70)
    print(f"\nMinimum Completion Time: {results['min_completion_time']}")
    print(f"\nTopological Order: {' -> '.join(results['topological_order'])}")
    print(f"\nCritical Tasks: {', '.join(results['critical_tasks'])}")
    print("\nDetailed Task Information:")
    print("-" * 70)
    print(f"{'Task':<10} {'Time':<6} {'ES':<6} {'EF':<6} {'LS':<6} {'LF':<6} {'Slack':<6} {'Critical':<10}")
    print("-" * 70)
    n = len(results['ES'])
    task_names = results.get('task_names', [f"Task{i + 1}" for i in range(n)])
    for i in range(n):
        is_critical = "Yes" if results['slack'][i] == 0 else "No"
        print(f"{task_names[i]:<10} {results.get('T', [0] * n)[i]:<6} "
              f"{results['ES'][i]:<6} {results['EF'][i]:<6} "
              f"{results['LS'][i]:<6} {results['LF'][i]:<6} "
              f"{results['slack'][i]:<6} {is_critical:<10}")
    print("=" * 70)


# Example usage and test cases
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Simple Project")
    print("=" * 70)

    # Example 1: Simple project with 6 tasks
    # Task dependencies (from assignment examples):
    # Task A (0): 3 days, no predecessors
    # Task B (1): 2 days, no predecessors
    # Task C (2): 4 days, depends on A
    # Task D (3): 5 days, depends on A
    # Task E (4): 3 days, depends on B, C
    # Task F (5): 2 days, depends on D, E

    # Method 1: Using Node class
    print("\n--- METHOD 1: Using Node Class ---\n")
    tasks_ex1 = [
        Node("A", 3),
        Node("B", 2),
        Node("C", 4),
        Node("D", 5),
        Node("E", 3),
        Node("F", 2)
    ]

    # Adjacency matrix: adj[i][j] = 1 if j is immediate successor of i
    adj_matrix_ex1 = [
        [0, 0, 1, 1, 0, 0],  # A -> C, D
        [0, 0, 0, 0, 1, 0],  # B -> E
        [0, 0, 0, 0, 1, 0],  # C -> E
        [0, 0, 0, 0, 0, 1],  # D -> F
        [0, 0, 0, 0, 0, 1],  # E -> F
        [0, 0, 0, 0, 0, 0]  # F (final task)
    ]

    min_time1, critical1, tasks1 = critical_path_method_class(tasks_ex1, adj_matrix_ex1)
    print_results_class(min_time1, critical1, tasks1)

    # Method 2: Using arrays
    print("\n--- METHOD 2: Using Arrays ---\n")
    n_ex1 = 6
    T_ex1 = [3, 2, 4, 5, 3, 2]
    task_names_ex1 = ["A", "B", "C", "D", "E", "F"]

    results_ex1 = critical_path_method_arrays(n_ex1, T_ex1, adj_matrix_ex1, task_names_ex1)
    results_ex1['T'] = T_ex1
    results_ex1['task_names'] = task_names_ex1
    print_results_arrays(results_ex1)

    # Example 2: Another project
    print("\n" + "=" * 70)
    print("EXAMPLE 2: More Complex Project")
    print("=" * 70)

    # 7 tasks with more complex dependencies
    tasks_ex2 = [
        Node("Start", 0),
        Node("Task1", 4),
        Node("Task2", 3),
        Node("Task3", 6),
        Node("Task4", 2),
        Node("Task5", 5),
        Node("End", 0)
    ]

    adj_matrix_ex2 = [
        [0, 1, 1, 0, 0, 0, 0],  # Start -> Task1, Task2
        [0, 0, 0, 1, 1, 0, 0],  # Task1 -> Task3, Task4
        [0, 0, 0, 1, 0, 0, 0],  # Task2 -> Task3
        [0, 0, 0, 0, 0, 1, 0],  # Task3 -> Task5
        [0, 0, 0, 0, 0, 1, 0],  # Task4 -> Task5
        [0, 0, 0, 0, 0, 0, 1],  # Task5 -> End
        [0, 0, 0, 0, 0, 0, 0]  # End
    ]

    print("\n--- METHOD 1: Using Node Class ---\n")
    min_time2, critical2, tasks2 = critical_path_method_class(tasks_ex2, adj_matrix_ex2)
    print_results_class(min_time2, critical2, tasks2)

    print("\n--- METHOD 2: Using Arrays ---\n")
    n_ex2 = 7
    T_ex2 = [0, 4, 3, 6, 2, 5, 0]
    task_names_ex2 = ["Start", "Task1", "Task2", "Task3", "Task4", "Task5", "End"]
    results_ex2 = critical_path_method_arrays(n_ex2, T_ex2, adj_matrix_ex2, task_names_ex2)
    results_ex2['T'] = T_ex2
    results_ex2['task_names'] = task_names_ex2
    print_results_arrays(results_ex2)