import argparse
from pathlib import Path
from .io_utils import load_parcels, load_graph, write_text
from .planner import create_plan, format_plan
from .benchmark import run_benchmark, benchmark_csv

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description="Mini-Courier Planner — DAA Capstone")
    parser.add_argument("--parcels", default=str(ROOT / "data" / "parcels.csv"))
    parser.add_argument("--roads", default=str(ROOT / "data" / "roads.csv"))
    parser.add_argument("--depot", default="DEPOT")
    parser.add_argument("--capacity", type=int, default=25)
    parser.add_argument("--benchmark", action="store_true", help="run runtime comparison")
    args = parser.parse_args()

    parcels = load_parcels(args.parcels)
    graph = load_graph(args.roads)
    plan = create_plan(parcels, graph, args.depot, args.capacity)
    report = format_plan(plan, args.depot)
    print(report)
    write_text(ROOT / "outputs" / "delivery_plan.txt", report)

    if args.benchmark:
        results = run_benchmark(graph, args.depot)
        csv_path = ROOT / "outputs" / "benchmark_results.csv"
        benchmark_csv(results, csv_path)
        print("\\nBENCHMARK RESULTS")
        print("Parcels | Sorting ms | Knapsack ms | Dijkstra ms")
        for row in results:
            print(f"{row[0]:7} | {row[1]:10.4f} | {row[2]:11.4f} | {row[3]:10.4f}")
        print(f"Saved benchmark data to: {csv_path}")

if __name__ == "__main__":
    main()
