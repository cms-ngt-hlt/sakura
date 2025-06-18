#!/bin/env python3

import sys
import os
import struct

def check_raw_file(rawfilepaths):
    open_files = []
    hdr_event_count = []
    for rfp in rawfilepaths:
        if not os.path.exists(rfp):
            print(f"file does not exist: {rfp}")
            sys.exit(2)


        fin = open(rfp, 'rb')
        ffhdr = fin.read(24)
        ecount = struct.unpack_from('<H', ffhdr[-14:-12])[0]
        ls = struct.unpack_from('<I', ffhdr[-12:-8])[0]
        hdr_event_count.append([ecount,ls])
        open_files.append([fin,ls])

    counters = [ 0 for x in open_files[0]]
    event_ids = [set() for x in open_files[0]]
    event_ids_min = [-1 for x in open_files[0]]
    event_ids_max = [-1 for x in open_files[0]]
    sums = [ 0 for x in open_files[0]]
    sums2 = [ 0 for x in open_files[0]]
    while True:
                        #new event
                        ebuf = bytearray()
                        esize = 0
                        fhdr = fhdr0 = None
                        idx = 0
                        this_event_id = -1
                        for finarr in open_files:
                            fin = finarr[0]
                            ls = finarr[1]
                            thiscnt = 0
                            fhdr = fin.read(24)
                            if not fhdr0:
                                fhdr0 = fhdr
                            if not fhdr:
                                #break
                                print(f"break {idx}")
                                continue
                            if fhdr[0] < 5 or fhdr[0] > 6:
                                raise Exception(f"unknown FRD event version {fhdr[0]}")
                            r_size = struct.unpack_from('<I', fhdr[-8:-4])[0]
                            event_id = struct.unpack_from('<I', fhdr[-12:-8])[0]
                            e_ls = struct.unpack_from('<I', fhdr[-16:-12])[0]

                            if this_event_id == -1:
                                this_event_id = event_id
                            elif this_event_id != event_id:
                                raise Exception(f"ERROR: inconsistent event ID previous:{this_event_id} this:{event_id} in file {idx}")
                            if event_id in event_ids[idx]:
                                raise Exception(f"WARNING: duplicate event id in file {idx}")
                            else:
                                event_ids[idx].add(event_id)
                            if event_ids_min[idx] == -1:
                                event_ids_min[idx] = event_id
                                event_ids_max[idx] = event_id
                            else:
                                if event_id > event_ids_max[idx]: event_ids_max[idx] = event_id
                                if event_id < event_ids_min[idx]: event_ids_min[idx] = event_id
                            esize += r_size
                            tmpbuf = fin.read(r_size)
                            ebuf += tmpbuf
                            counters[idx] += 1
                            sums[idx] += r_size + 24
                            sums2[idx] += len(tmpbuf) + len(fhdr)
                            print(f"index {idx} eventID: {event_id} add : {r_size + 24} {len(tmpbuf) + 24} {sums[idx]} {sums2[idx]} cnt: {counters[idx]}")
                            if e_ls != ls:
                                result = f"ERROR: inconsistent lumisection for this event! file: {ls} event: {e_ls}"
                                raise Exception(result)
                            idx += 1

                        if not fhdr:
                            break
    for index in range(0, len(rawfilepaths)):
        print(f"Summary for file {rawfilepaths[index]} events:{counters[idx]} eventsHeader:{hdr_event_count[idx][0]} ls: {hdr_event_count[idx][1]}")


if len(sys.argv) < 2:
    print("Provide one or more raw file paths as command line parameters")
    sys.exit(1)
check_raw_file(sys.argv[1:])
