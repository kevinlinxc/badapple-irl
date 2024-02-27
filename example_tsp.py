from python_tsp.exact import solve_tsp_dynamic_programming
import numpy as np

# Define the distances
distances = np.array([
    [0, 8, 3, 11, 7],
    [8, 0, 4, 5, 10],
    [3, 4, 0, 5, 4],
    [11, 5, 5, 0, 6],
    [7, 10, 4, 6, 0]
])

# Get the unique cities from the distances

# Solve TSP using dynamic programming
tour, distance = solve_tsp_dynamic_programming(distances)

# Print the result
print("Optimal Tour:", [city + 1 for city in tour])
print("Total Distance:", distance)