import csv
from pathlib import Path
from .models import Parcel
from .algorithms import build_graph

def load_parcels(path):
    parcels = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            parcels.append(Parcel(
                parcel_id=row["parcel_id"],
                destination=row["destination"],
                weight=int(row["weight"]),
                priority=int(row["priority"]),
                deadline=row["deadline"],
                value=int(row["value"]),
            ))
    return parcels

def load_graph(path):
    with open(path, newline="", encoding="utf-8") as f:
        return build_graph(csv.DictReader(f))

def write_text(path, content):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")
