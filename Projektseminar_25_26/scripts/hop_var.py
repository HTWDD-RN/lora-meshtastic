# somewhat based on radmir's script

import sqlite3
import numpy

import meshtastic.protobuf.mesh_pb2
import matplotlib.pyplot as plt

# config
sqlite_path = "./meshtastic.db"

draw_movement_connections = False
hide_moving_nodes = False
heatmap_hop_count = False   # use the hop count to colour a spot on the map, instead of the hop count stddev of the node
min_packets = 10
relay_min_clients = 5   # if a relay is used very rarely, it doesn't really provide any extra information
relay_min_packets = 5   # per client, if too few packets were sent through a relay, it's not useful
# since packets may be corrupted when received, and there is no error checking, positions may be incorrect
# if they are further away from a specified centre point, they are ignored
# this could be done automatically by finding bounds that include x% of the readings, or growing from the centre until the step to include the next point is too large
pos_mid_point = (510372110,137357750)
pos_allowed_range = (8000000,8000000)
filter_positions = True

con = sqlite3.connect(sqlite_path)
cur = con.cursor()
cur.execute("""
    SELECT id, rawpackets.'from', hopStart, hopLimit, relayNode, (hopStart - hopLimit) as hops from rawpackets;
""")

class PositionReading:
    def __init__(self, lat, long, alt, precision, hops):
        self.lat = lat
        self.long = long
        self.alt = alt
        self.precision = precision
        self.hops = hops

class Client:
    def __init__(self, addr):
        self.id = addr
        self.packets = {}
        self.positions = []

    def addPosition(self, position : PositionReading):
        self.positions.append(position)

    def getPositionsAsPoints(self):
        points = []
        for p in self.positions:
            point = (p.lat, p.long)
            points.append(point)
        return points

    def addPacket(self, lastRelay, hops):
        if lastRelay not in self.packets:
            self.packets[lastRelay] = []
        self.packets[lastRelay].append(hops)

    def printStats(self):
        totalHops = [x for relay in self.packets for x in self.packets[relay]] # unreadable list comprehension, turns it into one flat list
        if len(totalHops) < min_packets:
            return
        #print(totalHops)
        print(f"{self.id} Combined: mean {numpy.mean(totalHops)} std {numpy.std(totalHops)}")
        if len(self.packets) > 1:
            # no sense in printing this out if never more than one relay Node was reported anyways
            for relay in self.packets:
                print(f"\trelay {relay} count {len(self.packets[relay])} mean {numpy.mean(self.packets[relay])} std {numpy.std(self.packets[relay])} min {numpy.min(self.packets[relay])} max {numpy.max(self.packets[relay])}")

    # a list of all relay nodes that have been used with this node
    def getRelays(self) -> list:
        return self.packets.keys()
    
    # a list of hop counts for one specific relay node for this node, or None
    def getRelay(self, relay):
        if relay in self.packets:
            return self.packets[relay]
        return None

    # mean stddev over all qualifying relays
    # just stddev over all packets is not as useful, as all routes might be static, but just have different lengths
    def getMeanHopStddev(self):
        stddevs = []
        for relay in self.packets:
            if relay == 0:
                continue
            if len(self.packets[relay]) < relay_min_packets:
                continue
            stddevs.append(numpy.std(self.packets[relay]))
        if len(stddevs) == 0:
            return 0
        return numpy.mean(stddevs)
        

# this is less memory efficient, but more convenient with numpy
hops_bundled = {}
clients = {}
relays = {}
for packetid, src, hopStart, hopLimit, relayNode, hops in cur.fetchall():
    if(hops < 0):
        # this sometimes happens when a packet isn't received quite correctly
        continue
    
    if src not in clients.keys():
        clients[src] = Client(src)
    clients[src].addPacket(relayNode, hops)

for src in clients:
    clients[src].printStats()

    crelays = clients[src].getRelays()
    for relay in crelays:
        if relay not in relays:
            relays[relay] = []
        relays[relay].append(numpy.std(clients[src].getRelay(relay)))

print("Relay nodes:")
for relay in relays:
    if len(relays[relay]) < relay_min_clients:
        continue
    print(f"{relay}: Node count {len(relays[relay])} mean dev {numpy.mean(relays[relay])} stddev dev {numpy.std(relays[relay])}")


# node positions
cur = con.cursor()
cur.execute("""
    SELECT id, rawpackets.'from', payload, hopStart - hopLimit as hops from rawpackets WHERE port = 'POSITION_APP' GROUP BY id, payload;
""")

def attempt_pos(payload, hops):
    try:
        data = meshtastic.protobuf.mesh_pb2.Position()
        data.ParseFromString(payload)
        reading = PositionReading(data.latitude_i, data.longitude_i, data.altitude, data.precision_bits, hops)
        #print(data)
        return reading
    except:
        return

def check_pos(position : PositionReading):
    # currently a simple bounds check
    if abs(position.lat - pos_mid_point[0]) > pos_allowed_range[0] or abs(position.long - pos_mid_point[1]) > pos_allowed_range[1]:
        return False
    return True

for packetid, src, payload, hops in cur.fetchall():
    reading = attempt_pos(payload, hops)
    if reading is not None:
        if src not in clients.keys():
            print("Client missing?")
            continue
        if check_pos(reading) or filter_positions == False:
            clients[src].addPosition(reading)


# at this point, all data should be added to all objects and they can be plotted or printed or something
fig, ax = plt.subplots()
ax.set_aspect(1)

# treating the positions as X and Y is incorrect, but on a small enough area far enough away from the poles, it should be fine for visualization
positions_x = []
positions_y = []
positions_client = []
position_client_breaks = []

for client in clients.items():
    if len(client[1].positions) > 0:
        if hide_moving_nodes:
            pos_std = numpy.std(client[1].getPositionsAsPoints(), axis=0)
            #print(pos_std)
            if pos_std[0] > 0 or pos_std[1] > 0:
                continue
        position_client_breaks.append(len(positions_x))
        for p in client[1].positions:
            positions_x.append(p.long)
            positions_y.append(p.lat)
            #positions_client.append(client[0])
            if heatmap_hop_count:
                positions_client.append(p.hops)
            else:
                positions_client.append(client[1].getMeanHopStddev())
        #print(f"{client[1].id}: {len(client[1].positions)} positions {numpy.std(client[1].getPositionsAsPoints(), axis=0)} relays {client[1].packets.keys()}")
position_client_breaks.append(len(positions_x)) # otherwise, the last client gets skipped

ax.scatter(positions_x, positions_y, c=positions_client)
# to better see movement traces, draw a connecting line
last_start = 0
for start in position_client_breaks:
    if start != last_start:
        if draw_movement_connections:
            ax.plot(positions_x[last_start:start], positions_y[last_start:start])
        last_start = start
#ax.plot(positions_x, positions_y, c=positions_client)

plt.show()

# collect stddevs per relay node to compare relay nodes (and thereby somewhat directions) - done, only seems moderately useful (directions still need to be identified, which is a bit harder)
# look for position packets to find mobile nodes (won't be that reliable, probably not too many will send their location that often) - done (manual), there are some nodes with various mobility
# with positions known (and thereby directions, if the sniffer position is known, or it could probably be approximated well enough for this purpose), try assigning direction to relays and more nodes (through relays)
# maybe check if packets usually arrive through multiple paths with the same fluctuations or different fluctuations (could help localising issues better, but sounds a lot more complicated)
