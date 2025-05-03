# Graph Coloring Algorithm - Demonstrating NP-Completeness of the COL Problem

This project implements a graph coloring algorithm to demonstrate the NP-Completeness of the COL problem. The algorithm is designed to solve the problem in polynomial time, efficiently coloring the nodes of a graph such that no two adjacent nodes share the same color.
There is no proof that this algorithem always uses the least amount of colors. But I'm certain. :)

## Features

- **Graph Generation**: Generates random geometric graphs or allows custom edge lists to define graphs.
- **Graph Coloring**: Implements a step-by-step graph coloring algorithm that prioritizes nodes with the most connections.
- **Visualization**: Visualizes the graph with nodes and edges using Matplotlib, showing the coloring process.
- **Time Complexity Analysis**: Measures and plots the time complexity of the algorithm for varying graph sizes.
- **Command-Line Interface**: Run the program with different options to visualize examples or analyze time efficiency.

## How to Run

1. Clone the repository and install the required dependencies:
   - `networkx`
   - `matplotlib`

2. Run the program from the command line:
   - `python COL_Problems.py --example`: Visualizes an example graph coloring.
   - `python COL_Problems.py --time_efficiency`: Analyzes the time complexity of the algorithm.

3. Customize the graph by modifying the `n_nodes` and `n_edges` parameters or providing a custom edge list.

## Example Output

The program generates a graph visualization with nodes colored based on the algorithm's output. It also provides metrics such as the number of colors used and the time efficiency of the algorithm.

## Dependencies

- Python 3.x
- `networkx`
- `matplotlib`

## Files

- **`COL_Problems.py`**: Main script containing the graph coloring algorithm, visualization logic, and command-line interface.

## License

This project is licensed under the MIT License.
