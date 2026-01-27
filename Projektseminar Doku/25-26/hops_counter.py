import sqlite3
from collections import defaultdict
import csv

DB_PATH = "meshtastic.db"       # Path to SQLite DB
CSV_PATH = "hop_nodes.csv"      # Output CSV with per-node info
CSV_SUMMARY_PATH = "hop_summary.csv"  # Output CSV with per-distance counts

# If you want: only report nodes up to this hop distance (None = no limit)
MAX_HOPS = None  # e.g. 4


def compute_min_hops(db_path: str):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("""
        SELECT "from", hopStart, hopLimit
        FROM rawpackets
        WHERE hopStart IS NOT NULL
          AND hopLimit IS NOT NULL
          AND "from" IS NOT NULL
    """)

    min_hops = {}
    counts = defaultdict(int)
    negative_dist_rows = 0

    for from_id, hop_start, hop_limit in cur:
        counts[from_id] += 1

        dist = hop_start - hop_limit
        if dist < 0:
            negative_dist_rows += 1
            continue

        prev = min_hops.get(from_id)
        if prev is None or dist < prev:
            min_hops[from_id] = dist

    con.close()
    return min_hops, counts, negative_dist_rows


def guess_my_node_id(min_hops, counts):
    """
    guesses the node ID of "my" node as the one with min hop distance 0 
    """
    candidates = [(node, counts.get(node, 0)) for node, d in min_hops.items() if d == 0]
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0][0]


def group_nodes_by_distance(min_hops, max_hops=None):
    """
    Groups nodes by their min hop distance.
    Uses set() to guarantee uniqueness.
    """
    groups = defaultdict(set)
    for node, d in min_hops.items():
        if max_hops is not None and d > max_hops:
            continue
        groups[d].add(node)
    # Convert sets to sorted lists for stable output
    return {d: sorted(nodes) for d, nodes in sorted(groups.items())}


def write_csv_nodes(groups, counts, my_node, path):
    """
    Writes per-node CSV: node_id, hop_distance, packet_count, is_me
    """
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["node_id", "hop_distance", "packet_count", "is_me"])
        for d in sorted(groups):
            for node in groups[d]:
                w.writerow([node, d, counts.get(node, 0), 1 if node == my_node else 0])


def write_csv_summary(groups, path):
    """
    Writes summary CSV: hop_distance, node_count
    """
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["hop_distance", "node_count"])
        for d in sorted(groups):
            w.writerow([d, len(groups[d])])


def print_report(groups, counts, my_node, csv_nodes_path, csv_summary_path):
    """
    Prints only a short summary to console (no per-node listing).
    """
    total_nodes = sum(len(nodes) for nodes in groups.values())

    print("\n===== Mesh Analysis Summary =====")
    print(f"Total unique nodes (with non-negative min distance): {total_nodes}")

    if my_node is not None:
        print(f"My node (heuristic): {my_node}  (Packets: {counts.get(my_node, 0)})")
    else:
        print("My node could not be determined heuristically.")

    print("\nOutput files:")
    print(f"  - Per-node data:     {csv_nodes_path}")
    print(f"  - Hop summary data:  {csv_summary_path}")
    print("=================================\n")



if __name__ == "__main__":
    min_hops, counts, negative_rows = compute_min_hops(DB_PATH)
    my_node = guess_my_node_id(min_hops, counts)

    print(f"DB: {DB_PATH}")
    if my_node is not None:
        print(f"Vermutlich dein Node: {my_node} (Pakete: {counts.get(my_node, 0)})")
    else:
        print("Konnte deinen Node nicht erraten (keine Kandidaten mit Distanz 0).")

    print(f"Rows ignored due to negative distance (hopStart - hopLimit < 0): {negative_rows}")

    groups = group_nodes_by_distance(min_hops, max_hops=MAX_HOPS)

    print_report(groups, counts, my_node, CSV_PATH, CSV_SUMMARY_PATH)

    # CSV exports
    write_csv_nodes(groups, counts, my_node, CSV_PATH)
    write_csv_summary(groups, CSV_SUMMARY_PATH)

    print(f"\nCSV geschrieben: {CSV_PATH}")
    print(f"CSV Summary geschrieben: {CSV_SUMMARY_PATH}")
