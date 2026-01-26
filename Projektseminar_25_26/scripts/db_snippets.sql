-- Various snippets to evaluate sniffer data

-- packet duplication rate
SELECT AVG(repeats) FROM 
    (SELECT COUNT() as repeats,* FROM rawpackets GROUP BY id, rawpackets.'from', payload);
-- 1 would theoretically be the best, but 2 would be the best case value with 
-- managed flooding the way meshtastic does it (assuming no packets reach their hop limit)

-- duplication rate ignoring packets that can't be further rebroadcasted due to the hop limit
SELECT AVG(repeats) as clean_repeats FROM
    (SELECT COUNT() as repeats,* FROM rawpackets GROUP BY id, rawpackets.'from', payload 
        HAVING hopLimit > 0 OR repeats > 1);
-- while the previous duplication rate would be ideally 2 for meshtastic, that's only possible
-- if no packets reach their hop limit. Those are filtered out here, giving the average amount
-- of times that packets that can or were rebroadcasted were received.

-- duplication rate of duplicated packets
SELECT AVG(repeats) FROM 
(SELECT COUNT() as repeats,* FROM rawpackets 
    GROUP BY id, rawpackets.'from' HAVING COUNT() > 1);
-- this time only for duplicated packets. A number >2 means inefficiency in flooding

-- duplicated packets (just a list of them, mostly useful to build other queries)
SELECT COUNT() as repeats,* 
FROM rawpackets GROUP BY id, rawpackets.'from' HAVING COUNT() > 1;

-- relay nodes
SELECT relayNode, COUNT() FROM rawpackets GROUP BY relayNode ORDER BY COUNT() DESC;

-- relay node and source address
SELECT relayNode, COUNT(), rawpackets.'from' FROM rawpackets 
    GROUP BY relayNode, rawpackets.'from' ORDER BY COUNT() DESC;

-- duplicate received packets by source address, not counting corrupted packets
SELECT *, AVG(repeats), SUM(repeats) FROM 
(SELECT COUNT() as repeats, rawpackets.'from' as src FROM rawpackets 
    GROUP BY id, rawpackets.'from', payload HAVING COUNT() > 1)
GROUP BY src
ORDER BY SUM(repeats) DESC;
-- could be used to find nodes that flood the mesh with a lot of repeated packets
-- a lot of repeats are likely not directly the node's fault, but instead
-- caused by the mesh

-- packets with want_ack (deduplicated)
SELECT COUNT() FROM 
    (SELECT id, rawpackets.'from' FROM rawpackets WHERE wantack = 1 GROUP BY id, rawpackets.'from');
-- mostly things like direct messages

-- packet count (deduplicated)
SELECT COUNT() FROM 
    (SELECT id, rawpackets.'from' FROM rawpackets GROUP BY id, rawpackets.'from');
-- find very active nodes

-- packets (deduplicated) which are not broadcasts
SELECT COUNT() FROM 
(SELECT id, rawpackets.'from' FROM rawpackets WHERE rawpackets.'to' != 4294967295 GROUP BY id, rawpackets.'from');
-- if most packets are broadcasts, there wouldn't be much of a point in optimising DMs



-- common ports, deduplicated (not necessarily entirely correct due to corrupted packets)
SELECT port, COUNT() FROM 
    (SELECT id, rawpackets.'from', port FROM rawpackets GROUP BY id, rawpackets.'from') 
GROUP BY port ORDER BY COUNT() DESC;
-- can give a rough idea of the usage of the mesh

-- common ports, including duplicates
SELECT port, COUNT() from rawpackets GROUP BY port ORDER BY COUNT() DESC;
-- similar, could be useful if specific applications were somehow causing a lot of duplicated packets
-- could also be useful in evaluating the effectiveness of adjusting rebroadcasting depending on the port

-- packets with mqtt (deduplicated)
SELECT COUNT() FROM 
(SELECT id, rawpackets.'from' FROM rawpackets WHERE mqtt = 1 GROUP BY id, rawpackets.'from');
-- just interesting to see




-- port distribution stuff
-- distribution of ports
SELECT COUNT(), port, total_count, COUNT()/CAST(total_count as REAL) FROM 
packets JOIN 
(SELECT COUNT() as total_count FROM packets WHERE transport IS NOT NULL) 
WHERE transport IS NOT NULL GROUP BY port ORDER BY COUNT() DESC;
-- like the rawpackets version, but also gives a percentage


-- things to guess the usage of encrypted packets
-- length of encrypted packets, grouped
SELECT length(payload)*3/4 as length, COUNT() 
FROM packets 
WHERE transport IS NOT NULL AND port IS NULL 
GROUP BY length(payload) ORDER BY COUNT() DESC;

-- payload length (not quite accurate to packet length)
SELECT length(payload) as length, COUNT(), port 
FROM packets 
WHERE transport IS NOT NULL AND port IS NOT NULL 
GROUP BY length(payload) ORDER BY COUNT() DESC;

-- length of raw packets, encrypted
SELECT length(decrypt) as length, COUNT() FROM 
(SELECT id, rawpackets.'from', decrypt, port FROM rawpackets 
    GROUP BY id, rawpackets.'from')
WHERE port IS NULL 
GROUP BY length(decrypt) ORDER BY COUNT() DESC;

-- length of raw packets, decrypted
SELECT length(decrypt) as length, COUNT(), port FROM 
(SELECT id, rawpackets.'from', decrypt, port FROM rawpackets 
    GROUP BY id, rawpackets.'from')
WHERE port IS NOT NULL 
GROUP BY length(decrypt), port ORDER BY COUNT() DESC;


