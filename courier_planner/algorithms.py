"""Core DAA algorithms used by the Mini-Courier Planner."""
from __future__ import annotations
from collections import defaultdict
from heapq import heappop, heappush
from typing import Dict, List, Tuple
from .models import Parcel

Graph = Dict[str, List[Tuple[str, int]]]


def build_graph(rows) -> Graph:
    """Build an undirected weighted adjacency-list graph from edge rows."""
    graph = defaultdict(list)
    for row in rows:
        a, b, distance = row["from"], row["to"], int(row["distance"])
        if distance < 0:
            raise ValueError("Dijkstra requires non-negative edge distances.")
        graph[a].append((b, distance))
        graph[b].append((a, distance))
    return dict(graph)


def prioritize_parcels(parcels: List[Parcel]) -> List[Parcel]:
    """Sort by descending priority, then earliest deadline, then parcel ID."""
    return sorted(parcels, key=lambda p: (-p.priority, p.deadline_key(), p.parcel_id))


def select_parcels_knapsack(parcels: List[Parcel], capacity: int):
    """
    0/1 Knapsack DP. Maximize total parcel value subject to weight capacity.
    Returns (selected parcels, maximum value, DP table).
    """
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i, parcel in enumerate(parcels, start=1):
        for cap in range(capacity + 1):
            dp[i][cap] = dp[i - 1][cap]
            if parcel.weight <= cap:
                dp[i][cap] = max(
                    dp[i][cap],
                    parcel.value + dp[i - 1][cap - parcel.weight]
                )

    selected = []
    cap = capacity
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            parcel = parcels[i - 1]
            selected.append(parcel)
            cap -= parcel.weight
    selected.reverse()
    return selected, dp[n][capacity], dp


def dijkstra(graph: Graph, source: str):
    """Return shortest distances and predecessor map from source."""
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    if source not in graph:
        raise ValueError(f"Unknown source node: {source}")
    distances[source] = 0
    heap = [(0, source)]
    while heap:
        current_distance, node = heappop(heap)
        if current_distance != distances[node]:
            continue
        for neighbor, weight in graph[node]:
            candidate = current_distance + weight
            if candidate < distances.get(neighbor, float("inf")):
                distances[neighbor] = candidate
                previous[neighbor] = node
                heappush(heap, (candidate, neighbor))
    return distances, previous


def reconstruct_path(previous, source: str, target: str):
    """Reconstruct a shortest path; return [] if target is unreachable."""
    if target == source:
        return [source]
    if target not in previous or previous[target] is None:
        return []
    path = [target]
    while path[-1] != source:
        parent = previous.get(path[-1])
        if parent is None:
            return []
        path.append(parent)
    return list(reversed(path))


def nearest_neighbor_tsp(graph: Graph, start: str, destinations: List[str]):
    """
    Approximate a delivery tour using nearest-neighbor over Dijkstra distances.
    Each leg is a shortest path in the road graph. The route returns to depot.
    Returns route nodes, expanded road path, and total distance.
    """
    if start not in graph:
        raise ValueError(f"Unknown depot node: {start}")
    remaining = list(dict.fromkeys(d for d in destinations if d != start))
    current = start
    visit_order = [start]
    expanded_path = [start]
    total_distance = 0

    while remaining:
        distances, previous = dijkstra(graph, current)
        reachable = [(distances.get(node, float("inf")), node) for node in remaining]
        distance, next_node = min(reachable)
        if distance == float("inf"):
            raise ValueError(f"No route from {current} to any remaining destination.")
        leg = reconstruct_path(previous, current, next_node)
        if not leg:
            raise ValueError(f"Unable to reconstruct route to {next_node}.")
        expanded_path.extend(leg[1:])
        total_distance += distance
        current = next_node
        visit_order.append(current)
        remaining.remove(current)

    if current != start:
        distances, previous = dijkstra(graph, current)
        back_distance = distances.get(start, float("inf"))
        if back_distance == float("inf"):
            raise ValueError(f"No return route from {current} to depot {start}.")
        leg = reconstruct_path(previous, current, start)
        expanded_path.extend(leg[1:])
        total_distance += back_distance
        visit_order.append(start)

    return visit_order, expanded_path, total_distance
