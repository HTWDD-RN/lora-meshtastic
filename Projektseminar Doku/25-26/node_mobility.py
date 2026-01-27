#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from collections import Counter

DB_FILE = "meshtastic-2.db"
MIN_POSITION_PACKETS = 5


def main():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    # zählen die Anzahl der POSITION_APP Pakete pro Knoten
    cur.execute("""
        SELECT
            "from",
            COUNT(*) as cnt
        FROM rawpackets
        WHERE port = 'POSITION_APP'
        GROUP BY "from"
    """)

    print("Node mobility (heuristic based on POSITION_APP activity)")
    print("=" * 60)

    for node, count in sorted(cur.fetchall()):
        if count < MIN_POSITION_PACKETS:
            continue

        print(
            f"Node {node:>10} | "
            f"position packets: {count}"
        )

    con.close()


if __name__ == "__main__":
    main()
