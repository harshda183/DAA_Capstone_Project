from .algorithms import prioritize_parcels, select_parcels_knapsack, nearest_neighbor_tsp, dijkstra

def create_plan(parcels, graph, depot, capacity):
    """Run prioritization, package selection, shortest paths and route approximation."""
    prioritized = prioritize_parcels(parcels)
    selected, total_value, dp = select_parcels_knapsack(prioritized, capacity)

    # A parcel may share a destination with another parcel; visit each location once.
    destinations = list(dict.fromkeys(p.destination for p in selected))
    visit_order, road_path, route_distance = nearest_neighbor_tsp(graph, depot, destinations)

    shortest_paths = {}
    depot_distances, depot_previous = dijkstra(graph, depot)
    for destination in destinations:
        shortest_paths[destination] = depot_distances.get(destination, float("inf"))

    return {
        "prioritized": prioritized,
        "selected": selected,
        "total_weight": sum(p.weight for p in selected),
        "total_value": total_value,
        "capacity": capacity,
        "visit_order": visit_order,
        "road_path": road_path,
        "route_distance": route_distance,
        "shortest_paths": shortest_paths,
        "dp": dp,
    }

def format_plan(plan, depot):
    lines = [
        "=" * 68,
        "                 MINI-COURIER PLANNER — DELIVERY PLAN",
        "=" * 68,
        f"Depot: {depot}",
        f"Vehicle capacity: {plan['capacity']} kg",
        "",
        "1. PRIORITIZED PARCEL QUEUE",
        "-" * 68,
        "ID       Destination   Weight   Priority   Deadline",
    ]
    for p in plan["prioritized"]:
        lines.append(f"{p.parcel_id:<8} {p.destination:<13} {p.weight:>4} kg   {p.priority:>4}      {p.deadline}")
    lines += [
        "",
        "2. OPTIMAL PACKAGE SELECTION (0/1 KNAPSACK)",
        "-" * 68,
        f"Selected parcels: {len(plan['selected'])}",
        f"Total weight: {plan['total_weight']} / {plan['capacity']} kg",
        f"Maximum total value: {plan['total_value']}",
    ]
    for p in plan["selected"]:
        lines.append(f"  • {p.parcel_id} → {p.destination} | {p.weight} kg | value {p.value}")
    lines += [
        "",
        "3. SHORTEST-PATH DISTANCES FROM DEPOT (DIJKSTRA)",
        "-" * 68,
    ]
    for destination, distance in plan["shortest_paths"].items():
        lines.append(f"{depot} → {destination}: {distance} km")
    lines += [
        "",
        "4. APPROXIMATED DELIVERY TOUR (NEAREST-NEIGHBOR TSP)",
        "-" * 68,
        "Visit order: " + " → ".join(plan["visit_order"]),
        "Road path:   " + " → ".join(plan["road_path"]),
        f"Total tour distance (including return to depot): {plan['route_distance']} km",
        "",
        "Algorithm note: Dijkstra finds shortest paths between stops; nearest-neighbor",
        "chooses the closest unvisited destination at each step. This is a heuristic,",
        "not a guaranteed optimal solution to the Traveling Salesperson Problem.",
        "=" * 68,
    ]
    return "\n".join(lines)
