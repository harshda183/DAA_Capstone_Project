"""Small reproducible runtime experiment for the main algorithm components."""
import random
import time
from .models import Parcel
from .algorithms import prioritize_parcels, select_parcels_knapsack, dijkstra

def run_benchmark(graph, depot, max_n=160):
    rng = random.Random(42)
    results = []
    for n in (10, 25, 50, 100, max_n):
        parcels = [
            Parcel(f"B{i:03}", f"N{i % max(1, len(graph))}", rng.randint(1, 12),
                   rng.randint(1, 5), "2026-12-01 17:00", rng.randint(10, 100))
            for i in range(n)
        ]
        t0 = time.perf_counter()
        prioritize_parcels(parcels)
        sort_ms = (time.perf_counter() - t0) * 1000

        # Keep capacity bounded so the DP experiment remains quick and comparable.
        t0 = time.perf_counter()
        select_parcels_knapsack(parcels, 100)
        dp_ms = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        dijkstra(graph, depot)
        graph_ms = (time.perf_counter() - t0) * 1000
        results.append((n, sort_ms, dp_ms, graph_ms))
    return results

def benchmark_csv(results, path):
    import csv
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["parcel_count", "sorting_ms", "knapsack_dp_ms", "dijkstra_ms"])
        writer.writerows(results)
