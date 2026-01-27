#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from statistics import median, mean
from collections import defaultdict


DB_FILE = "meshtastic-2.db"   # Path to DB        
MIN_PACKETS = 5               # minimum anzahl packets für analyse 


def compute_hops(hop_start, hop_limit): #wie viele hops hat Paket gemacht
    """
    hops = hopStart - hopLimit
    """
    if hop_start is None or hop_limit is None:
        return None

    try:
        hops = int(hop_start) - int(hop_limit)
    except ValueError:
        return None

    if hops < 0:
        return None

    return hops


def main():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    # Nehmen alle Pakete, die wir bekommen haben
    # aus der Datenbank
    cur.execute("""
        SELECT
            "from",
            hopStart,
            hopLimit
        FROM packets
        WHERE
            hopStart IS NOT NULL
            AND hopLimit IS NOT NULL
    """)

    hops_per_node = defaultdict(list)

    for node_from, hop_start, hop_limit in cur.fetchall():
        hops = compute_hops(hop_start, hop_limit)
        if hops is not None:
            hops_per_node[node_from].append(hops)

    con.close()

    print("Estimated hop distance FROM US to other nodes")
    print("")

    for node, hops_list in sorted(hops_per_node.items()):
        if len(hops_list) < MIN_PACKETS:
            continue

        print(
            f"Node {node:>10} | "
            f"median: {median(hops_list):.0f} hops | "
            f"avg: {mean(hops_list):.2f} | "
            f"packets: {len(hops_list)}"
        )


if __name__ == "__main__":
    main()
