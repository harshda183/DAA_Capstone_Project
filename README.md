# Mini-Courier Planner — DAA Capstone Project

**A Python application combining sorting, dynamic programming, graph algorithms and approximation algorithms to plan a courier delivery trip.**

## 1. Project overview

The application accepts a set of parcels, a road network and a vehicle weight capacity. It then:

1. Prioritizes parcels by priority (highest first), earliest deadline and parcel ID.
2. Uses **0/1 Knapsack dynamic programming** to select the highest-value combination of parcels that fits the vehicle.
3. Models delivery points as a weighted, undirected graph.
4. Uses **Dijkstra's algorithm** to calculate shortest paths from the depot.
5. Uses a **nearest-neighbor TSP heuristic** to create an approximate delivery tour and return to the depot.
6. Benchmarks sorting, knapsack DP and Dijkstra on increasing parcel counts.

The project is a prototype for academic demonstration. Distances are illustrative sample data, not live road distances.

## 2. Requirements

- Python 3.9 or newer
- No third-party Python packages are required.

## 3. Folder structure

```text
mini_courier_planner/
├── courier_planner/
│   ├── __init__.py
│   ├── algorithms.py
│   ├── benchmark.py
│   ├── io_utils.py
│   ├── main.py
│   ├── models.py
│   └── planner.py
├── data/
│   ├── parcels.csv
│   └── roads.csv
├── outputs/
│   └── (generated output files)
├── tests/
│   └── test_algorithms.py
├── README.md
├── requirements.txt
└── PROJECT_REPORT.md
```

## 4. How to run (Windows)

1. Download and extract the ZIP file.
2. Open the extracted `mini_courier_planner` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Check Python:

   ```bash
   python --version
   ```

5. Run the planner from the project root:

   ```bash
   python -m courier_planner.main
   ```

6. Run with performance testing:

   ```bash
   python -m courier_planner.main --benchmark
   ```

7. Change vehicle capacity:

   ```bash
   python -m courier_planner.main --capacity 30 --benchmark
   ```

The application prints the delivery plan and also saves it to `outputs/delivery_plan.txt`. Benchmark mode additionally saves `outputs/benchmark_results.csv`.

### macOS / Linux

Use `python3` instead of `python` if that is the command configured on your system.

## 5. Input data formats

### `data/parcels.csv`

| Column | Meaning |
|---|---|
| parcel_id | Unique parcel identifier |
| destination | Delivery node name; must exist in roads.csv |
| weight | Parcel weight in kg (positive integer) |
| priority | Priority score; larger means more urgent |
| deadline | `YYYY-MM-DD HH:MM` |
| value | Benefit/value used by knapsack (positive integer) |

### `data/roads.csv`

| Column | Meaning |
|---|---|
| from | First connected node |
| to | Second connected node |
| distance | Non-negative distance/cost |

Each road is treated as bidirectional. The graph must connect the depot and every selected destination.

## 6. Algorithms and complexity

Let `n` be the number of parcels, `W` the vehicle capacity, `V` the number of graph vertices and `E` the number of graph edges.

| Component | Algorithm | Time complexity | Space complexity |
|---|---|---:|---:|
| Parcel prioritization | Comparison sorting | O(n log n) | O(n) |
| Package selection | 0/1 Knapsack DP | O(nW) | O(nW) |
| Shortest path | Dijkstra with binary heap | O((V+E) log V) | O(V+E) |
| Delivery tour | Nearest-neighbor TSP heuristic | O(k(V+E) log V) | O(V+E), where k is stops |

The nearest-neighbor method is an approximation/heuristic. It is fast and understandable, but it does not guarantee the globally shortest TSP tour.

## 7. Testing

Run the built-in unit tests from the project root:

```bash
python -m unittest discover -s tests -v
```

Tests cover sorting, knapsack capacity/value, Dijkstra shortest path reconstruction and a depot-returning delivery tour.

## 8. Common errors

- **`python` is not recognized:** install Python 3 and select “Add Python to PATH”, or use `py` on Windows.
- **No module named courier_planner:** make sure the terminal is opened at the project root (the folder containing `courier_planner`).
- **Unknown source node:** check that the depot name exists in `roads.csv`; default is `DEPOT`.
- **No route:** make sure the road graph connects all selected delivery points to the depot.
- **Invalid deadline:** use exactly `YYYY-MM-DD HH:MM`.

## 9. Academic honesty / customization

Before submission, replace sample parcel and road data with your own meaningful scenario, add your name/course/section/roll number to the report cover details, run the program on your machine, and capture screenshots of your actual output. Do not describe illustrative distances as real-world GPS distances.
