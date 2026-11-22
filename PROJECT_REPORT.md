# CAPSTONE PROJECT REPORT
## Mini-Courier Planner

**Subject:** Design and Analysis of Algorithms (DAA)  
**Project Type:** Python-based algorithm integration prototype

> Complete the student/institution details on the cover page before submission.

| Particular | Details |
|---|---|
| Student Name | ______________________________ |
| Roll Number | ______________________________ |
| Programme / Section | ______________________________ |
| University | ______________________________ |
| Subject | Design and Analysis of Algorithms |
| Project Title | Mini-Courier Planner |
| Faculty Name | ______________________________ |
| Submission Date | ______________________________ |

---

## Abstract

Mini-Courier Planner is a Python application that demonstrates how fundamental algorithm design techniques can be combined to solve a simplified courier-planning problem. Given a collection of parcels, a vehicle capacity and a weighted road network, the application prioritizes parcels, selects a high-value feasible package set, calculates shortest paths and produces an approximate delivery tour. The solution integrates comparison sorting, dynamic programming, Dijkstra's shortest-path algorithm and the nearest-neighbor approximation heuristic for the Traveling Salesperson Problem. A benchmark mode records execution time for selected components at increasing input sizes. The application uses CSV files for input and requires only the Python standard library.

## 1. Introduction

Courier services need to decide which parcels should be loaded into a vehicle and in what order delivery locations should be visited. A practical system must consider parcel urgency, vehicle capacity and travel distance. These decisions map naturally to well-known problems in Design and Analysis of Algorithms.

This project creates a small, reproducible prototype. It is not connected to live maps or courier-company systems; the included road distances are sample values intended for algorithm demonstration.

## 2. Problem statement

Design and implement a Python application that accepts parcel information and a weighted graph of delivery locations, then generates:
- a prioritized parcel queue;
- a feasible, high-value parcel selection within vehicle capacity;
- shortest-path distances from the depot;
- an approximate route visiting selected delivery locations and returning to the depot; and
- runtime measurements for selected algorithmic components.

## 3. Objectives

1. Apply sorting to prioritize urgent parcels.
2. Apply 0/1 Knapsack dynamic programming to optimize package selection.
3. Represent delivery locations using a weighted adjacency-list graph.
4. Apply Dijkstra's algorithm for shortest paths.
5. Apply a nearest-neighbor heuristic to approximate a TSP delivery tour.
6. Analyze time and space complexity.
7. Test correctness and compare runtime for different input sizes.

## 4. Scope and assumptions

- Parcel weights, priorities and values are positive integers.
- Larger priority scores indicate greater urgency.
- Earlier deadlines are preferred when priority scores are equal.
- Each parcel is either selected completely or not selected (0/1 selection).
- The vehicle has one fixed maximum weight capacity.
- Road links are undirected and have non-negative integer distances.
- Every selected destination is reachable from the depot.
- Multiple parcels at the same destination require only one visit.
- The route returns to the depot after the final delivery.
- The nearest-neighbor TSP heuristic is not guaranteed to find the globally optimal tour.

## 5. System design

### 5.1 Input

**Parcel data:** parcel ID, destination, weight, priority, deadline and value.  
**Road data:** source node, destination node and distance.  
**Configuration:** depot node and vehicle capacity.

### 5.2 Processing pipeline

```text
Parcel CSV + Road CSV
          |
          v
   Validate and load data
          |
          v
 Sort parcels by priority/deadline
          |
          v
  0/1 Knapsack DP selection
          |
          v
 Build selected destination list
          |
          v
 Dijkstra shortest-path calculations
          |
          v
 Nearest-neighbor delivery tour
          |
          v
 Plan report + benchmark CSV
```

### 5.3 Output

The program prints and saves a report containing the prioritized parcel queue, selected parcels, total selected weight/value, shortest-path distances, visit order, expanded road path and total tour distance. Benchmark mode writes a CSV file containing measured runtimes.

## 6. Algorithms used

### 6.1 Sorting — parcel prioritization

The parcel list is sorted by:
1. priority in descending order;
2. deadline in ascending order; and
3. parcel ID in ascending order for deterministic ties.

Python's comparison sort is used. Its time complexity is **O(n log n)**.

### 6.2 Dynamic Programming — 0/1 Knapsack

Let `dp[i][c]` represent the maximum total value obtainable from the first `i` parcels with capacity `c`.

For parcel `i` with weight `w` and value `v`:

- If `w > c`, `dp[i][c] = dp[i-1][c]`.
- Otherwise, `dp[i][c] = max(dp[i-1][c], v + dp[i-1][c-w])`.

The selected parcel set is reconstructed by tracing backwards through the DP table. Time complexity is **O(nW)** and space complexity is **O(nW)**, where `W` is the integer capacity.

### 6.3 Graph representation

The road network is stored as an adjacency list. Each node stores its connected neighbors and the corresponding edge distances. This representation is suitable for sparse road networks.

### 6.4 Dijkstra's shortest-path algorithm

Dijkstra's algorithm uses a min-priority queue to repeatedly process the currently closest unvisited node and relax its outgoing edges. It is valid because all road distances are non-negative. With a binary heap, the complexity is **O((V+E) log V)**.

### 6.5 Nearest-neighbor TSP heuristic

Starting at the depot, the algorithm repeatedly selects the nearest unvisited delivery destination using shortest-path distances. It then returns to the depot. The method is a practical approximation for a small prototype, but it does not guarantee an optimal TSP tour.

## 7. Implementation

The code is separated into modules:
- `models.py`: parcel data model.
- `io_utils.py`: CSV loading and text output.
- `algorithms.py`: sorting, knapsack, Dijkstra and nearest-neighbor algorithms.
- `planner.py`: integrates the algorithms into a delivery plan.
- `benchmark.py`: measures runtime.
- `main.py`: command-line interface.

No external libraries are needed.

## 8. Complexity analysis

| Algorithm | Time complexity | Space complexity |
|---|---:|---:|
| Parcel sorting | O(n log n) | O(n) |
| 0/1 Knapsack DP | O(nW) | O(nW) |
| Dijkstra (binary heap) | O((V+E) log V) | O(V+E) |
| Nearest-neighbor tour with Dijkstra legs | O(k(V+E) log V) | O(V+E) |

Here, `n` is the number of parcels, `W` is vehicle capacity, `V` is the number of graph vertices, `E` is the number of edges and `k` is the number of unique selected destinations.

## 9. Testing and validation

The test suite checks:
- parcel priority ordering;
- knapsack selection does not exceed capacity and achieves the expected value for a known test case;
- Dijkstra returns the expected shortest distance and path; and
- the approximate tour starts and ends at the depot with the expected distance on a small graph.

Run tests with:

```bash
python -m unittest discover -s tests -v
```

For demonstration, run:

```bash
python -m courier_planner.main --benchmark
```

The application generates `outputs/delivery_plan.txt` and `outputs/benchmark_results.csv`.

## 10. Performance evaluation

Benchmark mode tests sorting and knapsack with 10, 25, 50, 100 and 160 parcels. It also records Dijkstra runtime for the supplied graph. The values are measured on the computer executing the program, so they can vary by processor, operating system and Python version.

Use the generated `benchmark_results.csv` to create a runtime chart for the final presentation. Include a screenshot of the chart and terminal output from your own execution. Do not copy or invent runtime values.

## 11. Results and discussion

The application demonstrates the integration of multiple DAA concepts in a single workflow. Sorting produces a deterministic urgency queue. Knapsack selects the combination with maximum total value under the capacity constraint. Dijkstra provides shortest paths in the supplied road graph, and nearest-neighbor uses those distances to construct a feasible delivery tour.

There is an important modeling distinction: the knapsack objective maximizes parcel value, while urgency is used to order the input list and resolve equal-value DP choices indirectly through deterministic processing. A production system could combine urgency and value into a carefully defined objective or use mandatory-priority constraints.

## 12. Limitations

- Sample road distances are static and illustrative.
- The model does not include traffic, time windows, fuel, driver hours or service time.
- Knapsack uses integer capacity units.
- Nearest-neighbor may produce a route longer than the optimal TSP route.
- The prototype plans one vehicle and one trip.

## 13. Future enhancements

1. Integrate real map/road APIs and live traffic.
2. Add delivery time windows and service durations.
3. Add multiple vehicles and vehicle-routing algorithms.
4. Compare nearest-neighbor with 2-opt local search.
5. Add a graphical user interface and interactive map.
6. Add input validation reports and persistent delivery history.

## 14. Conclusion

Mini-Courier Planner demonstrates how sorting, dynamic programming, graph algorithms and approximation techniques can be integrated to address a simplified courier-planning problem. It produces a prioritized parcel queue, a capacity-constrained package selection and an approximate delivery route. The modular implementation, sample CSV data, unit tests and runtime benchmark make the project suitable for academic demonstration and further development.

## References

1. Cormen, T. H., Leiserson, C. E., Rivest, R. L. and Stein, C. *Introduction to Algorithms*. MIT Press.
2. Kleinberg, J. and Tardos, É. *Algorithm Design*. Pearson.
3. Python Software Foundation. *Python 3 Documentation*: https://docs.python.org/3/
