-- to run, just pipe the script into sqlite3
-- since this is just a dump of packets, there's no primary key. A pcapng would work too, but a database is nice to process later
CREATE TABLE packets ("time" BIGINT, "id" BIGINT, "from" INTEGER, "to" INTEGER, "rxTime" INTEGER,
     "hopStart" INTEGER, "hopLimit" INTEGER, "transport" TEXT,
     "rxSnr" REAL, "rxRssi" REAL, 
     "channel" INTEGER, "relayNode" INTEGER, "priority" TEXT,
     "encrypted" INTEGER, "port" TEXT, "payload" BLOB);
-- port is TEXT instead of INTEGER, as the meshtastic module gives out a string, and I don't want to convert stuff if I don't need to

CREATE TABLE rawpackets ("time" BIGINT, "id" BIGINT, "from" INTEGER, "to" INTEGER,
     "hopStart" INTEGER, "hopLimit" INTEGER,
     "hash" INTEGER, "relayNode" INTEGER, "wantack" INTEGER, "nexthop" INTEGER, "mqtt" INTEGER, "port" TEXT, "payload" BLOB, "decrypt" BLOB,
     "rssi" INTEGER, "snr" INTEGER);