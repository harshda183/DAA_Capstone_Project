import unittest
from courier_planner.models import Parcel
from courier_planner.algorithms import (
    prioritize_parcels, select_parcels_knapsack, build_graph, dijkstra,
    reconstruct_path, nearest_neighbor_tsp
)

class AlgorithmTests(unittest.TestCase):
    def setUp(self):
        self.parcels = [
            Parcel("P1", "A", 4, 3, "2026-11-12 10:00", 40),
            Parcel("P2", "B", 5, 5, "2026-11-11 10:00", 50),
            Parcel("P3", "C", 7, 2, "2026-11-13 10:00", 90),
        ]

    def test_priority_sort(self):
        ordered = prioritize_parcels(self.parcels)
        self.assertEqual(ordered[0].parcel_id, "P2")

    def test_knapsack_capacity_and_value(self):
        chosen, value, _ = select_parcels_knapsack(self.parcels, 9)
        self.assertLessEqual(sum(p.weight for p in chosen), 9)
        self.assertEqual(value, 90)

    def test_dijkstra_and_path(self):
        graph = build_graph([
            {"from":"DEPOT","to":"A","distance":"4"},
            {"from":"DEPOT","to":"B","distance":"2"},
            {"from":"B","to":"A","distance":"1"},
        ])
        dist, prev = dijkstra(graph, "DEPOT")
        self.assertEqual(dist["A"], 3)
        self.assertEqual(reconstruct_path(prev, "DEPOT", "A"), ["DEPOT", "B", "A"])

    def test_tour_returns_to_depot(self):
        graph = build_graph([
            {"from":"DEPOT","to":"A","distance":"2"},
            {"from":"A","to":"B","distance":"3"},
            {"from":"B","to":"DEPOT","distance":"4"},
        ])
        order, path, distance = nearest_neighbor_tsp(graph, "DEPOT", ["A", "B"])
        self.assertEqual(order[0], "DEPOT")
        self.assertEqual(order[-1], "DEPOT")
        self.assertEqual(distance, 9)

if __name__ == "__main__":
    unittest.main()
