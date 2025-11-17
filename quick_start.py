"""
Quick Start Example - Simple CPM Problem
Run this file to see a basic example
"""

from critical_path_method import Node, critical_path_method_class, print_results_class

# Simple example: Building a house
# A: Lay foundation (4 days)
# B: Order materials (1 day)
# C: Build walls (5 days) - requires A
# D: Build roof (3 days) - requires C
# E: Install plumbing (2 days) - requires A
# F: Install electrical (2 days) - requires A
# G: Interior finishing (4 days) - requires D, E, F

tasks = [
    Node("Lay Foundation", 4),  # 0
    Node("Order Materials", 1),  # 1
    Node("Build Walls", 5),  # 2
    Node("Build Roof", 3),  # 3
    Node("Install Plumbing", 2),  # 4
    Node("Install Electrical", 2),  # 5
    Node("Interior Finishing", 4)  # 6
]

# Adjacency matrix
adj_matrix = [
    [0, 0, 1, 0, 1, 1, 0],  # Foundation -> Walls, Plumbing, Electrical
    [0, 0, 0, 0, 0, 0, 0],  # Materials (independent)
    [0, 0, 0, 1, 0, 0, 0],  # Walls -> Roof
    [0, 0, 0, 0, 0, 0, 1],  # Roof -> Finishing
    [0, 0, 0, 0, 0, 0, 1],  # Plumbing -> Finishing
    [0, 0, 0, 0, 0, 0, 1],  # Electrical -> Finishing
    [0, 0, 0, 0, 0, 0, 0]  # Finishing (final)
]

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("HOUSE BUILDING PROJECT - CRITICAL PATH ANALYSIS")
    print("=" * 70)
    print("\nProject Tasks:")
    print("- Lay Foundation (4 days)")
    print("- Order Materials (1 day) - can be done anytime")
    print("- Build Walls (5 days) - requires foundation")
    print("- Build Roof (3 days) - requires walls")
    print("- Install Plumbing (2 days) - requires foundation")
    print("- Install Electrical (2 days) - requires foundation")
    print("- Interior Finishing (4 days) - requires roof, plumbing, electrical")

    min_time, critical_tasks, results = critical_path_method_class(tasks, adj_matrix)
    print_results_class(min_time, critical_tasks, results)

    print("\nInterpretation:")
    print("-" * 70)
    print(f"The project will take {min_time} days to complete.")
    print(f"Critical tasks (must stay on schedule): {', '.join(critical_tasks)}")
    print("\nNon-critical tasks can be delayed by their slack time without")
    print("affecting the overall project completion date.")
